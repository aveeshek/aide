"""Deterministic persistence / data-model extractor (Graph Engineering Pass 4).

Scope and non-goals
-------------------
This extractor reads Python source with :mod:`ast` and emits *candidates* only. It never
imports or executes the inspected application, never starts a service, never opens a
database connection, never writes canonical knowledge, never touches Neo4j or Graphiti, and
never calls an LLM.

It records only what the source states explicitly:

* ``Database -CONTAINS-> Table`` when a service's database mapping is proven
* ``Table -CONTAINS-> Column`` for statically declared columns
* ``Service -READS/WRITES-> Table`` for relational access proven through the ORM
* ``Service -READS/WRITES-> Schema`` for document access proven through the ODM
* ``Table -DEPENDS_ON-> Table`` only for an explicit, resolvable foreign key
* ``Migration -CHANGED_BY`` linkage only when the migration names its target

Why a name is never enough
--------------------------
A class is not a persistence model because it has fields, and a method is not a database
read because it is called ``get_order``. Every model and every access reported here is
*rooted*: the declaring base class, or the receiver of the operation, must trace statically
to a symbol imported from a discovered persistence library. Only then is the declaration or
the method name interpreted. That is what keeps an ordinary Pydantic request schema or a
plain domain dataclass out of the persistence graph.

Bounded tracing
---------------
Real repositories hide the ORM behind wrappers. FTGO's services call
``DatabaseRepository.fetch(dto_class, query)``, and that method calls
``session.execute(select(model_class))`` where ``model_class`` comes from a class-level
``{DTO: Model}`` map. Two bounded traces make this provable without becoming an interpreter:

``_MAX_WRAPPER_HOPS``
    How far an application call site may be from the real ORM/ODM call.
``_MAX_VALUE_HOPS``
    How far a value may be from a persistence-library symbol through annotations and
    return types.

Anything beyond the bounds is recorded in ``unresolved_accesses``.

Ontology
--------
Relational and document persistence are modelled symmetrically, following the approved
ontology decision that added ``Collection`` as a first-class kind:

* relational: ``Database -CONTAINS-> Table -CONTAINS-> Column`` and
  ``Service -READS/WRITES-> Table``
* document:   ``Database -CONTAINS-> Collection -USES_SCHEMA-> Schema`` and
  ``Service -READS/WRITES-> Collection``

``Collection`` is the physical MongoDB collection; ``Schema`` remains the source-backed
document model with its fields, indexes and references. A service access points at the
Collection, never at both, and document fields stay structured attributes on the Schema
rather than becoming ``Column`` entities. A document model with no statically proven
collection name yields no Collection and is reported in ``unresolved_collection_names``.
"""

from __future__ import annotations

import ast
import json
import re
from dataclasses import dataclass, field, replace
from typing import Any

import yaml

from ..repository_manifest import RepositoryRecord, resolve_source_files
from .compose import extract_compose
from .fastapi import (
    Provenance,
    module_dotted_name,
    normalize_dotted,
    normalize_token,
    service_location,
)

EXTRACTOR_KIND = "data-model"
CANDIDATE_STATUS = "candidate"
CANDIDATE_REVIEW_STATUS = "pending"
EVIDENCE_TYPE = "implemented"
REDACTED_PLACEHOLDER = "[redacted]"

# Output subdirectories owned by this extractor, used for stale-candidate pruning.
CANDIDATE_SUBDIRECTORIES = ("tables", "columns", "collections", "schemas", "migrations")
DATABASE_DELTAS_FILENAME = "database-relation-deltas.json"
SERVICE_DELTAS_FILENAME = "service-relation-deltas.json"

# Ontology kinds used. All five exist in ontology/entity-types.yaml; ``Collection`` was
# added by an explicit, approved ontology decision for the document-persistence layer.
TABLE_KIND = "Table"
COLUMN_KIND = "Column"
COLLECTION_KIND = "Collection"
SCHEMA_KIND = "Schema"
MIGRATION_KIND = "Migration"
CONTAINS = "CONTAINS"
DEPENDS_ON = "DEPENDS_ON"
USES_SCHEMA = "USES_SCHEMA"
READS = "READS"
WRITES = "WRITES"
CHANGED_BY = "CHANGED_BY"

READ_ROLE = "read"
WRITE_ROLE = "write"

# Manifest source kind scanned by this pass.
SOURCE_KIND = "code"
PYTHON_SUFFIX = ".py"
# Application source lives under the service ``src`` root; migrations sit beside it and are
# explicitly in scope for this pass (Phase 7) even though earlier passes exclude them.
SOURCE_SEGMENT = "src"
MIGRATIONS_SEGMENT = "migrations"
IN_SCOPE_ROOT_SEGMENTS = (SOURCE_SEGMENT, MIGRATIONS_SEGMENT)

# ---------------------------------------------------------------------------------------
# Persistence stack vocabulary
#
# Nothing here is treated as evidence on its own: a library only counts once an import is
# found, and an operation only counts once its receiver is rooted in one of these libraries.
# ---------------------------------------------------------------------------------------

RELATIONAL_LIBRARIES: tuple[str, ...] = (
    "asyncpg",
    "asyncpg_client",
    "databases",
    "psycopg",
    "psycopg2",
    "sqlalchemy",
    "sqlmodel",
    "tortoise",
)
DOCUMENT_LIBRARIES: tuple[str, ...] = (
    "beanie",
    "mongo_motors",
    "mongoengine",
    "motor",
    "odmantic",
    "pymongo",
)
MIGRATION_LIBRARIES: tuple[str, ...] = ("alembic",)
# Redis is persistence infrastructure but holds no table or document model. It is reported
# as a detected library and produces no entity, because the ontology has no cache kind.
CACHE_LIBRARIES: tuple[str, ...] = (
    "aioredis",
    "aredis_client",
    "redis",
    "redis_client",
)

PERSISTENCE_LIBRARIES: tuple[str, ...] = tuple(
    sorted(set(RELATIONAL_LIBRARIES + DOCUMENT_LIBRARIES + MIGRATION_LIBRARIES + CACHE_LIBRARIES))
)

ENGINE_POSTGRESQL = "postgresql"
ENGINE_MONGODB = "mongodb"
ENGINE_REDIS = "redis"
LIBRARY_ENGINES: dict[str, str] = {
    "asyncpg": ENGINE_POSTGRESQL,
    "asyncpg_client": ENGINE_POSTGRESQL,
    "psycopg": ENGINE_POSTGRESQL,
    "psycopg2": ENGINE_POSTGRESQL,
    "sqlalchemy": ENGINE_POSTGRESQL,
    "sqlmodel": ENGINE_POSTGRESQL,
    "beanie": ENGINE_MONGODB,
    "mongo_motors": ENGINE_MONGODB,
    "mongoengine": ENGINE_MONGODB,
    "motor": ENGINE_MONGODB,
    "odmantic": ENGINE_MONGODB,
    "pymongo": ENGINE_MONGODB,
    "aioredis": ENGINE_REDIS,
    "aredis_client": ENGINE_REDIS,
    "redis": ENGINE_REDIS,
    "redis_client": ENGINE_REDIS,
}

PERSISTENCE_ROLE_TABLE = "relational_table"
PERSISTENCE_ROLE_DOCUMENT = "document_model"

# Declarative bases that mark a class as a relational mapped model.
RELATIONAL_BASE_SYMBOLS = frozenset({"DeclarativeBase", "DeclarativeMeta", "Model", "SQLModel"})
# Declarative bases that mark a class as a document model.
DOCUMENT_BASE_SYMBOLS = frozenset({"Document", "DynamicDocument", "EmbeddedDocument", "Model"})

# Column constructors.
COLUMN_CONSTRUCTORS = frozenset({"Column", "mapped_column"})
FOREIGN_KEY_CONSTRUCTOR = "ForeignKey"
RELATIONSHIP_CONSTRUCTOR = "relationship"
INDEX_MODEL_CONSTRUCTOR = "IndexModel"
DOCUMENT_LINK_CONSTRUCTS = frozenset({"Link", "BackLink", "Indexed"})

# ORM/ODM operations, consulted only after the receiver is rooted.
RELATIONAL_READ_OPERATIONS = frozenset({"select", "query", "scalar", "scalars", "get", "exists"})
RELATIONAL_WRITE_OPERATIONS = frozenset(
    {"add", "add_all", "delete", "insert", "merge", "update", "bulk_save_objects"}
)
DOCUMENT_READ_OPERATIONS = frozenset(
    {"aggregate", "count", "find", "find_all", "find_many", "find_one", "get"}
)
DOCUMENT_WRITE_OPERATIONS = frozenset(
    {
        "delete",
        "delete_all",
        "insert",
        "insert_many",
        "insert_one",
        "replace",
        "save",
        "save_changes",
        "set",
        "update",
        "update_all",
        "upsert",
    }
)
# Session lifecycle calls prove a write happened but name no model; they are recorded as
# supporting evidence, never as a target on their own.
SESSION_FLUSH_OPERATIONS = frozenset({"commit", "flush", "refresh"})

# Alembic operations that name a physical table.
ALEMBIC_TABLE_OPERATIONS = frozenset(
    {
        "add_column",
        "alter_column",
        "create_index",
        "create_table",
        "drop_column",
        "drop_index",
        "drop_table",
        "rename_table",
    }
)

# ---------------------------------------------------------------------------------------
# Secret safety
# ---------------------------------------------------------------------------------------

# Names whose *values* are credentials or connection coordinates and must never be emitted.
SENSITIVE_NAME_MARKERS = (
    "PASSWORD",
    "PASSWD",
    "SECRET",
    "TOKEN",
    "CREDENTIAL",
    "DSN",
)
# ``pass``, ``key``, ``auth``, ``user``, ``uri`` and ``url`` are only sensitive as whole
# connection-configuration names. Applying them as substrings would redact ordinary domain
# fields: FTGO legitimately declares ``hashed_password`` (a real column that must appear,
# with no value), ``user_id``, ``owner_user_id``, ``restaurant_licence_id`` and
# ``menu_item_id``. The intent is to protect connection credentials, not domain columns.
SENSITIVE_EXACT_NAMES = frozenset(
    {
        "auth",
        "connection_string",
        "conn_str",
        "credentials",
        "db_pass",
        "db_password",
        "db_url",
        "db_uri",
        "dsn",
        "key",
        "pass",
        "passwd",
        "password",
        "secret",
        "secret_key",
        "sqlalchemy_url",
        "token",
        "uri",
        "url",
        "user",
        "username",
    }
)
# Any URI carrying userinfo is redacted wherever it would be emitted.
_URI_CREDENTIAL_PATTERN = re.compile(
    r"\b([a-z][a-z0-9+.\-]*://)[^/\s:@]+:[^/\s@]+@", re.IGNORECASE
)
_URI_USERINFO_PATTERN = re.compile(
    r"\b[a-z][a-z0-9+.\-]*://([^/\s:@]+):([^/\s@]+)@", re.IGNORECASE
)
# A bare scheme URI still reveals structure only; hosts and ports are safe to keep.
_MIN_SCANNABLE_SECRET_LENGTH = 4

# Directories never scanned.
EXCLUDED_PATH_SEGMENTS = frozenset(
    {
        ".git",
        ".mypy_cache",
        ".pytest_cache",
        ".ruff_cache",
        ".tox",
        ".venv",
        "__pycache__",
        "build",
        "dist",
        "node_modules",
        "site-packages",
        "venv",
    }
)
TEST_PATH_SEGMENTS = frozenset({"test", "tests"})
GENERATED_FILENAME_SUFFIXES = ("_pb2.py", "_pb2_grpc.py", "_pb2.pyi")
GENERATED_HEADER_MARKERS = ("@generated", "generated by", "do not edit this file")
_GENERATED_HEADER_LINES = 5

_MAX_WRAPPER_HOPS = 2
_MAX_VALUE_HOPS = 3
_MAX_RESOLUTION_DEPTH = 24
_MAX_EXPRESSION_LENGTH = 200

# How a model target was pinned down, recorded on every access so a reviewer can judge it.
RESOLUTION_DIRECT = "direct_model_reference"
RESOLUTION_WRAPPER = "wrapper_argument"
RESOLUTION_MODEL_MAP = "model_map_enumeration"
RESOLUTION_CLASS_ATTRIBUTE = "class_attribute"


# ---------------------------------------------------------------------------------------
# Normalization and safety helpers
# ---------------------------------------------------------------------------------------


def table_id(repository_slug: str, service_slug: str, table_name: str) -> str:
    """Build a byte-stable Table id from the physical table name."""
    return f"table.{repository_slug}.{service_slug}.{normalize_token(table_name)}"


def column_id(
    repository_slug: str, service_slug: str, table_name: str, column_name: str
) -> str:
    """Build a byte-stable Column id from its table and column names."""
    return (
        f"column.{repository_slug}.{service_slug}."
        f"{normalize_token(table_name)}.{normalize_token(column_name)}"
    )


def document_schema_id(
    repository_slug: str, service_slug: str, module: str, class_name: str
) -> str:
    """Build a byte-stable persistence Schema id for a document model."""
    qualified = f"{module}.{class_name}" if module else class_name
    return f"schema.{repository_slug}.{service_slug}.persistence.{normalize_dotted(qualified)}"


def collection_id(repository_slug: str, service_slug: str, collection_name: str) -> str:
    """Build a byte-stable Collection id from the physical collection name."""
    return f"collection.{repository_slug}.{service_slug}.{normalize_token(collection_name)}"


def migration_id(repository_slug: str, service_slug: str, revision: str) -> str:
    """Build a byte-stable Migration id from the migration's own revision identifier."""
    return f"migration.{repository_slug}.{service_slug}.{normalize_token(revision)}"


def service_entity_id(repository_slug: str, service_slug: str) -> str:
    return f"service.{repository_slug}.{service_slug}"


def is_sensitive_name(name: str) -> bool:
    """True when a binding name holds a credential or a connection coordinate.

    Marker substrings are deliberately narrow and the ambiguous words are matched only as
    whole names. FTGO proves why: ``hashed_password`` is a real column of ``user_profile``
    that must appear in the graph, and ``owner_user_id`` is an ordinary foreign-key-ish
    column. Redacting either would corrupt the data model this pass exists to describe.
    """
    lowered = str(name).strip().lower()
    if lowered in SENSITIVE_EXACT_NAMES:
        return True
    upper = lowered.upper()
    return any(marker in upper for marker in SENSITIVE_NAME_MARKERS)


def redact_uri(text: str) -> str:
    """Strip userinfo from any credential-bearing URI in ``text``."""
    return _URI_CREDENTIAL_PATTERN.sub(rf"\1{REDACTED_PLACEHOLDER}@", str(text))


def _expression_text(source: str, node: ast.AST | None) -> str | None:
    """Return the collapsed source text of ``node``, never an evaluated value."""
    if node is None:
        return None
    try:
        segment = ast.get_source_segment(source, node)
    except (ValueError, IndexError, TypeError):
        return None
    if segment is None:
        return None
    collapsed = " ".join(segment.split())
    if not collapsed:
        return None
    return redact_uri(collapsed[:_MAX_EXPRESSION_LENGTH])


def _dotted_expression(node: ast.expr) -> str | None:
    """Flatten ``a.b.c`` into ``"a.b.c"``; return None for any other expression shape."""
    parts: list[str] = []
    current: ast.expr = node
    while isinstance(current, ast.Attribute):
        parts.append(current.attr)
        current = current.value
    if not isinstance(current, ast.Name):
        return None
    parts.append(current.id)
    return ".".join(reversed(parts))


def _unwrap(node: ast.expr) -> ast.expr:
    """Strip ``await`` so ``await X.create()`` reads like ``X.create()``."""
    seen = 0
    while isinstance(node, ast.Await) and seen < _MAX_RESOLUTION_DEPTH:
        node = node.value
        seen += 1
    return node


def _constant_string(node: ast.expr | None) -> str | None:
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    return None


def _constant_bool(node: ast.expr | None) -> bool | None:
    if isinstance(node, ast.Constant) and isinstance(node.value, bool):
        return node.value
    return None


def _keyword_node(call: ast.Call, name: str) -> ast.expr | None:
    for keyword in call.keywords:
        if keyword.arg == name:
            return keyword.value
    return None


def library_root(module: str) -> str | None:
    """Return the persistence library that owns ``module``, or None."""
    for library in PERSISTENCE_LIBRARIES:
        if module == library or module.startswith(f"{library}."):
            return library
    return None


def skip_reason(relative_path: str) -> str | None:
    """Return why a manifest-matched file is out of scope, or None when it is in scope."""
    if not relative_path.endswith(PYTHON_SUFFIX):
        return "not a Python source file"
    location = service_location(relative_path)
    if location is None:
        return "outside the known application service layout"
    _, service_root = location
    remainder = relative_path[len(service_root) :].strip("/").split("/")
    if not remainder or remainder[0] not in IN_SCOPE_ROOT_SEGMENTS:
        return "outside the service src and migrations roots"
    directories, filename = remainder[:-1], remainder[-1]
    for part in directories:
        if part in EXCLUDED_PATH_SEGMENTS or part.endswith(".egg-info"):
            return f"inside excluded directory {part!r}"
        if part in TEST_PATH_SEGMENTS:
            return f"inside test directory {part!r}"
    if filename.startswith("test_") or filename.endswith("_test.py"):
        return "test module"
    if filename.endswith(GENERATED_FILENAME_SUFFIXES):
        return "generated module"
    return None


def is_generated_source(text: str) -> bool:
    """True when a file header marks it as machine generated."""
    header = "\n".join(text.splitlines()[:_GENERATED_HEADER_LINES]).lower()
    return any(marker in header for marker in GENERATED_HEADER_MARKERS)


def is_migration_path(relative_path: str) -> bool:
    """True when a file lives under a service's migrations root."""
    location = service_location(relative_path)
    if location is None:
        return False
    remainder = relative_path[len(location[1]) :].strip("/").split("/")
    return bool(remainder) and remainder[0] == MIGRATIONS_SEGMENT


# ---------------------------------------------------------------------------------------
# Per-module AST facts
# ---------------------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class ImportedSymbol:
    """One name bound by an ``import`` statement. ``name is None`` means a module alias."""

    module: str
    name: str | None
    lineno: int
    level: int = 0


@dataclass(frozen=True, slots=True)
class ColumnFact:
    """A statically declared relational column."""

    name: str
    declared_type: str | None
    annotation: str | None
    primary_key: bool
    nullable: bool | None
    unique: bool | None
    indexed: bool | None
    has_default: bool
    has_server_default: bool
    autoincrement: bool | None
    foreign_key: str | None
    constructor: str
    lineno: int
    end_lineno: int

    def summary(self) -> dict[str, Any]:
        payload: dict[str, Any] = {"name": self.name, "primary_key": self.primary_key}
        for key, value in (
            ("declared_type", self.declared_type),
            ("annotation", self.annotation),
            ("nullable", self.nullable),
            ("unique", self.unique),
            ("indexed", self.indexed),
            ("autoincrement", self.autoincrement),
            ("foreign_key", self.foreign_key),
        ):
            if value is not None:
                payload[key] = value
        payload["has_default"] = self.has_default
        payload["has_server_default"] = self.has_server_default
        payload["constructor"] = self.constructor
        payload["line"] = self.lineno
        return payload


@dataclass(frozen=True, slots=True)
class DocumentFieldFact:
    """A statically declared document field."""

    name: str
    annotation: str | None
    required: bool | None
    has_default: bool
    indexed: bool | None
    references: tuple[str, ...]
    lineno: int

    def summary(self) -> dict[str, Any]:
        payload: dict[str, Any] = {"name": self.name}
        if self.annotation:
            payload["annotation"] = self.annotation
        if self.required is not None:
            payload["required"] = self.required
        payload["has_default"] = self.has_default
        if self.indexed is not None:
            payload["indexed"] = self.indexed
        if self.references:
            payload["references"] = list(self.references)
        payload["line"] = self.lineno
        return payload


@dataclass(frozen=True, slots=True)
class OrmRelationshipFact:
    """An explicit ORM ``relationship(...)`` declaration."""

    attribute: str
    target_expression: str | None
    back_populates: str | None
    lineno: int

    def summary(self) -> dict[str, Any]:
        payload: dict[str, Any] = {"attribute": self.attribute, "line": self.lineno}
        if self.target_expression:
            payload["target"] = self.target_expression
        if self.back_populates:
            payload["back_populates"] = self.back_populates
        return payload


@dataclass(frozen=True, slots=True)
class ModelClassFact:
    """A class that may be a persistence model, with everything needed to decide."""

    name: str
    bases: tuple[ast.expr, ...]
    base_expressions: tuple[str, ...]
    table_name: str | None
    table_name_expression: str | None
    is_abstract: bool
    columns: tuple[ColumnFact, ...]
    relationships: tuple[OrmRelationshipFact, ...]
    fields: tuple[DocumentFieldFact, ...]
    collection_name: str | None
    collection_name_expression: str | None
    declared_indexes: tuple[str, ...]
    settings_present: bool
    class_attributes: dict[str, ast.expr]
    lineno: int
    end_lineno: int


@dataclass(frozen=True, slots=True)
class FunctionFacts:
    """A function or method and what this pass needs to trace persistence use through it."""

    name: str
    qualified_name: str
    owner_class: str | None
    parameters: tuple[str, ...]
    returns: ast.expr | None
    node: ast.FunctionDef | ast.AsyncFunctionDef
    lineno: int
    end_lineno: int


@dataclass(frozen=True, slots=True)
class MigrationFact:
    """An Alembic revision module."""

    revision: str
    down_revision: str | None
    description: str | None
    touched_tables: tuple[str, ...]
    operations: tuple[str, ...]
    lineno: int
    end_lineno: int


@dataclass(frozen=True, slots=True)
class ModuleFacts:
    """Everything this pass needs from one Python file."""

    relative_path: str
    service: str
    service_root: str
    module: str
    is_package: bool
    is_migration: bool
    source: str
    tree: ast.Module
    imports: dict[str, ImportedSymbol]
    constants: dict[str, ast.expr]
    classes: dict[str, ModelClassFact]
    functions: dict[str, FunctionFacts]
    migration: MigrationFact | None
    withheld_values: frozenset[str]

    def qualified(self, symbol: str) -> str:
        return f"{self.module}.{symbol}" if self.module else symbol


def _collect_imports(tree: ast.Module) -> dict[str, ImportedSymbol]:
    """Build the local-name -> imported-symbol table used for every resolution."""
    imports: dict[str, ImportedSymbol] = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.asname:
                    local, module = alias.asname, alias.name
                else:
                    local = module = alias.name.split(".", 1)[0]
                imports.setdefault(
                    local, ImportedSymbol(module=module, name=None, lineno=node.lineno)
                )
        elif isinstance(node, ast.ImportFrom):
            for alias in node.names:
                if alias.name == "*":
                    continue
                local = alias.asname or alias.name
                imports.setdefault(
                    local,
                    ImportedSymbol(
                        module=node.module or "",
                        name=alias.name,
                        lineno=node.lineno,
                        level=node.level,
                    ),
                )
    return imports


def _function_parameters(node: ast.FunctionDef | ast.AsyncFunctionDef) -> tuple[str, ...]:
    """Positional parameter names, with an implicit ``self``/``cls`` receiver dropped."""
    arguments = node.args
    names = [item.arg for item in (*arguments.posonlyargs, *arguments.args)]
    if names and names[0] in ("self", "cls"):
        names = names[1:]
    return tuple(names)


def _foreign_key_target(source: str, call: ast.Call) -> str | None:
    """Read the target of a ``ForeignKey("table.column")`` argument."""
    del source
    for argument in (*call.args, *(keyword.value for keyword in call.keywords)):
        inner = _unwrap(argument)
        if isinstance(inner, ast.Call):
            name = _dotted_expression(inner.func)
            if name and name.split(".")[-1] == FOREIGN_KEY_CONSTRUCTOR:
                target = _constant_string(inner.args[0]) if inner.args else None
                if target is None:
                    target = _constant_string(_keyword_node(inner, "column"))
                return target
    return None


def _column_fact(
    source: str,
    name: str,
    annotation: ast.expr | None,
    call: ast.Call,
    constructor: str,
    lineno: int,
    end_lineno: int,
) -> ColumnFact:
    """Project a ``Column(...)`` / ``mapped_column(...)`` declaration into metadata only."""
    declared_type: str | None = None
    for argument in call.args:
        inner = _unwrap(argument)
        dotted = _dotted_expression(inner.func) if isinstance(inner, ast.Call) else None
        if dotted and dotted.split(".")[-1] == FOREIGN_KEY_CONSTRUCTOR:
            continue
        declared_type = _expression_text(source, argument)
        break
    if declared_type is None:
        declared_type = _expression_text(source, _keyword_node(call, "type_"))

    return ColumnFact(
        name=name,
        declared_type=declared_type,
        annotation=_expression_text(source, annotation),
        primary_key=bool(_constant_bool(_keyword_node(call, "primary_key"))),
        nullable=_constant_bool(_keyword_node(call, "nullable")),
        unique=_constant_bool(_keyword_node(call, "unique")),
        indexed=_constant_bool(_keyword_node(call, "index")),
        # Only the *presence* of a default is recorded. The expression is never evaluated
        # and never emitted, so a credential default cannot escape through it.
        has_default=_keyword_node(call, "default") is not None,
        has_server_default=_keyword_node(call, "server_default") is not None,
        autoincrement=_constant_bool(_keyword_node(call, "autoincrement")),
        foreign_key=_foreign_key_target(source, call),
        constructor=constructor,
        lineno=lineno,
        end_lineno=end_lineno,
    )


def _document_references(source: str, annotation: ast.expr | None) -> tuple[str, ...]:
    """Collect explicit ODM reference constructs such as ``Link[OrderItem]``."""
    del source
    if annotation is None:
        return ()
    targets: list[str] = []
    for node in ast.walk(annotation):
        if not isinstance(node, ast.Subscript):
            continue
        owner = _dotted_expression(node.value)
        if owner is None or owner.split(".")[-1] not in DOCUMENT_LINK_CONSTRUCTS:
            continue
        inner = node.slice
        elements = inner.elts if isinstance(inner, ast.Tuple) else [inner]
        for element in elements:
            dotted = _dotted_expression(element)
            if dotted:
                targets.append(dotted)
    return tuple(sorted(set(targets)))


def _settings_facts(
    source: str, node: ast.ClassDef
) -> tuple[str | None, str | None, tuple[str, ...], bool]:
    """Read a nested ``class Settings`` for collection name and declared indexes."""
    for member in node.body:
        if not isinstance(member, ast.ClassDef) or member.name not in ("Settings", "Config"):
            continue
        collection_name: str | None = None
        collection_expression: str | None = None
        indexes: list[str] = []
        for statement in member.body:
            targets: list[ast.expr] = []
            value: ast.expr | None = None
            if isinstance(statement, ast.Assign):
                targets = list(statement.targets)
                value = statement.value
            elif isinstance(statement, ast.AnnAssign):
                targets = [statement.target]
                value = statement.value
            for target in targets:
                if not isinstance(target, ast.Name):
                    continue
                if target.id in ("name", "collection", "collection_name"):
                    collection_name = _constant_string(value)
                    if collection_name is None:
                        collection_expression = _expression_text(source, value)
                elif target.id == "indexes" and isinstance(value, ast.List | ast.Tuple):
                    for element in value.elts:
                        inner = _unwrap(element)
                        literal = _constant_string(inner)
                        if literal is not None:
                            indexes.append(literal)
                            continue
                        if isinstance(inner, ast.Call):
                            dotted = _dotted_expression(inner.func)
                            if dotted and dotted.split(".")[-1] == INDEX_MODEL_CONSTRUCTOR:
                                declared = _constant_string(_keyword_node(inner, "name"))
                                indexes.append(declared or (_expression_text(source, inner) or ""))
        return collection_name, collection_expression, tuple(indexes), True
    return None, None, (), False


def _model_class_fact(source: str, node: ast.ClassDef) -> ModelClassFact:
    """Collect every declaration of a class that could be a persistence model."""
    columns: list[ColumnFact] = []
    relationships: list[OrmRelationshipFact] = []
    fields: list[DocumentFieldFact] = []
    attributes: dict[str, ast.expr] = {}
    table_name: str | None = None
    table_name_expression: str | None = None
    is_abstract = False

    for statement in node.body:
        annotation: ast.expr | None = None
        targets: list[ast.expr] = []
        value: ast.expr | None = None
        if isinstance(statement, ast.AnnAssign) and isinstance(statement.target, ast.Name):
            annotation = statement.annotation
            targets = [statement.target]
            value = statement.value
        elif isinstance(statement, ast.Assign):
            targets = list(statement.targets)
            value = statement.value
        else:
            continue

        for target in targets:
            if not isinstance(target, ast.Name):
                continue
            name = target.id
            attributes.setdefault(name, value) if value is not None else None

            if name == "__tablename__":
                table_name = _constant_string(value)
                if table_name is None:
                    table_name_expression = _expression_text(source, value)
                continue
            if name == "__abstract__":
                is_abstract = bool(_constant_bool(value))
                continue
            if name.startswith("__") and name.endswith("__"):
                continue

            inner = _unwrap(value) if value is not None else None
            constructor = (
                (_dotted_expression(inner.func) or "").split(".")[-1]
                if isinstance(inner, ast.Call)
                else None
            )
            if isinstance(inner, ast.Call) and constructor in COLUMN_CONSTRUCTORS:
                columns.append(
                    _column_fact(
                        source,
                        name,
                        annotation,
                        inner,
                        constructor,
                        statement.lineno,
                        statement.end_lineno or statement.lineno,
                    )
                )
                continue
            if isinstance(inner, ast.Call) and constructor == RELATIONSHIP_CONSTRUCTOR:
                target_expression = (
                    _expression_text(source, inner.args[0]) if inner.args else None
                )
                relationships.append(
                    OrmRelationshipFact(
                        attribute=name,
                        target_expression=target_expression,
                        back_populates=_constant_string(
                            _keyword_node(inner, "back_populates")
                        ),
                        lineno=statement.lineno,
                    )
                )
                continue
            if annotation is not None:
                indexed: bool | None = None
                required: bool | None = None
                if isinstance(inner, ast.Call):
                    indexed = _constant_bool(_keyword_node(inner, "index"))
                    # ``Field(...)`` with Ellipsis as first argument means required.
                    if inner.args and isinstance(inner.args[0], ast.Constant):
                        required = inner.args[0].value is Ellipsis
                fields.append(
                    DocumentFieldFact(
                        name=name,
                        annotation=_expression_text(source, annotation),
                        required=required if required is not None else (value is None or None),
                        has_default=value is not None,
                        indexed=indexed,
                        references=_document_references(source, annotation),
                        lineno=statement.lineno,
                    )
                )

    collection_name, collection_expression, indexes, settings_present = _settings_facts(
        source, node
    )
    return ModelClassFact(
        name=node.name,
        bases=tuple(node.bases),
        base_expressions=tuple(
            _expression_text(source, base) or "<unresolved>" for base in node.bases
        ),
        table_name=table_name,
        table_name_expression=table_name_expression,
        is_abstract=is_abstract,
        columns=tuple(columns),
        relationships=tuple(relationships),
        fields=tuple(fields),
        collection_name=collection_name,
        collection_name_expression=collection_expression,
        declared_indexes=indexes,
        settings_present=settings_present,
        class_attributes=attributes,
        lineno=node.lineno,
        end_lineno=node.end_lineno or node.lineno,
    )


def _migration_fact(source: str, tree: ast.Module) -> MigrationFact | None:
    """Read an Alembic revision module: its identifier and the tables it names."""
    constants: dict[str, ast.expr] = {}
    for statement in tree.body:
        if isinstance(statement, ast.Assign):
            for target in statement.targets:
                if isinstance(target, ast.Name):
                    constants.setdefault(target.id, statement.value)
    revision = _constant_string(constants.get("revision"))
    if revision is None:
        return None

    tables: set[str] = set()
    operations: set[str] = set()
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call) or not isinstance(node.func, ast.Attribute):
            continue
        operation = node.func.attr
        if operation not in ALEMBIC_TABLE_OPERATIONS:
            continue
        operations.add(operation)
        named = _constant_string(node.args[0]) if node.args else None
        if named is None:
            named = _constant_string(_keyword_node(node, "table_name"))
        if named:
            tables.add(named)

    docstring = ast.get_docstring(tree)
    description = docstring.strip().splitlines()[0].strip() if docstring else None
    return MigrationFact(
        revision=revision,
        down_revision=_constant_string(constants.get("down_revision")),
        description=redact_uri(description) if description else None,
        touched_tables=tuple(sorted(tables)),
        operations=tuple(sorted(operations)),
        lineno=1,
        end_lineno=len(source.splitlines()) or 1,
    )


def _collect_withheld(tree: ast.Module) -> set[str]:
    """Collect credential literals so leaks can be measured rather than assumed."""
    withheld: set[str] = set()

    def remember(value: str | None) -> None:
        if value and len(value.strip()) >= _MIN_SCANNABLE_SECRET_LENGTH:
            withheld.add(value.strip())

    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                name = target.id if isinstance(target, ast.Name) else getattr(target, "attr", "")
                if name and is_sensitive_name(name):
                    remember(_constant_string(node.value))
        elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            if is_sensitive_name(node.target.id):
                remember(_constant_string(node.value))
        elif isinstance(node, ast.Call):
            for keyword in node.keywords:
                if keyword.arg and is_sensitive_name(keyword.arg):
                    remember(_constant_string(keyword.value))
            positional = [_constant_string(item) for item in node.args]
            if any(text is not None and is_sensitive_name(text) for text in positional):
                for keyword in node.keywords:
                    remember(_constant_string(keyword.value))
        elif isinstance(node, ast.Constant) and isinstance(node.value, str):
            userinfo = _URI_USERINFO_PATTERN.search(node.value)
            if userinfo is not None:
                remember(userinfo.group(2))
    return withheld


def analyze_module(
    source: str,
    tree: ast.Module,
    *,
    relative_path: str,
    service: str,
    service_root: str,
    module: str,
    is_package: bool,
    warnings: list[str],
) -> ModuleFacts:
    """Gather imports, constants, model classes, functions, and migrations from one module."""
    imports = _collect_imports(tree)
    constants: dict[str, ast.expr] = {}
    classes: dict[str, ModelClassFact] = {}
    functions: dict[str, FunctionFacts] = {}

    def register_function(
        node: ast.FunctionDef | ast.AsyncFunctionDef, owner: str | None
    ) -> FunctionFacts:
        return FunctionFacts(
            name=node.name,
            qualified_name=f"{owner}.{node.name}" if owner else node.name,
            owner_class=owner,
            parameters=_function_parameters(node),
            returns=node.returns,
            node=node,
            lineno=node.lineno,
            end_lineno=node.end_lineno or node.lineno,
        )

    for statement in tree.body:
        if isinstance(statement, ast.Assign):
            for target in statement.targets:
                if isinstance(target, ast.Name):
                    constants.setdefault(target.id, statement.value)
        elif isinstance(statement, ast.AnnAssign) and isinstance(statement.target, ast.Name):
            if statement.value is not None:
                constants.setdefault(statement.target.id, statement.value)
        elif isinstance(statement, ast.FunctionDef | ast.AsyncFunctionDef):
            if statement.name in functions:
                warnings.append(
                    f"{relative_path}: function {statement.name!r} is defined more than once; "
                    f"kept the first definition at line {functions[statement.name].lineno}"
                )
            else:
                functions[statement.name] = register_function(statement, None)
        elif isinstance(statement, ast.ClassDef):
            if statement.name in classes:
                warnings.append(
                    f"{relative_path}: class {statement.name!r} is defined more than once; "
                    f"kept the first definition at line {classes[statement.name].lineno}"
                )
                continue
            classes[statement.name] = _model_class_fact(source, statement)
            for member in statement.body:
                if isinstance(member, ast.FunctionDef | ast.AsyncFunctionDef):
                    functions.setdefault(
                        f"{statement.name}.{member.name}",
                        register_function(member, statement.name),
                    )

    is_migration = is_migration_path(relative_path)
    return ModuleFacts(
        relative_path=relative_path,
        service=service,
        service_root=service_root,
        module=module,
        is_package=is_package,
        is_migration=is_migration,
        source=source,
        tree=tree,
        imports=imports,
        constants=constants,
        classes=classes,
        functions=functions,
        migration=_migration_fact(source, tree) if is_migration else None,
        withheld_values=frozenset(_collect_withheld(tree)),
    )


# ---------------------------------------------------------------------------------------
# Symbol resolution
# ---------------------------------------------------------------------------------------

SYMBOL_CLASS = "class"
SYMBOL_FUNCTION = "function"
SYMBOL_CONSTANT = "constant"
SYMBOL_MODULE = "module"
SYMBOL_LIBRARY = "persistence_library"
SYMBOL_EXTERNAL = "external"
SYMBOL_UNKNOWN = "unknown"


@dataclass(frozen=True, slots=True)
class SymbolRef:
    """Where a name was traced to."""

    kind: str
    module: str | None = None
    name: str | None = None
    library: str | None = None
    reason: str | None = None


@dataclass(frozen=True, slots=True)
class SourceIndex:
    """All analyzed modules, addressable by dotted name and by dotted suffix."""

    modules: dict[tuple[str, str], ModuleFacts]
    suffixes: dict[tuple[str, str], frozenset[str]]

    def facts(self, service: str, module: str) -> ModuleFacts | None:
        return self.modules.get((service, module))

    def resolve_module(
        self, service: str, current_module: str, imported: ImportedSymbol
    ) -> str | None:
        """Resolve an import target to a scanned module name, or None when external."""
        if imported.level:
            facts = self.facts(service, current_module)
            parts = current_module.split(".") if current_module else []
            base = parts if (facts is not None and facts.is_package) else parts[:-1]
            drop = imported.level - 1
            if drop:
                base = base[:-drop] if drop <= len(base) else []
            tail = imported.module.split(".") if imported.module else []
            target = ".".join(part for part in [*base, *tail] if part)
        else:
            target = imported.module
        if not target:
            return None
        if (service, target) in self.modules:
            return target
        candidates = self.suffixes.get((service, target))
        if candidates and len(candidates) == 1:
            return next(iter(candidates))
        return None

    def resolve_symbol(
        self,
        service: str,
        module: str,
        name: str,
        *,
        _seen: frozenset[tuple[str, str, str]] = frozenset(),
    ) -> SymbolRef:
        """Trace ``name`` from ``module`` to its definition, following import aliases."""
        if len(_seen) > _MAX_RESOLUTION_DEPTH:
            return SymbolRef(SYMBOL_UNKNOWN, module, name, reason="resolution depth exceeded")
        facts = self.facts(service, module)
        if facts is None:
            return SymbolRef(
                SYMBOL_EXTERNAL, module, name, reason="module is outside scanned source"
            )
        if name in facts.classes:
            return SymbolRef(SYMBOL_CLASS, module, name)
        if name in facts.functions:
            return SymbolRef(SYMBOL_FUNCTION, module, name)
        if name in facts.constants:
            return SymbolRef(SYMBOL_CONSTANT, module, name)

        imported = facts.imports.get(name)
        if imported is None:
            return SymbolRef(
                SYMBOL_UNKNOWN, module, name, reason="name is not defined or imported here"
            )
        library = library_root(imported.module)
        if library is not None:
            return SymbolRef(
                SYMBOL_LIBRARY, imported.module, imported.name or name, library=library
            )
        target_module = self.resolve_module(service, module, imported)
        if target_module is None:
            return SymbolRef(
                SYMBOL_EXTERNAL,
                imported.module or module,
                imported.name or name,
                reason="imported from a module outside scanned source",
            )
        if imported.name is None:
            return SymbolRef(SYMBOL_MODULE, target_module, None)
        key = (service, target_module, imported.name)
        if key in _seen:
            return SymbolRef(SYMBOL_UNKNOWN, target_module, imported.name, reason="import cycle")
        return self.resolve_symbol(service, target_module, imported.name, _seen=_seen | {key})

    def resolve_dotted(self, service: str, module: str, dotted: str) -> SymbolRef:
        """Resolve ``a.b.c`` where ``a`` is a name in ``module``."""
        parts = dotted.split(".")
        head = self.resolve_symbol(service, module, parts[0])
        if len(parts) == 1:
            return head
        if head.kind == SYMBOL_LIBRARY:
            return SymbolRef(SYMBOL_LIBRARY, head.module, parts[-1], library=head.library)
        if head.kind == SYMBOL_MODULE and head.module is not None:
            return self.resolve_dotted(service, head.module, ".".join(parts[1:]))
        if head.kind == SYMBOL_CLASS:
            return head
        return SymbolRef(
            SYMBOL_UNKNOWN, module, dotted, reason="attribute chain could not be traced"
        )

    def resolve_class(
        self, service: str, module: str, node: ast.expr, *, _depth: int = 0
    ) -> tuple[str, str] | None:
        """Resolve an expression to a locally defined class as ``(module, class name)``.

        A module-level alias is followed, which is what lets FTGO's restaurant service work:
        ``models/base.py`` declares ``Base: Type[DeclarativeBase] = DBTable`` and every model
        inherits from that alias rather than from the class directly.
        """
        if _depth > _MAX_RESOLUTION_DEPTH:
            return None
        dotted = _dotted_expression(node)
        if dotted is None:
            return None
        resolved = self.resolve_dotted(service, module, dotted)
        if (
            resolved.kind == SYMBOL_CLASS
            and resolved.module is not None
            and resolved.name is not None
        ):
            return resolved.module, resolved.name
        if (
            resolved.kind == SYMBOL_CONSTANT
            and resolved.module is not None
            and resolved.name is not None
        ):
            target = self.facts(service, resolved.module)
            if target is not None:
                value = target.constants.get(resolved.name)
                if value is not None:
                    return self.resolve_class(
                        service, resolved.module, value, _depth=_depth + 1
                    )
        return None

    def base_chain(
        self, service: str, module: str, class_name: str
    ) -> list[tuple[str, str, ModelClassFact]]:
        """Return the class and its locally resolvable ancestors, nearest first."""
        chain: list[tuple[str, str, ModelClassFact]] = []
        seen: set[tuple[str, str]] = set()
        queue: list[tuple[str, str]] = [(module, class_name)]
        while queue and len(chain) <= _MAX_RESOLUTION_DEPTH:
            current_module, current_name = queue.pop(0)
            if (current_module, current_name) in seen:
                continue
            seen.add((current_module, current_name))
            facts = self.facts(service, current_module)
            if facts is None:
                continue
            declaration = facts.classes.get(current_name)
            if declaration is None:
                continue
            chain.append((current_module, current_name, declaration))
            for base in declaration.bases:
                resolved = self.resolve_class(service, current_module, base)
                if resolved is not None:
                    queue.append(resolved)
        return chain

    def library_base(
        self, service: str, module: str, class_name: str
    ) -> tuple[str, str, str] | None:
        """Find the persistence-library base a class ultimately inherits from.

        Returns ``(library, symbol, declaring module)``. This is the rooting step: without a
        library base a class is not a persistence model no matter how many fields it has.
        """
        for current_module, _, declaration in self.base_chain(service, module, class_name):
            for base in declaration.bases:
                dotted = _dotted_expression(base)
                if dotted is None:
                    continue
                resolved = self.resolve_dotted(service, current_module, dotted)
                if resolved.kind == SYMBOL_LIBRARY and resolved.library is not None:
                    return resolved.library, resolved.name or dotted, current_module
                # An alias may hide the library base behind a module constant.
                if resolved.kind == SYMBOL_CONSTANT and resolved.module is not None:
                    target = self.facts(service, resolved.module)
                    if target is None or resolved.name is None:
                        continue
                    value = target.constants.get(resolved.name)
                    if value is None:
                        continue
                    aliased = self.resolve_class(service, resolved.module, value)
                    if aliased is not None:
                        nested = self.library_base(service, aliased[0], aliased[1])
                        if nested is not None:
                            return nested
        return None


def build_source_index(modules: list[ModuleFacts]) -> SourceIndex:
    """Index analyzed modules by exact dotted name and by every dotted suffix."""
    indexed: dict[tuple[str, str], ModuleFacts] = {}
    suffix_sets: dict[tuple[str, str], set[str]] = {}
    for item in sorted(modules, key=lambda entry: (entry.service, entry.module)):
        indexed.setdefault((item.service, item.module), item)
        if not item.module:
            continue
        parts = item.module.split(".")
        for start in range(len(parts)):
            suffix_sets.setdefault((item.service, ".".join(parts[start:])), set()).add(item.module)
    return SourceIndex(
        modules=indexed,
        suffixes={key: frozenset(value) for key, value in suffix_sets.items()},
    )


# ---------------------------------------------------------------------------------------
# Model classification
# ---------------------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class ModelClassification:
    """The proven persistence identity of a class."""

    role: str
    library: str
    base_symbol: str
    engine: str


def classify_model(
    index: SourceIndex, service: str, module: str, class_name: str
) -> ModelClassification | None:
    """Decide whether a class is a persistence model, and of which kind.

    Rooting is mandatory. A Pydantic ``BaseModel`` request schema and a plain domain class
    both return ``None`` here, because ``pydantic`` is not a persistence library and a bare
    class has no library base at all.
    """
    rooted = index.library_base(service, module, class_name)
    if rooted is None:
        return None
    library, symbol, _ = rooted
    if library in RELATIONAL_LIBRARIES and symbol in RELATIONAL_BASE_SYMBOLS:
        role = PERSISTENCE_ROLE_TABLE
    elif library in DOCUMENT_LIBRARIES and symbol in DOCUMENT_BASE_SYMBOLS:
        role = PERSISTENCE_ROLE_DOCUMENT
    else:
        return None
    return ModelClassification(
        role=role,
        library=library,
        base_symbol=symbol,
        engine=LIBRARY_ENGINES.get(library, library),
    )


@dataclass(frozen=True, slots=True)
class InheritedColumn:
    """A column together with the class that declared it."""

    column: ColumnFact
    declaring_module: str
    declaring_class: str
    declaring_path: str


def collect_columns(
    index: SourceIndex, service: str, module: str, class_name: str
) -> list[InheritedColumn]:
    """Collect a mapped class's own columns plus those inherited from abstract bases.

    Inherited columns are real columns of the physical table: FTGO declares ``id``,
    ``created_at`` and ``updated_at`` once on an ``__abstract__`` ``Base`` and every concrete
    table carries them. Omitting them would misrepresent the schema; inventing them would be
    worse, so each one keeps provenance pointing at the base class that declared it.
    """
    collected: dict[str, InheritedColumn] = {}
    for current_module, current_name, declaration in index.base_chain(
        service, module, class_name
    ):
        facts = index.facts(service, current_module)
        path = facts.relative_path if facts is not None else current_module
        for column in declaration.columns:
            # Nearest definition wins: the chain is ordered child first.
            if column.name not in collected:
                collected[column.name] = InheritedColumn(
                    column=column,
                    declaring_module=current_module,
                    declaring_class=current_name,
                    declaring_path=path,
                )
    return [collected[name] for name in sorted(collected)]


def collect_document_fields(
    index: SourceIndex, service: str, module: str, class_name: str
) -> list[DocumentFieldFact]:
    """Collect a document model's own fields plus those inherited from local bases."""
    collected: dict[str, DocumentFieldFact] = {}
    for current_module, _, declaration in index.base_chain(service, module, class_name):
        del current_module
        for item in declaration.fields:
            if item.name not in collected:
                collected[item.name] = item
    return [collected[name] for name in sorted(collected)]


# ---------------------------------------------------------------------------------------
# Candidate model
# ---------------------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class ServiceScan:
    """One existing application service and what this pass found inside it."""

    slug: str
    entity_id: str
    python_files: int
    libraries: tuple[str, ...]
    tables: int
    collections: int
    document_models: int
    migrations: int
    database: str | None

    def summary(self) -> dict[str, Any]:
        return {
            "service": self.entity_id,
            "slug": self.slug,
            "python_files": self.python_files,
            "persistence_libraries": list(self.libraries),
            "tables": self.tables,
            "collections": self.collections,
            "document_models": self.document_models,
            "migrations": self.migrations,
            "database": self.database,
        }


@dataclass(frozen=True, slots=True)
class ColumnCandidate:
    id: str
    kind: str
    title: str
    service: str
    table_id: str
    table_name: str
    column: ColumnFact
    declaring_class: str
    provenance: Provenance

    def summary(self) -> dict[str, Any]:
        payload = {
            "id": self.id,
            "kind": self.kind,
            "table": self.table_id,
            "declaring_class": self.declaring_class,
        }
        payload.update(self.column.summary())
        payload["source"] = self.provenance.as_dict()
        return payload


@dataclass(frozen=True, slots=True)
class TableCandidate:
    id: str
    kind: str
    title: str
    service: str
    table_name: str
    model_class: str
    library: str
    engine: str
    database: str | None
    primary_key: tuple[str, ...]
    foreign_keys: tuple[dict[str, str], ...]
    unique_columns: tuple[str, ...]
    indexed_columns: tuple[str, ...]
    orm_relationships: tuple[OrmRelationshipFact, ...]
    schema_name: str | None
    provenance: Provenance
    attributes: dict[str, Any] = field(default_factory=dict)

    def summary(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "kind": self.kind,
            "table_name": self.table_name,
            "service": self.service,
            "model_class": self.model_class,
            "persistence_library": self.library,
            "storage_engine": self.engine,
            "database": self.database,
            "primary_key": list(self.primary_key),
            "foreign_keys": [dict(item) for item in self.foreign_keys],
            "unique_columns": list(self.unique_columns),
            "indexed_columns": list(self.indexed_columns),
            "orm_relationships": [item.summary() for item in self.orm_relationships],
            "schema": self.schema_name,
            "attributes": self.attributes,
            "source": self.provenance.as_dict(),
        }


@dataclass(frozen=True, slots=True)
class DocumentSchemaCandidate:
    id: str
    kind: str
    title: str
    service: str
    model_class: str
    qualified_name: str
    library: str
    engine: str
    database: str | None
    collection_name: str | None
    fields: tuple[DocumentFieldFact, ...]
    declared_indexes: tuple[str, ...]
    references: tuple[str, ...]
    provenance: Provenance
    attributes: dict[str, Any] = field(default_factory=dict)

    def summary(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "kind": self.kind,
            "persistence_role": PERSISTENCE_ROLE_DOCUMENT,
            "service": self.service,
            "model_class": self.model_class,
            "qualified_name": self.qualified_name,
            "persistence_library": self.library,
            "storage_engine": self.engine,
            "database": self.database,
            "collection": self.collection_name,
            "fields": [item.summary() for item in self.fields],
            "declared_indexes": list(self.declared_indexes),
            "references": list(self.references),
            "attributes": self.attributes,
            "source": self.provenance.as_dict(),
        }


@dataclass(frozen=True, slots=True)
class CollectionCandidate:
    """A physical MongoDB collection proven by an explicit collection name in source."""

    id: str
    kind: str
    title: str
    service: str
    collection_name: str
    library: str
    engine: str
    database: str | None
    schema_id: str
    model_class: str
    declared_indexes: tuple[str, ...]
    provenance: Provenance
    attributes: dict[str, Any] = field(default_factory=dict)

    def summary(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "kind": self.kind,
            "collection_name": self.collection_name,
            "service": self.service,
            "database": self.database,
            "schema": self.schema_id,
            "model_class": self.model_class,
            "persistence_library": self.library,
            "storage_engine": self.engine,
            "declared_indexes": list(self.declared_indexes),
            "attributes": self.attributes,
            "source": self.provenance.as_dict(),
        }


@dataclass(frozen=True, slots=True)
class MigrationCandidate:
    id: str
    kind: str
    title: str
    service: str
    revision: str
    down_revision: str | None
    tool: str
    touched_tables: tuple[str, ...]
    operations: tuple[str, ...]
    provenance: Provenance

    def summary(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "kind": self.kind,
            "service": self.service,
            "revision": self.revision,
            "down_revision": self.down_revision,
            "tool": self.tool,
            "touched_tables": list(self.touched_tables),
            "operations": list(self.operations),
            "source": self.provenance.as_dict(),
        }


@dataclass(frozen=True, slots=True)
class CallSite:
    """One concrete source location that supports a semantic access relationship."""

    operation: str
    expression: str | None
    resolution: str
    provenance: Provenance

    @property
    def path(self) -> str:
        return self.provenance.source_path

    @property
    def symbol(self) -> str:
        return self.provenance.symbol or ""

    @property
    def line(self) -> int:
        return self.provenance.line_start or 0

    @property
    def key(self) -> tuple[str, int, str, str]:
        return (self.path, self.line, self.operation, self.resolution)

    def summary(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "operation": self.operation,
            "resolution": self.resolution,
        }
        if self.expression:
            payload["call"] = self.expression
        payload.update(self.provenance.as_dict())
        return payload


@dataclass(frozen=True, slots=True)
class AccessCandidate:
    """A deduplicated ``Service -READS/WRITES-> target`` with every supporting call site."""

    service: str
    role: str
    relation_type: str
    target: str
    target_kind: str
    library: str
    call_sites: tuple[CallSite, ...]

    @property
    def anchor_provenance(self) -> Provenance:
        """Provenance of the first supporting call site in deterministic order."""
        return self.call_sites[0].provenance

    def summary(self) -> dict[str, Any]:
        return {
            "service": service_entity_id_placeholder(self.service),
            "role": self.role,
            "type": self.relation_type,
            "target": self.target,
            "target_kind": self.target_kind,
            "persistence_library": self.library,
            "call_site_count": len(self.call_sites),
            "call_sites": [item.summary() for item in self.call_sites],
        }


def service_entity_id_placeholder(value: str) -> str:
    """Return an already-qualified service id unchanged.

    Access candidates store the fully qualified service entity id, so this keeps the
    summary readable without re-deriving the repository slug.
    """
    return value


@dataclass(frozen=True, slots=True)
class RelationshipCandidate:
    source: str
    type: str
    target: str
    provenance: Provenance
    role: str | None = None
    detail: dict[str, Any] = field(default_factory=dict)

    def summary(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "source": self.source,
            "type": self.type,
            "target": self.target,
        }
        if self.role:
            payload["role"] = self.role
        payload.update(self.detail)
        payload["source_evidence"] = self.provenance.as_dict()
        return payload


@dataclass(frozen=True, slots=True)
class DatabaseMapping:
    """A proven service-to-database correlation."""

    service: str
    service_entity_id: str
    database: str
    engine: str
    libraries: tuple[str, ...]
    evidence: tuple[str, ...]
    provenance: Provenance

    def summary(self) -> dict[str, Any]:
        return {
            "service": self.service_entity_id,
            "database": self.database,
            "storage_engine": self.engine,
            "persistence_libraries": list(self.libraries),
            "evidence": list(self.evidence),
            "source": self.provenance.as_dict(),
        }


@dataclass(frozen=True, slots=True)
class UnresolvedFinding:
    """Anything this pass refused to guess."""

    category: str
    service: str | None
    subject: str
    reason: str
    provenance: Provenance | None = None

    def summary(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "category": self.category,
            "subject": self.subject,
            "reason": self.reason,
        }
        if self.service:
            payload["service"] = self.service
        if self.provenance is not None:
            payload["source_evidence"] = self.provenance.as_dict()
        return payload


@dataclass(frozen=True, slots=True)
class IdentityCollision:
    entity_id: str
    kind: str
    participants: tuple[str, ...]

    def summary(self) -> dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "kind": self.kind,
            "participants": list(self.participants),
            "reason": (
                "distinct source declarations normalize to the same entity id; no entity or "
                "relationship was created and human review is required"
            ),
        }


@dataclass(frozen=True, slots=True)
class OntologyGap:
    """A persistence concept the current ontology cannot express faithfully."""

    concept: str
    requested_kind: str
    modelled_as: str
    reason: str
    evidence: tuple[str, ...]

    def summary(self) -> dict[str, Any]:
        return {
            "concept": self.concept,
            "requested_kind": self.requested_kind,
            "modelled_as": self.modelled_as,
            "reason": self.reason,
            "evidence": list(self.evidence),
            "action": "requires an explicit ontology decision in a separate change",
        }


@dataclass(frozen=True, slots=True)
class DataModelExtraction:
    repository: str
    commit: str
    owner: str | None
    source_files: tuple[str, ...]
    skipped_files: tuple[str, ...]
    services_scanned: tuple[ServiceScan, ...]
    libraries: tuple[str, ...]
    wrappers: tuple[str, ...]
    tables: tuple[TableCandidate, ...]
    columns: tuple[ColumnCandidate, ...]
    collections: tuple[CollectionCandidate, ...]
    document_schemas: tuple[DocumentSchemaCandidate, ...]
    migrations: tuple[MigrationCandidate, ...]
    database_mappings: tuple[DatabaseMapping, ...]
    accesses: tuple[AccessCandidate, ...]
    relationships: tuple[RelationshipCandidate, ...]
    unresolved: tuple[UnresolvedFinding, ...]
    identity_collisions: tuple[IdentityCollision, ...]
    ontology_gaps: tuple[OntologyGap, ...]
    warnings: tuple[str, ...]
    withheld_values: frozenset[str]

    def unresolved_of(self, category: str) -> tuple[UnresolvedFinding, ...]:
        return tuple(item for item in self.unresolved if item.category == category)

    def relations_for(self, entity_id: str) -> tuple[RelationshipCandidate, ...]:
        return tuple(item for item in self.relationships if item.source == entity_id)

    def inbound_relations_for(self, entity_id: str) -> tuple[RelationshipCandidate, ...]:
        return tuple(item for item in self.relationships if item.target == entity_id)


UNRESOLVED_DATABASE = "unresolved_database_mappings"
UNRESOLVED_TABLE_NAME = "unresolved_table_names"
UNRESOLVED_COLLECTION_NAME = "unresolved_collection_names"
UNRESOLVED_MODEL_REFERENCE = "unresolved_model_references"
UNRESOLVED_ACCESS = "unresolved_accesses"


# ---------------------------------------------------------------------------------------
# Persistence value typing and scopes
# ---------------------------------------------------------------------------------------

VALUE_LIBRARY = "library"
VALUE_MODEL = "model"
VALUE_UNKNOWN = "unknown"

# Members of a rooted persistence object whose result is still a rooted persistence object.
LIBRARY_FACTORY_MEMBERS = frozenset(
    {
        "begin",
        "connect",
        "create",
        "create_async_engine",
        "get_database",
        "get_or_create_session",
        "get_session",
        "session",
        "sessionmaker",
    }
)


@dataclass(frozen=True, slots=True)
class ValueType:
    kind: str
    library: str | None = None
    module: str | None = None
    class_name: str | None = None

    @property
    def is_library(self) -> bool:
        return self.kind == VALUE_LIBRARY

    @property
    def is_model(self) -> bool:
        return self.kind == VALUE_MODEL


UNKNOWN_VALUE = ValueType(VALUE_UNKNOWN)


@dataclass
class Scope:
    """Flat per-function view of local bindings.

    Bindings are gathered for the whole function body rather than per block, which is what
    lets an operation inside ``async with ... as session: try: ...`` still see the session.
    """

    values: dict[str, ValueType] = field(default_factory=dict)
    expressions: dict[str, ast.expr] = field(default_factory=dict)
    parameters: tuple[str, ...] = ()


def _scope_nodes(root: ast.AST) -> list[ast.AST]:
    """All descendants of ``root`` without entering a nested function or class scope."""
    collected: list[ast.AST] = []
    stack: list[ast.AST] = list(ast.iter_child_nodes(root))
    while stack:
        node = stack.pop()
        collected.append(node)
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
            continue
        stack.extend(ast.iter_child_nodes(node))
    return collected


class PersistenceTyper:
    """Infers whether an expression is a rooted persistence object or a model, in bounds."""

    def __init__(self, index: SourceIndex) -> None:
        self.index = index

    def annotation_type(
        self, service: str, module: str, annotation: ast.expr | None, hops: int
    ) -> ValueType:
        if annotation is None or hops > _MAX_VALUE_HOPS:
            return UNKNOWN_VALUE
        for node in ast.walk(annotation):
            if not isinstance(node, ast.Name | ast.Attribute):
                continue
            dotted = _dotted_expression(node)
            if dotted is None:
                continue
            resolved = self.index.resolve_dotted(service, module, dotted)
            if resolved.kind == SYMBOL_LIBRARY and resolved.library is not None:
                return ValueType(VALUE_LIBRARY, library=resolved.library)
            model = self.index.resolve_class(service, module, node)
            if model is not None and classify_model(self.index, service, *model) is not None:
                return ValueType(VALUE_MODEL, module=model[0], class_name=model[1])
        return UNKNOWN_VALUE

    def class_attribute_type(
        self, service: str, module: str, owner_class: str, attribute: str, hops: int
    ) -> ValueType:
        """Type a ``cls.X`` / ``self.X`` class attribute from its annotation or its value."""
        if hops > _MAX_VALUE_HOPS:
            return UNKNOWN_VALUE
        for current_module, _, declaration in self.index.base_chain(service, module, owner_class):
            value = declaration.class_attributes.get(attribute)
            if value is not None:
                model = self.index.resolve_class(service, current_module, value)
                if model is not None and classify_model(self.index, service, *model) is not None:
                    return ValueType(VALUE_MODEL, module=model[0], class_name=model[1])
            facts = self.index.facts(service, current_module)
            if facts is None:
                continue
            node = facts.tree
            for statement in ast.walk(node):
                if (
                    isinstance(statement, ast.AnnAssign)
                    and isinstance(statement.target, ast.Name)
                    and statement.target.id == attribute
                ):
                    typed = self.annotation_type(
                        service, current_module, statement.annotation, hops + 1
                    )
                    if typed.kind != VALUE_UNKNOWN:
                        return typed
        return UNKNOWN_VALUE

    def value_type(
        self,
        service: str,
        module: str,
        node: ast.expr | None,
        scope: Scope,
        owner_class: str | None = None,
        *,
        hops: int = 0,
    ) -> ValueType:
        if node is None or hops > _MAX_VALUE_HOPS:
            return UNKNOWN_VALUE
        node = _unwrap(node)

        if isinstance(node, ast.Name):
            known = scope.values.get(node.id)
            if known is not None:
                return known
            resolved = self.index.resolve_symbol(service, module, node.id)
            if resolved.kind == SYMBOL_LIBRARY and resolved.library is not None:
                return ValueType(VALUE_LIBRARY, library=resolved.library)
            model = self.index.resolve_class(service, module, node)
            if model is not None and classify_model(self.index, service, *model) is not None:
                return ValueType(VALUE_MODEL, module=model[0], class_name=model[1])
            return UNKNOWN_VALUE

        if isinstance(node, ast.Attribute):
            if (
                isinstance(node.value, ast.Name)
                and node.value.id in ("cls", "self")
                and owner_class is not None
            ):
                typed = self.class_attribute_type(
                    service, module, owner_class, node.attr, hops + 1
                )
                if typed.kind != VALUE_UNKNOWN:
                    return typed
            receiver = self.value_type(
                service, module, node.value, scope, owner_class, hops=hops + 1
            )
            if receiver.is_library:
                return receiver
            model = self.index.resolve_class(service, module, node)
            if model is not None and classify_model(self.index, service, *model) is not None:
                return ValueType(VALUE_MODEL, module=model[0], class_name=model[1])
            return UNKNOWN_VALUE

        if isinstance(node, ast.Call):
            function = _unwrap(node.func)
            if isinstance(function, ast.Attribute):
                receiver = self.value_type(
                    service, module, function.value, scope, owner_class, hops=hops + 1
                )
                if receiver.is_library and function.attr in LIBRARY_FACTORY_MEMBERS:
                    return receiver
                if receiver.is_model:
                    return receiver
                return UNKNOWN_VALUE
            if isinstance(function, ast.Name):
                resolved = self.index.resolve_symbol(service, module, function.id)
                if resolved.kind == SYMBOL_LIBRARY and resolved.library is not None:
                    return ValueType(VALUE_LIBRARY, library=resolved.library)
                model = self.index.resolve_class(service, module, function)
                if model is not None and classify_model(self.index, service, *model) is not None:
                    return ValueType(VALUE_MODEL, module=model[0], class_name=model[1])
            return UNKNOWN_VALUE

        if isinstance(node, ast.ListComp | ast.SetComp | ast.GeneratorExp):
            return self.value_type(service, module, node.elt, scope, owner_class, hops=hops + 1)
        if isinstance(node, ast.List | ast.Tuple | ast.Set) and node.elts:
            return self.value_type(service, module, node.elts[0], scope, owner_class, hops=hops + 1)
        if isinstance(node, ast.Subscript):
            return self.value_type(service, module, node.value, scope, owner_class, hops=hops + 1)
        return UNKNOWN_VALUE


def build_scope(
    typer: PersistenceTyper,
    facts: ModuleFacts,
    root: ast.AST,
    parameters: tuple[str, ...],
    owner_class: str | None,
) -> Scope:
    """Collect the local bindings a persistence operation in ``root`` can see."""
    scope = Scope(parameters=parameters)
    nodes = _scope_nodes(root)

    bindings: list[tuple[int, str, ast.expr]] = []
    for node in nodes:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    bindings.append((node.lineno, target.id, node.value))
        elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            if node.value is not None:
                bindings.append((node.lineno, node.target.id, node.value))
        elif isinstance(node, ast.With | ast.AsyncWith):
            for item in node.items:
                if isinstance(item.optional_vars, ast.Name):
                    bindings.append((node.lineno, item.optional_vars.id, item.context_expr))
        elif isinstance(node, ast.For | ast.AsyncFor):
            if isinstance(node.target, ast.Name):
                bindings.append((node.lineno, node.target.id, node.iter))
    bindings.sort(key=lambda item: (item[0], item[1]))

    for _, name, value in bindings:
        scope.expressions.setdefault(name, value)
        inferred = typer.value_type(facts.service, facts.module, value, scope, owner_class)
        if inferred.kind != VALUE_UNKNOWN:
            scope.values.setdefault(name, inferred)
    return scope


# ---------------------------------------------------------------------------------------
# Access detection
# ---------------------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class CodeUnit:
    facts: ModuleFacts
    root: ast.AST
    symbol: str
    owner_class: str | None
    parameters: tuple[str, ...]
    member_name: str | None


def _code_units(facts: ModuleFacts) -> list[CodeUnit]:
    """Enumerate the scopes of one module in deterministic order."""
    units = [
        CodeUnit(facts, facts.tree, facts.module or "<module>", None, (), None)
    ]
    for name in sorted(facts.functions):
        declaration = facts.functions[name]
        units.append(
            CodeUnit(
                facts,
                declaration.node,
                facts.qualified(declaration.qualified_name),
                declaration.owner_class,
                declaration.parameters,
                declaration.qualified_name,
            )
        )
    return units


def _calls_in(root: ast.AST) -> list[ast.Call]:
    calls = [node for node in _scope_nodes(root) if isinstance(node, ast.Call)]
    calls.sort(key=lambda node: (node.lineno, node.col_offset))
    return calls


@dataclass(frozen=True, slots=True)
class PersistenceWrapper:
    """A local method that forwards a model argument to a rooted persistence operation."""

    service: str
    module: str
    qualified_name: str
    role: str
    operation: str
    library: str
    parameter_index: int
    parameter_name: str
    hops: int
    relative_path: str
    lineno: int

    @property
    def key(self) -> tuple[str, str, str]:
        return (self.service, self.module, self.qualified_name)

    @property
    def symbol(self) -> str:
        return f"{self.module}.{self.qualified_name}" if self.module else self.qualified_name


def _model_map_targets(
    index: SourceIndex, service: str, module: str, owner_class: str
) -> list[tuple[str, str]]:
    """Enumerate model classes named by a class-level ``{key: Model}`` mapping.

    FTGO's repositories resolve their model through ``_dto_model_mapping[dto_class]``. The
    concrete model is not knowable at the call site, but the mapping literally enumerates
    every model the repository can touch, so the set is source-backed rather than guessed.
    """
    targets: list[tuple[str, str]] = []
    for current_module, _, declaration in index.base_chain(service, module, owner_class):
        for value in declaration.class_attributes.values():
            if not isinstance(value, ast.Dict):
                continue
            for entry in value.values:
                if entry is None:
                    continue
                resolved = index.resolve_class(service, current_module, entry)
                if resolved is not None and classify_model(index, service, *resolved) is not None:
                    targets.append(resolved)
    unique = sorted(set(targets))
    return unique


def _operation_role(operation: str, library: str) -> str | None:
    """Classify a rooted operation as a read or a write, never by name alone."""
    relational = library in RELATIONAL_LIBRARIES
    document = library in DOCUMENT_LIBRARIES
    if relational:
        if operation in RELATIONAL_WRITE_OPERATIONS:
            return WRITE_ROLE
        if operation in RELATIONAL_READ_OPERATIONS:
            return READ_ROLE
    if document:
        if operation in DOCUMENT_WRITE_OPERATIONS:
            return WRITE_ROLE
        if operation in DOCUMENT_READ_OPERATIONS:
            return READ_ROLE
    return None


# ---------------------------------------------------------------------------------------
# Source discovery and database mapping
# ---------------------------------------------------------------------------------------


def _discover_source_files(record: RepositoryRecord) -> tuple[tuple[str, ...], list[str]]:
    """Split manifest-matched code sources into in-scope Python files and skips."""
    candidates = resolve_source_files(record, SOURCE_KIND)
    in_scope: list[str] = []
    skipped: list[str] = []
    for relative_path in candidates:
        reason = skip_reason(relative_path)
        if reason is None:
            in_scope.append(relative_path)
        elif relative_path.endswith(PYTHON_SUFFIX):
            skipped.append(f"{relative_path}: {reason}")
    return tuple(sorted(in_scope)), skipped


def resolve_database_mappings(
    record: RepositoryRecord,
    commit: str,
    repository_slug: str,
    engines_by_service: dict[str, dict[str, set[str]]],
    warnings: list[str],
) -> tuple[list[DatabaseMapping], list[UnresolvedFinding]]:
    """Correlate each service's proven storage engine with an existing Database entity.

    The engine comes from this pass (imports and models). The candidate databases come from
    Compose, re-derived from the same frozen commit rather than hard-coded: Compose is where
    ``POSTGRES_HOST=user_postgres`` is declared, and Pass 1 already turned those declarations
    into the canonical ``database.*`` entities. A mapping is emitted only when exactly one
    Compose-declared database matches the engine the source proves, so no duplicate Database
    entity is ever created and no name similarity is ever trusted.
    """
    mappings: list[DatabaseMapping] = []
    unresolved: list[UnresolvedFinding] = []
    try:
        compose = extract_compose(record, commit)
    except Exception as exc:  # pragma: no cover - compose sources are validated in Pass 1
        warnings.append(
            f"Compose evidence could not be read, so no database mapping was attempted ({exc})"
        )
        for service in sorted(engines_by_service):
            unresolved.append(
                UnresolvedFinding(
                    category=UNRESOLVED_DATABASE,
                    service=service_entity_id(repository_slug, service),
                    subject=service,
                    reason="Compose evidence unavailable",
                )
            )
        return mappings, unresolved

    databases = {
        entity.id: entity for entity in compose.infrastructure if entity.kind == "Database"
    }
    edges: dict[str, list[str]] = {}
    for relation in compose.relationships:
        if relation.target in databases:
            slug = relation.source.split(".")[-1]
            edges.setdefault(slug, []).append(relation.target)

    for service in sorted(engines_by_service):
        engines = engines_by_service[service]
        # Only engines that actually back a model matter for a Database mapping.
        model_engines = sorted(engines.get("model", set()))
        if not model_engines:
            continue
        candidates = sorted(set(edges.get(service, [])))
        provenance = Provenance(
            repository=record.id,
            commit=commit,
            source_path="backend/docker-compose.yaml",
            symbol=f"services/{service}",
            evidence_type=EVIDENCE_TYPE,
        )
        for engine in model_engines:
            matching = [
                identifier
                for identifier in candidates
                if databases[identifier].engine == engine
            ]
            if len(matching) == 1:
                mappings.append(
                    DatabaseMapping(
                        service=service,
                        service_entity_id=service_entity_id(repository_slug, service),
                        database=matching[0],
                        engine=engine,
                        libraries=tuple(sorted(engines.get("library", set()))),
                        evidence=(
                            f"source models root in a {engine} library",
                            f"Compose declares a {engine} dependency for this service",
                        ),
                        provenance=provenance,
                    )
                )
                continue
            reason = (
                f"no Compose-declared {engine} database is linked to this service"
                if not matching
                else f"{len(matching)} Compose-declared {engine} databases match: "
                f"{', '.join(matching)}"
            )
            unresolved.append(
                UnresolvedFinding(
                    category=UNRESOLVED_DATABASE,
                    service=service_entity_id(repository_slug, service),
                    subject=f"{service} ({engine})",
                    reason=reason,
                    provenance=provenance,
                )
            )
    return mappings, unresolved


# ---------------------------------------------------------------------------------------
# Extraction
# ---------------------------------------------------------------------------------------


def extract_data_model(
    record: RepositoryRecord,
    commit: str,
    *,
    source_kind: str = SOURCE_KIND,
) -> DataModelExtraction:
    """Extract FTGO's persistence data model with AST only.

    ``commit`` must already be verified against the manifest baseline by the caller. The
    inspected repository is only ever read: no module is imported, no code is executed, and
    no database connection is opened.
    """
    del source_kind
    repository = record.id
    repository_slug = normalize_token(record.id)
    warnings: list[str] = []
    unresolved: list[UnresolvedFinding] = []

    candidates, skipped = _discover_source_files(record)
    modules: list[ModuleFacts] = []
    scanned: list[str] = []
    withheld: set[str] = set()
    files_per_service: dict[str, int] = {}

    for relative_path in candidates:
        location = service_location(relative_path)
        if location is None:  # pragma: no cover - skip_reason already filtered these
            continue
        service, service_root = location
        try:
            text = (record.path / relative_path).read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as exc:
            warnings.append(f"{relative_path}: unreadable, skipped ({exc})")
            continue
        if is_generated_source(text):
            skipped.append(f"{relative_path}: generated source header")
            continue
        try:
            tree = ast.parse(text, filename=relative_path)
        except SyntaxError as exc:
            warnings.append(f"{relative_path}: invalid Python syntax, skipped ({exc.msg})")
            continue
        scanned.append(relative_path)
        files_per_service[service] = files_per_service.get(service, 0) + 1
        modules.append(
            analyze_module(
                text,
                tree,
                relative_path=relative_path,
                service=service,
                service_root=service_root,
                module=module_dotted_name(relative_path, service_root),
                is_package=relative_path.rsplit("/", 1)[-1] == "__init__.py",
                warnings=warnings,
            )
        )
        withheld |= modules[-1].withheld_values

    index = build_source_index(modules)
    typer = PersistenceTyper(index)

    # --- persistence libraries per service -------------------------------------------------
    libraries_by_service: dict[str, set[str]] = {}
    for facts in modules:
        for imported in facts.imports.values():
            library = library_root(imported.module)
            if library is not None:
                libraries_by_service.setdefault(facts.service, set()).add(library)

    # --- models --------------------------------------------------------------------------
    tables: dict[str, TableCandidate] = {}
    columns: dict[str, ColumnCandidate] = {}
    collections: dict[str, CollectionCandidate] = {}
    document_schemas: dict[str, DocumentSchemaCandidate] = {}
    collisions: list[IdentityCollision] = []
    table_claims: dict[str, list[str]] = {}
    schema_claims: dict[str, list[str]] = {}
    collection_claims: dict[str, list[str]] = {}
    model_targets: dict[tuple[str, str, str], tuple[str, str]] = {}
    engines_by_service: dict[str, dict[str, set[str]]] = {}

    for facts in sorted(modules, key=lambda item: item.relative_path):
        if facts.is_migration:
            continue
        for class_name in sorted(facts.classes):
            declaration = facts.classes[class_name]
            classification = classify_model(index, facts.service, facts.module, class_name)
            if classification is None:
                continue
            engines_by_service.setdefault(facts.service, {}).setdefault("library", set()).add(
                classification.library
            )
            symbol = facts.qualified(class_name)
            provenance = Provenance(
                repository=repository,
                commit=commit,
                source_path=facts.relative_path,
                symbol=symbol,
                line_start=declaration.lineno,
                line_end=declaration.end_lineno,
                evidence_type=EVIDENCE_TYPE,
            )

            if classification.role == PERSISTENCE_ROLE_TABLE:
                if declaration.is_abstract or declaration.table_name is None:
                    if declaration.table_name_expression:
                        unresolved.append(
                            UnresolvedFinding(
                                category=UNRESOLVED_TABLE_NAME,
                                service=service_entity_id(repository_slug, facts.service),
                                subject=symbol,
                                reason=(
                                    "__tablename__ is not a string literal: "
                                    f"{declaration.table_name_expression}"
                                ),
                                provenance=provenance,
                            )
                        )
                    # An abstract or unnamed mapped class is not a physical table.
                    continue
                engines_by_service[facts.service].setdefault("model", set()).add(
                    classification.engine
                )
                identifier = table_id(repository_slug, facts.service, declaration.table_name)
                table_claims.setdefault(identifier, []).append(
                    f"{facts.relative_path}:{declaration.lineno} {symbol} "
                    f"(__tablename__={declaration.table_name})"
                )
                model_targets[(facts.service, facts.module, class_name)] = (TABLE_KIND, identifier)
                if identifier in tables:
                    continue
                inherited = collect_columns(index, facts.service, facts.module, class_name)
                primary_key = tuple(
                    item.column.name for item in inherited if item.column.primary_key
                )
                foreign_keys = tuple(
                    {"column": item.column.name, "references": item.column.foreign_key}
                    for item in inherited
                    if item.column.foreign_key
                )
                tables[identifier] = TableCandidate(
                    id=identifier,
                    kind=TABLE_KIND,
                    title=declaration.table_name,
                    service=facts.service,
                    table_name=declaration.table_name,
                    model_class=symbol,
                    library=classification.library,
                    engine=classification.engine,
                    database=None,
                    primary_key=primary_key,
                    foreign_keys=foreign_keys,
                    unique_columns=tuple(
                        item.column.name for item in inherited if item.column.unique
                    ),
                    indexed_columns=tuple(
                        item.column.name for item in inherited if item.column.indexed
                    ),
                    orm_relationships=declaration.relationships,
                    schema_name=None,
                    provenance=provenance,
                    attributes={
                        "persistence_role": PERSISTENCE_ROLE_TABLE,
                        "declarative_base": classification.base_symbol,
                        "column_count": len(inherited),
                    },
                )
                for item in inherited:
                    column_identifier = column_id(
                        repository_slug, facts.service, declaration.table_name, item.column.name
                    )
                    columns.setdefault(
                        column_identifier,
                        ColumnCandidate(
                            id=column_identifier,
                            kind=COLUMN_KIND,
                            title=item.column.name,
                            service=facts.service,
                            table_id=identifier,
                            table_name=declaration.table_name,
                            column=item.column,
                            declaring_class=f"{item.declaring_module}.{item.declaring_class}"
                            if item.declaring_module
                            else item.declaring_class,
                            provenance=Provenance(
                                repository=repository,
                                commit=commit,
                                source_path=item.declaring_path,
                                symbol=f"{item.declaring_module}.{item.declaring_class}."
                                f"{item.column.name}"
                                if item.declaring_module
                                else f"{item.declaring_class}.{item.column.name}",
                                line_start=item.column.lineno,
                                line_end=item.column.end_lineno,
                                evidence_type=EVIDENCE_TYPE,
                            ),
                        ),
                    )
            else:
                engines_by_service[facts.service].setdefault("model", set()).add(
                    classification.engine
                )
                identifier = document_schema_id(
                    repository_slug, facts.service, facts.module, class_name
                )
                schema_claims.setdefault(identifier, []).append(
                    f"{facts.relative_path}:{declaration.lineno} {symbol}"
                )
                collection_identifier = (
                    collection_id(
                        repository_slug, facts.service, declaration.collection_name
                    )
                    if declaration.collection_name
                    else None
                )
                # A service access points at the physical Collection when one is proven, and
                # at the Schema only when no collection name could be resolved. It never
                # points at both.
                model_targets[(facts.service, facts.module, class_name)] = (
                    (COLLECTION_KIND, collection_identifier)
                    if collection_identifier is not None
                    else (SCHEMA_KIND, identifier)
                )
                if declaration.collection_name is None:
                    unresolved.append(
                        UnresolvedFinding(
                            category=UNRESOLVED_COLLECTION_NAME,
                            service=service_entity_id(repository_slug, facts.service),
                            subject=symbol,
                            reason=(
                                "collection name is not a string literal: "
                                f"{declaration.collection_name_expression}"
                                if declaration.collection_name_expression
                                else (
                                    "no explicit collection name is declared; the ODM default "
                                    "is not stated in source, so no Collection was created"
                                )
                            ),
                            provenance=provenance,
                        )
                    )
                fields = collect_document_fields(index, facts.service, facts.module, class_name)
                references: list[str] = []
                for item in fields:
                    for reference in item.references:
                        resolved = index.resolve_class(
                            facts.service, facts.module, ast.Name(id=reference.split(".")[-1])
                        )
                        if resolved is not None:
                            references.append(f"{resolved[0]}.{resolved[1]}")
                        else:
                            unresolved.append(
                                UnresolvedFinding(
                                    category=UNRESOLVED_MODEL_REFERENCE,
                                    service=service_entity_id(repository_slug, facts.service),
                                    subject=f"{symbol}.{item.name} -> {reference}",
                                    reason="document reference target is not a scanned class",
                                    provenance=provenance,
                                )
                            )
                document_schemas.setdefault(
                    identifier,
                    DocumentSchemaCandidate(
                        id=identifier,
                        kind=SCHEMA_KIND,
                        title=class_name,
                        service=facts.service,
                        model_class=symbol,
                        qualified_name=symbol,
                        library=classification.library,
                        engine=classification.engine,
                        database=None,
                        collection_name=declaration.collection_name,
                        fields=tuple(fields),
                        declared_indexes=declaration.declared_indexes,
                        references=tuple(sorted(set(references))),
                        provenance=provenance,
                        attributes={
                            "persistence_role": PERSISTENCE_ROLE_DOCUMENT,
                            "storage_engine": classification.engine,
                            "document_base": classification.base_symbol,
                            "field_count": len(fields),
                            "settings_declared": declaration.settings_present,
                        },
                    ),
                )
                if collection_identifier is not None and declaration.collection_name:
                    collection_claims.setdefault(collection_identifier, []).append(
                        f"{facts.relative_path}:{declaration.lineno} {symbol} "
                        f"(collection={declaration.collection_name})"
                    )
                    collections.setdefault(
                        collection_identifier,
                        CollectionCandidate(
                            id=collection_identifier,
                            kind=COLLECTION_KIND,
                            title=declaration.collection_name,
                            service=facts.service,
                            collection_name=declaration.collection_name,
                            library=classification.library,
                            engine=classification.engine,
                            database=None,
                            schema_id=identifier,
                            model_class=symbol,
                            declared_indexes=declaration.declared_indexes,
                            provenance=provenance,
                            attributes={
                                "persistence_role": PERSISTENCE_ROLE_DOCUMENT,
                                "storage_engine": classification.engine,
                                "document_base": classification.base_symbol,
                            },
                        ),
                    )

    for identifier, claims in sorted(table_claims.items()):
        if len({claim.split(" ", 1)[1] for claim in claims}) > 1:
            collisions.append(
                IdentityCollision(identifier, TABLE_KIND, tuple(sorted(claims)))
            )
    for identifier, claims in sorted(schema_claims.items()):
        if len(set(claims)) > 1:
            collisions.append(
                IdentityCollision(identifier, SCHEMA_KIND, tuple(sorted(claims)))
            )
    for identifier, claims in sorted(collection_claims.items()):
        if len({claim.split(" ", 1)[1] for claim in claims}) > 1:
            collisions.append(
                IdentityCollision(identifier, COLLECTION_KIND, tuple(sorted(claims)))
            )
    for collision in collisions:
        tables.pop(collision.entity_id, None)
        document_schemas.pop(collision.entity_id, None)
        collections.pop(collision.entity_id, None)

    # --- database mappings ----------------------------------------------------------------
    mappings, mapping_unresolved = resolve_database_mappings(
        record, commit, repository_slug, engines_by_service, warnings
    )
    unresolved.extend(mapping_unresolved)
    database_by_service = {item.service: item for item in mappings}

    def owning_database(service: str) -> str | None:
        mapping = database_by_service.get(service)
        return mapping.database if mapping is not None else None

    tables = {
        identifier: replace(candidate, database=owning_database(candidate.service))
        for identifier, candidate in tables.items()
    }
    document_schemas = {
        identifier: replace(candidate, database=owning_database(candidate.service))
        for identifier, candidate in document_schemas.items()
    }
    collections = {
        identifier: replace(candidate, database=owning_database(candidate.service))
        for identifier, candidate in collections.items()
    }

    # --- accesses -------------------------------------------------------------------------
    wrappers, accesses, access_unresolved = extract_accesses(
        index,
        typer,
        modules,
        model_targets,
        repository,
        repository_slug,
        commit,
    )
    unresolved.extend(access_unresolved)

    # --- migrations -----------------------------------------------------------------------
    migrations: dict[str, MigrationCandidate] = {}
    for facts in sorted(modules, key=lambda item: item.relative_path):
        if facts.migration is None:
            continue
        fact = facts.migration
        identifier = migration_id(repository_slug, facts.service, fact.revision)
        migrations.setdefault(
            identifier,
            MigrationCandidate(
                id=identifier,
                kind=MIGRATION_KIND,
                title=fact.description or fact.revision,
                service=facts.service,
                revision=fact.revision,
                down_revision=fact.down_revision,
                tool="alembic",
                touched_tables=fact.touched_tables,
                operations=fact.operations,
                provenance=Provenance(
                    repository=repository,
                    commit=commit,
                    source_path=facts.relative_path,
                    symbol=facts.qualified("revision"),
                    line_start=fact.lineno,
                    line_end=fact.end_lineno,
                    evidence_type=EVIDENCE_TYPE,
                ),
            ),
        )

    relationships = build_relationships(
        repository_slug,
        tables,
        columns,
        collections,
        document_schemas,
        migrations,
        accesses,
        unresolved,
    )

    # The MongoDB collection gap was closed by an explicit ontology decision that added the
    # Collection kind, so no gap is reported for it. The mechanism stays in place for any
    # future concept the ontology genuinely cannot express.
    ontology_gaps: list[OntologyGap] = []

    services_scanned = tuple(
        ServiceScan(
            slug=slug,
            entity_id=service_entity_id(repository_slug, slug),
            python_files=files_per_service[slug],
            libraries=tuple(sorted(libraries_by_service.get(slug, set()))),
            tables=sum(1 for item in tables.values() if item.service == slug),
            collections=sum(1 for item in collections.values() if item.service == slug),
            document_models=sum(1 for item in document_schemas.values() if item.service == slug),
            migrations=sum(1 for item in migrations.values() if item.service == slug),
            database=(
                database_by_service[slug].database if slug in database_by_service else None
            ),
        )
        for slug in sorted(files_per_service)
    )
    for scan in services_scanned:
        if not scan.libraries:
            warnings.append(
                f"{scan.slug}: {scan.python_files} Python file(s) scanned and no persistence "
                f"library import found; no data model was created for {scan.entity_id}"
            )
        elif not scan.tables and not scan.collections and not scan.document_models:
            # A service can use persistence infrastructure without owning a data model. FTGO's
            # gateway is exactly that: it caches through Redis but persists nothing, and the
            # ontology has no cache kind, so no entity is created for it.
            warnings.append(
                f"{scan.slug}: persistence libraries {', '.join(scan.libraries)} are imported "
                f"but no relational or document model is declared; no data model entity was "
                f"created for {scan.entity_id}"
            )

    return DataModelExtraction(
        repository=repository,
        commit=commit,
        owner=record.owner,
        source_files=tuple(scanned),
        skipped_files=tuple(sorted(skipped)),
        services_scanned=services_scanned,
        libraries=tuple(
            sorted({item for values in libraries_by_service.values() for item in values})
        ),
        wrappers=tuple(sorted(wrapper.symbol for wrapper in wrappers)),
        tables=tuple(sorted(tables.values(), key=lambda item: item.id)),
        columns=tuple(sorted(columns.values(), key=lambda item: item.id)),
        collections=tuple(sorted(collections.values(), key=lambda item: item.id)),
        document_schemas=tuple(sorted(document_schemas.values(), key=lambda item: item.id)),
        migrations=tuple(sorted(migrations.values(), key=lambda item: item.id)),
        database_mappings=tuple(sorted(mappings, key=lambda item: item.service_entity_id)),
        accesses=tuple(
            sorted(accesses, key=lambda item: (item.service, item.relation_type, item.target))
        ),
        relationships=tuple(
            sorted(relationships, key=lambda item: (item.source, item.type, item.target))
        ),
        unresolved=tuple(
            sorted(unresolved, key=lambda item: (item.category, item.subject, item.reason))
        ),
        identity_collisions=tuple(sorted(collisions, key=lambda item: item.entity_id)),
        ontology_gaps=tuple(ontology_gaps),
        warnings=tuple(sorted(warnings)),
        withheld_values=frozenset(withheld),
    )


# ---------------------------------------------------------------------------------------
# Access extraction
# ---------------------------------------------------------------------------------------


def _rooted_operation(
    index: SourceIndex,
    typer: PersistenceTyper,
    facts: ModuleFacts,
    call: ast.Call,
    scope: Scope,
    owner_class: str | None,
) -> tuple[str, str, str, ast.expr | None] | None:
    """Return ``(role, operation, library, target expression)`` for a rooted call.

    Rooting happens first and the method name is consulted second. ``save()`` on an ordinary
    object, ``get()`` on a dict and ``delete()`` on a cache all fail the rooting step and are
    therefore never reported.
    """
    function = _unwrap(call.func)

    # ``select(Model)`` and friends imported straight from the library.
    if isinstance(function, ast.Name):
        resolved = index.resolve_symbol(facts.service, facts.module, function.id)
        if resolved.kind == SYMBOL_LIBRARY and resolved.library is not None:
            role = _operation_role(resolved.name or function.id, resolved.library)
            if role is not None:
                target = call.args[0] if call.args else None
                return role, resolved.name or function.id, resolved.library, target
        return None

    if not isinstance(function, ast.Attribute):
        return None

    operation = function.attr
    receiver = typer.value_type(facts.service, facts.module, function.value, scope, owner_class)

    if receiver.is_library and receiver.library is not None:
        role = _operation_role(operation, receiver.library)
        if role is None:
            return None
        target = call.args[0] if call.args else None
        return role, operation, receiver.library, target

    if receiver.is_model and receiver.module is not None and receiver.class_name is not None:
        classification = classify_model(index, facts.service, receiver.module, receiver.class_name)
        if classification is None:
            return None
        role = _operation_role(operation, classification.library)
        if role is None:
            return None
        # The receiver *is* the model, so the target is the receiver itself.
        return role, operation, classification.library, function.value
    return None


def extract_accesses(
    index: SourceIndex,
    typer: PersistenceTyper,
    modules: list[ModuleFacts],
    model_targets: dict[tuple[str, str, str], tuple[str, str]],
    repository: str,
    repository_slug: str,
    commit: str,
) -> tuple[list[PersistenceWrapper], list[AccessCandidate], list[UnresolvedFinding]]:
    """Discover persistence wrappers, then every rooted read and write they enable."""
    wrappers: dict[tuple[str, str, str], PersistenceWrapper] = {}
    unresolved: list[UnresolvedFinding] = []

    def target_ids(
        facts: ModuleFacts, node: ast.expr | None, scope: Scope, owner_class: str | None
    ) -> tuple[list[tuple[str, str]], str] | None:
        """Resolve an operation target to graph entities, recording how it was resolved."""
        if node is not None:
            typed = typer.value_type(facts.service, facts.module, node, scope, owner_class)
            if typed.is_model and typed.module is not None and typed.class_name is not None:
                found = model_targets.get((facts.service, typed.module, typed.class_name))
                if found is not None:
                    resolution = (
                        RESOLUTION_CLASS_ATTRIBUTE
                        if isinstance(node, ast.Attribute)
                        and isinstance(node.value, ast.Name)
                        and node.value.id in ("cls", "self")
                        else RESOLUTION_DIRECT
                    )
                    return [found], resolution
        if owner_class is not None:
            enumerated = _model_map_targets(index, facts.service, facts.module, owner_class)
            resolved = [
                model_targets[(facts.service, module, name)]
                for module, name in enumerated
                if (facts.service, module, name) in model_targets
            ]
            if resolved:
                return sorted(set(resolved)), RESOLUTION_MODEL_MAP
        return None

    # --- wrapper discovery ------------------------------------------------------------------
    for hop in range(1, _MAX_WRAPPER_HOPS + 1):
        discovered: list[PersistenceWrapper] = []
        for facts in sorted(modules, key=lambda item: item.relative_path):
            if facts.is_migration:
                continue
            for unit in _code_units(facts):
                if unit.member_name is None or not unit.parameters:
                    continue
                key = (facts.service, facts.module, unit.member_name)
                if key in wrappers:
                    continue
                scope = build_scope(typer, facts, unit.root, unit.parameters, unit.owner_class)
                for call in _calls_in(unit.root):
                    rooted = _rooted_operation(index, typer, facts, call, scope, unit.owner_class)
                    if rooted is None:
                        continue
                    role, operation, library, target = rooted
                    if hop > 1:
                        continue
                    if not isinstance(target, ast.Name) or target.id not in unit.parameters:
                        continue
                    discovered.append(
                        PersistenceWrapper(
                            service=facts.service,
                            module=facts.module,
                            qualified_name=unit.member_name,
                            role=role,
                            operation=operation,
                            library=library,
                            parameter_index=unit.parameters.index(target.id),
                            parameter_name=target.id,
                            hops=hop,
                            relative_path=facts.relative_path,
                            lineno=call.lineno,
                        )
                    )
                    break
        if not discovered:
            break
        for wrapper in sorted(discovered, key=lambda item: item.key):
            wrappers.setdefault(wrapper.key, wrapper)

    # --- access sites -----------------------------------------------------------------------
    grouped: dict[tuple[str, str, str], list[CallSite]] = {}
    kinds: dict[tuple[str, str, str], tuple[str, str]] = {}

    for facts in sorted(modules, key=lambda item: item.relative_path):
        if facts.is_migration:
            continue
        for unit in _code_units(facts):
            scope = build_scope(typer, facts, unit.root, unit.parameters, unit.owner_class)
            wrapper_here = wrappers.get((facts.service, facts.module, unit.member_name or ""))
            for call in _calls_in(unit.root):
                rooted = _rooted_operation(index, typer, facts, call, scope, unit.owner_class)
                role: str | None = None
                operation = ""
                library = ""
                target: ast.expr | None = None
                resolution = RESOLUTION_DIRECT

                if rooted is not None:
                    role, operation, library, target = rooted
                    if (
                        wrapper_here is not None
                        and isinstance(target, ast.Name)
                        and target.id in unit.parameters
                    ):
                        # The wrapper's own forwarding call; the model belongs to its callers.
                        continue
                else:
                    callee = _resolve_callee(index, typer, facts, call, scope, unit.owner_class)
                    if callee is None:
                        continue
                    wrapper = wrappers.get((facts.service, callee[0], callee[1]))
                    if wrapper is None:
                        continue
                    role = wrapper.role
                    operation = wrapper.operation
                    library = wrapper.library
                    resolution = RESOLUTION_WRAPPER
                    target = (
                        call.args[wrapper.parameter_index]
                        if wrapper.parameter_index < len(call.args)
                        else _keyword_node(call, wrapper.parameter_name)
                    )

                if role is None:
                    continue
                provenance_symbol = unit.symbol
                site_provenance = Provenance(
                    repository=repository,
                    commit=commit,
                    source_path=facts.relative_path,
                    symbol=provenance_symbol,
                    line_start=call.lineno,
                    line_end=call.end_lineno or call.lineno,
                    evidence_type=EVIDENCE_TYPE,
                )
                resolved = target_ids(facts, target, scope, unit.owner_class)
                if resolved is None:
                    unresolved.append(
                        UnresolvedFinding(
                            category=UNRESOLVED_ACCESS,
                            service=service_entity_id(repository_slug, facts.service),
                            subject=f"{provenance_symbol} {operation}",
                            reason=(
                                "the persistence operation is rooted but its model target is "
                                "not statically resolvable"
                            ),
                            provenance=site_provenance,
                        )
                    )
                    continue
                entity_targets, resolution_kind = resolved
                if resolution == RESOLUTION_WRAPPER:
                    resolution_kind = RESOLUTION_WRAPPER
                site = CallSite(
                    operation=operation,
                    expression=_expression_text(facts.source, call),
                    resolution=resolution_kind,
                    provenance=site_provenance,
                )
                for target_kind, target_id in entity_targets:
                    key = (facts.service, role, target_id)
                    grouped.setdefault(key, []).append(site)
                    kinds[key] = (target_kind, library)

    accesses: list[AccessCandidate] = []
    for (service, role, target_id), sites in grouped.items():
        target_kind, library = kinds[(service, role, target_id)]
        # Many call sites collapse into one semantic relationship, but every one is retained.
        unique_sites = {item.key: item for item in sites}
        accesses.append(
            AccessCandidate(
                service=service_entity_id(repository_slug, service),
                role=role,
                relation_type=READS if role == READ_ROLE else WRITES,
                target=target_id,
                target_kind=target_kind,
                library=library,
                call_sites=tuple(
                    unique_sites[key] for key in sorted(unique_sites)
                ),
            )
        )
    return list(wrappers.values()), accesses, unresolved


def _resolve_callee(
    index: SourceIndex,
    typer: PersistenceTyper,
    facts: ModuleFacts,
    call: ast.Call,
    scope: Scope,
    owner_class: str | None,
) -> tuple[str, str] | None:
    """Resolve a call target to ``(module, qualified name)`` in scanned source."""
    function = _unwrap(call.func)
    if isinstance(function, ast.Name):
        resolved = index.resolve_symbol(facts.service, facts.module, function.id)
        if (
            resolved.kind == SYMBOL_FUNCTION
            and resolved.module is not None
            and resolved.name is not None
        ):
            return resolved.module, resolved.name
        return None
    if not isinstance(function, ast.Attribute):
        return None
    receiver = function.value
    if isinstance(receiver, ast.Name) and receiver.id in ("cls", "self") and owner_class:
        for module, name, declaration in index.base_chain(
            facts.service, facts.module, owner_class
        ):
            del declaration
            target = index.facts(facts.service, module)
            if target is not None and f"{name}.{function.attr}" in target.functions:
                return module, f"{name}.{function.attr}"
        return None
    del typer
    resolved_class = index.resolve_class(facts.service, facts.module, receiver)
    if resolved_class is not None:
        module, class_name = resolved_class
        target = index.facts(facts.service, module)
        if target is not None and f"{class_name}.{function.attr}" in target.functions:
            return module, f"{class_name}.{function.attr}"
    return None


def build_relationships(
    repository_slug: str,
    tables: dict[str, TableCandidate],
    columns: dict[str, ColumnCandidate],
    collections: dict[str, CollectionCandidate],
    document_schemas: dict[str, DocumentSchemaCandidate],
    migrations: dict[str, MigrationCandidate],
    accesses: list[AccessCandidate],
    unresolved: list[UnresolvedFinding],
) -> list[RelationshipCandidate]:
    """Assemble every relationship this pass is allowed to emit."""
    del repository_slug
    relationships: list[RelationshipCandidate] = []
    tables_by_name: dict[tuple[str, str], TableCandidate] = {
        (item.service, item.table_name): item for item in tables.values()
    }

    for table in sorted(tables.values(), key=lambda item: item.id):
        if table.database:
            relationships.append(
                RelationshipCandidate(
                    source=table.database,
                    type=CONTAINS,
                    target=table.id,
                    provenance=table.provenance,
                    detail={"table_name": table.table_name, "storage_engine": table.engine},
                )
            )
        for foreign_key in table.foreign_keys:
            reference = foreign_key.get("references") or ""
            target_table = reference.split(".")[0] if "." in reference else reference
            resolved = tables_by_name.get((table.service, target_table))
            if resolved is None:
                unresolved.append(
                    UnresolvedFinding(
                        category=UNRESOLVED_MODEL_REFERENCE,
                        service=None,
                        subject=f"{table.table_name}.{foreign_key.get('column')} -> {reference}",
                        reason="foreign key target table is not declared in scanned source",
                        provenance=table.provenance,
                    )
                )
                continue
            if resolved.id == table.id:
                continue
            relationships.append(
                RelationshipCandidate(
                    source=table.id,
                    type=DEPENDS_ON,
                    target=resolved.id,
                    provenance=table.provenance,
                    detail={
                        "foreign_key_column": foreign_key.get("column"),
                        "references": reference,
                    },
                )
            )

    for column in sorted(columns.values(), key=lambda item: item.id):
        relationships.append(
            RelationshipCandidate(
                source=column.table_id,
                type=CONTAINS,
                target=column.id,
                provenance=column.provenance,
                detail={"column_name": column.column.name},
            )
        )

    # Document persistence mirrors the relational shape: the Database contains the physical
    # Collection, and the Collection uses the source-backed document Schema.
    for collection in sorted(collections.values(), key=lambda item: item.id):
        if collection.database:
            relationships.append(
                RelationshipCandidate(
                    source=collection.database,
                    type=CONTAINS,
                    target=collection.id,
                    provenance=collection.provenance,
                    detail={
                        "collection_name": collection.collection_name,
                        "storage_engine": collection.engine,
                    },
                )
            )
        if collection.schema_id in document_schemas:
            relationships.append(
                RelationshipCandidate(
                    source=collection.id,
                    type=USES_SCHEMA,
                    target=collection.schema_id,
                    provenance=collection.provenance,
                    detail={
                        "model_class": collection.model_class,
                        "persistence_role": PERSISTENCE_ROLE_DOCUMENT,
                    },
                )
            )

    for access in sorted(
        accesses, key=lambda item: (item.service, item.relation_type, item.target)
    ):
        anchor = access.anchor_provenance
        relationships.append(
            RelationshipCandidate(
                source=access.service,
                type=access.relation_type,
                target=access.target,
                role=access.role,
                provenance=anchor,
                detail={
                    "target_kind": access.target_kind,
                    "persistence_library": access.library,
                    "call_site_count": len(access.call_sites),
                    "call_sites": [item.summary() for item in access.call_sites],
                },
            )
        )

    for migration in sorted(migrations.values(), key=lambda item: item.id):
        for table_name in migration.touched_tables:
            resolved = tables_by_name.get((migration.service, table_name))
            if resolved is None:
                unresolved.append(
                    UnresolvedFinding(
                        category=UNRESOLVED_MODEL_REFERENCE,
                        service=None,
                        subject=f"migration {migration.revision} -> {table_name}",
                        reason="migration names a table that is not declared in scanned source",
                        provenance=migration.provenance,
                    )
                )
                continue
            relationships.append(
                RelationshipCandidate(
                    source=resolved.id,
                    type=CHANGED_BY,
                    target=migration.id,
                    provenance=migration.provenance,
                    detail={
                        "revision": migration.revision,
                        "operations": list(migration.operations),
                    },
                )
            )
    return relationships


# ---------------------------------------------------------------------------------------
# Candidate rendering
# ---------------------------------------------------------------------------------------


def _render_page(frontmatter: dict[str, Any], body: list[str]) -> str:
    rendered = yaml.safe_dump(
        frontmatter,
        sort_keys=False,
        default_flow_style=False,
        allow_unicode=True,
        width=100,
    ).rstrip("\n")
    return "\n".join(["---", rendered, "---", "", *body, ""])


def _base_frontmatter(
    *,
    identifier: str,
    kind: str,
    title: str,
    extraction: DataModelExtraction,
    service_entity: str,
) -> dict[str, Any]:
    """Frontmatter shared by every candidate page. Never approved, never canonical."""
    frontmatter: dict[str, Any] = {
        "id": identifier,
        "kind": kind,
        # The canonical loader requires kind and OKF type to agree.
        "type": kind,
        "title": title,
        "status": CANDIDATE_STATUS,
        "review_status": CANDIDATE_REVIEW_STATUS,
        "candidate_of": f"{EXTRACTOR_KIND}-extraction",
        "repository": extraction.repository,
        "commit": extraction.commit,
        "evidence_type": EVIDENCE_TYPE,
        "extractor": EXTRACTOR_KIND,
        "service": service_entity,
    }
    if extraction.owner:
        frontmatter["owner"] = extraction.owner
    return frontmatter


def _relation_entries(relations: tuple[RelationshipCandidate, ...]) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    for relation in relations:
        entry: dict[str, Any] = {"type": relation.type, "target": relation.target}
        if relation.role:
            entry["role"] = relation.role
        entry.update(relation.detail)
        entry.update(relation.provenance.as_dict())
        entries.append(entry)
    return entries


def _inbound_entries(relations: tuple[RelationshipCandidate, ...]) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    for relation in relations:
        entry: dict[str, Any] = {"type": relation.type, "source": relation.source}
        if relation.role:
            entry["role"] = relation.role
        entry.update(relation.detail)
        entry.update(relation.provenance.as_dict())
        entries.append(entry)
    return entries


def _service_entity(extraction: DataModelExtraction, service: str) -> str:
    return service_entity_id(normalize_token(extraction.repository), service)


def render_table_markdown(table: TableCandidate, extraction: DataModelExtraction) -> str:
    frontmatter = _base_frontmatter(
        identifier=table.id,
        kind=table.kind,
        title=table.title,
        extraction=extraction,
        service_entity=_service_entity(extraction, table.service),
    )
    frontmatter["table_name"] = table.table_name
    frontmatter["storage_engine"] = table.engine
    frontmatter["persistence_library"] = table.library
    frontmatter["database"] = table.database
    frontmatter["model_class"] = table.model_class
    frontmatter["primary_key"] = list(table.primary_key)
    if table.foreign_keys:
        frontmatter["foreign_keys"] = [dict(item) for item in table.foreign_keys]
    if table.unique_columns:
        frontmatter["unique_columns"] = list(table.unique_columns)
    if table.indexed_columns:
        frontmatter["indexed_columns"] = list(table.indexed_columns)
    if table.orm_relationships:
        frontmatter["orm_relationships"] = [item.summary() for item in table.orm_relationships]
    frontmatter["source_refs"] = [table.provenance.as_dict()]
    inbound = extraction.inbound_relations_for(table.id)
    if inbound:
        frontmatter["inbound_relations"] = _inbound_entries(inbound)
    outbound = extraction.relations_for(table.id)
    if outbound:
        frontmatter["relations"] = _relation_entries(outbound)
    frontmatter["attributes"] = table.attributes

    body = [
        f"# {table.table_name}",
        "",
        f"Candidate relational table extracted from an ORM mapping in "
        f"`{extraction.repository}` at commit `{extraction.commit}`.",
        "",
        f"- Owning service: `{_service_entity(extraction, table.service)}`",
        f"- Database: `{table.database or 'unresolved'}`",
        f"- Mapped class: `{table.model_class}`",
        f"- Persistence library: `{table.library}`",
        f"- Declared in: `{table.provenance.source_path}` "
        f"(lines {table.provenance.line_start}-{table.provenance.line_end})",
        f"- Evidence class: `{EVIDENCE_TYPE}`",
        "",
        "## Review notes",
        "",
        "This page is a candidate awaiting review. The physical table name comes from an "
        "explicit `__tablename__`; column metadata is read from the mapping and no default "
        "value is ever evaluated or emitted.",
        "",
    ]
    return _render_page(frontmatter, body)


def render_column_markdown(column: ColumnCandidate, extraction: DataModelExtraction) -> str:
    frontmatter = _base_frontmatter(
        identifier=column.id,
        kind=column.kind,
        title=column.title,
        extraction=extraction,
        service_entity=_service_entity(extraction, column.service),
    )
    frontmatter["table"] = column.table_id
    frontmatter["table_name"] = column.table_name
    frontmatter["declaring_class"] = column.declaring_class
    frontmatter.update(
        {key: value for key, value in column.column.summary().items() if key != "name"}
    )
    frontmatter["source_refs"] = [column.provenance.as_dict()]
    inbound = extraction.inbound_relations_for(column.id)
    if inbound:
        frontmatter["inbound_relations"] = _inbound_entries(inbound)

    body = [
        f"# {column.table_name}.{column.title}",
        "",
        f"Candidate column extracted from an ORM mapping in `{extraction.repository}` at "
        f"commit `{extraction.commit}`.",
        "",
        f"- Table: `{column.table_id}`",
        f"- Declared by: `{column.declaring_class}`",
        f"- Declared in: `{column.provenance.source_path}` "
        f"(lines {column.provenance.line_start}-{column.provenance.line_end})",
        f"- Evidence class: `{EVIDENCE_TYPE}`",
        "",
        "## Review notes",
        "",
        "This page is a candidate awaiting review. Only the presence of a default is "
        "recorded, never its value.",
        "",
    ]
    return _render_page(frontmatter, body)


def render_schema_markdown(
    schema: DocumentSchemaCandidate, extraction: DataModelExtraction
) -> str:
    frontmatter = _base_frontmatter(
        identifier=schema.id,
        kind=schema.kind,
        title=schema.title,
        extraction=extraction,
        service_entity=_service_entity(extraction, schema.service),
    )
    frontmatter["persistence_role"] = PERSISTENCE_ROLE_DOCUMENT
    frontmatter["storage_engine"] = schema.engine
    frontmatter["persistence_library"] = schema.library
    frontmatter["database"] = schema.database
    frontmatter["collection"] = schema.collection_name
    frontmatter["model_class"] = schema.model_class
    frontmatter["fields"] = [item.summary() for item in schema.fields]
    if schema.declared_indexes:
        frontmatter["declared_indexes"] = list(schema.declared_indexes)
    if schema.references:
        frontmatter["document_references"] = list(schema.references)
    frontmatter["source_refs"] = [schema.provenance.as_dict()]
    inbound = extraction.inbound_relations_for(schema.id)
    if inbound:
        frontmatter["inbound_relations"] = _inbound_entries(inbound)
    frontmatter["attributes"] = schema.attributes

    body = [
        f"# {schema.title}",
        "",
        f"Candidate persistent document model extracted from an ODM declaration in "
        f"`{extraction.repository}` at commit `{extraction.commit}`.",
        "",
        f"- Owning service: `{_service_entity(extraction, schema.service)}`",
        f"- Database: `{schema.database or 'unresolved'}`",
        f"- Collection: `{schema.collection_name or 'unresolved'}`",
        f"- Persistence library: `{schema.library}`",
        f"- Declared in: `{schema.provenance.source_path}` "
        f"(lines {schema.provenance.line_start}-{schema.provenance.line_end})",
        f"- Evidence class: `{EVIDENCE_TYPE}`",
        "",
        "## Ontology note",
        "",
        f"The ontology has no `Collection` kind, so this document model is recorded as a "
        f"`{SCHEMA_KIND}` with `persistence_role: {PERSISTENCE_ROLE_DOCUMENT}` and the "
        "collection name kept as an attribute. See `ontology_gaps` in the extraction report.",
        "",
        "## Review notes",
        "",
        "This page is a candidate awaiting review. Fields are recorded as declared source "
        "text and no default is evaluated.",
        "",
    ]
    return _render_page(frontmatter, body)


def render_collection_markdown(
    collection: CollectionCandidate, extraction: DataModelExtraction
) -> str:
    frontmatter = _base_frontmatter(
        identifier=collection.id,
        kind=collection.kind,
        title=collection.title,
        extraction=extraction,
        service_entity=_service_entity(extraction, collection.service),
    )
    frontmatter["collection_name"] = collection.collection_name
    frontmatter["storage_engine"] = collection.engine
    frontmatter["persistence_library"] = collection.library
    frontmatter["database"] = collection.database
    frontmatter["schema"] = collection.schema_id
    frontmatter["model_class"] = collection.model_class
    if collection.declared_indexes:
        frontmatter["declared_indexes"] = list(collection.declared_indexes)
    frontmatter["source_refs"] = [collection.provenance.as_dict()]
    inbound = extraction.inbound_relations_for(collection.id)
    if inbound:
        frontmatter["inbound_relations"] = _inbound_entries(inbound)
    outbound = extraction.relations_for(collection.id)
    if outbound:
        frontmatter["relations"] = _relation_entries(outbound)
    frontmatter["attributes"] = collection.attributes

    body = [
        f"# {collection.collection_name}",
        "",
        f"Candidate MongoDB collection extracted from an explicit ODM collection name in "
        f"`{extraction.repository}` at commit `{extraction.commit}`.",
        "",
        f"- Owning service: `{_service_entity(extraction, collection.service)}`",
        f"- Database: `{collection.database or 'unresolved'}`",
        f"- Document schema: `{collection.schema_id}`",
        f"- Model class: `{collection.model_class}`",
        f"- Persistence library: `{collection.library}`",
        f"- Declared in: `{collection.provenance.source_path}` "
        f"(lines {collection.provenance.line_start}-{collection.provenance.line_end})",
        f"- Evidence class: `{EVIDENCE_TYPE}`",
        "",
        "## Review notes",
        "",
        "This page is a candidate awaiting review. The collection name comes from an explicit "
        "ODM `Settings` declaration; the document model itself is the linked `Schema`, and no "
        "`Column` entity is created for a document field.",
        "",
    ]
    return _render_page(frontmatter, body)


def render_migration_markdown(
    migration: MigrationCandidate, extraction: DataModelExtraction
) -> str:
    frontmatter = _base_frontmatter(
        identifier=migration.id,
        kind=migration.kind,
        title=migration.title,
        extraction=extraction,
        service_entity=_service_entity(extraction, migration.service),
    )
    frontmatter["revision"] = migration.revision
    frontmatter["down_revision"] = migration.down_revision
    frontmatter["tool"] = migration.tool
    frontmatter["touched_tables"] = list(migration.touched_tables)
    frontmatter["operations"] = list(migration.operations)
    frontmatter["source_refs"] = [migration.provenance.as_dict()]
    inbound = extraction.inbound_relations_for(migration.id)
    if inbound:
        frontmatter["inbound_relations"] = _inbound_entries(inbound)

    body = [
        f"# {migration.title}",
        "",
        f"Candidate migration extracted from an Alembic revision in "
        f"`{extraction.repository}` at commit `{extraction.commit}`.",
        "",
        f"- Revision: `{migration.revision}`",
        f"- Previous revision: `{migration.down_revision or 'none'}`",
        f"- Declared in: `{migration.provenance.source_path}`",
        f"- Evidence class: `{EVIDENCE_TYPE}`",
        "",
        "## Review notes",
        "",
        "This page is a candidate awaiting review. Table linkage is created only for tables "
        "the migration names explicitly and that exist in scanned source.",
        "",
    ]
    return _render_page(frontmatter, body)


def render_all(extraction: DataModelExtraction) -> dict[str, str]:
    """Render every candidate page keyed by output-relative POSIX path."""
    rendered: dict[str, str] = {}
    for table in extraction.tables:
        rendered[f"tables/{table.id}.md"] = render_table_markdown(table, extraction)
    for column in extraction.columns:
        rendered[f"columns/{column.id}.md"] = render_column_markdown(column, extraction)
    for collection in extraction.collections:
        rendered[f"collections/{collection.id}.md"] = render_collection_markdown(
            collection, extraction
        )
    for schema in extraction.document_schemas:
        rendered[f"schemas/{schema.id}.md"] = render_schema_markdown(schema, extraction)
    for migration in extraction.migrations:
        rendered[f"migrations/{migration.id}.md"] = render_migration_markdown(
            migration, extraction
        )
    return rendered


def build_database_relation_deltas(extraction: DataModelExtraction) -> dict[str, Any]:
    """Outgoing relations to merge later into existing canonical Database pages."""
    by_database: dict[str, list[RelationshipCandidate]] = {}
    for relation in extraction.relationships:
        if relation.source.startswith("database."):
            by_database.setdefault(relation.source, []).append(relation)
    return {
        "version": 1,
        "extractor": EXTRACTOR_KIND,
        "repository": extraction.repository,
        "commit": extraction.commit,
        "status": CANDIDATE_STATUS,
        "review_status": CANDIDATE_REVIEW_STATUS,
        "note": (
            "Candidate outgoing relations for existing canonical Database pages. This file is "
            "not canonical knowledge and must not be copied into wiki/ without review."
        ),
        "databases": [
            {
                "database": identifier,
                "relation_count": len(by_database[identifier]),
                "relations": [
                    relation.summary()
                    for relation in sorted(
                        by_database[identifier], key=lambda item: (item.type, item.target)
                    )
                ],
            }
            for identifier in sorted(by_database)
        ],
    }


def build_service_relation_deltas(extraction: DataModelExtraction) -> dict[str, Any]:
    """Outgoing READS/WRITES relations to merge later into canonical Service pages."""
    by_service: dict[str, list[RelationshipCandidate]] = {}
    for relation in extraction.relationships:
        if relation.type in (READS, WRITES):
            by_service.setdefault(relation.source, []).append(relation)
    return {
        "version": 1,
        "extractor": EXTRACTOR_KIND,
        "repository": extraction.repository,
        "commit": extraction.commit,
        "status": CANDIDATE_STATUS,
        "review_status": CANDIDATE_REVIEW_STATUS,
        "note": (
            "Candidate outgoing READS/WRITES relations for existing canonical Service pages. "
            "This file is not canonical knowledge and must not be copied into wiki/ without "
            "review."
        ),
        "services": [
            {
                "service": identifier,
                "relation_count": len(by_service[identifier]),
                "relations": [
                    relation.summary()
                    for relation in sorted(
                        by_service[identifier], key=lambda item: (item.type, item.target)
                    )
                ],
            }
            for identifier in sorted(by_service)
        ],
    }


def build_report(extraction: DataModelExtraction, secret_values_emitted: int) -> dict[str, Any]:
    """Assemble extraction-report.json. Contains no timestamp, so runs stay comparable."""
    relationship_counts: dict[str, int] = {}
    for relation in extraction.relationships:
        relationship_counts[relation.type] = relationship_counts.get(relation.type, 0) + 1
    reads = [item for item in extraction.accesses if item.role == READ_ROLE]
    writes = [item for item in extraction.accesses if item.role == WRITE_ROLE]

    return {
        "version": 1,
        "extractor": EXTRACTOR_KIND,
        "repository": extraction.repository,
        "commit": extraction.commit,
        "commit_verified": True,
        "evidence_type": EVIDENCE_TYPE,
        "analysis": "python-ast/static",
        "modules_imported": 0,
        "modules_executed": 0,
        "database_connections_opened": 0,
        "source_files": list(extraction.source_files),
        "skipped_files": list(extraction.skipped_files),
        "services_scanned": [scan.summary() for scan in extraction.services_scanned],
        "persistence_libraries_detected": list(extraction.libraries),
        "local_persistence_wrappers": list(extraction.wrappers),
        "relational_models": [
            {"model_class": item.model_class, "table": item.id} for item in extraction.tables
        ],
        "document_models": [
            {"model_class": item.model_class, "schema": item.id, "collection": item.collection_name}
            for item in extraction.document_schemas
        ],
        "tables": [item.summary() for item in extraction.tables],
        "columns": [item.summary() for item in extraction.columns],
        "collections": [item.summary() for item in extraction.collections],
        "schemas": [item.summary() for item in extraction.document_schemas],
        "migrations": [item.summary() for item in extraction.migrations],
        "database_mappings": [item.summary() for item in extraction.database_mappings],
        "read_accesses": [item.summary() for item in reads],
        "write_accesses": [item.summary() for item in writes],
        "relationships": [item.summary() for item in extraction.relationships],
        "relationships_by_type": dict(sorted(relationship_counts.items())),
        "counts": {
            "source_files": len(extraction.source_files),
            "skipped_files": len(extraction.skipped_files),
            "services_scanned": len(extraction.services_scanned),
            "persistence_libraries": len(extraction.libraries),
            "local_persistence_wrappers": len(extraction.wrappers),
            "tables": len(extraction.tables),
            "columns": len(extraction.columns),
            "collections": len(extraction.collections),
            "document_models": len(extraction.document_schemas),
            "migrations": len(extraction.migrations),
            "database_mappings": len(extraction.database_mappings),
            "read_accesses": len(reads),
            "write_accesses": len(writes),
            "relationships": len(extraction.relationships),
            "identity_collisions": len(extraction.identity_collisions),
            "ontology_gaps": len(extraction.ontology_gaps),
            "warnings": len(extraction.warnings),
        },
        "unresolved_database_mappings": [
            item.summary() for item in extraction.unresolved_of(UNRESOLVED_DATABASE)
        ],
        "unresolved_table_names": [
            item.summary() for item in extraction.unresolved_of(UNRESOLVED_TABLE_NAME)
        ],
        "unresolved_collection_names": [
            item.summary() for item in extraction.unresolved_of(UNRESOLVED_COLLECTION_NAME)
        ],
        "unresolved_model_references": [
            item.summary() for item in extraction.unresolved_of(UNRESOLVED_MODEL_REFERENCE)
        ],
        "unresolved_accesses": [
            item.summary() for item in extraction.unresolved_of(UNRESOLVED_ACCESS)
        ],
        "identity_collisions": [item.summary() for item in extraction.identity_collisions],
        "ontology_gaps": [item.summary() for item in extraction.ontology_gaps],
        "warnings": list(extraction.warnings),
        "secret_values_emitted": secret_values_emitted,
        "graph_mutations": 0,
        "wiki_writes": 0,
        "neo4j_mutations": 0,
        "graphiti_mutations": 0,
        "graphiti": "disabled",
    }


def count_secret_leaks(extraction: DataModelExtraction, rendered: dict[str, str]) -> int:
    """Measure credential leakage by whole-token match, not raw substring.

    A credential has leaked only when its value appears as a standalone token. Matching on
    substrings would flag ordinary identifiers that merely contain the same characters.
    """
    scannable = {
        value.strip()
        for value in extraction.withheld_values
        if len(value.strip()) >= _MIN_SCANNABLE_SECRET_LENGTH and not value.strip().isdigit()
    }
    leaks = 0
    for content in rendered.values():
        for secret in sorted(scannable):
            pattern = re.compile(rf"(?<![A-Za-z0-9_-]){re.escape(secret)}(?![A-Za-z0-9_-])")
            leaks += len(pattern.findall(content))
    return leaks


def render_report_json(report: dict[str, Any]) -> str:
    return json.dumps(report, indent=2, ensure_ascii=False) + "\n"


def render_bundle(extraction: DataModelExtraction) -> tuple[dict[str, str], dict[str, Any]]:
    """Render candidates plus the report, with the leak count measured over all output."""
    rendered = render_all(extraction)
    provisional = build_report(extraction, 0)
    scanned = {
        **rendered,
        "extraction-report.json": render_report_json(provisional),
        DATABASE_DELTAS_FILENAME: render_report_json(
            build_database_relation_deltas(extraction)
        ),
        SERVICE_DELTAS_FILENAME: render_report_json(build_service_relation_deltas(extraction)),
    }
    leaks = count_secret_leaks(extraction, scanned)
    return rendered, build_report(extraction, leaks)


def render_sidecars(
    extraction: DataModelExtraction, report: dict[str, Any]
) -> dict[str, str]:
    """Extra output files this extractor owns beyond the candidate pages and the report."""
    del report
    return {
        DATABASE_DELTAS_FILENAME: render_report_json(
            build_database_relation_deltas(extraction)
        ),
        SERVICE_DELTAS_FILENAME: render_report_json(build_service_relation_deltas(extraction)),
    }


def summarize(extraction: DataModelExtraction, report: dict[str, Any]) -> dict[str, Any]:
    """CLI-facing summary of one extraction run."""
    return {
        "extractor": report["extractor"],
        "repository": extraction.repository,
        "commit": extraction.commit,
        "commit_verified": True,
        "analysis": "python-ast/static",
        "modules_imported": 0,
        "modules_executed": 0,
        "database_connections_opened": 0,
        "source_files": list(extraction.source_files),
        "counts": report["counts"],
        "services_scanned": [scan.summary() for scan in extraction.services_scanned],
        "persistence_libraries_detected": list(extraction.libraries),
        "local_persistence_wrappers": list(extraction.wrappers),
        "database_mappings": [item.summary() for item in extraction.database_mappings],
        "tables": [item.id for item in extraction.tables],
        "collections": [item.id for item in extraction.collections],
        "document_models": [item.id for item in extraction.document_schemas],
        "migrations": [item.id for item in extraction.migrations],
        "relationships_by_type": report["relationships_by_type"],
        "unresolved_database_mappings": report["unresolved_database_mappings"],
        "unresolved_table_names": report["unresolved_table_names"],
        "unresolved_collection_names": report["unresolved_collection_names"],
        "unresolved_model_references": report["unresolved_model_references"],
        "unresolved_accesses": report["unresolved_accesses"],
        "identity_collisions": report["identity_collisions"],
        "ontology_gaps": report["ontology_gaps"],
        "warnings": list(extraction.warnings),
        "secret_values_emitted": report["secret_values_emitted"],
        "graph_mutations": 0,
        "wiki_writes": 0,
        "neo4j_mutations": 0,
        "graphiti": "disabled",
    }
