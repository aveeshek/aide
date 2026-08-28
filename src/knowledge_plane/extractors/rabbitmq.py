"""Deterministic RabbitMQ/RPC interaction extractor (Graph Engineering Pass 3).

Scope and non-goals
-------------------
This extractor reads Python source with :mod:`ast` and emits *candidates* only. It never
imports or executes the inspected application, never starts a service, never opens an AMQP
connection, never writes canonical knowledge, never touches Neo4j or Graphiti, and never
calls an LLM.

It records only what the Python source states explicitly:

* ``Service -PUBLISHES-> Event`` where a broker send/RPC-request call is statically proven
* ``Service -CONSUMES-> Event`` where a handler registration or queue binding is proven

HTTP APIs, database models, message payload schemas, tests, and business flows are out of
scope for this pass. No ``CALLS`` edge is created between services: cross-service paths are
expressed by two services sharing one ``Event`` identity. No ``DEPENDS_ON`` edge to the
broker is created either, because Compose Pass 1 already owns infrastructure dependencies.

Why a name is never enough
--------------------------
A method called ``publish()`` or ``send()`` proves nothing on its own; plenty of unrelated
objects have such methods. Every operation this extractor reports is therefore *rooted*:
the receiver of the call must be traced back, statically, to a symbol imported from a known
broker library (``rabbitmq_rpc`` or ``aio_pika``). Only once the receiver is proven to be a
broker client is the method name consulted. The same discipline applies to identities: an
event key, queue, exchange, or routing key is accepted only when it resolves to a string
through literals, module constants, Enum members, imported constants, or concatenation of
those. Anything computed at runtime is reported unresolved rather than guessed.

Bounded tracing
---------------
Real code hides the broker behind wrappers. FTGO's gateway calls
``Microservice._call_rpc('order.create', ...)``, and that wrapper calls
``rpc_client.call(event_name, ...)`` on a client obtained from ``RPCBroker.get_client()``.
Two bounded traces make this provable without becoming an interpreter:

``_MAX_WRAPPER_HOPS``
    How far an application call site may be from the real broker call (application ->
    wrapper -> broker library).
``_MAX_VALUE_HOPS``
    How far a value may be from a broker-library symbol through return annotations
    (``RPCBroker.get_instance()`` -> ``RPCBroker`` -> ``.get_client()`` -> ``RPCClient``).

Anything beyond the bounds is reported unresolved.

Determinism
-----------
Identifiers derive from the repository slug, the service slug, and the statically resolved
broker identity. No hash, counter, timestamp, or absolute workstation path enters the
output, so re-running against an unchanged commit produces byte-identical candidates.
"""

from __future__ import annotations

import ast
import json
import re
from dataclasses import dataclass, field
from typing import Any

import yaml

from ..repository_manifest import RepositoryRecord, resolve_source_files
from .fastapi import (
    Provenance,
    module_dotted_name,
    normalize_dotted,
    normalize_token,
    service_location,
)

EXTRACTOR_KIND = "rabbitmq"
CANDIDATE_STATUS = "candidate"
CANDIDATE_REVIEW_STATUS = "pending"
EVIDENCE_TYPE = "implemented"
REDACTED_PLACEHOLDER = "[redacted]"

# Output subdirectory owned by this extractor, used for stale-candidate pruning.
CANDIDATE_SUBDIRECTORIES = ("events",)
DELTAS_FILENAME = "service-relation-deltas.json"

# Ontology types used. Both already exist in ontology/; this pass introduces none.
EVENT_KIND = "Event"
PUBLISHES = "PUBLISHES"
CONSUMES = "CONSUMES"

PUBLISHER_ROLE = "publisher"
CONSUMER_ROLE = "consumer"

# Manifest source kind scanned by this pass.
SOURCE_KIND = "code"
PYTHON_SUFFIX = ".py"
# Only application source under a service's ``src`` root is in scope.
REQUIRED_SOURCE_SEGMENT = "src"

# Broker libraries that can root an operation. A call is only ever reported when its
# receiver traces back to one of these.
BROKER_LIBRARIES: tuple[str, ...] = ("rabbitmq_rpc", "aio_pika")

# Method names consulted *only after* the receiver is proven to be a broker client.
PUBLISH_OPERATIONS = frozenset(
    {
        "basic_publish",
        "call",
        "emit",
        "publish",
        "publish_message",
        "rpc_call",
        "send",
        "send_message",
    }
)
CONSUME_OPERATIONS = frozenset(
    {
        "add_handler",
        "basic_consume",
        "consume",
        "listen",
        "on_event",
        "register",
        "register_event",
        "register_handler",
        "subscribe",
    }
)
BROKER_OPERATIONS = PUBLISH_OPERATIONS | CONSUME_OPERATIONS

# Keyword arguments that may carry the logical identity, in priority order.
IDENTITY_KEYWORDS: tuple[str, ...] = (
    "event",
    "event_name",
    "operation",
    "method",
    "routing_key",
    "topic",
    "queue",
    "queue_name",
    "exchange",
    "name",
    "key",
)
EXCHANGE_KEYWORDS: tuple[str, ...] = ("exchange", "exchange_name")
QUEUE_KEYWORDS: tuple[str, ...] = ("queue", "queue_name")
ROUTING_KEY_KEYWORDS: tuple[str, ...] = ("routing_key", "topic")
HANDLER_KEYWORDS: tuple[str, ...] = ("handler", "callback", "consumer", "func", "listener")

# Broker vocabulary that must never be treated as a credential name. See
# :func:`is_credential_name`.
TOPOLOGY_SAFE_KEYWORDS = frozenset(
    IDENTITY_KEYWORDS + EXCHANGE_KEYWORDS + QUEUE_KEYWORDS + ROUTING_KEY_KEYWORDS
    + HANDLER_KEYWORDS
)

# Interaction mechanism labels, derived from the operation, never guessed from names.
MECHANISM_RPC = "rpc"
MECHANISM_MESSAGE = "message"
RPC_OPERATIONS = frozenset({"call", "rpc_call", "register_event", "register_handler"})

# Secret-safety markers. A value bound to a name containing one of these is never emitted.
SECRET_KEY_MARKERS = (
    "PASSWORD",
    "PASS",
    "SECRET",
    "TOKEN",
    "KEY",
    "CREDENTIAL",
    "AUTH",
)
# Markers that identify a credential on their own.
_STRONG_CREDENTIAL_MARKERS = (
    "PASSWORD",
    "PASS",
    "SECRET",
    "TOKEN",
    "CREDENTIAL",
    "AUTH",
)
# ``KEY`` alone is not a credential: FTGO uses ``*_KEY`` names for Redis cache keys and
# RabbitMQ routing keys. It counts only when qualified as a credential key.
_QUALIFIED_KEY_MARKERS = (
    "ACCESS_KEY",
    "API_KEY",
    "ENCRYPTION_KEY",
    "PRIVATE_KEY",
    "PUBLIC_KEY",
    "SECRET_KEY",
    "SIGNING_KEY",
)
# Short or numeric withheld values would create false leak reports against ordinary small
# numbers in the output, so only distinctive values enter the leak scan.
_MIN_SCANNABLE_SECRET_LENGTH = 4
# An AMQP URL carrying userinfo is redacted wherever it is emitted.
_AMQP_CREDENTIAL_PATTERN = re.compile(r"(amqps?://)[^/\s:@]+:[^/\s@]+@", re.IGNORECASE)
_AMQP_USERINFO_PATTERN = re.compile(r"amqps?://([^/\s:@]+):([^/\s@]+)@", re.IGNORECASE)

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
        "migrations",
        "node_modules",
        "site-packages",
        "venv",
    }
)
TEST_PATH_SEGMENTS = frozenset({"test", "tests"})
GENERATED_FILENAME_SUFFIXES = ("_pb2.py", "_pb2_grpc.py", "_pb2.pyi")
GENERATED_HEADER_MARKERS = ("@generated", "generated by", "do not edit this file")
_GENERATED_HEADER_LINES = 5

# Bounded traces. Both are deliberately small: this is static analysis, not evaluation.
_MAX_WRAPPER_HOPS = 2
_MAX_VALUE_HOPS = 3
_MAX_RESOLUTION_DEPTH = 24
_MAX_EXPRESSION_LENGTH = 200
_MAX_CONCAT_PARTS = 8

# Interaction correlation outcomes.
STATUS_MATCHED = "matched"
STATUS_PUBLISHER_ONLY = "publisher_only"
STATUS_CONSUMER_ONLY = "consumer_only"


# ---------------------------------------------------------------------------------------
# Normalization and safety helpers
# ---------------------------------------------------------------------------------------


def normalize_identity(value: str) -> str:
    """Normalize a broker identity into stable dot-delimited id tokens.

    ``Order.Create`` and ``order.create`` normalize identically, which is exactly why a
    collision between two *different* raw identities has to be reported rather than merged.
    """
    return normalize_dotted(value)


def event_id(repository_slug: str, identity: str) -> str:
    """Build a byte-stable Event id from the canonical broker identity."""
    normalized = normalize_identity(identity)
    return f"event.{repository_slug}.{EXTRACTOR_KIND}.{normalized}"


def service_entity_id(repository_slug: str, service_slug: str) -> str:
    return f"service.{repository_slug}.{service_slug}"


def is_secret_name(name: str) -> bool:
    """True when a binding name looks like it holds a credential."""
    upper = str(name).upper()
    return any(marker in upper for marker in SECRET_KEY_MARKERS)


def is_credential_name(name: str) -> bool:
    """True when a binding name holds a credential rather than broker or cache topology.

    Two exemptions keep this precise, and both are load-bearing against real FTGO source:

    * broker vocabulary. ``routing_key`` contains the ``KEY`` marker and an event name may
      contain ``AUTH`` (FTGO really does publish ``user.profile.resend_auth_code``). Those
      are the *subject* of this pass.
    * bare ``*_KEY`` names. FTGO's ``DRIVER_STATUS_KEY`` is a Redis cache key whose value is
      ``driver_status``; treating it as a credential made the leak scanner flag the substring
      inside the unrelated method name ``get_driver_status``.

    Without these exemptions the scanner reports false leaks against the topology it exists
    to protect, which would make ``secret_values_emitted`` meaningless.
    """
    lowered = str(name).strip().lower()
    if lowered in TOPOLOGY_SAFE_KEYWORDS:
        return False
    upper = lowered.upper()
    if any(marker in upper for marker in _QUALIFIED_KEY_MARKERS):
        return True
    return any(marker in upper for marker in _STRONG_CREDENTIAL_MARKERS)


def redact_amqp(text: str) -> str:
    """Strip userinfo from any AMQP URL in ``text``."""
    return _AMQP_CREDENTIAL_PATTERN.sub(rf"\1{REDACTED_PLACEHOLDER}@", str(text))


def safe_expression(text: str | None) -> str | None:
    """Project an expression for emission, redacting embedded AMQP credentials."""
    if text is None:
        return None
    return redact_amqp(text)


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
    return redact_amqp(collapsed[:_MAX_EXPRESSION_LENGTH])


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


def _keyword_node(call: ast.Call, name: str) -> ast.expr | None:
    for keyword in call.keywords:
        if keyword.arg == name:
            return keyword.value
    return None


def _first_keyword(call: ast.Call, names: tuple[str, ...]) -> tuple[str, ast.expr] | None:
    for name in names:
        node = _keyword_node(call, name)
        if node is not None:
            return name, node
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
    if not remainder or remainder[0] != REQUIRED_SOURCE_SEGMENT:
        return f"outside the service {REQUIRED_SOURCE_SEGMENT!r} root"
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
class FunctionFacts:
    """A function or method, with what this pass needs to trace broker usage through it."""

    name: str
    qualified_name: str
    owner_class: str | None
    parameters: tuple[str, ...]
    returns: ast.expr | None
    node: ast.FunctionDef | ast.AsyncFunctionDef
    lineno: int
    end_lineno: int


@dataclass(frozen=True, slots=True)
class ClassFacts:
    """A class definition with its declared bases and its methods."""

    name: str
    bases: tuple[ast.expr, ...]
    methods: dict[str, FunctionFacts]
    enum_members: dict[str, str]
    is_enum: bool
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
    source: str
    tree: ast.Module
    imports: dict[str, ImportedSymbol]
    constants: dict[str, ast.expr]
    classes: dict[str, ClassFacts]
    functions: dict[str, FunctionFacts]
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
                    # ``import a.b`` binds ``a``, not ``a.b``.
                    local = module = alias.name.split(".", 1)[0]
                imports.setdefault(
                    local, ImportedSymbol(module=module, name=None, lineno=node.lineno)
                )
        elif isinstance(node, ast.ImportFrom):
            for alias in node.names:
                if alias.name == "*":
                    # A star import binds unknown names; nothing can be resolved from it.
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
    """Positional parameter names, with an implicit ``self``/``cls`` receiver dropped.

    Dropping the receiver is what lets ``cls._call_rpc('order.create')`` line up with
    ``def _call_rpc(cls, event_name, ...)`` on argument index 0.
    """
    arguments = node.args
    names = [item.arg for item in (*arguments.posonlyargs, *arguments.args)]
    if names and names[0] in ("self", "cls"):
        names = names[1:]
    return tuple(names)


def _enum_members(node: ast.ClassDef) -> dict[str, str]:
    """Statically declared ``MEMBER = "value"`` entries of a class body."""
    members: dict[str, str] = {}
    for statement in node.body:
        targets: list[ast.expr] = []
        value: ast.expr | None = None
        if isinstance(statement, ast.Assign):
            targets = list(statement.targets)
            value = statement.value
        elif isinstance(statement, ast.AnnAssign):
            targets = [statement.target]
            value = statement.value
        literal = _constant_string(value)
        if literal is None:
            continue
        for target in targets:
            if isinstance(target, ast.Name):
                members.setdefault(target.id, literal)
    return members


def _collect_withheld(source: str, tree: ast.Module) -> set[str]:
    """Collect credential string literals so leaks can be measured rather than assumed.

    Three precise signals are used, deliberately narrow so the count stays a real
    measurement:

    * a string assigned to a credential-named target (``password = "..."``)
    * a string passed to a credential-named keyword (``password="..."``)
    * the ``default=`` of a lookup whose positional key is credential-named, which is how
      ``env_var("RABBITMQ_PASS", default="rabbitmq_password")`` gives itself away
    * the userinfo of any AMQP URL literal

    Broker vocabulary is exempt via :func:`is_credential_name`.
    """
    del source
    withheld: set[str] = set()

    def remember(value: str | None) -> None:
        if value and len(value.strip()) >= _MIN_SCANNABLE_SECRET_LENGTH:
            withheld.add(value.strip())

    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                name = target.id if isinstance(target, ast.Name) else getattr(target, "attr", "")
                if name and is_credential_name(name):
                    remember(_constant_string(node.value))
        elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            if is_credential_name(node.target.id):
                remember(_constant_string(node.value))
        elif isinstance(node, ast.Call):
            for keyword in node.keywords:
                if keyword.arg and is_credential_name(keyword.arg):
                    remember(_constant_string(keyword.value))
            positional = [_constant_string(item) for item in node.args]
            if any(text is not None and is_credential_name(text) for text in positional):
                for keyword in node.keywords:
                    remember(_constant_string(keyword.value))
        elif isinstance(node, ast.Constant) and isinstance(node.value, str):
            userinfo = _AMQP_USERINFO_PATTERN.search(node.value)
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
    """Gather imports, module constants, classes, and functions from one parsed module."""
    imports = _collect_imports(tree)
    constants: dict[str, ast.expr] = {}
    classes: dict[str, ClassFacts] = {}
    functions: dict[str, FunctionFacts] = {}

    def register_function(
        node: ast.FunctionDef | ast.AsyncFunctionDef, owner: str | None
    ) -> FunctionFacts:
        qualified = f"{owner}.{node.name}" if owner else node.name
        return FunctionFacts(
            name=node.name,
            qualified_name=qualified,
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
                    f"{relative_path}: function {statement.name!r} is defined more than "
                    f"once; kept the first definition at line {functions[statement.name].lineno}"
                )
            else:
                functions[statement.name] = register_function(statement, None)
        elif isinstance(statement, ast.ClassDef):
            methods: dict[str, FunctionFacts] = {}
            for member in statement.body:
                if isinstance(member, ast.FunctionDef | ast.AsyncFunctionDef):
                    methods.setdefault(member.name, register_function(member, statement.name))
            members = _enum_members(statement)
            base_names = {_dotted_expression(base) or "" for base in statement.bases}
            is_enum = any(
                name.split(".")[-1] in ("Enum", "StrEnum", "IntEnum", "Flag", "IntFlag")
                for name in base_names
                if name
            )
            if statement.name in classes:
                warnings.append(
                    f"{relative_path}: class {statement.name!r} is defined more than once; "
                    f"kept the first definition at line {classes[statement.name].lineno}"
                )
            else:
                classes[statement.name] = ClassFacts(
                    name=statement.name,
                    bases=tuple(statement.bases),
                    methods=methods,
                    enum_members=members,
                    is_enum=is_enum,
                    lineno=statement.lineno,
                    end_lineno=statement.end_lineno or statement.lineno,
                )

    return ModuleFacts(
        relative_path=relative_path,
        service=service,
        service_root=service_root,
        module=module,
        is_package=is_package,
        source=source,
        tree=tree,
        imports=imports,
        constants=constants,
        classes=classes,
        functions=functions,
        withheld_values=frozenset(_collect_withheld(source, tree)),
    )


# ---------------------------------------------------------------------------------------
# Symbol resolution
# ---------------------------------------------------------------------------------------

SYMBOL_CLASS = "class"
SYMBOL_FUNCTION = "function"
SYMBOL_CONSTANT = "constant"
SYMBOL_MODULE = "module"
SYMBOL_BROKER = "broker_library"
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


def broker_library_of(module: str) -> str | None:
    """Return the broker library that owns ``module``, or None."""
    for library in BROKER_LIBRARIES:
        if module == library or module.startswith(f"{library}."):
            return library
    return None


@dataclass(frozen=True, slots=True)
class SourceIndex:
    """All analyzed modules, addressable by dotted name and by dotted suffix.

    Suffix lookup exists because a repository's ``sys.path`` root is not knowable from the
    filesystem alone. A suffix is only usable when it identifies exactly one module, so an
    ambiguous import resolves to nothing rather than to a guess.
    """

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
                SYMBOL_UNKNOWN,
                module,
                name,
                reason="name is not defined or imported in this module",
            )
        # A broker library is recognized before any local lookup: it is never scanned
        # source, and it is the only thing that can root an operation.
        library = broker_library_of(imported.module)
        if library is not None:
            return SymbolRef(
                SYMBOL_BROKER, imported.module, imported.name or name, library=library
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
        if head.kind == SYMBOL_BROKER:
            # Any attribute reached through a broker library stays broker-rooted.
            return SymbolRef(
                SYMBOL_BROKER, head.module, parts[-1], library=head.library
            )
        if head.kind == SYMBOL_MODULE and head.module is not None:
            return self.resolve_dotted(service, head.module, ".".join(parts[1:]))
        if head.kind == SYMBOL_CLASS and head.module is not None and head.name is not None:
            return head
        return SymbolRef(
            SYMBOL_UNKNOWN, module, dotted, reason="attribute chain could not be traced"
        )

    def lookup_method(
        self,
        service: str,
        module: str,
        class_name: str,
        method_name: str,
        *,
        _depth: int = 0,
    ) -> tuple[str, FunctionFacts] | None:
        """Find ``method_name`` on a class or its statically declared bases.

        FTGO's gateway relies on this: ``OrderService`` declares no ``_call_rpc``, it
        inherits it from ``Microservice`` in another module.
        """
        if _depth > _MAX_RESOLUTION_DEPTH:
            return None
        facts = self.facts(service, module)
        if facts is None:
            return None
        declaration = facts.classes.get(class_name)
        if declaration is None:
            return None
        method = declaration.methods.get(method_name)
        if method is not None:
            return module, method
        for base in declaration.bases:
            dotted = _dotted_expression(base)
            if dotted is None:
                continue
            resolved = self.resolve_dotted(service, module, dotted)
            if (
                resolved.kind == SYMBOL_CLASS
                and resolved.module is not None
                and resolved.name is not None
            ):
                found = self.lookup_method(
                    service, resolved.module, resolved.name, method_name, _depth=_depth + 1
                )
                if found is not None:
                    return found
        return None

    def lookup_attribute_string(
        self, service: str, module: str, class_name: str, attribute: str
    ) -> str | None:
        """Return a statically declared string attribute of a class or its bases."""
        facts = self.facts(service, module)
        if facts is None:
            return None
        declaration = facts.classes.get(class_name)
        if declaration is None:
            return None
        if attribute in declaration.enum_members:
            return declaration.enum_members[attribute]
        for base in declaration.bases:
            dotted = _dotted_expression(base)
            if dotted is None:
                continue
            resolved = self.resolve_dotted(service, module, dotted)
            if (
                resolved.kind == SYMBOL_CLASS
                and resolved.module is not None
                and resolved.name is not None
            ):
                found = self.lookup_attribute_string(
                    service, resolved.module, resolved.name, attribute
                )
                if found is not None:
                    return found
        return None

    def is_enum_class(self, service: str, module: str, class_name: str) -> bool:
        facts = self.facts(service, module)
        if facts is None:
            return False
        declaration = facts.classes.get(class_name)
        return bool(declaration and declaration.is_enum)


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
            key = (item.service, ".".join(parts[start:]))
            suffix_sets.setdefault(key, set()).add(item.module)
    return SourceIndex(
        modules=indexed,
        suffixes={key: frozenset(value) for key, value in suffix_sets.items()},
    )


# ---------------------------------------------------------------------------------------
# Broker value typing
# ---------------------------------------------------------------------------------------

VALUE_BROKER = "broker"
VALUE_LOCAL_INSTANCE = "local_instance"
VALUE_UNKNOWN = "unknown"

# Broker-library members whose result is itself a broker object. Used only when the
# receiver is already proven broker-rooted, so this never widens detection by itself.
BROKER_FACTORY_MEMBERS = frozenset(
    {
        "channel",
        "connect",
        "connect_robust",
        "create",
        "declare_exchange",
        "declare_queue",
        "from_url",
        "get_channel",
        "get_client",
        "get_exchange",
        "get_queue",
    }
)


@dataclass(frozen=True, slots=True)
class ValueType:
    """What a local variable holds, as far as static evidence proves."""

    kind: str
    module: str | None = None
    class_name: str | None = None
    library: str | None = None

    @property
    def is_broker(self) -> bool:
        return self.kind == VALUE_BROKER


UNKNOWN_VALUE = ValueType(VALUE_UNKNOWN)


@dataclass(frozen=True, slots=True)
class IterationBinding:
    """A loop variable bound to statically known strings, with optional paired values."""

    entries: tuple[tuple[str, ast.expr | None, int], ...]
    origin: str


@dataclass
class Scope:
    """Flat per-function view of local bindings.

    Bindings are collected for the whole function body rather than per block. That is a
    deliberate, bounded approximation: it lets a broker call inside ``for ... : try: ...``
    still see the client assigned at the top of the function, which is exactly FTGO's
    shape. Any name bound twice to different broker meanings is reported as a warning
    instead of being silently resolved.
    """

    values: dict[str, ValueType] = field(default_factory=dict)
    expressions: dict[str, ast.expr] = field(default_factory=dict)
    dicts: dict[str, tuple[tuple[str, ast.expr], ...]] = field(default_factory=dict)
    sequences: dict[str, tuple[str, ...]] = field(default_factory=dict)
    iterations: dict[str, IterationBinding] = field(default_factory=dict)
    parameters: frozenset[str] = frozenset()


class BrokerTyper:
    """Infers whether an expression evaluates to a broker object, within bounded hops."""

    def __init__(self, index: SourceIndex) -> None:
        self.index = index

    def annotation_type(
        self, service: str, module: str, annotation: ast.expr | None, hops: int
    ) -> ValueType:
        """Read a return annotation as evidence of what a call produces."""
        if annotation is None or hops > _MAX_VALUE_HOPS:
            return UNKNOWN_VALUE
        literal = _constant_string(annotation)
        if literal is not None:
            # A forward reference such as ``-> 'RPCBroker'``.
            resolved = self.index.resolve_symbol(service, module, literal)
        else:
            dotted = _dotted_expression(annotation)
            if dotted is None:
                return UNKNOWN_VALUE
            resolved = self.index.resolve_dotted(service, module, dotted)
        if resolved.kind == SYMBOL_BROKER:
            return ValueType(VALUE_BROKER, resolved.module, resolved.name, resolved.library)
        if resolved.kind == SYMBOL_CLASS:
            return ValueType(VALUE_LOCAL_INSTANCE, resolved.module, resolved.name)
        return UNKNOWN_VALUE

    def value_type(
        self,
        service: str,
        module: str,
        node: ast.expr | None,
        scope: Scope,
        *,
        hops: int = 0,
    ) -> ValueType:
        """Best-effort static type of ``node``, limited to broker-relevant conclusions."""
        if node is None or hops > _MAX_VALUE_HOPS:
            return UNKNOWN_VALUE
        node = _unwrap(node)

        if isinstance(node, ast.Name):
            known = scope.values.get(node.id)
            if known is not None:
                return known
            resolved = self.index.resolve_symbol(service, module, node.id)
            if resolved.kind == SYMBOL_BROKER:
                return ValueType(VALUE_BROKER, resolved.module, resolved.name, resolved.library)
            if resolved.kind == SYMBOL_CLASS:
                return ValueType(VALUE_LOCAL_INSTANCE, resolved.module, resolved.name)
            return UNKNOWN_VALUE

        if isinstance(node, ast.Attribute):
            receiver = self.value_type(service, module, node.value, scope, hops=hops + 1)
            if receiver.is_broker:
                return receiver
            dotted = _dotted_expression(node)
            if dotted is not None:
                resolved = self.index.resolve_dotted(service, module, dotted)
                if resolved.kind == SYMBOL_BROKER:
                    return ValueType(
                        VALUE_BROKER, resolved.module, resolved.name, resolved.library
                    )
                if resolved.kind == SYMBOL_CLASS:
                    return ValueType(VALUE_LOCAL_INSTANCE, resolved.module, resolved.name)
            return UNKNOWN_VALUE

        if isinstance(node, ast.Call):
            return self._call_type(service, module, node, scope, hops)

        return UNKNOWN_VALUE

    def _call_type(
        self, service: str, module: str, node: ast.Call, scope: Scope, hops: int
    ) -> ValueType:
        function = _unwrap(node.func)

        if isinstance(function, ast.Attribute):
            receiver = self.value_type(service, module, function.value, scope, hops=hops + 1)
            if receiver.is_broker:
                # ``RPCClient.create(...)`` / ``connection.channel()`` stay broker objects;
                # anything else returns something this pass cannot vouch for.
                if function.attr in BROKER_FACTORY_MEMBERS:
                    return receiver
                return UNKNOWN_VALUE
            if (
                receiver.kind == VALUE_LOCAL_INSTANCE
                and receiver.module is not None
                and receiver.class_name is not None
            ):
                found = self.index.lookup_method(
                    service, receiver.module, receiver.class_name, function.attr
                )
                if found is not None:
                    owner_module, method = found
                    return self.annotation_type(service, owner_module, method.returns, hops + 1)
            return UNKNOWN_VALUE

        if isinstance(function, ast.Name):
            resolved = self.index.resolve_symbol(service, module, function.id)
            if resolved.kind == SYMBOL_BROKER:
                return ValueType(VALUE_BROKER, resolved.module, resolved.name, resolved.library)
            if (
                resolved.kind == SYMBOL_CLASS
                and resolved.module is not None
                and resolved.name is not None
            ):
                return ValueType(VALUE_LOCAL_INSTANCE, resolved.module, resolved.name)
            if (
                resolved.kind == SYMBOL_FUNCTION
                and resolved.module is not None
                and resolved.name is not None
            ):
                target = self.index.facts(service, resolved.module)
                if target is not None:
                    declaration = target.functions.get(resolved.name)
                    if declaration is not None:
                        return self.annotation_type(
                            service, resolved.module, declaration.returns, hops + 1
                        )
        return UNKNOWN_VALUE


# ---------------------------------------------------------------------------------------
# Identity resolution
# ---------------------------------------------------------------------------------------

IDENTITY_LITERAL = "literal"
IDENTITY_LOCAL_VARIABLE = "local_variable"
IDENTITY_MODULE_CONSTANT = "module_constant"
IDENTITY_IMPORTED_CONSTANT = "imported_constant"
IDENTITY_ENUM_MEMBER = "enum_member"
IDENTITY_CLASS_CONSTANT = "class_constant"
IDENTITY_CONCATENATION = "concatenation"
IDENTITY_ITERATION = "iteration"


@dataclass(frozen=True, slots=True)
class ResolvedIdentity:
    """One statically resolved broker identity string."""

    value: str
    source_kind: str
    paired: ast.expr | None = None
    declared_lineno: int | None = None


@dataclass(frozen=True, slots=True)
class IdentityResolution:
    """Either one-or-more resolved identities, or a reason none could be proven."""

    identities: tuple[ResolvedIdentity, ...] = ()
    reason: str | None = None

    @property
    def resolved(self) -> bool:
        return bool(self.identities)


class IdentityResolver:
    """Resolves broker identifiers through statically knowable string sources only.

    Accepted: string literals, module-level string constants, Enum/class string members,
    constants imported from scanned source, deterministic concatenation of those, and loop
    variables bound to a literal dict or sequence. Everything else, including
    ``env_var(...)`` and f-strings with substitutions, is reported unresolved.
    """

    def __init__(self, index: SourceIndex) -> None:
        self.index = index

    def resolve(
        self,
        service: str,
        module: str,
        node: ast.expr | None,
        scope: Scope,
        *,
        _depth: int = 0,
    ) -> IdentityResolution:
        if node is None:
            return IdentityResolution(reason="no identity argument was supplied")
        if _depth > _MAX_RESOLUTION_DEPTH:
            return IdentityResolution(reason="identity resolution depth exceeded")

        literal = _constant_string(node)
        if literal is not None:
            return IdentityResolution((ResolvedIdentity(literal, IDENTITY_LITERAL),))

        if isinstance(node, ast.Name):
            return self._resolve_name(service, module, node, scope, _depth)

        if isinstance(node, ast.Attribute):
            return self._resolve_attribute(service, module, node, _depth)

        if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
            return self._resolve_concatenation(service, module, node, scope, _depth)

        if isinstance(node, ast.JoinedStr):
            parts: list[str] = []
            for value in node.values:
                text = _constant_string(value)
                if text is None:
                    return IdentityResolution(
                        reason="f-string interpolates a runtime value"
                    )
                parts.append(text)
            return IdentityResolution(
                (ResolvedIdentity("".join(parts), IDENTITY_LITERAL),)
            )

        if isinstance(node, ast.Call):
            return IdentityResolution(
                reason="identity is computed by a call and cannot be resolved statically"
            )

        return IdentityResolution(reason="identity expression is not a static string")

    def _resolve_name(
        self, service: str, module: str, node: ast.Name, scope: Scope, depth: int
    ) -> IdentityResolution:
        iteration = scope.iterations.get(node.id)
        if iteration is not None:
            return IdentityResolution(
                tuple(
                    ResolvedIdentity(value, IDENTITY_ITERATION, paired, lineno)
                    for value, paired, lineno in iteration.entries
                )
            )
        if node.id in scope.parameters:
            return IdentityResolution(
                reason=(
                    f"identity comes from parameter {node.id!r}, which is only known at "
                    f"the call site"
                )
            )
        local = scope.expressions.get(node.id)
        if local is not None:
            nested = self.resolve(service, module, local, scope, _depth=depth + 1)
            if nested.resolved:
                return IdentityResolution(
                    tuple(
                        ResolvedIdentity(item.value, IDENTITY_LOCAL_VARIABLE, item.paired)
                        for item in nested.identities
                    )
                )
            return nested
        facts = self.index.facts(service, module)
        if facts is not None and node.id in facts.constants:
            nested = self.resolve(
                service, module, facts.constants[node.id], Scope(), _depth=depth + 1
            )
            if nested.resolved:
                return IdentityResolution(
                    tuple(
                        ResolvedIdentity(item.value, IDENTITY_MODULE_CONSTANT)
                        for item in nested.identities
                    )
                )
            return nested
        resolved = self.index.resolve_symbol(service, module, node.id)
        if (
            resolved.kind == SYMBOL_CONSTANT
            and resolved.module is not None
            and resolved.name is not None
        ):
            target = self.index.facts(service, resolved.module)
            if target is not None:
                nested = self.resolve(
                    service,
                    resolved.module,
                    target.constants[resolved.name],
                    Scope(),
                    _depth=depth + 1,
                )
                if nested.resolved:
                    return IdentityResolution(
                        tuple(
                            ResolvedIdentity(item.value, IDENTITY_IMPORTED_CONSTANT)
                            for item in nested.identities
                        )
                    )
                return nested
        return IdentityResolution(
            reason=f"name {node.id!r} could not be traced to a static string"
        )

    def _resolve_attribute(
        self, service: str, module: str, node: ast.Attribute, depth: int
    ) -> IdentityResolution:
        del depth
        dotted = _dotted_expression(node)
        if dotted is None:
            return IdentityResolution(reason="attribute chain is not a dotted name")
        parts = dotted.split(".")
        # ``EventNames.ORDER_CREATE.value`` and ``EventNames.ORDER_CREATE`` are equivalent
        # for a string Enum, so a trailing ``.value`` is peeled off.
        if len(parts) >= 3 and parts[-1] == "value":
            parts = parts[:-1]
        if len(parts) < 2:
            return IdentityResolution(reason="attribute chain has no owner")
        owner_dotted, attribute = ".".join(parts[:-1]), parts[-1]
        resolved = self.index.resolve_dotted(service, module, owner_dotted)
        if (
            resolved.kind != SYMBOL_CLASS
            or resolved.module is None
            or resolved.name is None
        ):
            return IdentityResolution(
                reason=f"{owner_dotted!r} is not a class defined in scanned source"
            )
        value = self.index.lookup_attribute_string(
            service, resolved.module, resolved.name, attribute
        )
        if value is None:
            return IdentityResolution(
                reason=f"{dotted!r} is not a statically declared string member"
            )
        kind = (
            IDENTITY_ENUM_MEMBER
            if self.index.is_enum_class(service, resolved.module, resolved.name)
            else IDENTITY_CLASS_CONSTANT
        )
        return IdentityResolution((ResolvedIdentity(value, kind),))

    def _resolve_concatenation(
        self, service: str, module: str, node: ast.BinOp, scope: Scope, depth: int
    ) -> IdentityResolution:
        parts: list[ast.expr] = []
        stack: list[ast.expr] = [node]
        while stack:
            if len(parts) > _MAX_CONCAT_PARTS:
                return IdentityResolution(reason="concatenation has too many operands")
            current = stack.pop()
            if isinstance(current, ast.BinOp) and isinstance(current.op, ast.Add):
                stack.extend((current.right, current.left))
            else:
                parts.append(current)
        pieces: list[str] = []
        for part in parts:
            nested = self.resolve(service, module, part, scope, _depth=depth + 1)
            if len(nested.identities) != 1:
                return IdentityResolution(
                    reason=nested.reason or "concatenation operand is not a single string"
                )
            pieces.append(nested.identities[0].value)
        return IdentityResolution(
            (ResolvedIdentity("".join(pieces), IDENTITY_CONCATENATION),)
        )


# ---------------------------------------------------------------------------------------
# Candidate model
# ---------------------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class ServiceScan:
    """One existing application service and what this pass found inside it."""

    slug: str
    entity_id: str
    python_files: int
    publisher_calls: int
    consumer_bindings: int

    def summary(self) -> dict[str, Any]:
        return {
            "service": self.entity_id,
            "slug": self.slug,
            "python_files": self.python_files,
            "publisher_calls": self.publisher_calls,
            "consumer_bindings": self.consumer_bindings,
        }


@dataclass(frozen=True, slots=True)
class BrokerWrapper:
    """A local function that forwards one of its parameters to a real broker operation."""

    service: str
    module: str
    qualified_name: str
    direction: str
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

    def summary(self) -> dict[str, Any]:
        return {
            "service": self.service,
            "symbol": self.symbol,
            "direction": self.direction,
            "operation": self.operation,
            "broker_library": self.library,
            "identity_parameter": self.parameter_name,
            "identity_parameter_index": self.parameter_index,
            "hops_to_broker": self.hops,
            "path": self.relative_path,
            "line": self.lineno,
        }


@dataclass(frozen=True, slots=True)
class BrokerInteraction:
    """One proven publisher call or consumer binding at one source site."""

    service: str
    role: str
    identity: str
    identity_source: str
    operation: str
    library: str
    mechanism: str
    exchange: str | None
    queue: str | None
    routing_key: str | None
    handler: str | None
    via_wrapper: str | None
    hops: int
    call_expression: str | None
    provenance: Provenance

    @property
    def site(self) -> str:
        return f"{self.provenance.source_path}:{self.provenance.line_start}"

    def summary(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "service": self.service,
            "role": self.role,
            "identity": self.identity,
            "identity_source": self.identity_source,
            "operation": self.operation,
            "broker_library": self.library,
            "mechanism": self.mechanism,
            "hops_to_broker": self.hops,
        }
        for key, value in (
            ("exchange", self.exchange),
            ("queue", self.queue),
            ("routing_key", self.routing_key),
            ("handler", self.handler),
            ("via_wrapper", self.via_wrapper),
            ("call", self.call_expression),
        ):
            if value:
                payload[key] = value
        payload["source"] = self.provenance.as_dict()
        return payload


@dataclass(frozen=True, slots=True)
class EventCandidate:
    """A logical broker interaction that publishers and consumers share."""

    id: str
    kind: str
    title: str
    identity: str
    status: str
    publishers: tuple[str, ...]
    consumers: tuple[str, ...]
    attributes: dict[str, Any]
    provenance: Provenance

    def summary(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "kind": self.kind,
            "identity": self.identity,
            "status": self.status,
            "publishers": list(self.publishers),
            "consumers": list(self.consumers),
            "attributes": self.attributes,
            "source": self.provenance.as_dict(),
        }


@dataclass(frozen=True, slots=True)
class RelationshipCandidate:
    source: str
    type: str
    target: str
    role: str
    provenance: Provenance
    detail: dict[str, Any] = field(default_factory=dict)

    def summary(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "source": self.source,
            "type": self.type,
            "target": self.target,
            "role": self.role,
        }
        payload.update(self.detail)
        payload["source_evidence"] = self.provenance.as_dict()
        return payload


@dataclass(frozen=True, slots=True)
class UnresolvedIdentifier:
    """A proven broker operation whose logical identity is not statically knowable."""

    service: str
    role: str
    operation: str
    library: str
    reason: str
    expression: str | None
    provenance: Provenance

    def summary(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "service": self.service,
            "role": self.role,
            "operation": self.operation,
            "broker_library": self.library,
            "reason": self.reason,
        }
        if self.expression:
            payload["expression"] = self.expression
        payload["source_evidence"] = self.provenance.as_dict()
        return payload


@dataclass(frozen=True, slots=True)
class IdentityCollision:
    """Two different raw identities that would collapse to one Event id."""

    event_id: str
    raw_identities: tuple[str, ...]
    sites: tuple[str, ...]

    def summary(self) -> dict[str, Any]:
        return {
            "event_id": self.event_id,
            "raw_identities": list(self.raw_identities),
            "sites": list(self.sites),
            "reason": (
                "distinct broker identities normalize to the same Event id; no Event entity "
                "or relationship was created and human review is required"
            ),
        }


@dataclass(frozen=True, slots=True)
class RabbitExtraction:
    repository: str
    commit: str
    owner: str | None
    source_files: tuple[str, ...]
    skipped_files: tuple[str, ...]
    services_scanned: tuple[ServiceScan, ...]
    broker_libraries: tuple[str, ...]
    wrappers: tuple[BrokerWrapper, ...]
    publisher_calls: tuple[BrokerInteraction, ...]
    consumer_bindings: tuple[BrokerInteraction, ...]
    events: tuple[EventCandidate, ...]
    relationships: tuple[RelationshipCandidate, ...]
    identity_collisions: tuple[IdentityCollision, ...]
    unresolved_identifiers: tuple[UnresolvedIdentifier, ...]
    warnings: tuple[str, ...]
    withheld_values: frozenset[str]

    def inbound_relations_for(self, entity_id: str) -> tuple[RelationshipCandidate, ...]:
        return tuple(item for item in self.relationships if item.target == entity_id)

    def events_by_status(self, status: str) -> tuple[EventCandidate, ...]:
        return tuple(item for item in self.events if item.status == status)


# ---------------------------------------------------------------------------------------
# Scope construction
# ---------------------------------------------------------------------------------------


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


def _string_dict_entries(node: ast.expr) -> tuple[tuple[str, ast.expr], ...] | None:
    """Read ``{"a": handler_a, "b": handler_b}`` with every key a string literal."""
    if not isinstance(node, ast.Dict):
        return None
    entries: list[tuple[str, ast.expr]] = []
    for key, value in zip(node.keys, node.values, strict=False):
        literal = _constant_string(key)
        if literal is None or value is None:
            return None
        entries.append((literal, value))
    return tuple(entries) if entries else None


def _string_sequence(node: ast.expr) -> tuple[str, ...] | None:
    """Read ``["a", "b"]`` with every element a string literal."""
    if not isinstance(node, ast.List | ast.Tuple | ast.Set):
        return None
    values = [_constant_string(element) for element in node.elts]
    if not values or any(value is None for value in values):
        return None
    return tuple(value for value in values if value is not None)


def _loop_bindings(scope: Scope, node: ast.For | ast.AsyncFor) -> dict[str, IterationBinding]:
    """Bind loop targets to statically known strings when the iterable is a literal.

    This is what makes FTGO's consumer registration provable: every microservice declares a
    literal ``{event: handler}`` map and registers it in a ``for ... .items()`` loop, so the
    keys are static even though the ``register_event`` call sees only a loop variable.
    """
    iterable = node.iter
    target = node.target
    bindings: dict[str, IterationBinding] = {}

    entries: tuple[tuple[str, ast.expr], ...] | None = None
    keys_only: tuple[str, ...] | None = None
    origin = ""

    if isinstance(iterable, ast.Call) and isinstance(iterable.func, ast.Attribute):
        owner = iterable.func.value
        member = iterable.func.attr
        if isinstance(owner, ast.Name) and owner.id in scope.dicts:
            if member == "items":
                entries = scope.dicts[owner.id]
                origin = f"{owner.id}.items()"
            elif member == "keys":
                keys_only = tuple(key for key, _ in scope.dicts[owner.id])
                origin = f"{owner.id}.keys()"
    elif isinstance(iterable, ast.Name):
        if iterable.id in scope.dicts:
            keys_only = tuple(key for key, _ in scope.dicts[iterable.id])
            origin = iterable.id
        elif iterable.id in scope.sequences:
            keys_only = scope.sequences[iterable.id]
            origin = iterable.id
    else:
        literal_sequence = _string_sequence(iterable)
        if literal_sequence is not None:
            keys_only = literal_sequence
            origin = "literal sequence"

    if entries is not None and isinstance(target, ast.Tuple) and len(target.elts) == 2:
        key_target, value_target = target.elts
        if isinstance(key_target, ast.Name):
            bindings[key_target.id] = IterationBinding(
                tuple(
                    (key, value, getattr(value, "lineno", node.lineno))
                    for key, value in entries
                ),
                origin,
            )
        if isinstance(value_target, ast.Name):
            # The paired handler is not an identity, but recording the binding prevents it
            # from being mistaken for an unrelated free name later.
            bindings.setdefault(
                f"__paired__{value_target.id}", IterationBinding((), origin)
            )
    elif keys_only is not None and isinstance(target, ast.Name):
        bindings[target.id] = IterationBinding(
            tuple((key, None, node.lineno) for key in keys_only), origin
        )

    return bindings


def build_scope(
    typer: BrokerTyper,
    facts: ModuleFacts,
    root: ast.AST,
    *,
    parameters: tuple[str, ...] = (),
    warnings: list[str] | None = None,
) -> Scope:
    """Collect the local bindings a broker call in ``root`` can see."""
    scope = Scope(parameters=frozenset(parameters))
    nodes = _scope_nodes(root)

    assignments: list[tuple[int, str, ast.expr]] = []
    for node in nodes:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    assignments.append((node.lineno, target.id, node.value))
        elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            if node.value is not None:
                assignments.append((node.lineno, node.target.id, node.value))
    assignments.sort(key=lambda item: (item[0], item[1]))

    for lineno, name, value in assignments:
        entries = _string_dict_entries(value)
        if entries is not None:
            scope.dicts[name] = entries
        sequence = _string_sequence(value)
        if sequence is not None:
            scope.sequences[name] = sequence
        if name in scope.expressions and warnings is not None:
            warnings.append(
                f"{facts.relative_path}:{lineno}: {name!r} is rebound; broker resolution "
                f"uses the first binding in source order"
            )
        else:
            scope.expressions[name] = value
        inferred = typer.value_type(facts.service, facts.module, value, scope)
        if inferred.kind != VALUE_UNKNOWN:
            scope.values.setdefault(name, inferred)

    for node in nodes:
        if isinstance(node, ast.For | ast.AsyncFor):
            for name, binding in _loop_bindings(scope, node).items():
                scope.iterations.setdefault(name, binding)

    return scope


# ---------------------------------------------------------------------------------------
# Broker call classification
# ---------------------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class BrokerCallInfo:
    """A call proven to reach a broker operation, plus where its identity comes from."""

    direction: str
    role: str
    operation: str
    library: str
    identity_node: ast.expr | None
    exchange_node: ast.expr | None
    queue_node: ast.expr | None
    routing_node: ast.expr | None
    handler_node: ast.expr | None
    via_wrapper: str | None
    hops: int


def _identity_argument(call: ast.Call) -> ast.expr | None:
    """Pick the argument carrying the logical identity: a known keyword, else argument 0."""
    keyed = _first_keyword(call, IDENTITY_KEYWORDS)
    if keyed is not None:
        return keyed[1]
    return call.args[0] if call.args else None


def _direction_for(operation: str) -> tuple[str, str] | None:
    if operation in PUBLISH_OPERATIONS:
        return PUBLISHES, PUBLISHER_ROLE
    if operation in CONSUME_OPERATIONS:
        return CONSUMES, CONSUMER_ROLE
    return None


def _mechanism_for(operation: str) -> str:
    return MECHANISM_RPC if operation in RPC_OPERATIONS else MECHANISM_MESSAGE


def _wrapper_argument(call: ast.Call, wrapper: BrokerWrapper) -> ast.expr | None:
    """Find the argument a wrapper forwards as the broker identity."""
    node = _keyword_node(call, wrapper.parameter_name)
    if node is not None:
        return node
    if wrapper.parameter_index < len(call.args):
        return call.args[wrapper.parameter_index]
    return None


class CallClassifier:
    """Decides whether a call reaches a broker operation, directly or through a wrapper."""

    def __init__(self, index: SourceIndex, typer: BrokerTyper) -> None:
        self.index = index
        self.typer = typer

    def resolve_callee(
        self, facts: ModuleFacts, node: ast.Call, scope: Scope, owner_class: str | None
    ) -> tuple[str, str] | None:
        """Resolve a call target to ``(module, qualified name)`` in scanned source."""
        function = _unwrap(node.func)
        service, module = facts.service, facts.module

        if isinstance(function, ast.Name):
            resolved = self.index.resolve_symbol(service, module, function.id)
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
        # ``cls.method(...)`` / ``self.method(...)`` inside a class body.
        if isinstance(receiver, ast.Name) and receiver.id in ("cls", "self"):
            if owner_class is None:
                return None
            found = self.index.lookup_method(service, module, owner_class, function.attr)
            return None if found is None else (found[0], found[1].qualified_name)

        inferred = self.typer.value_type(service, module, receiver, scope)
        if (
            inferred.kind == VALUE_LOCAL_INSTANCE
            and inferred.module is not None
            and inferred.class_name is not None
        ):
            found = self.index.lookup_method(
                service, inferred.module, inferred.class_name, function.attr
            )
            return None if found is None else (found[0], found[1].qualified_name)

        dotted = _dotted_expression(receiver)
        if dotted is not None:
            resolved = self.index.resolve_dotted(service, module, dotted)
            if (
                resolved.kind == SYMBOL_CLASS
                and resolved.module is not None
                and resolved.name is not None
            ):
                found = self.index.lookup_method(
                    service, resolved.module, resolved.name, function.attr
                )
                return None if found is None else (found[0], found[1].qualified_name)
        return None

    def classify(
        self,
        facts: ModuleFacts,
        node: ast.Call,
        scope: Scope,
        owner_class: str | None,
        wrappers: dict[tuple[str, str, str], BrokerWrapper],
    ) -> BrokerCallInfo | None:
        """Return broker call information, or None when the call is not broker-rooted."""
        function = _unwrap(node.func)

        # --- direct: the receiver itself is a proven broker object ---------------------
        if isinstance(function, ast.Attribute):
            operation = function.attr
            direction = _direction_for(operation)
            if direction is not None:
                receiver = self.typer.value_type(
                    facts.service, facts.module, function.value, scope
                )
                if receiver.is_broker:
                    exchange = _first_keyword(node, EXCHANGE_KEYWORDS)
                    queue = _first_keyword(node, QUEUE_KEYWORDS)
                    routing = _first_keyword(node, ROUTING_KEY_KEYWORDS)
                    handler = _first_keyword(node, HANDLER_KEYWORDS)
                    return BrokerCallInfo(
                        direction=direction[0],
                        role=direction[1],
                        operation=operation,
                        library=receiver.library or BROKER_LIBRARIES[0],
                        identity_node=_identity_argument(node),
                        exchange_node=exchange[1] if exchange else None,
                        queue_node=queue[1] if queue else None,
                        routing_node=routing[1] if routing else None,
                        handler_node=handler[1] if handler else None,
                        via_wrapper=None,
                        hops=0,
                    )

        # --- indirect: the call target is a known local wrapper ------------------------
        callee = self.resolve_callee(facts, node, scope, owner_class)
        if callee is None:
            return None
        wrapper = wrappers.get((facts.service, callee[0], callee[1]))
        if wrapper is None:
            return None
        return BrokerCallInfo(
            direction=wrapper.direction,
            role=PUBLISHER_ROLE if wrapper.direction == PUBLISHES else CONSUMER_ROLE,
            operation=wrapper.operation,
            library=wrapper.library,
            identity_node=_wrapper_argument(node, wrapper),
            exchange_node=None,
            queue_node=None,
            routing_node=None,
            handler_node=None,
            via_wrapper=(
                f"{wrapper.module}.{wrapper.qualified_name}"
                if wrapper.module
                else wrapper.qualified_name
            ),
            hops=wrapper.hops,
        )


# ---------------------------------------------------------------------------------------
# Source discovery
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
            # Only Python skips are reported; other file types are simply not this pass.
            skipped.append(f"{relative_path}: {reason}")
    return tuple(sorted(in_scope)), skipped


@dataclass(frozen=True, slots=True)
class CodeUnit:
    """One scope in which a broker call can appear: a function/method, or module level."""

    facts: ModuleFacts
    root: ast.AST
    symbol: str
    owner_class: str | None
    parameters: tuple[str, ...]
    wrapper_name: str | None


def _code_units(facts: ModuleFacts) -> list[CodeUnit]:
    """Enumerate the scopes of one module in deterministic order."""
    units: list[CodeUnit] = [
        CodeUnit(
            facts=facts,
            root=facts.tree,
            symbol=facts.module or "<module>",
            owner_class=None,
            parameters=(),
            wrapper_name=None,
        )
    ]
    for name in sorted(facts.functions):
        declaration = facts.functions[name]
        units.append(
            CodeUnit(
                facts=facts,
                root=declaration.node,
                symbol=facts.qualified(declaration.qualified_name),
                owner_class=None,
                parameters=declaration.parameters,
                wrapper_name=declaration.qualified_name,
            )
        )
    for class_name in sorted(facts.classes):
        declaration = facts.classes[class_name]
        for method_name in sorted(declaration.methods):
            method = declaration.methods[method_name]
            units.append(
                CodeUnit(
                    facts=facts,
                    root=method.node,
                    symbol=facts.qualified(method.qualified_name),
                    owner_class=class_name,
                    parameters=method.parameters,
                    wrapper_name=method.qualified_name,
                )
            )
    return units


def _calls_in(root: ast.AST) -> list[ast.Call]:
    """Calls in one scope, ordered by position so output never depends on walk order."""
    calls = [node for node in _scope_nodes(root) if isinstance(node, ast.Call)]
    calls.sort(key=lambda node: (node.lineno, node.col_offset))
    return calls


# ---------------------------------------------------------------------------------------
# Wrapper discovery
# ---------------------------------------------------------------------------------------


def discover_wrappers(
    index: SourceIndex,
    modules: list[ModuleFacts],
    typer: BrokerTyper,
    classifier: CallClassifier,
    warnings: list[str],
) -> dict[tuple[str, str, str], BrokerWrapper]:
    """Find local functions that forward a parameter to a proven broker operation.

    Discovery runs in rounds: round one finds functions that call the broker library
    directly, round two finds functions that call a round-one wrapper. The number of rounds
    is capped by ``_MAX_WRAPPER_HOPS`` so the trace can never run away.
    """
    wrappers: dict[tuple[str, str, str], BrokerWrapper] = {}
    for hop in range(1, _MAX_WRAPPER_HOPS + 1):
        discovered: list[BrokerWrapper] = []
        for facts in sorted(modules, key=lambda item: (item.service, item.relative_path)):
            for unit in _code_units(facts):
                if unit.wrapper_name is None or not unit.parameters:
                    continue
                key = (facts.service, facts.module, unit.wrapper_name)
                if key in wrappers:
                    continue
                scope = build_scope(typer, facts, unit.root, parameters=unit.parameters)
                for call in _calls_in(unit.root):
                    info = classifier.classify(facts, call, scope, unit.owner_class, wrappers)
                    if info is None or info.hops != hop - 1:
                        continue
                    node = info.identity_node
                    if not isinstance(node, ast.Name) or node.id not in unit.parameters:
                        continue
                    discovered.append(
                        BrokerWrapper(
                            service=facts.service,
                            module=facts.module,
                            qualified_name=unit.wrapper_name,
                            direction=info.direction,
                            operation=info.operation,
                            library=info.library,
                            parameter_index=unit.parameters.index(node.id),
                            parameter_name=node.id,
                            hops=hop,
                            relative_path=facts.relative_path,
                            lineno=call.lineno,
                        )
                    )
                    break
        if not discovered:
            break
        for wrapper in sorted(discovered, key=lambda item: item.key):
            existing = wrappers.get(wrapper.key)
            if existing is None:
                wrappers[wrapper.key] = wrapper
            elif existing.direction != wrapper.direction:
                warnings.append(
                    f"{wrapper.relative_path}:{wrapper.lineno}: {wrapper.qualified_name!r} "
                    f"forwards to both a publish and a consume operation; kept "
                    f"{existing.direction}"
                )
    return wrappers


# ---------------------------------------------------------------------------------------
# Interaction extraction
# ---------------------------------------------------------------------------------------


def _compose_identity(
    exchange: str | None, queue: str | None, routing_key: str | None, primary: str
) -> str:
    """Build the canonical identity from the strongest resolved broker coordinates.

    The preferred tuple is ``(exchange, queue, routing_key, operation identifier)``; only
    statically resolved parts take part, and a part already present is not repeated.
    """
    ordered = [part for part in (exchange, queue, routing_key, primary) if part]
    unique: list[str] = []
    for part in ordered:
        if part not in unique:
            unique.append(part)
    return ".".join(unique) if unique else primary


def _resolve_single(
    resolver: IdentityResolver, facts: ModuleFacts, node: ast.expr | None, scope: Scope
) -> str | None:
    if node is None:
        return None
    resolution = resolver.resolve(facts.service, facts.module, node, scope)
    if len(resolution.identities) == 1:
        return resolution.identities[0].value
    return None


def extract_interactions(
    index: SourceIndex,
    modules: list[ModuleFacts],
    typer: BrokerTyper,
    classifier: CallClassifier,
    resolver: IdentityResolver,
    wrappers: dict[tuple[str, str, str], BrokerWrapper],
    repository: str,
    commit: str,
    warnings: list[str],
) -> tuple[list[BrokerInteraction], list[UnresolvedIdentifier]]:
    """Walk every scope and record each proven broker interaction, or why it is unresolved."""
    del warnings
    interactions: list[BrokerInteraction] = []
    unresolved: list[UnresolvedIdentifier] = []

    for facts in sorted(modules, key=lambda item: item.relative_path):
        for unit in _code_units(facts):
            scope = build_scope(typer, facts, unit.root, parameters=unit.parameters)
            wrapper_here = (
                wrappers.get((facts.service, facts.module, unit.wrapper_name))
                if unit.wrapper_name
                else None
            )
            for call in _calls_in(unit.root):
                info = classifier.classify(facts, call, scope, unit.owner_class, wrappers)
                if info is None:
                    continue
                identity_node = info.identity_node
                # A wrapper's own forwarding call is bookkeeping, not an interaction: its
                # identity belongs to the caller and is recorded at each call site instead.
                if (
                    wrapper_here is not None
                    and isinstance(identity_node, ast.Name)
                    and identity_node.id in unit.parameters
                ):
                    continue

                provenance = Provenance(
                    repository=repository,
                    commit=commit,
                    source_path=facts.relative_path,
                    symbol=unit.symbol,
                    line_start=call.lineno,
                    line_end=call.end_lineno or call.lineno,
                    evidence_type=EVIDENCE_TYPE,
                )
                resolution = resolver.resolve(
                    facts.service, facts.module, identity_node, scope
                )
                if not resolution.resolved:
                    unresolved.append(
                        UnresolvedIdentifier(
                            service=facts.service,
                            role=info.role,
                            operation=info.operation,
                            library=info.library,
                            reason=resolution.reason or "identity could not be resolved",
                            expression=_expression_text(facts.source, identity_node),
                            provenance=provenance,
                        )
                    )
                    continue

                exchange = _resolve_single(resolver, facts, info.exchange_node, scope)
                queue = _resolve_single(resolver, facts, info.queue_node, scope)
                routing_key = _resolve_single(resolver, facts, info.routing_node, scope)
                declared_handler = _expression_text(facts.source, info.handler_node)
                call_expression = _expression_text(facts.source, call)

                for resolved in resolution.identities:
                    handler = (
                        _expression_text(facts.source, resolved.paired)
                        if resolved.paired is not None
                        else declared_handler
                    )
                    interactions.append(
                        BrokerInteraction(
                            service=facts.service,
                            role=info.role,
                            identity=_compose_identity(
                                exchange, queue, routing_key, resolved.value
                            ),
                            identity_source=resolved.source_kind,
                            operation=info.operation,
                            library=info.library,
                            mechanism=_mechanism_for(info.operation),
                            exchange=exchange,
                            queue=queue,
                            routing_key=routing_key,
                            handler=handler if info.role == CONSUMER_ROLE else None,
                            via_wrapper=info.via_wrapper,
                            hops=info.hops,
                            call_expression=call_expression,
                            provenance=provenance,
                        )
                    )
    return interactions, unresolved


# ---------------------------------------------------------------------------------------
# Event assembly and correlation
# ---------------------------------------------------------------------------------------


def _sorted_unique(values: list[str | None]) -> list[str]:
    return sorted({value for value in values if value})


def assemble_events(
    repository_slug: str,
    repository: str,
    commit: str,
    interactions: list[BrokerInteraction],
) -> tuple[list[EventCandidate], list[RelationshipCandidate], list[IdentityCollision]]:
    """Group interactions into Events, then correlate publishers with consumers.

    Correlation is exact: two sides meet only when their resolved identities normalize to
    the same Event id. That is what surfaces naming drift instead of hiding it.
    """
    buckets: dict[str, list[BrokerInteraction]] = {}
    for interaction in interactions:
        buckets.setdefault(event_id(repository_slug, interaction.identity), []).append(
            interaction
        )

    events: list[EventCandidate] = []
    relationships: list[RelationshipCandidate] = []
    collisions: list[IdentityCollision] = []

    for identifier in sorted(buckets):
        members = sorted(
            buckets[identifier],
            key=lambda item: (
                item.provenance.source_path,
                item.provenance.line_start or 0,
                item.role,
                item.identity,
            ),
        )
        raw_identities = sorted({item.identity for item in members})
        if len(raw_identities) > 1:
            collisions.append(
                IdentityCollision(
                    event_id=identifier,
                    raw_identities=tuple(raw_identities),
                    sites=tuple(sorted({item.site for item in members})),
                )
            )
            continue

        publishers = [item for item in members if item.role == PUBLISHER_ROLE]
        consumers = [item for item in members if item.role == CONSUMER_ROLE]
        publisher_services = sorted(
            {service_entity_id(repository_slug, item.service) for item in publishers}
        )
        consumer_services = sorted(
            {service_entity_id(repository_slug, item.service) for item in consumers}
        )
        if publisher_services and consumer_services:
            status = STATUS_MATCHED
        elif publisher_services:
            status = STATUS_PUBLISHER_ONLY
        else:
            status = STATUS_CONSUMER_ONLY

        # The declaration side is the more informative evidence anchor: a consumer binding
        # names the handler, while a publisher call only names the request.
        anchor_pool = consumers or publishers
        anchor = anchor_pool[0]

        attributes: dict[str, Any] = {
            "identity": raw_identities[0],
            "mechanism": _sorted_unique([item.mechanism for item in members]),
            "broker_libraries": _sorted_unique([item.library for item in members]),
            "operations": _sorted_unique([item.operation for item in members]),
            "identity_sources": _sorted_unique([item.identity_source for item in members]),
            "correlation": status,
            "publisher_call_sites": len(publishers),
            "consumer_binding_sites": len(consumers),
        }
        for key, values in (
            ("exchange", [item.exchange for item in members]),
            ("queue", [item.queue for item in members]),
            ("routing_key", [item.routing_key for item in members]),
            ("handlers", [item.handler for item in members]),
        ):
            resolved = _sorted_unique(values)
            if resolved:
                attributes[key] = resolved

        events.append(
            EventCandidate(
                id=identifier,
                kind=EVENT_KIND,
                title=raw_identities[0],
                identity=raw_identities[0],
                status=status,
                publishers=tuple(publisher_services),
                consumers=tuple(consumer_services),
                attributes=attributes,
                provenance=anchor.provenance,
            )
        )

        for role, relation_type, group in (
            (PUBLISHER_ROLE, PUBLISHES, publishers),
            (CONSUMER_ROLE, CONSUMES, consumers),
        ):
            by_service: dict[str, list[BrokerInteraction]] = {}
            for item in group:
                by_service.setdefault(item.service, []).append(item)
            for slug in sorted(by_service):
                sites = sorted(
                    by_service[slug],
                    key=lambda item: (
                        item.provenance.source_path,
                        item.provenance.line_start or 0,
                    ),
                )
                detail: dict[str, Any] = {
                    "operation": sites[0].operation,
                    "broker_library": sites[0].library,
                    "mechanism": sites[0].mechanism,
                    "call_sites": [item.site for item in sites],
                }
                if sites[0].via_wrapper:
                    detail["via_wrapper"] = sites[0].via_wrapper
                handlers = _sorted_unique([item.handler for item in sites])
                if handlers:
                    detail["handlers"] = handlers
                relationships.append(
                    RelationshipCandidate(
                        source=service_entity_id(repository_slug, slug),
                        type=relation_type,
                        target=identifier,
                        role=role,
                        provenance=sites[0].provenance,
                        detail=detail,
                    )
                )

    return events, relationships, collisions


# ---------------------------------------------------------------------------------------
# Extraction
# ---------------------------------------------------------------------------------------


def extract_rabbitmq(
    record: RepositoryRecord,
    commit: str,
    *,
    source_kind: str = SOURCE_KIND,
) -> RabbitExtraction:
    """Extract RabbitMQ/RPC publisher and consumer interactions with AST only.

    ``commit`` must already be verified against the manifest baseline by the caller. The
    inspected repository is only ever read: no module is imported, no code is executed, and
    no AMQP connection is opened.
    """
    del source_kind  # Source selection is fixed to the manifest 'code' kind for this pass.
    repository = record.id
    repository_slug = normalize_token(record.id)
    warnings: list[str] = []

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
        facts = analyze_module(
            text,
            tree,
            relative_path=relative_path,
            service=service,
            service_root=service_root,
            module=module_dotted_name(relative_path, service_root),
            is_package=relative_path.rsplit("/", 1)[-1] == "__init__.py",
            warnings=warnings,
        )
        modules.append(facts)
        withheld |= facts.withheld_values

    claimed: dict[tuple[str, str], str] = {}
    for facts in modules:
        key = (facts.service, facts.module)
        previous = claimed.get(key)
        if previous is None:
            claimed[key] = facts.relative_path
        else:
            warnings.append(
                f"{facts.relative_path}: resolves to the same module name "
                f"{facts.module or '<root>'!r} as {previous}; kept {previous} for import "
                f"resolution"
            )

    index = build_source_index(modules)
    typer = BrokerTyper(index)
    classifier = CallClassifier(index, typer)
    resolver = IdentityResolver(index)

    libraries: set[str] = set()
    for facts in modules:
        for imported in facts.imports.values():
            library = broker_library_of(imported.module)
            if library is not None:
                libraries.add(library)

    wrappers = discover_wrappers(index, modules, typer, classifier, warnings)
    interactions, unresolved = extract_interactions(
        index,
        modules,
        typer,
        classifier,
        resolver,
        wrappers,
        repository,
        commit,
        warnings,
    )
    events, relationships, collisions = assemble_events(
        repository_slug, repository, commit, interactions
    )

    publishers = [item for item in interactions if item.role == PUBLISHER_ROLE]
    consumers = [item for item in interactions if item.role == CONSUMER_ROLE]

    def interaction_sort_key(item: BrokerInteraction) -> tuple[Any, ...]:
        return (
            item.service,
            item.identity,
            item.provenance.source_path,
            item.provenance.line_start or 0,
        )

    services_scanned = tuple(
        ServiceScan(
            slug=slug,
            entity_id=service_entity_id(repository_slug, slug),
            python_files=files_per_service[slug],
            publisher_calls=sum(1 for item in publishers if item.service == slug),
            consumer_bindings=sum(1 for item in consumers if item.service == slug),
        )
        for slug in sorted(files_per_service)
    )
    for scan in services_scanned:
        if scan.publisher_calls == 0 and scan.consumer_bindings == 0:
            warnings.append(
                f"{scan.slug}: {scan.python_files} Python file(s) scanned and no broker-rooted "
                f"publish or consume operation found; no relationship was created for "
                f"{scan.entity_id}"
            )

    return RabbitExtraction(
        repository=repository,
        commit=commit,
        owner=record.owner,
        source_files=tuple(scanned),
        skipped_files=tuple(sorted(skipped)),
        services_scanned=services_scanned,
        broker_libraries=tuple(sorted(libraries)),
        wrappers=tuple(sorted(wrappers.values(), key=lambda item: item.key)),
        publisher_calls=tuple(sorted(publishers, key=interaction_sort_key)),
        consumer_bindings=tuple(sorted(consumers, key=interaction_sort_key)),
        events=tuple(sorted(events, key=lambda item: item.id)),
        relationships=tuple(
            sorted(relationships, key=lambda item: (item.source, item.type, item.target))
        ),
        identity_collisions=tuple(sorted(collisions, key=lambda item: item.event_id)),
        unresolved_identifiers=tuple(
            sorted(
                unresolved,
                key=lambda item: (
                    item.provenance.source_path,
                    item.provenance.line_start or 0,
                    item.role,
                    item.reason,
                ),
            )
        ),
        warnings=tuple(sorted(warnings)),
        withheld_values=frozenset(withheld),
    )


# ---------------------------------------------------------------------------------------
# Candidate rendering
# ---------------------------------------------------------------------------------------


def render_event_markdown(event: EventCandidate, extraction: RabbitExtraction) -> str:
    """Render one Event candidate page. Always candidate / pending, never approved."""
    inbound = extraction.inbound_relations_for(event.id)
    frontmatter: dict[str, Any] = {
        "id": event.id,
        "kind": event.kind,
        # The canonical loader requires kind and OKF type to agree.
        "type": event.kind,
        "title": event.title,
        "status": CANDIDATE_STATUS,
        "review_status": CANDIDATE_REVIEW_STATUS,
        "candidate_of": f"{EXTRACTOR_KIND}-extraction",
        "repository": extraction.repository,
        "commit": extraction.commit,
        "evidence_type": EVIDENCE_TYPE,
        "extractor": EXTRACTOR_KIND,
        "correlation": event.status,
        "publishers": list(event.publishers),
        "consumers": list(event.consumers),
    }
    if extraction.owner:
        frontmatter["owner"] = extraction.owner
    frontmatter["source_refs"] = [event.provenance.as_dict()]
    if inbound:
        frontmatter["inbound_relations"] = [
            {
                "type": relation.type,
                "source": relation.source,
                "role": relation.role,
                **relation.detail,
                **relation.provenance.as_dict(),
            }
            for relation in inbound
        ]
    frontmatter["attributes"] = event.attributes

    body = [
        f"# {event.title}",
        "",
        f"Candidate RabbitMQ/RPC interaction extracted from Python source in "
        f"`{extraction.repository}` at commit `{extraction.commit}`.",
        "",
        f"- Broker identity: `{event.identity}`",
        f"- Correlation: `{event.status}`",
        f"- Mechanism: `{', '.join(event.attributes.get('mechanism', []))}`",
        f"- Broker library: `{', '.join(event.attributes.get('broker_libraries', []))}`",
        f"- Declared in: `{event.provenance.source_path}` "
        f"(lines {event.provenance.line_start}-{event.provenance.line_end})",
        f"- Evidence class: `{EVIDENCE_TYPE}`",
        "",
    ]
    if event.publishers:
        body.extend(["## Publishers", ""])
        body.extend(f"- `{service}` `{PUBLISHES}` -> `{event.id}`" for service in event.publishers)
        body.append("")
    if event.consumers:
        body.extend(["## Consumers", ""])
        body.extend(f"- `{service}` `{CONSUMES}` -> `{event.id}`" for service in event.consumers)
        body.append("")
    if event.status == STATUS_PUBLISHER_ONLY:
        body.extend(
            [
                "## Unmatched interaction",
                "",
                "A publisher was proven but no consumer binding for this exact identity was "
                "found in scanned source. The consumer side is deliberately not invented.",
                "",
            ]
        )
    elif event.status == STATUS_CONSUMER_ONLY:
        body.extend(
            [
                "## Unmatched interaction",
                "",
                "A consumer binding was proven but no publisher call for this exact identity "
                "was found in scanned source. The publisher side is deliberately not "
                "invented.",
                "",
            ]
        )
    body.extend(
        [
            "## Review notes",
            "",
            "This page is a candidate awaiting review. Every publisher and consumer above is "
            "rooted in a call whose receiver traces statically to a broker library; nothing "
            "was inferred from a method or service name.",
            "",
        ]
    )

    rendered = yaml.safe_dump(
        frontmatter,
        sort_keys=False,
        default_flow_style=False,
        allow_unicode=True,
        width=100,
    ).rstrip("\n")
    return "\n".join(["---", rendered, "---", "", *body, ""])


def render_all(extraction: RabbitExtraction) -> dict[str, str]:
    """Render every candidate page keyed by output-relative POSIX path."""
    return {
        f"events/{event.id}.md": render_event_markdown(event, extraction)
        for event in extraction.events
    }


def build_service_relation_deltas(extraction: RabbitExtraction) -> dict[str, Any]:
    """Outgoing relations that human promotion must merge into canonical Service pages.

    No Service candidate page is written by this pass: those pages already exist and are
    owned by Pass 1. This sidecar is the reviewable delta, and it is not canonical
    knowledge.
    """
    by_service: dict[str, list[RelationshipCandidate]] = {}
    for relation in extraction.relationships:
        by_service.setdefault(relation.source, []).append(relation)

    return {
        "version": 1,
        "extractor": EXTRACTOR_KIND,
        "repository": extraction.repository,
        "commit": extraction.commit,
        "status": CANDIDATE_STATUS,
        "review_status": CANDIDATE_REVIEW_STATUS,
        "note": (
            "Candidate outgoing relations for existing canonical Service pages. This file is "
            "not canonical knowledge and must not be copied into wiki/ without review."
        ),
        "services": [
            {
                "service": service,
                "relation_count": len(by_service[service]),
                "relations": [
                    relation.summary()
                    for relation in sorted(
                        by_service[service], key=lambda item: (item.type, item.target)
                    )
                ],
            }
            for service in sorted(by_service)
        ],
    }


def build_report(extraction: RabbitExtraction, secret_values_emitted: int) -> dict[str, Any]:
    """Assemble extraction-report.json. Contains no timestamp, so runs stay comparable."""
    relationship_counts: dict[str, int] = {}
    for relation in extraction.relationships:
        relationship_counts[relation.type] = relationship_counts.get(relation.type, 0) + 1

    def event_brief(event: EventCandidate) -> dict[str, Any]:
        return {
            "event": event.id,
            "identity": event.identity,
            "publishers": list(event.publishers),
            "consumers": list(event.consumers),
        }

    matched = extraction.events_by_status(STATUS_MATCHED)
    publisher_only = extraction.events_by_status(STATUS_PUBLISHER_ONLY)
    consumer_only = extraction.events_by_status(STATUS_CONSUMER_ONLY)

    return {
        "version": 1,
        "extractor": EXTRACTOR_KIND,
        "repository": extraction.repository,
        "commit": extraction.commit,
        "commit_verified": True,
        "evidence_type": EVIDENCE_TYPE,
        "analysis": "python-ast",
        "modules_imported": 0,
        "modules_executed": 0,
        "broker_connections_opened": 0,
        "source_files": list(extraction.source_files),
        "skipped_files": list(extraction.skipped_files),
        "services_scanned": [scan.summary() for scan in extraction.services_scanned],
        "broker_libraries_detected": list(extraction.broker_libraries),
        "broker_wrappers": [wrapper.summary() for wrapper in extraction.wrappers],
        "counts": {
            "source_files": len(extraction.source_files),
            "skipped_files": len(extraction.skipped_files),
            "services_scanned": len(extraction.services_scanned),
            "broker_wrappers": len(extraction.wrappers),
            "publisher_calls": len(extraction.publisher_calls),
            "consumer_bindings": len(extraction.consumer_bindings),
            "events": len(extraction.events),
            "matched_interactions": len(matched),
            "publisher_only": len(publisher_only),
            "consumer_only": len(consumer_only),
            "relationships": len(extraction.relationships),
            "identity_collisions": len(extraction.identity_collisions),
            "unresolved_identifiers": len(extraction.unresolved_identifiers),
            "warnings": len(extraction.warnings),
            "relationships_by_type": dict(sorted(relationship_counts.items())),
        },
        "publisher_calls": [item.summary() for item in extraction.publisher_calls],
        "consumer_bindings": [item.summary() for item in extraction.consumer_bindings],
        "events": [event.summary() for event in extraction.events],
        "matched_interactions": [event_brief(event) for event in matched],
        "publisher_only": [event_brief(event) for event in publisher_only],
        "consumer_only": [event_brief(event) for event in consumer_only],
        "relationships": [relation.summary() for relation in extraction.relationships],
        "identity_collisions": [item.summary() for item in extraction.identity_collisions],
        "unresolved_identifiers": [
            item.summary() for item in extraction.unresolved_identifiers
        ],
        "warnings": list(extraction.warnings),
        "secret_values_emitted": secret_values_emitted,
        "graph_mutations": 0,
        "wiki_writes": 0,
        "neo4j_mutations": 0,
        "graphiti_mutations": 0,
        "graphiti": "disabled",
    }


def count_secret_leaks(extraction: RabbitExtraction, rendered: dict[str, str]) -> int:
    """Verify redaction by scanning rendered output for credential values found in source.

    Matching is on identifier boundaries rather than raw substrings. A credential has leaked
    only when its value appears as a standalone token; a coincidental appearance *inside* a
    longer identifier is not a leak. FTGO proves why this matters: the cache value
    ``driver_status`` occurs inside the unrelated handler name ``get_driver_status``, and the
    word ``secret`` occurs inside this report's own ``secret_values_emitted`` field.

    ``secret_values_emitted`` in the report is this measured count, not a constant.
    """
    scannable = {
        value.strip()
        for value in extraction.withheld_values
        if len(value.strip()) >= _MIN_SCANNABLE_SECRET_LENGTH and not value.strip().isdigit()
    }
    leaks = 0
    for content in rendered.values():
        for secret in sorted(scannable):
            pattern = re.compile(
                rf"(?<![A-Za-z0-9_-]){re.escape(secret)}(?![A-Za-z0-9_-])"
            )
            leaks += len(pattern.findall(content))
    return leaks


def render_report_json(report: dict[str, Any]) -> str:
    return json.dumps(report, indent=2, ensure_ascii=False) + "\n"


def render_bundle(extraction: RabbitExtraction) -> tuple[dict[str, str], dict[str, Any]]:
    """Render candidates plus the report, with the leak count measured over all output."""
    rendered = render_all(extraction)
    provisional = build_report(extraction, 0)
    scanned = {
        **rendered,
        "extraction-report.json": render_report_json(provisional),
        DELTAS_FILENAME: render_report_json(build_service_relation_deltas(extraction)),
    }
    leaks = count_secret_leaks(extraction, scanned)
    return rendered, build_report(extraction, leaks)


def render_sidecars(extraction: RabbitExtraction, report: dict[str, Any]) -> dict[str, str]:
    """Extra output files this extractor owns beyond the candidate pages and the report."""
    del report
    return {DELTAS_FILENAME: render_report_json(build_service_relation_deltas(extraction))}


def summarize(extraction: RabbitExtraction, report: dict[str, Any]) -> dict[str, Any]:
    """CLI-facing summary of one extraction run."""
    return {
        "extractor": report["extractor"],
        "repository": extraction.repository,
        "commit": extraction.commit,
        "commit_verified": True,
        "analysis": "python-ast",
        "modules_imported": 0,
        "modules_executed": 0,
        "broker_connections_opened": 0,
        "source_files": list(extraction.source_files),
        "counts": report["counts"],
        "services_scanned": [scan.summary() for scan in extraction.services_scanned],
        "broker_libraries_detected": list(extraction.broker_libraries),
        "events": [f"{event.status}: {event.id}" for event in extraction.events],
        "relationships": [
            f"{relation.source} -{relation.type}-> {relation.target}"
            for relation in extraction.relationships
        ],
        "identity_collisions": [item.summary() for item in extraction.identity_collisions],
        "unresolved_identifiers": [
            item.summary() for item in extraction.unresolved_identifiers
        ],
        "warnings": list(extraction.warnings),
        "secret_values_emitted": report["secret_values_emitted"],
        "graph_mutations": 0,
        "wiki_writes": 0,
        "neo4j_mutations": 0,
        "graphiti": "disabled",
    }
