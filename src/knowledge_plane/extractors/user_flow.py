"""Deterministic user-flow / cross-layer execution-path extractor (Graph Engineering Pass 5).

Scope and non-goals
-------------------
This extractor reads Python source with :mod:`ast` and emits *candidates* only. It never
imports or executes the inspected application, never starts a service, never opens a broker
or database connection, never writes canonical knowledge, never touches Neo4j or Graphiti,
and never calls an LLM.

Its single job is stitching. Passes 2, 3 and 4 already proved the architecture layers in
isolation: endpoints, events, and persistence targets. Each of those is an island. This pass
proves the *execution path* that connects them::

    HTTP endpoint -> gateway service call -> RPC publish -> consumer handler -> persistence

Why call evidence, never names
------------------------------
``endpoint.ftgo.gateway.post.order.create`` and ``event.ftgo.rabbitmq.order.create`` look
like an obvious pair. This extractor refuses to pair them on that basis. A flow segment is
emitted only when a bounded AST call trace runs from the endpoint handler into the function
that Pass 3 independently proved performs the publish. The same discipline applies to the
consumer side: a service that writes a collection somewhere does not mean *this* event's
handler writes it, so the path from the registered handler to the persistence operation must
be traced for that event specifically.

Reuse rather than reinvention
-----------------------------
The authoritative entity identities come from running the existing extractors in memory, so
no Endpoint, Event, Service, Table, Collection or Schema page is ever recreated here and no
Neo4j lookup is needed. What this pass adds is a bounded local call graph and the UserFlow /
FlowStep layer that records the sequence.

Bounded tracing
---------------
``_MAX_CALL_DEPTH`` call-resolution hops from each anchor. Anything that needs reflection,
``getattr`` with a computed name, ``eval``/``exec``, or runtime injection is recorded as an
unresolved segment instead of being guessed. Ambiguity is reported, never resolved by
picking a plausible candidate.

Structure
---------
Flows are DAGs, not lists. One handler that fans out into several downstream calls keeps the
branch, and ``PRECEDES`` is emitted only between steps whose ordering the source actually
establishes; sibling calls with no proven order get no edge between them.
"""

from __future__ import annotations

import ast
import json
import re
from dataclasses import dataclass, field, replace
from typing import Any

import yaml

from ..repository_manifest import RepositoryRecord, resolve_source_files
from .data_model import extract_data_model
from .fastapi import (
    Provenance,
    extract_fastapi,
    module_dotted_name,
    normalize_dotted,
    normalize_token,
    service_location,
)
from .rabbitmq import extract_rabbitmq

EXTRACTOR_KIND = "user-flow"
CANDIDATE_STATUS = "candidate"
CANDIDATE_REVIEW_STATUS = "pending"
EVIDENCE_TYPE = "implemented"
REDACTED_PLACEHOLDER = "[redacted]"

# Output subdirectories owned by this extractor, used for stale-candidate pruning.
CANDIDATE_SUBDIRECTORIES = ("flows", "steps")
SERVICE_DELTAS_FILENAME = "service-relation-deltas.json"

# Ontology kinds used. Both already exist; this pass introduces none.
USER_FLOW_KIND = "UserFlow"
FLOW_STEP_KIND = "FlowStep"

# Relationship types used. All already exist; this pass introduces none.
CONTAINS = "CONTAINS"
PRECEDES = "PRECEDES"
IMPLEMENTS = "IMPLEMENTS"
DERIVED_FROM = "DERIVED_FROM"
PARTICIPATES_IN = "PARTICIPATES_IN"

# Step roles, in canonical execution order. The order is used for deterministic rendering
# and for deciding which steps may precede which; it is not a claim about runtime timing
# between siblings.
ROLE_HTTP_INGRESS = "http_ingress"
ROLE_SERVICE_DISPATCH = "service_dispatch"
ROLE_EVENT_PUBLISH = "event_publish"
ROLE_EVENT_CONSUME = "event_consume"
ROLE_PERSISTENCE_READ = "persistence_read"
ROLE_PERSISTENCE_WRITE = "persistence_write"
STEP_ROLE_ORDER: tuple[str, ...] = (
    ROLE_HTTP_INGRESS,
    ROLE_SERVICE_DISPATCH,
    ROLE_EVENT_PUBLISH,
    ROLE_EVENT_CONSUME,
    ROLE_PERSISTENCE_READ,
    ROLE_PERSISTENCE_WRITE,
)

# Completeness classification of an endpoint entrypoint.
COMPLETENESS_RESOLVED = "resolved"
COMPLETENESS_PARTIAL = "partial"
COMPLETENESS_UNRESOLVED = "unresolved"
COMPLETENESS_TRIVIAL = "trivial"

# Manifest source kind scanned by this pass.
SOURCE_KIND = "code"
PYTHON_SUFFIX = ".py"
SOURCE_SEGMENT = "src"

# Bounded trace. Deliberately small: this is static stitching, not program simulation.
_MAX_CALL_DEPTH = 3
_MAX_RESOLUTION_DEPTH = 24
_MAX_EXPRESSION_LENGTH = 200
_MAX_TRACES_PER_TARGET = 4

# Constructs that defeat static resolution and must be reported, never guessed.
DYNAMIC_CALL_MARKERS = frozenset(
    {"eval", "exec", "getattr", "setattr", "globals", "locals", "vars", "__import__", "compile"}
)

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

# Secret safety. A call expression is emitted only after redaction; a credential-shaped
# literal never reaches the output.
SENSITIVE_NAME_MARKERS = ("PASSWORD", "PASSWD", "SECRET", "TOKEN", "CREDENTIAL", "DSN")
SENSITIVE_EXACT_NAMES = frozenset(
    {
        "auth",
        "credentials",
        "dsn",
        "key",
        "pass",
        "passwd",
        "password",
        "secret",
        "token",
        "uri",
        "url",
    }
)
_URI_CREDENTIAL_PATTERN = re.compile(
    r"\b([a-z][a-z0-9+.\-]*://)[^/\s:@]+:[^/\s@]+@", re.IGNORECASE
)
_MIN_SCANNABLE_SECRET_LENGTH = 4


# ---------------------------------------------------------------------------------------
# Identity and safety helpers
# ---------------------------------------------------------------------------------------


def flow_id(endpoint_id: str) -> str:
    """Derive a UserFlow id mechanically from its entry Endpoint id.

    ``endpoint.ftgo.gateway.post.order.create`` -> ``flow.ftgo.gateway.post.order.create``.
    No business or marketing name is invented.
    """
    tail = endpoint_id.removeprefix("endpoint.")
    return f"flow.{normalize_dotted(tail)}"


def flow_slug(identifier: str) -> str:
    """The portion of a flow id that identifies it within the repository."""
    return identifier.removeprefix("flow.")


def step_id(flow_identifier: str, role_token: str, subject: str) -> str:
    """Build a semantic FlowStep id.

    Identity is derived from the role and the subject entity, never from ordinal position,
    so inserting a step later cannot rename the steps that follow it.
    """
    slug = flow_slug(flow_identifier)
    subject_slug = normalize_dotted(subject) if subject else ""
    if subject_slug:
        return f"step.{slug}.{role_token}.{subject_slug}"
    return f"step.{slug}.{role_token}"


def entity_tail(identifier: str, prefix: str) -> str:
    """Strip a known entity-id prefix so it can be embedded in a step id."""
    return identifier.removeprefix(prefix)


def is_sensitive_name(name: str) -> bool:
    lowered = str(name).strip().lower()
    if lowered in SENSITIVE_EXACT_NAMES:
        return True
    upper = lowered.upper()
    return any(marker in upper for marker in SENSITIVE_NAME_MARKERS)


def redact_expression(text: str | None) -> str | None:
    """Project a source expression for emission, removing credential-bearing content."""
    if text is None:
        return None
    redacted = _URI_CREDENTIAL_PATTERN.sub(rf"\1{REDACTED_PLACEHOLDER}@", str(text))
    # A keyword whose name is credential-shaped has its value replaced, keeping the shape of
    # the call visible without the value.
    def _mask(match: re.Match[str]) -> str:
        return f"{match.group(1)}={REDACTED_PLACEHOLDER}"

    return re.sub(
        r"\b([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(?:'[^']*'|\"[^\"]*\")",
        lambda match: _mask(match) if is_sensitive_name(match.group(1)) else match.group(0),
        redacted,
    )


def _expression_text(source: str, node: ast.AST | None) -> str | None:
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
    return redact_expression(collapsed[:_MAX_EXPRESSION_LENGTH])


def _dotted_expression(node: ast.expr) -> str | None:
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
    seen = 0
    while isinstance(node, ast.Await) and seen < _MAX_RESOLUTION_DEPTH:
        node = node.value
        seen += 1
    return node


def _is_none_literal(node: ast.expr) -> bool:
    if isinstance(node, ast.Constant) and node.value is None:
        return True
    # ``"None"`` inside a stringified annotation.
    return _constant_string(node) == "None"


def _unwrap_optional(node: ast.expr, depth: int = 0) -> ast.expr:
    """Strip an optional wrapper from a type annotation, leaving the single real type.

    Handles ``Optional[T]``, ``typing.Optional[T]``, ``Union[T, None]``,
    ``typing.Union[T, None]``, ``T | None`` and ``None | T``. A union of two real types is
    left alone: the receiver is then genuinely ambiguous and must not be guessed at.
    """
    if depth > _MAX_RESOLUTION_DEPTH:
        return node

    if isinstance(node, ast.Subscript):
        head = (_dotted_expression(node.value) or "").split(".")[-1]
        if head == "Optional":
            return _unwrap_optional(node.slice, depth + 1)
        if head == "Union":
            arguments = (
                list(node.slice.elts) if isinstance(node.slice, ast.Tuple) else [node.slice]
            )
            concrete = [item for item in arguments if not _is_none_literal(item)]
            if len(concrete) == 1:
                return _unwrap_optional(concrete[0], depth + 1)
        return node

    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.BitOr):
        concrete = [side for side in (node.left, node.right) if not _is_none_literal(side)]
        if len(concrete) == 1:
            return _unwrap_optional(concrete[0], depth + 1)
    return node


def _returns_own_instance(method: FunctionFacts, class_name: str) -> bool:
    """True when the body explicitly returns ``cls(...)`` or ``ClassName(...)``.

    This is the only body-derived typing the contract allows, and it is limited to the
    method's own scope: a nested closure that builds the class proves nothing about what the
    method itself returns. Anything looser would let a factory be attributed to the wrong
    class, which is how ``UserManager.load()`` used to be mistaken for a ``UserManager``.
    """
    if method.node is None:
        return False
    for statement in _scope_nodes(method.node):
        if not isinstance(statement, ast.Return) or statement.value is None:
            continue
        value = _unwrap(statement.value)
        if not isinstance(value, ast.Call):
            continue
        function = _unwrap(value.func)
        if isinstance(function, ast.Name) and function.id in ("cls", class_name):
            return True
    return False


def _constant_string(node: ast.expr | None) -> str | None:
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
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
    if not remainder or remainder[0] != SOURCE_SEGMENT:
        return f"outside the service {SOURCE_SEGMENT!r} root"
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
    header = "\n".join(text.splitlines()[:_GENERATED_HEADER_LINES]).lower()
    return any(marker in header for marker in GENERATED_HEADER_MARKERS)


# ---------------------------------------------------------------------------------------
# Per-module AST facts
# ---------------------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class ImportedSymbol:
    module: str
    name: str | None
    lineno: int
    level: int = 0


@dataclass(frozen=True, slots=True)
class CallSite:
    """One call expression inside a function body."""

    callee_expression: str
    dotted: str | None
    node: ast.Call
    lineno: int
    end_lineno: int
    dynamic_marker: str | None


@dataclass(frozen=True, slots=True)
class FunctionFacts:
    """A function or method plus its outgoing call sites."""

    name: str
    qualified_name: str
    owner_class: str | None
    parameters: tuple[str, ...]
    returns: ast.expr | None
    decorators: tuple[str, ...]
    calls: tuple[CallSite, ...]
    node: ast.FunctionDef | ast.AsyncFunctionDef
    lineno: int
    end_lineno: int


@dataclass(frozen=True, slots=True)
class ClassFacts:
    name: str
    bases: tuple[ast.expr, ...]
    methods: dict[str, FunctionFacts]
    class_attributes: dict[str, ast.expr]
    annotations: dict[str, ast.expr]
    lineno: int
    end_lineno: int


@dataclass(frozen=True, slots=True)
class ModuleFacts:
    relative_path: str
    service: str
    module: str
    is_package: bool
    source: str
    tree: ast.Module
    imports: dict[str, ImportedSymbol]
    constants: dict[str, ast.expr]
    classes: dict[str, ClassFacts]
    functions: dict[str, FunctionFacts]

    def qualified(self, symbol: str) -> str:
        return f"{self.module}.{symbol}" if self.module else symbol


def _collect_imports(tree: ast.Module) -> dict[str, ImportedSymbol]:
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
                imports.setdefault(
                    alias.asname or alias.name,
                    ImportedSymbol(
                        module=node.module or "",
                        name=alias.name,
                        lineno=node.lineno,
                        level=node.level,
                    ),
                )
    return imports


def _scope_nodes(root: ast.AST) -> list[ast.AST]:
    """Descendants of ``root`` without entering a nested function or class scope."""
    collected: list[ast.AST] = []
    stack: list[ast.AST] = list(ast.iter_child_nodes(root))
    while stack:
        node = stack.pop()
        collected.append(node)
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
            continue
        stack.extend(ast.iter_child_nodes(node))
    return collected


def _function_parameters(node: ast.FunctionDef | ast.AsyncFunctionDef) -> tuple[str, ...]:
    arguments = node.args
    names = [item.arg for item in (*arguments.posonlyargs, *arguments.args)]
    if names and names[0] in ("self", "cls"):
        names = names[1:]
    return tuple(names)


def _call_sites(source: str, node: ast.AST) -> tuple[CallSite, ...]:
    """Collect the outgoing calls of one function scope, ordered by position."""
    sites: list[CallSite] = []
    for candidate in _scope_nodes(node):
        if not isinstance(candidate, ast.Call):
            continue
        function = _unwrap(candidate.func)
        dotted = _dotted_expression(function)
        marker = None
        if dotted is not None and dotted.split(".")[-1] in DYNAMIC_CALL_MARKERS:
            marker = dotted.split(".")[-1]
        sites.append(
            CallSite(
                callee_expression=_expression_text(source, function) or "",
                dotted=dotted,
                node=candidate,
                lineno=candidate.lineno,
                end_lineno=candidate.end_lineno or candidate.lineno,
                dynamic_marker=marker,
            )
        )
    sites.sort(key=lambda item: (item.lineno, item.callee_expression))
    return tuple(sites)


def analyze_module(
    source: str,
    tree: ast.Module,
    *,
    relative_path: str,
    service: str,
    module: str,
    is_package: bool,
    warnings: list[str],
) -> ModuleFacts:
    """Gather imports, constants, classes, functions and call sites from one module."""
    imports = _collect_imports(tree)
    constants: dict[str, ast.expr] = {}
    classes: dict[str, ClassFacts] = {}
    functions: dict[str, FunctionFacts] = {}

    def build(node: ast.FunctionDef | ast.AsyncFunctionDef, owner: str | None) -> FunctionFacts:
        return FunctionFacts(
            name=node.name,
            qualified_name=f"{owner}.{node.name}" if owner else node.name,
            owner_class=owner,
            parameters=_function_parameters(node),
            returns=node.returns,
            decorators=tuple(
                sorted(
                    name
                    for name in (
                        _dotted_expression(_unwrap(item)) for item in node.decorator_list
                    )
                    if name
                )
            ),
            calls=_call_sites(source, node),
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
                functions[statement.name] = build(statement, None)
        elif isinstance(statement, ast.ClassDef):
            if statement.name in classes:
                warnings.append(
                    f"{relative_path}: class {statement.name!r} is defined more than once; "
                    f"kept the first definition at line {classes[statement.name].lineno}"
                )
                continue
            methods: dict[str, FunctionFacts] = {}
            attributes: dict[str, ast.expr] = {}
            annotations: dict[str, ast.expr] = {}
            for member in statement.body:
                if isinstance(member, ast.FunctionDef | ast.AsyncFunctionDef):
                    methods.setdefault(member.name, build(member, statement.name))
                elif isinstance(member, ast.Assign):
                    for target in member.targets:
                        if isinstance(target, ast.Name):
                            attributes.setdefault(target.id, member.value)
                elif isinstance(member, ast.AnnAssign) and isinstance(member.target, ast.Name):
                    annotations.setdefault(member.target.id, member.annotation)
                    if member.value is not None:
                        attributes.setdefault(member.target.id, member.value)
            classes[statement.name] = ClassFacts(
                name=statement.name,
                bases=tuple(statement.bases),
                methods=methods,
                class_attributes=attributes,
                annotations=annotations,
                lineno=statement.lineno,
                end_lineno=statement.end_lineno or statement.lineno,
            )
            for method in methods.values():
                functions.setdefault(method.qualified_name, method)

    # Module-level executable code can also make calls; record it under a synthetic symbol.
    module_calls = _call_sites(source, tree)
    if module_calls:
        functions.setdefault(
            "<module>",
            FunctionFacts(
                name="<module>",
                qualified_name="<module>",
                owner_class=None,
                parameters=(),
                returns=None,
                decorators=(),
                calls=module_calls,
                node=ast.FunctionDef(
                    name="<module>",
                    args=ast.arguments(
                        posonlyargs=[], args=[], kwonlyargs=[], kw_defaults=[], defaults=[]
                    ),
                    body=list(tree.body),
                    decorator_list=[],
                    lineno=1,
                    end_lineno=len(source.splitlines()) or 1,
                    col_offset=0,
                    end_col_offset=0,
                ),
                lineno=1,
                end_lineno=len(source.splitlines()) or 1,
            ),
        )

    return ModuleFacts(
        relative_path=relative_path,
        service=service,
        module=module,
        is_package=is_package,
        source=source,
        tree=tree,
        imports=imports,
        constants=constants,
        classes=classes,
        functions=functions,
    )


# ---------------------------------------------------------------------------------------
# Symbol resolution
# ---------------------------------------------------------------------------------------

SYMBOL_CLASS = "class"
SYMBOL_FUNCTION = "function"
SYMBOL_CONSTANT = "constant"
SYMBOL_MODULE = "module"
SYMBOL_EXTERNAL = "external"
SYMBOL_UNKNOWN = "unknown"


@dataclass(frozen=True, slots=True)
class SymbolRef:
    kind: str
    module: str | None = None
    name: str | None = None
    reason: str | None = None
    # Populated only when an import matched several scanned modules; the import is then
    # treated as unresolvable rather than guessed at.
    candidates: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class SourceIndex:
    """Analyzed modules addressable by dotted name and by dotted suffix, scoped per service."""

    modules: dict[tuple[str, str], ModuleFacts]
    suffixes: dict[tuple[str, str], frozenset[str]]

    def facts(self, service: str, module: str) -> ModuleFacts | None:
        return self.modules.get((service, module))

    def resolve_module(
        self, service: str, current_module: str, imported: ImportedSymbol
    ) -> tuple[str | None, tuple[str, ...]]:
        """Resolve an import to exactly one scanned module.

        Returns ``(module, candidates)``. When the import matches several scanned modules
        the module is ``None`` and every candidate is returned, so the caller can report a
        genuine ambiguity instead of silently picking one.
        """
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
            return None, ()
        if (service, target) in self.modules:
            return target, ()
        candidates = self.suffixes.get((service, target)) or frozenset()
        if len(candidates) == 1:
            return next(iter(candidates)), ()
        return None, tuple(sorted(candidates))

    def resolve_symbol(
        self,
        service: str,
        module: str,
        name: str,
        *,
        _seen: frozenset[tuple[str, str, str]] = frozenset(),
    ) -> SymbolRef:
        if len(_seen) > _MAX_RESOLUTION_DEPTH:
            return SymbolRef(SYMBOL_UNKNOWN, module, name, reason="resolution depth exceeded")
        facts = self.facts(service, module)
        if facts is None:
            return SymbolRef(SYMBOL_EXTERNAL, module, name, reason="module outside scanned source")
        if name in facts.classes:
            return SymbolRef(SYMBOL_CLASS, module, name)
        if name in facts.functions:
            return SymbolRef(SYMBOL_FUNCTION, module, name)
        if name in facts.constants:
            return SymbolRef(SYMBOL_CONSTANT, module, name)
        imported = facts.imports.get(name)
        if imported is None:
            return SymbolRef(SYMBOL_UNKNOWN, module, name, reason="name not defined or imported")
        target_module, candidates = self.resolve_module(service, module, imported)
        if target_module is None and candidates:
            return SymbolRef(
                SYMBOL_UNKNOWN,
                imported.module or module,
                imported.name or name,
                reason=(
                    f"import {imported.module or name!r} resolves to more than one module "
                    f"in scanned source"
                ),
                candidates=candidates,
            )
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
        parts = dotted.split(".")
        head = self.resolve_symbol(service, module, parts[0])
        if len(parts) == 1:
            return head
        if head.kind == SYMBOL_MODULE and head.module is not None:
            return self.resolve_dotted(service, head.module, ".".join(parts[1:]))
        if head.kind == SYMBOL_CLASS:
            return head
        return SymbolRef(SYMBOL_UNKNOWN, module, dotted, reason="attribute chain not traceable")

    def resolve_class(
        self, service: str, module: str, node: ast.expr, *, _depth: int = 0
    ) -> tuple[str, str] | None:
        """Resolve an expression to a locally defined class, following module aliases."""
        if _depth > _MAX_RESOLUTION_DEPTH:
            return None
        literal = _constant_string(node)
        if literal is not None:
            resolved = self.resolve_symbol(service, module, literal)
            if resolved.kind == SYMBOL_CLASS and resolved.module and resolved.name:
                return resolved.module, resolved.name
            return None
        dotted = _dotted_expression(node)
        if dotted is None:
            return None
        resolved = self.resolve_dotted(service, module, dotted)
        if resolved.kind == SYMBOL_CLASS and resolved.module and resolved.name:
            return resolved.module, resolved.name
        if resolved.kind == SYMBOL_CONSTANT and resolved.module and resolved.name:
            target = self.facts(service, resolved.module)
            if target is not None:
                value = target.constants.get(resolved.name)
                if value is not None:
                    return self.resolve_class(service, resolved.module, value, _depth=_depth + 1)
        return None

    def base_chain(
        self, service: str, module: str, class_name: str
    ) -> list[tuple[str, str, ClassFacts]]:
        chain: list[tuple[str, str, ClassFacts]] = []
        seen: set[tuple[str, str]] = set()
        queue = [(module, class_name)]
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

    def lookup_method(
        self, service: str, module: str, class_name: str, method: str
    ) -> tuple[str, FunctionFacts] | None:
        """Find a method on a class or its statically declared bases."""
        for current_module, _, declaration in self.base_chain(service, module, class_name):
            found = declaration.methods.get(method)
            if found is not None:
                return current_module, found
        return None

    def class_attribute(
        self, service: str, module: str, class_name: str, attribute: str
    ) -> tuple[str, ast.expr] | None:
        for current_module, _, declaration in self.base_chain(service, module, class_name):
            value = declaration.class_attributes.get(attribute)
            if value is not None:
                return current_module, value
        return None

    def class_annotation(
        self, service: str, module: str, class_name: str, attribute: str
    ) -> tuple[str, ast.expr] | None:
        for current_module, _, declaration in self.base_chain(service, module, class_name):
            value = declaration.annotations.get(attribute)
            if value is not None:
                return current_module, value
        return None


def build_source_index(modules: list[ModuleFacts]) -> SourceIndex:
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
# Callee resolution
# ---------------------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class ResolvedCallee:
    """A call site resolved to a concrete local function, or the reason it was not."""

    module: str | None
    qualified_name: str | None
    reason: str | None = None
    ambiguous: tuple[str, ...] = ()

    @property
    def resolved(self) -> bool:
        return self.module is not None and self.qualified_name is not None

    def symbol(self) -> str | None:
        if not self.resolved:
            return None
        return f"{self.module}.{self.qualified_name}" if self.module else self.qualified_name


class CalleeResolver:
    """Resolves a call site to a local function within the tracing contract.

    Handles direct local calls, imported local functions, class/static methods,
    ``cls``/``self`` dispatch through the declared base chain, and instance method calls
    where the receiver's class is statically knowable from a constructor call, a return
    annotation, or a class-attribute annotation. Anything else is reported unresolved.
    """

    def __init__(self, index: SourceIndex) -> None:
        self.index = index

    def instance_class(
        self,
        service: str,
        module: str,
        node: ast.expr,
        scope: dict[str, ast.expr],
        owner_class: str | None,
        depth: int = 0,
    ) -> tuple[str, str] | None:
        """Best-effort static class of a receiver expression."""
        if depth > _MAX_RESOLUTION_DEPTH:
            return None
        node = _unwrap(node)

        if isinstance(node, ast.Name):
            if node.id in ("self", "cls"):
                return (module, owner_class) if owner_class else None
            bound = scope.get(node.id)
            if bound is not None:
                return self.instance_class(
                    service, module, bound, {}, owner_class, depth + 1
                )
            return None

        if isinstance(node, ast.Attribute):
            if (
                isinstance(node.value, ast.Name)
                and node.value.id in ("self", "cls")
                and owner_class is not None
            ):
                annotated = self.index.class_annotation(service, module, owner_class, node.attr)
                if annotated is not None:
                    resolved = self.index.resolve_class(service, annotated[0], annotated[1])
                    if resolved is not None:
                        return resolved
                assigned = self.index.class_attribute(service, module, owner_class, node.attr)
                if assigned is not None:
                    resolved = self.index.resolve_class(service, assigned[0], assigned[1])
                    if resolved is not None:
                        return resolved
            return None

        if isinstance(node, ast.Call):
            function = _unwrap(node.func)
            if isinstance(function, ast.Attribute):
                return self._call_result_class(service, module, function, owner_class)
            # ``SomeClass(...)`` constructs an instance of that class.
            return self.index.resolve_class(service, module, function)
        return None

    def _call_result_class(
        self,
        service: str,
        module: str,
        function: ast.Attribute,
        owner_class: str | None,
    ) -> tuple[str, str] | None:
        """Type the result of ``receiver.attr(...)``.

        A method call is checked before construction on purpose. ``resolve_class`` reports any
        attribute chain rooted at a class as that class, so asking it first would type
        ``RPCBroker.get_client()`` as an ``RPCBroker`` and ``OrderService.create_order()`` as
        an ``OrderService`` - the receiver mis-typing that made ``response.get(...)`` look
        like ``OrderService.get``.
        """
        owner = self.index.resolve_class(service, module, function.value)
        if (
            owner is None
            and isinstance(function.value, ast.Name)
            and function.value.id in ("self", "cls")
            and owner_class is not None
        ):
            owner = (module, owner_class)
        if owner is not None:
            found = self.index.lookup_method(service, owner[0], owner[1], function.attr)
            if found is not None:
                owner_module, method = found
                if method.returns is not None:
                    # The declared return type is the answer, including through an optional
                    # wrapper. When it names something outside scanned source the answer is
                    # "unknown", never "the owning class": a factory on ``UserManager`` that
                    # returns a ``User`` must not be typed as a ``UserManager``.
                    return self.index.resolve_class(
                        service, owner_module, _unwrap_optional(method.returns)
                    )
                # With no annotation, only an explicit ``return cls(...)`` proves the factory
                # yields its owning class. Ownership alone proves nothing.
                if _returns_own_instance(method, owner[1]):
                    return owner
                return None

        # Not a known method, so this may be ``package.module.SomeClass(...)``. Accept it only
        # when the chain names the class itself rather than an attribute hanging off one.
        constructed = self.index.resolve_class(service, module, function)
        if constructed is not None and constructed[1] == function.attr:
            return constructed
        return None

    def resolve(
        self,
        facts: ModuleFacts,
        site: CallSite,
        scope: dict[str, ast.expr],
        owner_class: str | None,
    ) -> ResolvedCallee:
        """Resolve one call site to a local function symbol."""
        if site.dynamic_marker is not None:
            return ResolvedCallee(
                None,
                None,
                reason=f"dynamic call construct {site.dynamic_marker!r} cannot be traced",
            )
        function = _unwrap(site.node.func)
        service, module = facts.service, facts.module

        if isinstance(function, ast.Name):
            resolved = self.index.resolve_symbol(service, module, function.id)
            if resolved.kind == SYMBOL_FUNCTION and resolved.module and resolved.name:
                return ResolvedCallee(resolved.module, resolved.name)
            if resolved.kind == SYMBOL_CLASS:
                # Construction is not a traced execution step on its own.
                return ResolvedCallee(None, None, reason="call constructs a class instance")
            return ResolvedCallee(
                None,
                None,
                reason=resolved.reason or "callee is not a local function",
                ambiguous=resolved.candidates,
            )

        if not isinstance(function, ast.Attribute):
            return ResolvedCallee(None, None, reason="callee is not a name or attribute")

        receiver = function.value
        owner = self.instance_class(service, module, receiver, scope, owner_class)
        if owner is None:
            owner = self.index.resolve_class(service, module, receiver)
        if owner is None:
            dotted = _dotted_expression(receiver)
            head = (
                self.index.resolve_symbol(service, module, dotted.split(".")[0])
                if dotted
                else None
            )
            if head is not None and head.candidates:
                return ResolvedCallee(
                    None, None, reason=head.reason, ambiguous=head.candidates
                )
            # A receiver whose type is a parameter, a library object or an unannotated local
            # is outside the tracing contract by design; that is ordinary, not a finding.
            # Only a receiver that the index can see is worth surfacing as a gap.
            return ResolvedCallee(
                None,
                None,
                reason=(
                    f"receiver {dotted or '<expression>'!r} is not a statically typed "
                    f"instance of a class in scanned source"
                ),
            )
        found = self.index.lookup_method(service, owner[0], owner[1], function.attr)
        if found is None:
            return ResolvedCallee(
                None,
                None,
                reason=f"{owner[1]}.{function.attr} is not defined in scanned source",
            )
        owner_module, method = found
        return ResolvedCallee(owner_module, method.qualified_name)


def local_scope(function: FunctionFacts) -> dict[str, ast.expr]:
    """Local name bindings inside a function body, used only for receiver typing.

    Bindings are collected flat and first-write-wins in source order. That is what lets
    ``order = Order.create(...)`` followed by ``await order.save()`` resolve to the entity
    class without simulating control flow.
    """
    bindings: list[tuple[int, str, ast.expr]] = []
    for node in _scope_nodes(function.node):
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
    bindings.sort(key=lambda item: (item[0], item[1]))
    scope: dict[str, ast.expr] = {}
    for _, name, value in bindings:
        scope.setdefault(name, value)
    return scope


# ---------------------------------------------------------------------------------------
# Bounded call tracing
# ---------------------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class TraceHop:
    """One resolved call in a trace, with the exact call site that establishes it."""

    caller_symbol: str
    callee_symbol: str
    expression: str
    provenance: Provenance

    def summary(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "caller": self.caller_symbol,
            "callee": self.callee_symbol,
        }
        if self.expression:
            payload["call"] = self.expression
        payload.update(self.provenance.as_dict())
        return payload


@dataclass(frozen=True, slots=True)
class Trace:
    """An ordered chain of resolved calls from an anchor to a target function."""

    anchor_symbol: str
    target_symbol: str
    hops: tuple[TraceHop, ...]

    @property
    def depth(self) -> int:
        return len(self.hops)

    @property
    def key(self) -> tuple[str, ...]:
        return (self.anchor_symbol, self.target_symbol, *(hop.callee_symbol for hop in self.hops))

    def summary(self) -> list[dict[str, Any]]:
        return [hop.summary() for hop in self.hops]


@dataclass(frozen=True, slots=True)
class UnresolvedCall:
    """A call site that could not be resolved inside the tracing contract."""

    service: str
    caller_symbol: str
    expression: str
    reason: str
    provenance: Provenance

    def summary(self) -> dict[str, Any]:
        return {
            "service": self.service,
            "caller": self.caller_symbol,
            "expression": self.expression,
            "reason": self.reason,
            "source_evidence": self.provenance.as_dict(),
        }


@dataclass(frozen=True, slots=True)
class ReceiverGap:
    """A call the tracer declined to follow because the receiver's type is not static.

    This is a limit of the declared tracing contract rather than a defect in the source, so
    it is recorded once per call site with an occurrence count instead of being repeated for
    every flow that walks through the same code.
    """

    service: str
    caller_symbol: str
    expression: str
    reason: str
    provenance: Provenance
    occurrences: int

    def summary(self) -> dict[str, Any]:
        return {
            "service": self.service,
            "caller": self.caller_symbol,
            "expression": self.expression,
            "reason": self.reason,
            "traversals": self.occurrences,
            "source_evidence": self.provenance.as_dict(),
        }


class CallTracer:
    """Breadth-first bounded search over resolved local calls.

    The search is bounded by ``_MAX_CALL_DEPTH`` hops from the anchor. Every visited edge
    keeps its call-site provenance, so a reported flow segment can always be walked back to
    concrete source lines. Unresolvable call sites encountered along the way are collected
    rather than dropped, which is what makes a *partial* flow honest instead of silent.
    """

    def __init__(
        self,
        index: SourceIndex,
        resolver: CalleeResolver,
        repository: str,
        commit: str,
        *,
        interpreted_boundaries: dict[tuple[str, str], frozenset[str]] | None = None,
    ) -> None:
        self.index = index
        self.resolver = resolver
        self.repository = repository
        self.commit = commit
        # ``(service, symbol)`` -> the library operation names an earlier pass already turned
        # into an Event, Table or Collection at that site.
        self.interpreted_boundaries: dict[tuple[str, str], frozenset[str]] = (
            interpreted_boundaries or {}
        )
        # Receiver-typing limits are a property of the contract, not of one flow, so they are
        # accumulated once per call site across the whole run instead of per traced flow.
        self.receiver_gaps: dict[tuple[str, str, int, str], ReceiverGap] = {}
        # Calls suppressed because an earlier pass already interpreted them. Counted, not
        # hidden, so a reviewer can see exactly what was filtered and why.
        self.boundary_calls: dict[tuple[str, str, int, str], ReceiverGap] = {}

    def _record_once(
        self,
        sink: dict[tuple[str, str, int, str], ReceiverGap],
        service: str,
        caller_symbol: str,
        expression: str,
        reason: str,
        provenance: Provenance,
    ) -> None:
        """Accumulate one call site with a traversal count instead of one row per flow."""
        key = (
            provenance.source_path or "",
            caller_symbol,
            provenance.line_start or 0,
            expression,
        )
        existing = sink.get(key)
        if existing is None:
            sink[key] = ReceiverGap(
                service=service,
                caller_symbol=caller_symbol,
                expression=expression,
                reason=reason,
                provenance=provenance,
                occurrences=1,
            )
            return
        sink[key] = replace(existing, occurrences=existing.occurrences + 1)

    def _is_interpreted_boundary(self, service: str, symbol: str, site: CallSite) -> bool:
        """True when this call is the framework operation an earlier pass already resolved.

        The test is deliberately narrow: the enclosing function must be a site an earlier pass
        interpreted, *and* the called attribute must be the very operation it interpreted
        there. A dynamic construct is never a boundary, so ``setattr`` and friends keep
        surfacing even inside a publisher or a repository method.
        """
        if site.dynamic_marker is not None:
            return False
        operations = self.interpreted_boundaries.get((service, symbol))
        if not operations:
            return False
        return site.callee_expression.rsplit(".", 1)[-1] in operations

    def _function(self, service: str, symbol: str) -> tuple[ModuleFacts, FunctionFacts] | None:
        """Split a fully qualified symbol into its module and function."""
        parts = symbol.split(".")
        for cut in range(len(parts) - 1, 0, -1):
            module = ".".join(parts[:cut])
            remainder = ".".join(parts[cut:])
            facts = self.index.facts(service, module)
            if facts is None:
                continue
            declaration = facts.functions.get(remainder)
            if declaration is not None:
                return facts, declaration
        facts = self.index.facts(service, "")
        if facts is not None:
            declaration = facts.functions.get(symbol)
            if declaration is not None:
                return facts, declaration
        return None

    def trace_to(
        self,
        service: str,
        anchor_symbol: str,
        targets: set[str],
        *,
        max_depth: int = _MAX_CALL_DEPTH,
    ) -> tuple[dict[str, list[Trace]], list[UnresolvedCall]]:
        """Find bounded traces from ``anchor_symbol`` to any symbol in ``targets``.

        Returns traces grouped by the target symbol reached, plus every unresolved call site
        seen while searching. A target that *is* the anchor yields a zero-hop trace, which is
        how a handler that performs the operation itself is represented.
        """
        found: dict[str, list[Trace]] = {}
        unresolved: list[UnresolvedCall] = []
        seen_unresolved: set[tuple[str, str, int]] = set()

        if anchor_symbol in targets:
            found.setdefault(anchor_symbol, []).append(Trace(anchor_symbol, anchor_symbol, ()))

        visited: set[str] = {anchor_symbol}
        frontier: list[tuple[str, tuple[TraceHop, ...]]] = [(anchor_symbol, ())]
        depth = 0
        while frontier and depth < max_depth:
            next_frontier: list[tuple[str, tuple[TraceHop, ...]]] = []
            for symbol, hops in frontier:
                located = self._function(service, symbol)
                if located is None:
                    continue
                facts, declaration = located
                scope = local_scope(declaration)
                for site in declaration.calls:
                    resolved = self.resolver.resolve(
                        facts, site, scope, declaration.owner_class
                    )
                    provenance = Provenance(
                        repository=self.repository,
                        commit=self.commit,
                        source_path=facts.relative_path,
                        symbol=symbol,
                        line_start=site.lineno,
                        line_end=site.end_lineno,
                        evidence_type=EVIDENCE_TYPE,
                    )
                    if not resolved.resolved:
                        # Construction and library calls are ordinary, not findings; only
                        # genuinely opaque dispatch is worth reporting.
                        if self._is_interpreted_boundary(service, symbol, site):
                            # An earlier pass already read this exact framework operation and
                            # named the Event, Table or Collection it reaches. Counting it as
                            # an unresolved application path would contradict that result.
                            self._record_once(
                                self.boundary_calls,
                                service,
                                symbol,
                                site.callee_expression,
                                resolved.reason or "",
                                provenance,
                            )
                        elif resolved.reason and _RECEIVER_GAP_MARKER in resolved.reason:
                            self._record_once(
                                self.receiver_gaps,
                                service,
                                symbol,
                                site.callee_expression,
                                resolved.reason,
                                provenance,
                            )
                        elif resolved.reason and _is_reportable(resolved.reason):
                            key = (symbol, site.callee_expression, site.lineno)
                            if key not in seen_unresolved:
                                seen_unresolved.add(key)
                                unresolved.append(
                                    UnresolvedCall(
                                        service=service,
                                        caller_symbol=symbol,
                                        expression=site.callee_expression,
                                        reason=resolved.reason,
                                        provenance=provenance,
                                    )
                                )
                        continue
                    callee = resolved.symbol()
                    assert callee is not None  # guarded by resolved
                    hop = TraceHop(
                        caller_symbol=symbol,
                        callee_symbol=callee,
                        expression=site.callee_expression,
                        provenance=provenance,
                    )
                    chain = (*hops, hop)
                    if callee in targets:
                        traces = found.setdefault(callee, [])
                        if len(traces) < _MAX_TRACES_PER_TARGET:
                            traces.append(Trace(anchor_symbol, callee, chain))
                    if callee not in visited:
                        visited.add(callee)
                        next_frontier.append((callee, chain))
            frontier = next_frontier
            depth += 1

        for traces in found.values():
            traces.sort(key=lambda item: (item.depth, item.key))
        return found, unresolved


_REPORTABLE_REASON_MARKERS = (
    "dynamic call construct",
    "is not defined in scanned source",
    "resolves to more than one module",
)
# Receiver typing is bounded by the tracing contract, so a failure there is expected rather
# than a defect. Those sites are still counted and listed once each, under their own bucket,
# so nothing is hidden; they simply do not pollute the per-flow findings.
_RECEIVER_GAP_MARKER = "is not a statically typed instance"
_AMBIGUOUS_MARKER = "resolves to more than one module"

# Pass 4 resolution qualifier meaning "the call site names a model variable, so every model
# in the repository's map is a possible target". Pass 5 proves the call path to such a site
# but must not claim the specific table or collection was pinned by the source.
ENUMERATED_RESOLUTION = "model_map_enumeration"


def _is_reportable(reason: str) -> bool:
    """True when an unresolved call site is worth surfacing to a reviewer.

    Calls into libraries, constructors and framework helpers are expected and would drown
    the report; opaque dispatch and missing local definitions are the interesting cases.
    """
    return any(marker in reason for marker in _REPORTABLE_REASON_MARKERS)


def _trace_sort_key(trace: Trace) -> tuple[int, tuple[str, ...]]:
    """Order traces shallowest first, then lexically, so output never depends on discovery order."""
    return (trace.depth, trace.key)


def _merge_traces(first: tuple[Trace, ...], second: tuple[Trace, ...]) -> tuple[Trace, ...]:
    """Union two proof sets, deduplicated by call chain and capped at the trace budget."""
    seen: dict[tuple[str, ...], Trace] = {}
    for trace in (*first, *second):
        seen.setdefault(trace.key, trace)
    ordered = sorted(seen.values(), key=_trace_sort_key)
    return tuple(ordered[:_MAX_TRACES_PER_TARGET])


def _targets_shallowest_first(traces: dict[str, list[Trace]]) -> list[str]:
    """Resolved target symbols ordered by tightest proof, then by symbol name.

    Whichever target registers a shared step first supplies its provenance and
    attributes, so the shortest proven call path must win to keep the recorded
    evidence as direct as the source allows.
    """
    return sorted(
        traces,
        key=lambda symbol: (
            min(item.depth for item in traces[symbol]) if traces[symbol] else _MAX_CALL_DEPTH + 1,
            symbol,
        ),
    )


# ---------------------------------------------------------------------------------------
# Candidate model
# ---------------------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class FlowStepCandidate:
    id: str
    kind: str
    title: str
    role: str
    flow_id: str
    service: str
    service_entity_id: str
    anchor_id: str | None
    anchor_kind: str | None
    provenance: Provenance
    traces: tuple[Trace, ...] = ()
    attributes: dict[str, Any] = field(default_factory=dict)

    @property
    def role_rank(self) -> int:
        return STEP_ROLE_ORDER.index(self.role)

    def summary(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "id": self.id,
            "kind": self.kind,
            "role": self.role,
            "flow": self.flow_id,
            "service": self.service_entity_id,
        }
        if self.anchor_id:
            payload["derived_from"] = self.anchor_id
            payload["derived_from_kind"] = self.anchor_kind
        payload["attributes"] = self.attributes
        if self.traces:
            payload["trace"] = [trace.summary() for trace in self.traces]
        payload["source"] = self.provenance.as_dict()
        return payload


@dataclass(frozen=True, slots=True)
class UserFlowCandidate:
    id: str
    kind: str
    title: str
    endpoint_id: str
    http_method: str
    path: str
    path_resolution: str
    completeness: str
    handler_symbol: str
    services: tuple[str, ...]
    events: tuple[str, ...]
    persistence_targets: tuple[str, ...]
    # Targets whose only proof is Pass 4's enumeration over a generic repository's model map.
    # The call path is proven; the specific table or collection is not pinned by the call
    # site, so it is disclosed rather than presented as an exact hit.
    enumerated_persistence_targets: tuple[str, ...]
    step_ids: tuple[str, ...]
    unresolved_segments: tuple[str, ...]
    provenance: Provenance
    attributes: dict[str, Any] = field(default_factory=dict)

    def summary(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "kind": self.kind,
            "title": self.title,
            "endpoint": self.endpoint_id,
            "http_method": self.http_method,
            "path": self.path,
            "path_resolution": self.path_resolution,
            "completeness": self.completeness,
            "handler": self.handler_symbol,
            "participating_services": list(self.services),
            "events": list(self.events),
            "persistence_targets": list(self.persistence_targets),
            "enumerated_persistence_targets": list(self.enumerated_persistence_targets),
            "steps": list(self.step_ids),
            "unresolved_segments": list(self.unresolved_segments),
            "attributes": self.attributes,
            "source": self.provenance.as_dict(),
        }


@dataclass(frozen=True, slots=True)
class RelationshipCandidate:
    source: str
    type: str
    target: str
    provenance: Provenance
    role: str | None = None
    detail: dict[str, Any] = field(default_factory=dict)

    def summary(self) -> dict[str, Any]:
        payload: dict[str, Any] = {"source": self.source, "type": self.type, "target": self.target}
        if self.role:
            payload["role"] = self.role
        payload.update(self.detail)
        payload["source_evidence"] = self.provenance.as_dict()
        return payload


@dataclass(frozen=True, slots=True)
class EndpointClassification:
    endpoint_id: str
    completeness: str
    reason: str

    def summary(self) -> dict[str, Any]:
        return {
            "endpoint": self.endpoint_id,
            "completeness": self.completeness,
            "reason": self.reason,
        }


@dataclass(frozen=True, slots=True)
class UnresolvedFinding:
    category: str
    subject: str
    reason: str
    service: str | None = None
    provenance: Provenance | None = None

    def summary(self) -> dict[str, Any]:
        payload: dict[str, Any] = {"subject": self.subject, "reason": self.reason}
        if self.service:
            payload["service"] = self.service
        if self.provenance is not None:
            payload["source_evidence"] = self.provenance.as_dict()
        return payload


@dataclass(frozen=True, slots=True)
class UserFlowExtraction:
    repository: str
    commit: str
    owner: str | None
    source_files: tuple[str, ...]
    skipped_files: tuple[str, ...]
    services_scanned: tuple[str, ...]
    flows: tuple[UserFlowCandidate, ...]
    steps: tuple[FlowStepCandidate, ...]
    relationships: tuple[RelationshipCandidate, ...]
    classifications: tuple[EndpointClassification, ...]
    unresolved: tuple[UnresolvedFinding, ...]
    ambiguous_call_targets: tuple[UnresolvedFinding, ...]
    receiver_typing_gaps: tuple[ReceiverGap, ...]
    interpreted_boundary_calls: tuple[ReceiverGap, ...]
    identity_collisions: tuple[str, ...]
    cycles_detected: tuple[str, ...]
    warnings: tuple[str, ...]
    withheld_values: frozenset[str]

    def steps_of(self, flow_identifier: str) -> tuple[FlowStepCandidate, ...]:
        """Steps of one flow in stage order, matching the order on the flow page."""
        return tuple(
            sorted(
                (item for item in self.steps if item.flow_id == flow_identifier),
                key=lambda item: (item.role_rank, item.id),
            )
        )

    def unresolved_of(self, category: str) -> tuple[UnresolvedFinding, ...]:
        return tuple(item for item in self.unresolved if item.category == category)

    def classified(self, completeness: str) -> tuple[EndpointClassification, ...]:
        return tuple(item for item in self.classifications if item.completeness == completeness)

    def relations_for(self, entity_id: str) -> tuple[RelationshipCandidate, ...]:
        return tuple(item for item in self.relationships if item.source == entity_id)

    def inbound_relations_for(self, entity_id: str) -> tuple[RelationshipCandidate, ...]:
        return tuple(item for item in self.relationships if item.target == entity_id)


UNRESOLVED_DISPATCH = "unresolved_endpoint_dispatches"
UNRESOLVED_PUBLISHER = "unresolved_event_publishers"
UNRESOLVED_CONSUMER = "unresolved_consumer_handlers"
UNRESOLVED_PERSISTENCE = "unresolved_persistence_segments"


# ---------------------------------------------------------------------------------------
# Source discovery
# ---------------------------------------------------------------------------------------


def _discover_source_files(record: RepositoryRecord) -> tuple[tuple[str, ...], list[str]]:
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


def _module_of_path(index: SourceIndex, service: str, relative_path: str) -> ModuleFacts | None:
    for (candidate_service, _), facts in index.modules.items():
        if candidate_service == service and facts.relative_path == relative_path:
            return facts
    return None


# ---------------------------------------------------------------------------------------
# Stitching
# ---------------------------------------------------------------------------------------


def _service_entity(repository_slug: str, service: str) -> str:
    return f"service.{repository_slug}.{service}"


def extract_user_flow(
    record: RepositoryRecord,
    commit: str,
    *,
    source_kind: str = SOURCE_KIND,
) -> UserFlowExtraction:
    """Stitch the already proven architecture layers into source-backed execution flows.

    ``commit`` must already be verified against the manifest baseline by the caller. The
    inspected repository is only ever read: no module is imported, no code is executed, and
    no broker or database connection is opened.
    """
    del source_kind
    repository = record.id
    repository_slug = normalize_token(record.id)
    warnings: list[str] = []
    unresolved: list[UnresolvedFinding] = []
    ambiguous: list[UnresolvedFinding] = []

    # --- authoritative identities from the earlier passes, computed in memory --------------
    api = extract_fastapi(record, commit)
    broker = extract_rabbitmq(record, commit)
    data = extract_data_model(record, commit)

    # --- local call graph -----------------------------------------------------------------
    candidates, skipped = _discover_source_files(record)
    modules: list[ModuleFacts] = []
    scanned: list[str] = []
    services: set[str] = set()
    for relative_path in candidates:
        location = service_location(relative_path)
        if location is None:  # pragma: no cover - filtered by skip_reason
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
        services.add(service)
        modules.append(
            analyze_module(
                text,
                tree,
                relative_path=relative_path,
                service=service,
                module=module_dotted_name(relative_path, service_root),
                is_package=relative_path.rsplit("/", 1)[-1] == "__init__.py",
                warnings=warnings,
            )
        )

    index = build_source_index(modules)
    resolver = CalleeResolver(index)

    # --- anchor tables from the earlier passes --------------------------------------------
    # symbol -> publisher interactions proven by Pass 3
    publishers_by_symbol: dict[tuple[str, str], list[Any]] = {}
    for interaction in broker.publisher_calls:
        key = (interaction.service, interaction.provenance.symbol or "")
        publishers_by_symbol.setdefault(key, []).append(interaction)

    # event identity -> Event candidate proven by Pass 3
    events_by_identity = {item.identity: item for item in broker.events}
    # (service, identity) -> consumer bindings proven by Pass 3
    consumers_by_event: dict[str, list[Any]] = {}
    for binding in broker.consumer_bindings:
        consumers_by_event.setdefault(binding.identity, []).append(binding)

    # symbol -> persistence accesses proven by Pass 4
    accesses_by_symbol: dict[tuple[str, str], list[tuple[Any, Any]]] = {}
    for access in data.accesses:
        service_slug = access.service.split(".")[-1]
        for site in access.call_sites:
            accesses_by_symbol.setdefault((service_slug, site.symbol), []).append((access, site))

    # --- framework calls the earlier passes already interpreted ----------------------------
    # Maps ``(service, function symbol)`` to the library operation names Pass 3 or Pass 4
    # already read at that site. Inside those functions the untraceable call *is* the broker
    # or the database driver, and its architectural meaning is a known Event, Table or
    # Collection. Reporting it again as an unresolved application path would contradict a
    # result this pass depends on. The match is on the operation name, so an unrelated gap in
    # the same function - a dynamic ``setattr``, a missing local method - still surfaces.
    boundary_operations: dict[tuple[str, str], set[str]] = {}

    def note_boundary(service: str, symbol: str | None, operation: str | None) -> None:
        if not symbol or not operation:
            return
        boundary_operations.setdefault((service, symbol), set()).add(operation)

    for interaction in (*broker.publisher_calls, *broker.consumer_bindings):
        note_boundary(interaction.service, interaction.provenance.symbol, interaction.operation)
    for wrapper in broker.wrappers:
        # A publisher call site names the wrapper; the library call itself lives inside it.
        note_boundary(wrapper.service, wrapper.symbol, wrapper.operation)
    for access in data.accesses:
        service_slug = access.service.split(".")[-1]
        for site in access.call_sites:
            note_boundary(service_slug, site.symbol, site.operation)

    tracer = CallTracer(
        index,
        resolver,
        repository,
        commit,
        interpreted_boundaries={
            key: frozenset(value) for key, value in boundary_operations.items()
        },
    )

    flows: list[UserFlowCandidate] = []
    steps: dict[str, FlowStepCandidate] = {}
    relationships: list[RelationshipCandidate] = []
    classifications: list[EndpointClassification] = []
    participation: dict[tuple[str, str], list[Trace]] = {}
    collisions: list[str] = []

    def record_call_finding(category: str, subject_id: str, item: UnresolvedCall) -> None:
        """File one unresolved call site under the right bucket.

        A call whose import matched several scanned modules is an ambiguity, not a missing
        segment: the source is genuinely undecidable at this point, so it is kept apart from
        the ordinary "trace stopped here" findings.
        """
        finding = UnresolvedFinding(
            category=category,
            subject=f"{subject_id} -> {item.expression}",
            reason=item.reason,
            service=_service_entity(repository_slug, item.service),
            provenance=item.provenance,
        )
        if _AMBIGUOUS_MARKER in item.reason:
            ambiguous.append(finding)
            return
        unresolved.append(finding)

    def register_step(candidate: FlowStepCandidate) -> FlowStepCandidate:
        """Store a step, or merge a second proof of an already-known step.

        One step can be proven by more than one call path: two different local
        functions inside the same service may both write the same collection. The
        step identity stays keyed on ``(flow, role, anchor)``, and the extra call
        paths are kept as additional traces rather than discarded, so the report
        shows every bounded proof it found. Attributes and provenance stay those of
        the first registration, which is the tightest proof because callers iterate
        resolved targets shallowest-first.
        """
        existing = steps.get(candidate.id)
        if existing is None:
            steps[candidate.id] = candidate
            return candidate
        if existing.role != candidate.role or existing.anchor_id != candidate.anchor_id:
            collisions.append(
                f"{candidate.id}: {existing.role}->{existing.anchor_id} and "
                f"{candidate.role}->{candidate.anchor_id} claim the same step id"
            )
            return existing
        merged = _merge_traces(existing.traces, candidate.traces)
        if merged == existing.traces:
            return existing
        combined = replace(existing, traces=merged)
        steps[candidate.id] = combined
        return combined

    for endpoint in api.endpoints:
        handler_symbol = endpoint.provenance.symbol or ""
        endpoint_service = endpoint.service
        identifier = flow_id(endpoint.id)
        flow_unresolved: list[str] = []
        flow_steps: list[FlowStepCandidate] = []
        precedes: list[tuple[str, str, Provenance, dict[str, Any]]] = []
        flow_services: set[str] = {endpoint_service}
        flow_events: set[str] = set()
        flow_targets: set[str] = set()
        target_resolutions: dict[str, set[str]] = {}

        # --- step 1: HTTP ingress ----------------------------------------------------------
        ingress = FlowStepCandidate(
            id=step_id(identifier, "http-ingress", ""),
            kind=FLOW_STEP_KIND,
            title=f"{endpoint.method} {endpoint.effective_path} ingress",
            role=ROLE_HTTP_INGRESS,
            flow_id=identifier,
            service=endpoint_service,
            service_entity_id=_service_entity(repository_slug, endpoint_service),
            anchor_id=endpoint.id,
            anchor_kind="Endpoint",
            provenance=endpoint.provenance,
            attributes={
                "http_method": endpoint.method,
                "path": endpoint.effective_path,
                "path_resolution": endpoint.path_resolution,
                "handler": handler_symbol,
            },
        )

        # --- step 2+: gateway dispatch to a proven publisher ------------------------------
        publisher_targets = {
            symbol for (service, symbol) in publishers_by_symbol if service == endpoint_service
        }
        traces, dispatch_unresolved = tracer.trace_to(
            endpoint_service, handler_symbol, publisher_targets
        )
        for item in dispatch_unresolved:
            record_call_finding(UNRESOLVED_DISPATCH, endpoint.id, item)

        if not traces:
            classifications.append(
                EndpointClassification(
                    endpoint.id,
                    COMPLETENESS_TRIVIAL,
                    "no bounded call path from the handler reaches a proven publisher call",
                )
            )
            continue

        # Registered only once the flow is known to be non-trivial, so that a discarded
        # endpoint never contributes an orphan step page.
        ingress = register_step(ingress)
        flow_steps.append(ingress)
        for publisher_symbol in _targets_shallowest_first(traces):
            best = traces[publisher_symbol][0]
            interactions = publishers_by_symbol[(endpoint_service, publisher_symbol)]
            dispatch_step = register_step(
                FlowStepCandidate(
                    id=step_id(identifier, "dispatch", publisher_symbol),
                    kind=FLOW_STEP_KIND,
                    title=f"{publisher_symbol} dispatch",
                    role=ROLE_SERVICE_DISPATCH,
                    flow_id=identifier,
                    service=endpoint_service,
                    service_entity_id=_service_entity(repository_slug, endpoint_service),
                    anchor_id=endpoint.id,
                    anchor_kind="Endpoint",
                    # The evidence for a dispatch is the call site that reaches the
                    # publisher, so the provenance stays the last hop exactly as traced:
                    # its symbol is the calling function and its lines are the call. The
                    # callee is recorded in the attributes instead of being spliced into a
                    # provenance record that would then name a file it does not live in.
                    provenance=best.hops[-1].provenance if best.hops else endpoint.provenance,
                    traces=tuple(traces[publisher_symbol]),
                    attributes={
                        "gateway_symbol": publisher_symbol,
                        "call_depth": best.depth,
                    },
                )
            )
            flow_steps.append(dispatch_step)
            precedes.append(
                (
                    ingress.id,
                    dispatch_step.id,
                    best.hops[0].provenance if best.hops else endpoint.provenance,
                    {"established_by": "handler call site", "call_depth": best.depth},
                )
            )

            for interaction in sorted(interactions, key=lambda item: item.identity):
                event = events_by_identity.get(interaction.identity)
                if event is None:
                    unresolved.append(
                        UnresolvedFinding(
                            category=UNRESOLVED_PUBLISHER,
                            subject=f"{endpoint.id} -> {interaction.identity}",
                            reason=(
                                "the publisher identity has no Event entity, which happens when "
                                "distinct identities collide on one id"
                            ),
                            service=_service_entity(repository_slug, endpoint_service),
                            provenance=interaction.provenance,
                        )
                    )
                    flow_unresolved.append(f"publish:{interaction.identity}")
                    continue
                flow_events.add(event.id)
                publish_step = register_step(
                    FlowStepCandidate(
                        id=step_id(
                            identifier, "publish", entity_tail(event.id, "event.")
                        ),
                        kind=FLOW_STEP_KIND,
                        title=f"publish {event.identity}",
                        role=ROLE_EVENT_PUBLISH,
                        flow_id=identifier,
                        service=endpoint_service,
                        service_entity_id=_service_entity(repository_slug, endpoint_service),
                        anchor_id=event.id,
                        anchor_kind="Event",
                        provenance=interaction.provenance,
                        attributes={
                            "event_identity": event.identity,
                            "operation": interaction.operation,
                            "mechanism": interaction.mechanism,
                            "broker_library": interaction.library,
                            "via_wrapper": interaction.via_wrapper,
                            "correlation": event.status,
                        },
                    )
                )
                flow_steps.append(publish_step)
                precedes.append(
                    (
                        dispatch_step.id,
                        publish_step.id,
                        interaction.provenance,
                        {"established_by": "publisher call site"},
                    )
                )

                # --- consumer side ----------------------------------------------------------
                bindings = consumers_by_event.get(interaction.identity, [])
                if not bindings:
                    flow_unresolved.append(f"consume:{event.identity}")
                    continue
                for binding in sorted(
                    bindings, key=lambda item: (item.service, item.provenance.source_path)
                ):
                    consumer_service = binding.service
                    flow_services.add(consumer_service)
                    handler_expression = binding.handler or ""
                    consumer_symbol = _resolve_consumer_handler(
                        index, consumer_service, binding, handler_expression
                    )
                    event_tail = normalize_dotted(event.identity)
                    consume_step = register_step(
                        FlowStepCandidate(
                            id=step_id(
                                identifier,
                                "consume",
                                f"{consumer_service}.{event_tail}",
                            ),
                            kind=FLOW_STEP_KIND,
                            title=f"{consumer_service} consumes {event.identity}",
                            role=ROLE_EVENT_CONSUME,
                            flow_id=identifier,
                            service=consumer_service,
                            service_entity_id=_service_entity(repository_slug, consumer_service),
                            anchor_id=event.id,
                            anchor_kind="Event",
                            provenance=binding.provenance,
                            attributes={
                                "event_identity": event.identity,
                                "handler_expression": handler_expression,
                                "handler_symbol": consumer_symbol,
                                "operation": binding.operation,
                            },
                        )
                    )
                    flow_steps.append(consume_step)
                    precedes.append(
                        (
                            publish_step.id,
                            consume_step.id,
                            binding.provenance,
                            {"established_by": "handler registration"},
                        )
                    )
                    if consumer_symbol is None:
                        unresolved.append(
                            UnresolvedFinding(
                                category=UNRESOLVED_CONSUMER,
                                subject=f"{event.id} -> {handler_expression}",
                                reason=(
                                    "the registered handler expression does not resolve to a "
                                    "function defined in scanned source"
                                ),
                                service=_service_entity(repository_slug, consumer_service),
                                provenance=binding.provenance,
                            )
                        )
                        flow_unresolved.append(f"consume-handler:{handler_expression}")
                        continue

                    # --- persistence side ---------------------------------------------------
                    persistence_targets = {
                        symbol
                        for (service, symbol) in accesses_by_symbol
                        if service == consumer_service
                    }
                    access_traces, access_unresolved = tracer.trace_to(
                        consumer_service, consumer_symbol, persistence_targets
                    )
                    for item in access_unresolved:
                        record_call_finding(UNRESOLVED_PERSISTENCE, event.id, item)
                    if not access_traces:
                        flow_unresolved.append(f"persistence:{event.identity}")
                        continue
                    for access_symbol in _targets_shallowest_first(access_traces):
                        best_access = access_traces[access_symbol][0]
                        for access, site in sorted(
                            accesses_by_symbol[(consumer_service, access_symbol)],
                            key=lambda pair: (pair[0].role, pair[0].target),
                        ):
                            role = (
                                ROLE_PERSISTENCE_READ
                                if access.role == "read"
                                else ROLE_PERSISTENCE_WRITE
                            )
                            token = "read" if access.role == "read" else "write"
                            prefix = (
                                "collection." if access.target_kind == "Collection" else "table."
                            )
                            flow_targets.add(access.target)
                            target_resolutions.setdefault(access.target, set()).add(
                                site.resolution
                            )
                            persistence_step = register_step(
                                FlowStepCandidate(
                                    id=step_id(
                                        identifier,
                                        token,
                                        entity_tail(access.target, prefix),
                                    ),
                                    kind=FLOW_STEP_KIND,
                                    title=f"{token} {access.target}",
                                    role=role,
                                    flow_id=identifier,
                                    service=consumer_service,
                                    service_entity_id=_service_entity(
                                        repository_slug, consumer_service
                                    ),
                                    anchor_id=access.target,
                                    anchor_kind=access.target_kind,
                                    provenance=site.provenance,
                                    traces=tuple(access_traces[access_symbol]),
                                    attributes={
                                        "operation": site.operation,
                                        "persistence_library": access.library,
                                        "resolution": site.resolution,
                                        "call_depth": best_access.depth,
                                        "event_identity": event.identity,
                                    },
                                )
                            )
                            flow_steps.append(persistence_step)
                            precedes.append(
                                (
                                    consume_step.id,
                                    persistence_step.id,
                                    site.provenance,
                                    {
                                        "established_by": "consumer call trace",
                                        "call_depth": best_access.depth,
                                    },
                                )
                            )

        # --- completeness ------------------------------------------------------------------
        has_publish = any(item.role == ROLE_EVENT_PUBLISH for item in flow_steps)
        has_consume = any(item.role == ROLE_EVENT_CONSUME for item in flow_steps)
        has_persistence = any(
            item.role in (ROLE_PERSISTENCE_READ, ROLE_PERSISTENCE_WRITE) for item in flow_steps
        )
        if not has_publish:
            completeness = COMPLETENESS_UNRESOLVED
            reason = "the handler reaches a gateway dispatch but no Event identity is proven"
        elif has_persistence and not flow_unresolved:
            completeness = COMPLETENESS_RESOLVED
            reason = "endpoint, publish, consume and persistence are all source-backed"
        elif has_consume:
            completeness = COMPLETENESS_PARTIAL
            reason = "publish and consume are proven but a later segment is unresolved"
        else:
            completeness = COMPLETENESS_PARTIAL
            reason = "publish is proven but no consumer binding exists for the identity"
        classifications.append(EndpointClassification(endpoint.id, completeness, reason))

        ordered_steps = sorted(flow_steps, key=lambda item: (item.role_rank, item.id))
        step_ids = tuple(dict.fromkeys(item.id for item in ordered_steps))
        flow = UserFlowCandidate(
            id=identifier,
            kind=USER_FLOW_KIND,
            title=f"{endpoint.method} {endpoint.effective_path} execution flow",
            endpoint_id=endpoint.id,
            http_method=endpoint.method,
            path=endpoint.effective_path,
            path_resolution=endpoint.path_resolution,
            completeness=completeness,
            handler_symbol=handler_symbol,
            services=tuple(
                sorted(_service_entity(repository_slug, item) for item in flow_services)
            ),
            events=tuple(sorted(flow_events)),
            persistence_targets=tuple(sorted(flow_targets)),
            enumerated_persistence_targets=tuple(
                sorted(
                    target
                    for target, kinds in target_resolutions.items()
                    if kinds == {ENUMERATED_RESOLUTION}
                )
            ),
            step_ids=step_ids,
            unresolved_segments=tuple(sorted(set(flow_unresolved))),
            provenance=endpoint.provenance,
            attributes={
                "step_count": len(step_ids),
                "classification_reason": reason,
                "max_call_depth": _MAX_CALL_DEPTH,
            },
        )
        flows.append(flow)

        for step in ordered_steps:
            relationships.append(
                RelationshipCandidate(
                    source=flow.id,
                    type=CONTAINS,
                    target=step.id,
                    provenance=step.provenance,
                    detail={"role": step.role},
                )
            )
            relationships.append(
                RelationshipCandidate(
                    source=step.id,
                    type=IMPLEMENTS,
                    target=step.service_entity_id,
                    provenance=step.provenance,
                    detail={"role": step.role},
                )
            )
            if step.anchor_id and step.anchor_kind:
                relationships.append(
                    RelationshipCandidate(
                        source=step.id,
                        type=DERIVED_FROM,
                        target=step.anchor_id,
                        provenance=step.provenance,
                        detail={"anchor_kind": step.anchor_kind, "role": step.role},
                    )
                )
        for source_step, target_step, provenance, detail in precedes:
            if source_step == target_step:
                continue
            relationships.append(
                RelationshipCandidate(
                    source=source_step,
                    type=PRECEDES,
                    target=target_step,
                    provenance=provenance,
                    detail=detail,
                )
            )
        for service in sorted(flow_services):
            participation.setdefault(
                (_service_entity(repository_slug, service), flow.id), []
            )

    # --- Service PARTICIPATES_IN UserFlow -------------------------------------------------
    for (service_entity, flow_identifier), traces in sorted(participation.items()):
        del traces
        anchor = next(item for item in flows if item.id == flow_identifier)
        relationships.append(
            RelationshipCandidate(
                source=service_entity,
                type=PARTICIPATES_IN,
                target=flow_identifier,
                provenance=anchor.provenance,
                detail={"completeness": anchor.completeness},
            )
        )

    cycles = _detect_cycles(relationships)
    for cycle in cycles:
        warnings.append(f"PRECEDES cycle detected and dropped: {cycle}")
    if cycles:
        cycle_edges = {edge for cycle in cycles for edge in cycle.split(" -> ")}
        relationships = [
            item
            for item in relationships
            if not (
                item.type == PRECEDES
                and item.source in cycle_edges
                and item.target in cycle_edges
            )
        ]

    return UserFlowExtraction(
        repository=repository,
        commit=commit,
        owner=record.owner,
        source_files=tuple(scanned),
        skipped_files=tuple(sorted(skipped)),
        services_scanned=tuple(sorted(_service_entity(repository_slug, item) for item in services)),
        flows=tuple(sorted(flows, key=lambda item: item.id)),
        steps=tuple(sorted(steps.values(), key=lambda item: item.id)),
        relationships=tuple(
            sorted(
                {
                    (item.source, item.type, item.target): item for item in relationships
                }.values(),
                key=lambda item: (item.source, item.type, item.target),
            )
        ),
        classifications=tuple(sorted(classifications, key=lambda item: item.endpoint_id)),
        unresolved=tuple(
            sorted(unresolved, key=lambda item: (item.category, item.subject, item.reason))
        ),
        ambiguous_call_targets=tuple(
            sorted(ambiguous, key=lambda item: (item.subject, item.reason))
        ),
        receiver_typing_gaps=tuple(
            sorted(
                tracer.receiver_gaps.values(),
                key=lambda item: (
                    item.provenance.source_path or "",
                    item.provenance.line_start or 0,
                    item.expression,
                ),
            )
        ),
        interpreted_boundary_calls=tuple(
            sorted(
                tracer.boundary_calls.values(),
                key=lambda item: (
                    item.provenance.source_path or "",
                    item.provenance.line_start or 0,
                    item.expression,
                ),
            )
        ),
        identity_collisions=tuple(sorted(set(collisions))),
        cycles_detected=tuple(sorted(cycles)),
        warnings=tuple(sorted(warnings)),
        withheld_values=frozenset(),
    )


def _resolve_consumer_handler(
    index: SourceIndex, service: str, binding: Any, handler_expression: str
) -> str | None:
    """Resolve a registered handler expression to a concrete function symbol.

    The consumer is never guessed from the event name: the expression recorded at the
    registration site is resolved in the module where the registration happens.
    """
    if not handler_expression:
        return None
    facts = _module_of_path(index, service, binding.provenance.source_path)
    if facts is None:
        return None
    parts = handler_expression.split(".")
    if len(parts) == 1:
        resolved = index.resolve_symbol(service, facts.module, parts[0])
        if resolved.kind == SYMBOL_FUNCTION and resolved.module and resolved.name:
            return f"{resolved.module}.{resolved.name}" if resolved.module else resolved.name
        return None
    owner = index.resolve_class(service, facts.module, ast.Name(id=parts[-2]))
    if owner is None:
        return None
    found = index.lookup_method(service, owner[0], owner[1], parts[-1])
    if found is None:
        return None
    owner_module, method = found
    return f"{owner_module}.{method.qualified_name}" if owner_module else method.qualified_name


def _detect_cycles(relationships: list[RelationshipCandidate]) -> list[str]:
    """Find cycles among PRECEDES edges. A proven flow DAG must not contain one."""
    graph: dict[str, set[str]] = {}
    for item in relationships:
        if item.type == PRECEDES:
            graph.setdefault(item.source, set()).add(item.target)
    cycles: list[str] = []
    state: dict[str, int] = {}

    def visit(node: str, path: list[str]) -> None:
        state[node] = 1
        for successor in sorted(graph.get(node, ())):
            if state.get(successor) == 1:
                start = path.index(successor) if successor in path else 0
                cycles.append(" -> ".join([*path[start:], successor]))
            elif state.get(successor, 0) == 0:
                visit(successor, [*path, successor])
        state[node] = 2

    for node in sorted(graph):
        if state.get(node, 0) == 0:
            visit(node, [node])
    return sorted(set(cycles))


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
    *, identifier: str, kind: str, title: str, extraction: UserFlowExtraction
) -> dict[str, Any]:
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
    }
    if extraction.owner:
        frontmatter["owner"] = extraction.owner
    return frontmatter


def _relation_entries(relations: tuple[RelationshipCandidate, ...]) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    for relation in relations:
        entry: dict[str, Any] = {"type": relation.type, "target": relation.target}
        entry.update(relation.detail)
        entry.update(relation.provenance.as_dict())
        entries.append(entry)
    return entries


def _inbound_entries(relations: tuple[RelationshipCandidate, ...]) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    for relation in relations:
        entry: dict[str, Any] = {"type": relation.type, "source": relation.source}
        entry.update(relation.detail)
        entry.update(relation.provenance.as_dict())
        entries.append(entry)
    return entries


def render_flow_markdown(flow: UserFlowCandidate, extraction: UserFlowExtraction) -> str:
    frontmatter = _base_frontmatter(
        identifier=flow.id, kind=flow.kind, title=flow.title, extraction=extraction
    )
    frontmatter["entry_endpoint"] = flow.endpoint_id
    frontmatter["http_method"] = flow.http_method
    frontmatter["path"] = flow.path
    frontmatter["path_resolution"] = flow.path_resolution
    frontmatter["completeness"] = flow.completeness
    frontmatter["handler"] = flow.handler_symbol
    frontmatter["participating_services"] = list(flow.services)
    frontmatter["events"] = list(flow.events)
    frontmatter["persistence_targets"] = list(flow.persistence_targets)
    if flow.enumerated_persistence_targets:
        frontmatter["enumerated_persistence_targets"] = list(flow.enumerated_persistence_targets)
    if flow.unresolved_segments:
        frontmatter["unresolved_segments"] = list(flow.unresolved_segments)
    frontmatter["source_refs"] = [flow.provenance.as_dict()]
    outbound = extraction.relations_for(flow.id)
    if outbound:
        frontmatter["relations"] = _relation_entries(outbound)
    inbound = extraction.inbound_relations_for(flow.id)
    if inbound:
        frontmatter["inbound_relations"] = _inbound_entries(inbound)
    frontmatter["attributes"] = flow.attributes

    body = [
        f"# {flow.title}",
        "",
        f"Candidate execution flow stitched from source-backed call evidence in "
        f"`{extraction.repository}` at commit `{extraction.commit}`.",
        "",
        f"- Entry endpoint: `{flow.endpoint_id}`",
        f"- Completeness: `{flow.completeness}`",
        f"- Handler: `{flow.handler_symbol}`",
        f"- Declared in: `{flow.provenance.source_path}` "
        f"(lines {flow.provenance.line_start}-{flow.provenance.line_end})",
        f"- Evidence class: `{EVIDENCE_TYPE}`",
        "",
        "## Steps",
        "",
    ]
    for step in extraction.steps_of(flow.id):
        body.append(f"- `{step.role}` `{step.id}`")
    body.append("")
    if flow.unresolved_segments:
        body.extend(
            [
                "## Unresolved segments",
                "",
                "This flow is not complete. The following segments could not be proven from "
                "source and are deliberately not invented:",
                "",
            ]
        )
        body.extend(f"- `{segment}`" for segment in flow.unresolved_segments)
        body.append("")
    if flow.enumerated_persistence_targets:
        body.extend(
            [
                "## Persistence targets that are not pinned by the call site",
                "",
                "The call path to these targets is proven, but the target itself comes from a "
                "generic repository that takes the model as an argument, so every mapped model "
                "is a possible target. Treat the specific target as a candidate, not a fact:",
                "",
            ]
        )
        body.extend(f"- `{target}`" for target in flow.enumerated_persistence_targets)
        body.append("")
    body.extend(
        [
            "## Review notes",
            "",
            "This page is a candidate awaiting review. Every step is backed by a bounded call "
            f"trace of at most {_MAX_CALL_DEPTH} hops; no segment was inferred from the "
            "similarity between an endpoint path and an event name.",
            "",
        ]
    )
    return _render_page(frontmatter, body)


def render_step_markdown(step: FlowStepCandidate, extraction: UserFlowExtraction) -> str:
    frontmatter = _base_frontmatter(
        identifier=step.id, kind=step.kind, title=step.title, extraction=extraction
    )
    frontmatter["role"] = step.role
    frontmatter["flow"] = step.flow_id
    frontmatter["service"] = step.service_entity_id
    if step.anchor_id:
        frontmatter["derived_from"] = step.anchor_id
        frontmatter["derived_from_kind"] = step.anchor_kind
    frontmatter["source_refs"] = [step.provenance.as_dict()]
    if step.traces:
        # Kept as separate chains: a step can be reached by more than one call path, and
        # concatenating their hops would read as one longer chain that does not exist.
        frontmatter["traces"] = [
            {
                "target": trace.target_symbol,
                "depth": trace.depth,
                "hops": trace.summary(),
            }
            for trace in step.traces
        ]
    outbound = extraction.relations_for(step.id)
    if outbound:
        frontmatter["relations"] = _relation_entries(outbound)
    inbound = extraction.inbound_relations_for(step.id)
    if inbound:
        frontmatter["inbound_relations"] = _inbound_entries(inbound)
    frontmatter["attributes"] = step.attributes

    body = [
        f"# {step.title}",
        "",
        f"Candidate execution step extracted from call evidence in `{extraction.repository}` "
        f"at commit `{extraction.commit}`.",
        "",
        f"- Role: `{step.role}`",
        f"- Flow: `{step.flow_id}`",
        f"- Performed by: `{step.service_entity_id}`",
        f"- Anchored on: `{step.anchor_id or 'none'}` (`{step.anchor_kind or 'none'}`)",
        f"- Declared in: `{step.provenance.source_path}` "
        f"(lines {step.provenance.line_start}-{step.provenance.line_end})",
        f"- Evidence class: `{EVIDENCE_TYPE}`",
        "",
    ]
    if step.traces:
        body.extend(["## Call trace", ""])
        for trace in step.traces:
            for hop in trace.hops:
                body.append(
                    f"- `{hop.caller_symbol}` -> `{hop.callee_symbol}` "
                    f"(`{hop.provenance.source_path}:{hop.provenance.line_start}`)"
                )
        body.append("")
    body.extend(
        [
            "## Review notes",
            "",
            "This page is a candidate awaiting review. The step exists because a concrete call "
            "site proves it, and its ordering edges carry that call site as evidence.",
            "",
        ]
    )
    return _render_page(frontmatter, body)


def render_all(extraction: UserFlowExtraction) -> dict[str, str]:
    rendered: dict[str, str] = {}
    for flow in extraction.flows:
        rendered[f"flows/{flow.id}.md"] = render_flow_markdown(flow, extraction)
    for step in extraction.steps:
        rendered[f"steps/{step.id}.md"] = render_step_markdown(step, extraction)
    return rendered


def build_service_relation_deltas(extraction: UserFlowExtraction) -> dict[str, Any]:
    """Additive ``Service -PARTICIPATES_IN-> UserFlow`` relations for canonical Service pages."""
    by_service: dict[str, list[RelationshipCandidate]] = {}
    for relation in extraction.relationships:
        if relation.type == PARTICIPATES_IN:
            by_service.setdefault(relation.source, []).append(relation)
    return {
        "version": 1,
        "extractor": EXTRACTOR_KIND,
        "repository": extraction.repository,
        "commit": extraction.commit,
        "status": CANDIDATE_STATUS,
        "review_status": CANDIDATE_REVIEW_STATUS,
        "mode": "additive",
        "note": (
            "Candidate additive PARTICIPATES_IN relations for existing canonical Service pages. "
            "Existing Service relationships are untouched. This file is not canonical knowledge "
            "and must not be copied into wiki/ without review."
        ),
        "services": [
            {
                "service": identifier,
                "relation_count": len(by_service[identifier]),
                "relations": [
                    relation.summary()
                    for relation in sorted(by_service[identifier], key=lambda item: item.target)
                ],
            }
            for identifier in sorted(by_service)
        ],
    }


def build_report(extraction: UserFlowExtraction, secret_values_emitted: int) -> dict[str, Any]:
    """Assemble extraction-report.json. Contains no timestamp, so runs stay comparable."""
    counts: dict[str, int] = {}
    for relation in extraction.relationships:
        counts[relation.type] = counts.get(relation.type, 0) + 1
    role_counts: dict[str, int] = {}
    for step in extraction.steps:
        role_counts[step.role] = role_counts.get(step.role, 0) + 1
    participating = sorted(
        {item.source for item in extraction.relationships if item.type == PARTICIPATES_IN}
    )

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
        "runtime_connections_opened": 0,
        "max_call_depth": _MAX_CALL_DEPTH,
        "source_files": list(extraction.source_files),
        "skipped_files": list(extraction.skipped_files),
        "services_scanned": list(extraction.services_scanned),
        "endpoints_considered": len(extraction.classifications),
        "endpoints_resolved": len(extraction.classified(COMPLETENESS_RESOLVED)),
        "endpoints_partial": len(extraction.classified(COMPLETENESS_PARTIAL)),
        "endpoints_unresolved": len(extraction.classified(COMPLETENESS_UNRESOLVED)),
        "endpoints_trivial": len(extraction.classified(COMPLETENESS_TRIVIAL)),
        "flows": [flow.summary() for flow in extraction.flows],
        "flow_steps": [step.summary() for step in extraction.steps],
        "publisher_links_resolved": role_counts.get(ROLE_EVENT_PUBLISH, 0),
        "consumer_links_resolved": role_counts.get(ROLE_EVENT_CONSUME, 0),
        "persistence_links_resolved": (
            role_counts.get(ROLE_PERSISTENCE_READ, 0) + role_counts.get(ROLE_PERSISTENCE_WRITE, 0)
        ),
        "flows_with_enumerated_persistence_targets": sorted(
            item.id for item in extraction.flows if item.enumerated_persistence_targets
        ),
        "participating_services": participating,
        "relationships": [item.summary() for item in extraction.relationships],
        "relationships_by_type": dict(sorted(counts.items())),
        "counts": {
            "source_files": len(extraction.source_files),
            "skipped_files": len(extraction.skipped_files),
            "services_scanned": len(extraction.services_scanned),
            "flows": len(extraction.flows),
            "flow_steps": len(extraction.steps),
            "steps_by_role": dict(sorted(role_counts.items())),
            "relationships": len(extraction.relationships),
            "participating_services": len(participating),
            "receiver_typing_gaps": len(extraction.receiver_typing_gaps),
            "interpreted_boundary_calls": len(extraction.interpreted_boundary_calls),
            "warnings": len(extraction.warnings),
        },
        "endpoint_classifications": [item.summary() for item in extraction.classifications],
        "unresolved_endpoint_dispatches": [
            item.summary() for item in extraction.unresolved_of(UNRESOLVED_DISPATCH)
        ],
        "unresolved_event_publishers": [
            item.summary() for item in extraction.unresolved_of(UNRESOLVED_PUBLISHER)
        ],
        "unresolved_consumer_handlers": [
            item.summary() for item in extraction.unresolved_of(UNRESOLVED_CONSUMER)
        ],
        "unresolved_persistence_segments": [
            item.summary() for item in extraction.unresolved_of(UNRESOLVED_PERSISTENCE)
        ],
        "ambiguous_call_targets": [item.summary() for item in extraction.ambiguous_call_targets],
        # Calls the contract declines to follow, listed once per call site. They are not flow
        # defects; they are the published boundary of what static tracing can claim here.
        "receiver_typing_gaps": [item.summary() for item in extraction.receiver_typing_gaps],
        # Framework calls an earlier pass already turned into an Event, Table or Collection.
        # Listed rather than dropped, so the filtering is auditable.
        "interpreted_boundary_calls": [
            item.summary() for item in extraction.interpreted_boundary_calls
        ],
        "identity_collisions": list(extraction.identity_collisions),
        "cycles_detected": list(extraction.cycles_detected),
        "warnings": list(extraction.warnings),
        "secret_values_emitted": secret_values_emitted,
        "graph_mutations": 0,
        "wiki_writes": 0,
        "neo4j_mutations": 0,
        "graphiti_mutations": 0,
        "graphiti": "disabled",
    }


def count_secret_leaks(extraction: UserFlowExtraction, rendered: dict[str, str]) -> int:
    """Measure credential leakage by whole-token match, not raw substring."""
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


def render_bundle(extraction: UserFlowExtraction) -> tuple[dict[str, str], dict[str, Any]]:
    rendered = render_all(extraction)
    provisional = build_report(extraction, 0)
    scanned = {
        **rendered,
        "extraction-report.json": render_report_json(provisional),
        SERVICE_DELTAS_FILENAME: render_report_json(build_service_relation_deltas(extraction)),
    }
    leaks = count_secret_leaks(extraction, scanned)
    return rendered, build_report(extraction, leaks)


def render_sidecars(extraction: UserFlowExtraction, report: dict[str, Any]) -> dict[str, str]:
    del report
    return {
        SERVICE_DELTAS_FILENAME: render_report_json(build_service_relation_deltas(extraction))
    }


def summarize(extraction: UserFlowExtraction, report: dict[str, Any]) -> dict[str, Any]:
    """CLI-facing summary of one extraction run."""
    return {
        "extractor": report["extractor"],
        "repository": extraction.repository,
        "commit": extraction.commit,
        "commit_verified": True,
        "analysis": "python-ast/static",
        "modules_imported": 0,
        "modules_executed": 0,
        "runtime_connections_opened": 0,
        "max_call_depth": _MAX_CALL_DEPTH,
        "source_files": list(extraction.source_files),
        "services_scanned": list(extraction.services_scanned),
        "counts": report["counts"],
        "endpoints_considered": report["endpoints_considered"],
        "endpoints_resolved": report["endpoints_resolved"],
        "endpoints_partial": report["endpoints_partial"],
        "endpoints_unresolved": report["endpoints_unresolved"],
        "endpoints_trivial": report["endpoints_trivial"],
        "publisher_links_resolved": report["publisher_links_resolved"],
        "consumer_links_resolved": report["consumer_links_resolved"],
        "persistence_links_resolved": report["persistence_links_resolved"],
        "flows_with_enumerated_persistence_targets": report[
            "flows_with_enumerated_persistence_targets"
        ],
        "participating_services": report["participating_services"],
        "relationships_by_type": report["relationships_by_type"],
        "flows": [f"{item.completeness}: {item.id}" for item in extraction.flows],
        "unresolved_endpoint_dispatches": report["unresolved_endpoint_dispatches"],
        "unresolved_event_publishers": report["unresolved_event_publishers"],
        "unresolved_consumer_handlers": report["unresolved_consumer_handlers"],
        "unresolved_persistence_segments": report["unresolved_persistence_segments"],
        "ambiguous_call_targets": report["ambiguous_call_targets"],
        "identity_collisions": report["identity_collisions"],
        "cycles_detected": report["cycles_detected"],
        "warnings": list(extraction.warnings),
        "receiver_typing_gaps": len(extraction.receiver_typing_gaps),
        "interpreted_boundary_calls": len(extraction.interpreted_boundary_calls),
        "secret_values_emitted": report["secret_values_emitted"],
        "graph_mutations": 0,
        "wiki_writes": 0,
        "neo4j_mutations": 0,
        "graphiti": "disabled",
    }
