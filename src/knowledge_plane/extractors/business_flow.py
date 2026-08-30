"""Deterministic user/business flow composition extractor (Graph Engineering Pass 6).

Scope and non-goals
-------------------
This extractor reads Vue single-file components, the Vue Router table, the Vuex store and two
gateway configuration modules, and emits *candidates* only. It never imports or executes the
inspected application, never starts a browser or a service, never opens a broker or database
connection, never writes canonical knowledge, never touches Neo4j or Graphiti, and never calls
an LLM.

What this pass adds
-------------------
Pass 5 proved one technical execution path per HTTP endpoint::

    endpoint -> service dispatch -> event -> consumer -> persistence

Each of those ``UserFlow`` pages is an island from the *user's* point of view: nothing records
that a person registers and then verifies, or that a driver logs in and the app then bootstraps
vehicle and online status. Pass 6 composes several already-approved Pass-5 ``UserFlow`` pages
into ``BusinessFlow`` journeys. It never rediscovers or duplicates the Pass-5 technical graph:
every business step is a *reference* to an existing canonical ``UserFlow`` id read from
``wiki/flows/``.

Reachability, not intent
------------------------
A route transition is usable only when the route exists, its destination view exists, the view
actually mounts the intended component, and the hook that issues the next call is reachable.
At the frozen FTGO commit ``ui/src/views/MenuPage.vue`` is empty, so the customer path stops at
the menu page and no order-placement journey is emitted. That is not a judgement about the
product; it is what the source says.

Navigation is not execution
---------------------------
Arriving on a page does not mean every request on that page fires. A destination composes
automatically only through a lifecycle hook. A destination whose next call is a user action
composes only when that call *consumes Vuex state the earlier step wrote*, which is why
``register -> verify`` is provable and ``verify -> login`` is not.

Naming versus truth
-------------------
Business journeys need names, and a name cannot be derived from source. The catalog in
:data:`HYPOTHESES` therefore declares journey identity only: the id, the title, the entry
component, the entry handler, and the branch world to follow. Everything else - the steps,
their order, their conditions, their loops, their triggers, their actors and all evidence - is
derived from source and may reject the hypothesis. A declared journey the source does not
support is reported as rejected or partial; it is never padded to look complete.
"""

from __future__ import annotations

import ast
import bisect
import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

from ..repository_manifest import (
    RepositoryManifestError,
    RepositoryRecord,
    resolve_source_files,
)
from .fastapi import Provenance

EXTRACTOR_KIND = "business-flow"
CANDIDATE_STATUS = "candidate"
CANDIDATE_REVIEW_STATUS = "pending"
EVIDENCE_TYPE = "implemented"

# Output subdirectories owned by this pass. Deliberately disjoint from the Pass-5 pair
# ("flows", "steps") so a Pass-6 run can never prune or overwrite a Pass-5 candidate.
CANDIDATE_SUBDIRECTORIES = ("business-flows", "business-steps")

# Ontology kinds used. ``BusinessFlow`` is the single kind this pass introduces; ``FlowStep``
# already exists and is reused rather than shadowed by a new "BusinessStep".
BUSINESS_FLOW_KIND = "BusinessFlow"
FLOW_STEP_KIND = "FlowStep"
USER_FLOW_KIND = "UserFlow"

# Relationship types used. All three already exist; this pass introduces none.
CONTAINS = "CONTAINS"
DERIVED_FROM = "DERIVED_FROM"
PRECEDES = "PRECEDES"

# Every business-layer FlowStep carries these two markers so a business step can never be
# mistaken for one of Pass 5's technical steps.
BUSINESS_LAYER = "business"
BUSINESS_STEP_ROLE = "user_flow_reference"

# Business-step identity namespace. ``step.business.`` cannot collide with Pass 5's
# ``step.<repo>.<service>...`` namespace, and ``business-flow.`` cannot collide with ``flow.``.
BUSINESS_FLOW_PREFIX = "business-flow"
BUSINESS_STEP_PREFIX = "step.business"
PASS5_FLOW_PREFIX = "flow."
PASS5_STEP_PREFIX = "step."
UI_SURFACE = "ui"

# Trigger classification of a business step.
TRIGGER_USER_ACTION = "user_action"
TRIGGER_AUTOMATIC = "automatic"
TRIGGER_CONDITIONAL = "conditional"
TRIGGER_LIFECYCLE = "lifecycle"

# Ordering / composition evidence mechanisms.
MECHANISM_AWAIT = "await_sequence"
MECHANISM_THEN = "then_sequence"
MECHANISM_HELPER = "helper_call"
MECHANISM_NAVIGATION = "route_navigation"
MECHANISM_LIFECYCLE = "lifecycle_hook"
MECHANISM_VUEX = "vuex_dependency"
MECHANISM_ROLE_BRANCH = "role_branch"
MECHANISM_CONDITIONAL = "conditional_branch"
MECHANISM_INTERVAL = "interval_loop"
MECHANISM_ENTRY = "template_binding"

# Hypothesis outcomes.
OUTCOME_RESOLVED = "resolved"
OUTCOME_PARTIAL = "partial"
OUTCOME_REJECTED = "rejected"

# A BusinessFlow must compose at least two distinct existing Pass-5 UserFlows. A single
# request is already fully described by its Pass-5 page and adds nothing as a journey.
MIN_USER_FLOWS_PER_BUSINESS_FLOW = 2

# Bounded traversal. Deliberately small: this is static composition, not program simulation.
_MAX_HELPER_DEPTH = 4
_MAX_NAVIGATION_HOPS = 4
_MAX_CHAIN_STEPS = 12
_MAX_ACTOR_TRACE_DEPTH = 6
_MAX_EXPRESSION_LENGTH = 160

# Manifest source kinds this pass reads.
FRONTEND_SOURCE_KIND = "frontend"
CODE_SOURCE_KIND = "code"

# Frontend layout at the frozen commit. These are matched exactly, never by fuzzy search.
UI_ROOT = "ui/src"
COMPONENTS_DIR = f"{UI_ROOT}/components"
VIEWS_DIR = f"{UI_ROOT}/views"
ROUTER_PATH = f"{UI_ROOT}/router/index.js"
STORE_PATH = f"{UI_ROOT}/store/index.js"
VUE_SUFFIX = ".vue"
JS_SUFFIX = ".js"

# Gateway modules that make the ``/api/v1`` prefix a source-backed fact rather than a guess.
GATEWAY_SERVICE_CONFIG_PATH = "backend/gateway/src/config/service.py"
GATEWAY_MAIN_PATH = "backend/gateway/src/main.py"
API_PREFIX_ENV_NAME = "API_PREFIX"

# Canonical Pass-5 UserFlow pages. Reused, never regenerated.
CANONICAL_FLOWS_DIR = "wiki/flows"

HTTP_METHODS: frozenset[str] = frozenset({"get", "post", "put", "delete", "patch"})
AXIOS_RECEIVERS: frozenset[str] = frozenset({"axios", "Vue.axios", "this.axios", "this.$http"})
LIFECYCLE_HOOKS: tuple[str, ...] = ("created", "mounted")
ROUTER_PUSH = "this.$router.push"
NON_STATIC_NAVIGATION: frozenset[str] = frozenset(
    {"this.$router.go", "this.$router.back", "this.$router.replace", "this.$router.forward"}
)
INTERVAL_CALLS: frozenset[str] = frozenset({"setInterval", "window.setInterval"})
CONFIRM_CALLS: frozenset[str] = frozenset({"confirm", "window.confirm"})

_IDENTIFIER = re.compile(r"[A-Za-z_$][A-Za-z0-9_$]*")
_NUMBER = re.compile(r"[0-9][0-9_]*")
_JS_KEYWORDS_SKIPPED: frozenset[str] = frozenset(
    {
        "break",
        "case",
        "continue",
        "default",
        "delete",
        "in",
        "instanceof",
        "new",
        "of",
        "return",
        "throw",
        "typeof",
        "void",
        "yield",
    }
)
_DECLARATION_KEYWORDS: frozenset[str] = frozenset({"const", "let", "var"})

# Template event bindings that prove a handler is reachable from the rendered component.
_EVENT_BINDING = re.compile(
    r"""(?:@|v-on:)([A-Za-z][\w.:-]*)\s*=\s*(?P<q>["'])(?P<body>.*?)(?P=q)""",
    re.DOTALL,
)
_TEMPLATE_OPEN = re.compile(r"<template(?=[\s>])", re.IGNORECASE)
_TEMPLATE_CLOSE = re.compile(r"</template\s*>", re.IGNORECASE)
_SCRIPT_OPEN = re.compile(r"<script(?P<attrs>[^>]*)>", re.IGNORECASE)
_SCRIPT_CLOSE = re.compile(r"</script\s*>", re.IGNORECASE)


class BusinessFlowExtractionError(RepositoryManifestError):
    """Raised when Pass 6 cannot run at all, for example when Pass 5 output is missing."""


# ---------------------------------------------------------------------------------------
# Identity helpers
# ---------------------------------------------------------------------------------------


def normalize_slug(value: str) -> str:
    """Lowercase a token and reduce every non-alphanumeric run to a single dash."""
    lowered = re.sub(r"[^A-Za-z0-9]+", "-", str(value).strip().lower())
    return lowered.strip("-")


def business_flow_id(repository: str, journey_slug: str, *, surface: str = UI_SURFACE) -> str:
    """``business-flow.<repo>.<surface>.<journey>`` - disjoint from Pass 5's ``flow.`` space."""
    return f"{BUSINESS_FLOW_PREFIX}.{normalize_slug(repository)}.{surface}.{journey_slug}"


def business_step_id(repository: str, journey_slug: str, step_slug: str) -> str:
    """``step.business.<repo>.<journey>.<step>`` - disjoint from Pass 5's ``step.`` space."""
    return f"{BUSINESS_STEP_PREFIX}.{normalize_slug(repository)}.{journey_slug}.{step_slug}"


def journey_slug_of(identifier: str) -> str:
    """Recover the journey slug from a BusinessFlow id."""
    tail = identifier.removeprefix(f"{BUSINESS_FLOW_PREFIX}.")
    parts = tail.split(".")
    return ".".join(parts[2:]) if len(parts) > 2 else tail


def collides_with_pass5(identifier: str) -> bool:
    """True when an id would land in a namespace Pass 5 owns."""
    if identifier.startswith(BUSINESS_STEP_PREFIX) or identifier.startswith(BUSINESS_FLOW_PREFIX):
        return False
    return identifier.startswith(PASS5_FLOW_PREFIX) or identifier.startswith(PASS5_STEP_PREFIX)


def user_flow_step_slug(user_flow_id: str) -> tuple[str, str]:
    """Split a Pass-5 UserFlow id into ``(resource, action)`` slug parts.

    ``flow.ftgo.gateway.post.menu.get-all-menu-item`` -> ``("menu", "get-all-menu-item")``.
    The action alone is preferred for step ids; the resource qualifies it on collision.
    """
    parts = user_flow_id.split(".")
    if len(parts) < 2:
        return "", normalize_slug(user_flow_id)
    action = parts[-1]
    resource = parts[-2] if len(parts) >= 3 else ""
    return normalize_slug(resource), normalize_slug(action)


# ---------------------------------------------------------------------------------------
# Source text: line index, masking, and balanced-span scanning
# ---------------------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class SourceText:
    """One source file plus a masked twin used for structural scanning.

    In the masked twin every comment character and every string *content* character is a
    space, so brace, paren and bracket matching cannot be derailed by punctuation inside a
    string or a comment. Quote characters themselves are preserved, which is what lets a
    literal be recovered from the original text by span.
    """

    relative_path: str
    text: str
    masked: str
    line_offsets: tuple[int, ...]

    def line_of(self, index: int) -> int:
        return bisect.bisect_right(self.line_offsets, max(index, 0))

    def slice(self, start: int, end: int) -> str:
        return self.text[start:end]

    def collapsed(self, start: int, end: int) -> str:
        collapsed = " ".join(self.text[start:end].split())
        return collapsed[:_MAX_EXPRESSION_LENGTH]


def _line_offsets(text: str) -> tuple[int, ...]:
    offsets = [0]
    for index, character in enumerate(text):
        if character == "\n":
            offsets.append(index + 1)
    return tuple(offsets)


def mask_javascript(text: str, regions: tuple[tuple[int, int], ...] | None = None) -> str:
    """Blank comments and string contents inside ``regions`` (default: the whole text).

    Everything outside a region becomes spaces so an HTML template in a ``.vue`` file cannot
    contribute braces or quotes to the structural scan of its ``<script>`` block.
    """
    length = len(text)
    spans = regions if regions is not None else ((0, length),)
    masked = [" "] * length
    for character_index, character in enumerate(text):
        if character == "\n":
            masked[character_index] = "\n"
    for start, end in spans:
        index = start
        while index < end:
            character = text[index]
            if character == "/" and index + 1 < end and text[index + 1] == "/":
                while index < end and text[index] != "\n":
                    masked[index] = " "
                    index += 1
                continue
            if character == "/" and index + 1 < end and text[index + 1] == "*":
                masked[index] = " "
                index += 1
                while index < end and not (
                    text[index] == "*" and text[index + 1 : index + 2] == "/"
                ):
                    masked[index] = " " if text[index] != "\n" else "\n"
                    index += 1
                while index < end and text[index] != "/":
                    masked[index] = " "
                    index += 1
                if index < end:
                    masked[index] = " "
                    index += 1
                continue
            if character in "'\"`":
                masked[index] = character
                quote = character
                index += 1
                while index < end:
                    current = text[index]
                    if current == "\\":
                        masked[index] = " "
                        index += 1
                        if index < end:
                            masked[index] = " " if text[index] != "\n" else "\n"
                            index += 1
                        continue
                    if current == quote:
                        masked[index] = quote
                        index += 1
                        break
                    masked[index] = " " if current != "\n" else "\n"
                    index += 1
                continue
            masked[index] = character
            index += 1
    return "".join(masked)


def skip_space(masked: str, index: int, end: int) -> int:
    while index < end and masked[index].isspace():
        index += 1
    return index


def match_pair(masked: str, index: int, end: int) -> int:
    """Index of the delimiter matching the one at ``index``, or ``-1`` when unbalanced."""
    pairs = {"(": ")", "{": "}", "[": "]"}
    opening = masked[index]
    closing = pairs.get(opening)
    if closing is None:
        return -1
    depth = 0
    cursor = index
    while cursor < end:
        character = masked[cursor]
        if character == opening:
            depth += 1
        elif character == closing:
            depth -= 1
            if depth == 0:
                return cursor
        cursor += 1
    return -1


def read_identifier(masked: str, index: int, end: int) -> str | None:
    match = _IDENTIFIER.match(masked, index, end)
    return match.group(0) if match else None


def split_top_level(
    masked: str, start: int, end: int, separator: str = ","
) -> list[tuple[int, int]]:
    """Split ``[start, end)`` on ``separator`` occurrences that are not nested."""
    spans: list[tuple[int, int]] = []
    depth = 0
    segment_start = start
    cursor = start
    while cursor < end:
        character = masked[cursor]
        if character in "({[":
            depth += 1
        elif character in ")}]":
            depth -= 1
        elif character == separator and depth == 0:
            spans.append((segment_start, cursor))
            segment_start = cursor + 1
        cursor += 1
    spans.append((segment_start, end))
    return [(a, b) for a, b in spans if masked[a:b].strip()]


def find_top_level(masked: str, start: int, end: int, needle: str) -> int:
    """First index of ``needle`` in ``[start, end)`` at nesting depth zero, else ``-1``."""
    depth = 0
    cursor = start
    while cursor < end:
        character = masked[cursor]
        if character in "({[":
            depth += 1
        elif character in ")}]":
            depth -= 1
        elif depth == 0 and masked.startswith(needle, cursor):
            return cursor
        cursor += 1
    return -1


def string_literal_at(source: SourceText, start: int, end: int) -> str | None:
    """Return the single string literal filling ``[start, end)``, else ``None``."""
    cursor = skip_space(source.masked, start, end)
    if cursor >= end or source.masked[cursor] not in "'\"`":
        return None
    quote = source.masked[cursor]
    closing = source.masked.find(quote, cursor + 1, end)
    if closing == -1:
        return None
    if skip_space(source.masked, closing + 1, end) != end:
        return None
    raw = source.text[cursor + 1 : closing]
    if quote == "`" and "${" in raw:
        return None
    return raw


def number_literal_at(source: SourceText, start: int, end: int) -> int | None:
    text = source.masked[start:end].strip()
    if not _NUMBER.fullmatch(text):
        return None
    return int(text.replace("_", ""))


# ---------------------------------------------------------------------------------------
# Vue single-file component blocks
# ---------------------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class ScriptBlock:
    start: int
    end: int
    is_setup: bool

    @property
    def is_empty(self) -> bool:
        return self.end <= self.start


def extract_script_blocks(text: str) -> tuple[ScriptBlock, ...]:
    """Locate every ``<script>`` body in a single-file component, in source order."""
    blocks: list[ScriptBlock] = []
    cursor = 0
    while True:
        opening = _SCRIPT_OPEN.search(text, cursor)
        if opening is None:
            break
        closing = _SCRIPT_CLOSE.search(text, opening.end())
        if closing is None:
            break
        blocks.append(
            ScriptBlock(
                start=opening.end(),
                end=closing.start(),
                is_setup="setup" in opening.group("attrs").split(),
            )
        )
        cursor = closing.end()
    return tuple(blocks)


def extract_template_block(text: str) -> tuple[int, int] | None:
    """Locate the outermost ``<template>`` body, skipping nested scoped-slot templates."""
    opening = _TEMPLATE_OPEN.search(text)
    if opening is None:
        return None
    body_start = text.find(">", opening.end() - 1)
    if body_start == -1:
        return None
    body_start += 1
    depth = 1
    cursor = body_start
    while cursor < len(text):
        next_open = _TEMPLATE_OPEN.search(text, cursor)
        next_close = _TEMPLATE_CLOSE.search(text, cursor)
        if next_close is None:
            return None
        if next_open is not None and next_open.start() < next_close.start():
            depth += 1
            cursor = next_open.end()
            continue
        depth -= 1
        if depth == 0:
            return body_start, next_close.start()
        cursor = next_close.end()
    return None


def build_source_text(relative_path: str, text: str) -> SourceText:
    """Mask a source file, restricting JavaScript masking to its script regions."""
    normalized = text.replace("\r\n", "\n").replace("\r", "\n")
    if relative_path.endswith(VUE_SUFFIX):
        regions = tuple((block.start, block.end) for block in extract_script_blocks(normalized))
    else:
        regions = ((0, len(normalized)),)
    return SourceText(
        relative_path=relative_path,
        text=normalized,
        masked=mask_javascript(normalized, regions),
        line_offsets=_line_offsets(normalized),
    )


# ---------------------------------------------------------------------------------------
# Object-literal members
# ---------------------------------------------------------------------------------------

MEMBER_METHOD = "method"
MEMBER_VALUE = "value"
MEMBER_SPREAD = "spread"
MEMBER_SHORTHAND = "shorthand"


@dataclass(frozen=True, slots=True)
class ObjectMember:
    """One depth-one entry of an object literal."""

    key: str
    kind: str
    value_start: int
    value_end: int
    body_start: int
    body_end: int
    is_async: bool
    line: int
    end_line: int


def object_members(source: SourceText, brace_index: int) -> tuple[ObjectMember, ...]:
    """Enumerate the depth-one members of the object literal opening at ``brace_index``."""
    masked = source.masked
    closing = match_pair(masked, brace_index, len(masked))
    if closing == -1:
        return ()
    members: list[ObjectMember] = []
    cursor = brace_index + 1
    while cursor < closing:
        cursor = skip_space(masked, cursor, closing)
        if cursor >= closing:
            break
        if masked[cursor] in ",;":
            cursor += 1
            continue
        if masked.startswith("...", cursor):
            value_end = _member_value_end(masked, cursor, closing)
            members.append(
                _member(source, "...", MEMBER_SPREAD, cursor, value_end, cursor, value_end, False)
            )
            cursor = value_end
            continue
        is_async = False
        key_start = cursor
        key = read_identifier(masked, cursor, closing)
        if key == "async":
            after = skip_space(masked, cursor + len(key), closing)
            following = read_identifier(masked, after, closing)
            if following is not None:
                is_async = True
                cursor = after
                key_start = after
                key = following
        if key is None:
            literal_end = _quoted_key_end(source, cursor, closing)
            if literal_end is None:
                cursor += 1
                continue
            key = source.text[cursor + 1 : literal_end - 1]
            cursor = literal_end
        else:
            cursor += len(key)
        after_key = skip_space(masked, cursor, closing)
        if after_key < closing and masked[after_key] == "(":
            params_end = match_pair(masked, after_key, closing + 1)
            if params_end == -1:
                break
            body_open = skip_space(masked, params_end + 1, closing)
            if body_open < closing and masked[body_open] == "{":
                body_close = match_pair(masked, body_open, closing + 1)
                if body_close == -1:
                    break
                members.append(
                    _member(
                        source,
                        key,
                        MEMBER_METHOD,
                        key_start,
                        body_close + 1,
                        body_open + 1,
                        body_close,
                        is_async,
                    )
                )
                cursor = body_close + 1
                continue
            cursor = params_end + 1
            continue
        if after_key < closing and masked[after_key] == ":":
            value_start = skip_space(masked, after_key + 1, closing)
            value_end = _member_value_end(masked, value_start, closing)
            body = _function_value_body(source, value_start, value_end)
            members.append(
                _member(
                    source,
                    key,
                    MEMBER_METHOD if body is not None else MEMBER_VALUE,
                    value_start,
                    value_end,
                    body[0] if body else value_start,
                    body[1] if body else value_end,
                    _is_async_value(source, value_start, value_end),
                )
            )
            cursor = value_end
            continue
        members.append(
            _member(
                source, key, MEMBER_SHORTHAND, key_start, after_key, key_start, after_key, False
            )
        )
        cursor = after_key
    return tuple(members)


def _member(
    source: SourceText,
    key: str,
    kind: str,
    value_start: int,
    value_end: int,
    body_start: int,
    body_end: int,
    is_async: bool,
) -> ObjectMember:
    return ObjectMember(
        key=key,
        kind=kind,
        value_start=value_start,
        value_end=value_end,
        body_start=body_start,
        body_end=body_end,
        is_async=is_async,
        line=source.line_of(value_start),
        end_line=source.line_of(max(value_end - 1, value_start)),
    )


def _member_value_end(masked: str, start: int, limit: int) -> int:
    depth = 0
    cursor = start
    while cursor < limit:
        character = masked[cursor]
        if character in "({[":
            depth += 1
        elif character in ")}]":
            if depth == 0:
                return cursor
            depth -= 1
        elif character == "," and depth == 0:
            return cursor
        cursor += 1
    return limit


def _quoted_key_end(source: SourceText, index: int, limit: int) -> int | None:
    if source.masked[index] not in "'\"":
        return None
    quote = source.masked[index]
    closing = source.masked.find(quote, index + 1, limit)
    return None if closing == -1 else closing + 1


def _is_async_value(source: SourceText, start: int, end: int) -> bool:
    return read_identifier(source.masked, skip_space(source.masked, start, end), end) == "async"


def _function_value_body(source: SourceText, start: int, end: int) -> tuple[int, int] | None:
    """Body span of ``function (...) {...}`` or ``(...) => {...}`` filling ``[start, end)``."""
    masked = source.masked
    cursor = skip_space(masked, start, end)
    word = read_identifier(masked, cursor, end)
    if word == "async":
        cursor = skip_space(masked, cursor + len(word), end)
        word = read_identifier(masked, cursor, end)
    if word == "function":
        cursor = skip_space(masked, cursor + len(word), end)
        name = read_identifier(masked, cursor, end)
        if name:
            cursor = skip_space(masked, cursor + len(name), end)
    arrow = find_top_level(masked, cursor, end, "=>")
    if word != "function" and arrow == -1:
        return None
    if arrow != -1:
        body = skip_space(masked, arrow + 2, end)
        if body < end and masked[body] == "{":
            closing = match_pair(masked, body, end + 1)
            if closing != -1:
                return body + 1, closing
        return body, end
    if cursor < end and masked[cursor] == "(":
        params_end = match_pair(masked, cursor, end + 1)
        if params_end == -1:
            return None
        body = skip_space(masked, params_end + 1, end)
        if body < end and masked[body] == "{":
            closing = match_pair(masked, body, end + 1)
            if closing != -1:
                return body + 1, closing
    return None


def spread_helper_names(source: SourceText, member: ObjectMember) -> tuple[str, tuple[str, ...]]:
    """Read ``...mapActions(['a', 'b'])`` into ``("mapActions", ("a", "b"))``."""
    masked = source.masked
    cursor = skip_space(masked, member.value_start + 3, member.value_end)
    helper = read_identifier(masked, cursor, member.value_end)
    if helper is None:
        return "", ()
    cursor = skip_space(masked, cursor + len(helper), member.value_end)
    if cursor >= member.value_end or masked[cursor] != "(":
        return helper, ()
    args_end = match_pair(masked, cursor, member.value_end + 1)
    if args_end == -1:
        return helper, ()
    inner = skip_space(masked, cursor + 1, args_end)
    if inner < args_end and masked[inner] == "[":
        list_end = match_pair(masked, inner, args_end + 1)
        if list_end == -1:
            return helper, ()
        names = [
            string_literal_at(source, start, end)
            for start, end in split_top_level(masked, inner + 1, list_end)
        ]
        return helper, tuple(name for name in names if name)
    return helper, ()


# ---------------------------------------------------------------------------------------
# Handler operations
# ---------------------------------------------------------------------------------------

OP_API = "api_call"
OP_API_UNRESOLVED = "api_call_unresolved"
OP_THIS_CALL = "this_call"
OP_INTERVAL = "interval"
OP_NAVIGATION = "navigation"
OP_NAVIGATION_UNRESOLVED = "navigation_unresolved"

CONDITION_IF = "if"
CONDITION_ELSE = "else"
CONDITION_SWITCH_CASE = "switch_case"
CONDITION_SWITCH_DEFAULT = "switch_default"
CONDITION_CONFIRM = "confirmation_guard"


@dataclass(frozen=True, slots=True)
class Condition:
    """One guard that encloses an operation, kept as written in source."""

    text: str
    kind: str
    subject: str | None = None
    literal: str | None = None
    excluded_literal: str | None = None

    def summary(self) -> dict[str, Any]:
        payload: dict[str, Any] = {"condition": self.text, "kind": self.kind}
        if self.subject:
            payload["subject"] = self.subject
        if self.literal is not None:
            payload["literal"] = self.literal
        if self.excluded_literal is not None:
            payload["excluded_literal"] = self.excluded_literal
        return payload


@dataclass(frozen=True, slots=True)
class Operation:
    """One operation a handler performs, in source order."""

    kind: str
    line: int
    end_line: int
    awaited: bool
    conditions: tuple[Condition, ...]
    loop_interval_ms: int | None
    expression: str
    http_method: str | None = None
    url: str | None = None
    url_candidates: tuple[str, ...] = ()
    target: str | None = None
    route_path: str | None = None
    route_name: str | None = None
    reason: str | None = None
    then_operations: tuple[Operation, ...] = ()


@dataclass(frozen=True, slots=True)
class HandlerScan:
    """The declaration facts and operation list of one component function."""

    name: str
    line: int
    end_line: int
    is_async: bool
    body_start: int
    body_end: int
    operations: tuple[Operation, ...]


def _condition_from_expression(source: SourceText, start: int, end: int, kind: str) -> Condition:
    text = source.collapsed(start, end)
    masked = source.masked
    subject: str | None = None
    literal: str | None = None
    for operator in ("===", "=="):
        position = find_top_level(masked, start, end, operator)
        if position == -1:
            continue
        left = source.collapsed(start, position)
        right_literal = string_literal_at(source, position + len(operator), end)
        if right_literal is not None:
            subject, literal = left, right_literal
            break
        left_literal = string_literal_at(source, start, position)
        if left_literal is not None:
            subject, literal = source.collapsed(position + len(operator), end), left_literal
            break
    if any(
        find_top_level(masked, start, end, f"{name}(") != -1 for name in sorted(CONFIRM_CALLS)
    ):
        kind = CONDITION_CONFIRM
    return Condition(text=text, kind=kind, subject=subject, literal=literal)


def _member_expression(masked: str, index: int, end: int) -> tuple[str, int]:
    """Read a dotted member expression starting at ``index``; returns ``(text, next)``."""
    parts: list[str] = []
    cursor = index
    while cursor < end:
        identifier = read_identifier(masked, cursor, end)
        if identifier is None:
            break
        parts.append(identifier)
        cursor += len(identifier)
        lookahead = skip_space(masked, cursor, end)
        if lookahead < end and masked[lookahead] == "." and not masked.startswith("...", lookahead):
            cursor = skip_space(masked, lookahead + 1, end)
            continue
        cursor = lookahead
        break
    return ".".join(parts), cursor


@dataclass(slots=True)
class _ScanState:
    """Mutable per-function scanning state: local declarations used for URL resolution."""

    declarations: dict[str, tuple[int, int]] = field(default_factory=dict)
    ambiguous: set[str] = field(default_factory=set)


def _collect_declarations(source: SourceText, start: int, end: int) -> _ScanState:
    """Record ``const|let|var NAME = <expr>`` spans so an indirect URL can be resolved."""
    state = _ScanState()
    masked = source.masked
    declaration = re.compile(r"\b(?:const|let|var)\s+([A-Za-z_$][A-Za-z0-9_$]*)\s*=")
    for match in declaration.finditer(masked[start:end]):
        name = match.group(1)
        value_start = start + match.end()
        value_end = _declaration_value_end(masked, value_start, end)
        if name in state.declarations:
            state.ambiguous.add(name)
            continue
        state.declarations[name] = (value_start, value_end)
    return state


def _declaration_value_end(masked: str, start: int, limit: int) -> int:
    """End of a declaration's initializer, terminated only by a top-level semicolon.

    A newline cannot terminate it: a conditional URL is routinely written across three lines,
    and stopping at the first newline would hide the branch and report the request as opaque.
    An initializer that really has no semicolon over-extends, which the literal and conditional
    readers both reject, so the request is reported unresolved rather than misread.
    """
    depth = 0
    cursor = start
    while cursor < limit:
        character = masked[cursor]
        if character in "({[":
            depth += 1
        elif character in ")}]":
            if depth == 0:
                return cursor
            depth -= 1
        elif character == ";" and depth == 0:
            return cursor
        cursor += 1
    return limit


def _statement_end(masked: str, start: int, limit: int) -> int:
    depth = 0
    cursor = start
    while cursor < limit:
        character = masked[cursor]
        if character in "({[":
            depth += 1
        elif character in ")}]":
            if depth == 0:
                return cursor
            depth -= 1
        elif character in ";\n" and depth == 0:
            return cursor
        cursor += 1
    return limit


def scan_handler(source: SourceText, name: str, member: ObjectMember) -> HandlerScan:
    """Scan one component function into an ordered operation list."""
    state = _collect_declarations(source, member.body_start, member.body_end)
    operations = _scan_statements(source, member.body_start, member.body_end, (), None, state)
    return HandlerScan(
        name=name,
        line=member.line,
        end_line=member.end_line,
        is_async=member.is_async,
        body_start=member.body_start,
        body_end=member.body_end,
        operations=operations,
    )


def _scan_statements(
    source: SourceText,
    start: int,
    end: int,
    conditions: tuple[Condition, ...],
    loop_interval_ms: int | None,
    state: _ScanState,
) -> tuple[Operation, ...]:
    masked = source.masked
    operations: list[Operation] = []
    cursor = start
    awaited = False
    guard = 0
    while cursor < end and guard < 100_000:
        guard += 1
        cursor = skip_space(masked, cursor, end)
        if cursor >= end:
            break
        character = masked[cursor]
        if character in ";,":
            cursor += 1
            awaited = False
            continue
        if character == "{":
            closing = match_pair(masked, cursor, end + 1)
            if closing == -1:
                break
            operations.extend(
                _scan_statements(source, cursor + 1, closing, conditions, loop_interval_ms, state)
            )
            cursor = closing + 1
            continue
        if character == "}":
            break
        word = read_identifier(masked, cursor, end)
        if word is None:
            cursor += 1
            continue
        if word == "await":
            awaited = True
            cursor += len(word)
            continue
        if word == "async":
            cursor += len(word)
            continue
        if word in _DECLARATION_KEYWORDS or word in _JS_KEYWORDS_SKIPPED:
            cursor += len(word)
            continue
        if word in ("function", "class"):
            brace = masked.find("{", cursor, end)
            closing = match_pair(masked, brace, end + 1) if brace != -1 else -1
            cursor = closing + 1 if closing != -1 else end
            continue
        if word == "if":
            cursor, produced = _scan_if(
                source, cursor, end, conditions, loop_interval_ms, state
            )
            operations.extend(produced)
            awaited = False
            continue
        if word == "try":
            cursor, produced = _scan_try(
                source, cursor, end, conditions, loop_interval_ms, state
            )
            operations.extend(produced)
            awaited = False
            continue
        if word in ("catch", "finally"):
            cursor = _skip_guarded_block(masked, cursor + len(word), end)
            continue
        if word == "switch":
            cursor, produced = _scan_switch(
                source, cursor, end, conditions, loop_interval_ms, state
            )
            operations.extend(produced)
            awaited = False
            continue
        if word in ("for", "while", "do"):
            cursor, produced = _scan_plain_loop(
                source, cursor + len(word), end, conditions, loop_interval_ms, state
            )
            operations.extend(produced)
            awaited = False
            continue
        cursor, produced = _scan_expression(
            source, cursor, end, conditions, loop_interval_ms, state, awaited
        )
        operations.extend(produced)
        awaited = False
    return tuple(operations)


def _skip_guarded_block(masked: str, index: int, end: int) -> int:
    cursor = skip_space(masked, index, end)
    if cursor < end and masked[cursor] == "(":
        closing = match_pair(masked, cursor, end + 1)
        cursor = closing + 1 if closing != -1 else end
    cursor = skip_space(masked, cursor, end)
    if cursor < end and masked[cursor] == "{":
        closing = match_pair(masked, cursor, end + 1)
        return closing + 1 if closing != -1 else end
    return cursor


def _branch_body(
    source: SourceText,
    index: int,
    end: int,
    conditions: tuple[Condition, ...],
    loop_interval_ms: int | None,
    state: _ScanState,
) -> tuple[int, tuple[Operation, ...]]:
    masked = source.masked
    cursor = skip_space(masked, index, end)
    if cursor < end and masked[cursor] == "{":
        closing = match_pair(masked, cursor, end + 1)
        if closing == -1:
            return end, ()
        return closing + 1, _scan_statements(
            source, cursor + 1, closing, conditions, loop_interval_ms, state
        )
    statement_end = _statement_end(masked, cursor, end)
    return statement_end, _scan_statements(
        source, cursor, statement_end, conditions, loop_interval_ms, state
    )


def _scan_if(
    source: SourceText,
    index: int,
    end: int,
    conditions: tuple[Condition, ...],
    loop_interval_ms: int | None,
    state: _ScanState,
) -> tuple[int, tuple[Operation, ...]]:
    masked = source.masked
    cursor = skip_space(masked, index + len("if"), end)
    if cursor >= end or masked[cursor] != "(":
        return cursor, ()
    closing = match_pair(masked, cursor, end + 1)
    if closing == -1:
        return end, ()
    condition = _condition_from_expression(source, cursor + 1, closing, CONDITION_IF)
    cursor, produced = _branch_body(
        source, closing + 1, end, (*conditions, condition), loop_interval_ms, state
    )
    operations = list(produced)
    lookahead = skip_space(masked, cursor, end)
    if read_identifier(masked, lookahead, end) == "else":
        negated = Condition(
            text=f"!({condition.text})",
            kind=CONDITION_ELSE,
            subject=condition.subject,
            literal=None,
            excluded_literal=condition.literal,
        )
        after_else = skip_space(masked, lookahead + len("else"), end)
        if read_identifier(masked, after_else, end) == "if":
            cursor, nested = _scan_if(
                source, after_else, end, (*conditions, negated), loop_interval_ms, state
            )
            operations.extend(nested)
        else:
            cursor, nested = _branch_body(
                source, after_else, end, (*conditions, negated), loop_interval_ms, state
            )
            operations.extend(nested)
    return cursor, tuple(operations)


def _scan_try(
    source: SourceText,
    index: int,
    end: int,
    conditions: tuple[Condition, ...],
    loop_interval_ms: int | None,
    state: _ScanState,
) -> tuple[int, tuple[Operation, ...]]:
    """Scan the success path only: a ``catch`` body is failure handling, not the journey."""
    masked = source.masked
    cursor = skip_space(masked, index + len("try"), end)
    if cursor >= end or masked[cursor] != "{":
        return cursor, ()
    closing = match_pair(masked, cursor, end + 1)
    if closing == -1:
        return end, ()
    operations = _scan_statements(
        source, cursor + 1, closing, conditions, loop_interval_ms, state
    )
    cursor = closing + 1
    while True:
        lookahead = skip_space(masked, cursor, end)
        word = read_identifier(masked, lookahead, end)
        if word not in ("catch", "finally"):
            break
        cursor = _skip_guarded_block(masked, lookahead + len(word), end)
    return cursor, operations


def _scan_switch(
    source: SourceText,
    index: int,
    end: int,
    conditions: tuple[Condition, ...],
    loop_interval_ms: int | None,
    state: _ScanState,
) -> tuple[int, tuple[Operation, ...]]:
    masked = source.masked
    cursor = skip_space(masked, index + len("switch"), end)
    if cursor >= end or masked[cursor] != "(":
        return cursor, ()
    discriminant_end = match_pair(masked, cursor, end + 1)
    if discriminant_end == -1:
        return end, ()
    discriminant = source.collapsed(cursor + 1, discriminant_end)
    body_open = skip_space(masked, discriminant_end + 1, end)
    if body_open >= end or masked[body_open] != "{":
        return body_open, ()
    body_close = match_pair(masked, body_open, end + 1)
    if body_close == -1:
        return end, ()
    labels = _switch_labels(source, body_open + 1, body_close)
    operations: list[Operation] = []
    for label_start, label_end, segment_start, segment_end in labels:
        literal = string_literal_at(source, label_start, label_end)
        if label_start == label_end:
            condition = Condition(
                text=f"{discriminant} matches no declared case",
                kind=CONDITION_SWITCH_DEFAULT,
                subject=discriminant,
                literal=None,
            )
        else:
            condition = Condition(
                text=f"{discriminant} === {source.collapsed(label_start, label_end)}",
                kind=CONDITION_SWITCH_CASE,
                subject=discriminant,
                literal=literal,
            )
        nested = (*conditions, condition)
        operations.extend(
            _scan_statements(source, segment_start, segment_end, nested, loop_interval_ms, state)
        )
    return body_close + 1, tuple(operations)


def _switch_labels(
    source: SourceText, start: int, end: int
) -> tuple[tuple[int, int, int, int], ...]:
    """Return ``(label_start, label_end, body_start, body_end)`` per case, in source order.

    A ``default`` label yields an empty label span, which the caller renders as
    "matches no declared case" so a default branch is never confused with a literal case.
    """
    masked = source.masked
    markers: list[tuple[int, int, int]] = []
    depth = 0
    cursor = start
    while cursor < end:
        character = masked[cursor]
        if character in "({[":
            depth += 1
        elif character in ")}]":
            depth -= 1
        elif depth == 0:
            word = read_identifier(masked, cursor, end)
            if word in ("case", "default") and (
                cursor == start or not (masked[cursor - 1].isalnum() or masked[cursor - 1] == "_")
            ):
                label_start = skip_space(masked, cursor + len(word), end)
                colon = find_top_level(masked, label_start, end, ":")
                if colon != -1:
                    if word == "default":
                        markers.append((label_start, label_start, colon + 1))
                    else:
                        markers.append((label_start, colon, colon + 1))
                    cursor = colon + 1
                    continue
        cursor += 1
    labels: list[tuple[int, int, int, int]] = []
    for position, (label_start, label_end, body_start) in enumerate(markers):
        body_end = markers[position + 1][0] if position + 1 < len(markers) else end
        # Trim the trailing ``case``/``default`` keyword of the next marker.
        if position + 1 < len(markers):
            keyword = masked.rfind("case", body_start, body_end)
            fallback = masked.rfind("default", body_start, body_end)
            body_end = max(keyword, fallback, body_start)
        labels.append((label_start, label_end, body_start, body_end))
    return tuple(labels)


def _scan_plain_loop(
    source: SourceText,
    index: int,
    end: int,
    conditions: tuple[Condition, ...],
    loop_interval_ms: int | None,
    state: _ScanState,
) -> tuple[int, tuple[Operation, ...]]:
    masked = source.masked
    cursor = skip_space(masked, index, end)
    if cursor < end and masked[cursor] == "(":
        closing = match_pair(masked, cursor, end + 1)
        cursor = closing + 1 if closing != -1 else end
    return _branch_body(source, cursor, end, conditions, loop_interval_ms, state)


def _scan_expression(
    source: SourceText,
    index: int,
    end: int,
    conditions: tuple[Condition, ...],
    loop_interval_ms: int | None,
    state: _ScanState,
    awaited: bool,
) -> tuple[int, tuple[Operation, ...]]:
    """Classify one expression statement, following ``.then`` continuations."""
    masked = source.masked
    expression, cursor = _member_expression(masked, index, end)
    if not expression:
        return index + 1, ()
    cursor = skip_space(masked, cursor, end)
    if cursor >= end or masked[cursor] != "(":
        # An assignment keeps its right-hand side in scope: ``response = await axios.post(...)``
        # is the same request as ``await axios.post(...)``. An object or array initializer is a
        # value, not a statement list, so it is skipped rather than scanned as a block.
        if masked[cursor : cursor + 1] == "=" and masked[cursor : cursor + 2] not in ("==", "=>"):
            after = skip_space(masked, cursor + 1, end)
            if masked[after : after + 1] in ("{", "["):
                closing = match_pair(masked, after, end + 1)
                return (closing + 1 if closing != -1 else end), ()
            return after, ()
        statement_end = _statement_end(masked, index, end)
        return max(statement_end, index + 1), ()
    args_close = match_pair(masked, cursor, end + 1)
    if args_close == -1:
        return end, ()
    operations: list[Operation] = []
    receiver, _, method = expression.rpartition(".")
    line = source.line_of(index)
    end_line = source.line_of(args_close)

    if receiver in AXIOS_RECEIVERS and method.lower() in HTTP_METHODS:
        operation = _api_operation(
            source,
            expression=expression,
            statement_start=index,
            http_method=method.lower(),
            args_open=cursor,
            args_close=args_close,
            conditions=conditions,
            loop_interval_ms=loop_interval_ms,
            state=state,
            awaited=awaited,
            line=line,
            end_line=end_line,
        )
        chain_cursor, then_operations = _scan_promise_chain(
            source, args_close + 1, end, conditions, loop_interval_ms, state
        )
        operations.append(
            Operation(
                kind=operation.kind,
                line=operation.line,
                end_line=operation.end_line,
                awaited=operation.awaited,
                conditions=operation.conditions,
                loop_interval_ms=operation.loop_interval_ms,
                expression=operation.expression,
                http_method=operation.http_method,
                url=operation.url,
                url_candidates=operation.url_candidates,
                reason=operation.reason,
                then_operations=then_operations,
            )
        )
        return chain_cursor, tuple(operations)

    if expression == ROUTER_PUSH:
        route_path, route_name, reason = _navigation_target(source, cursor + 1, args_close)
        kind = OP_NAVIGATION if (route_path or route_name) else OP_NAVIGATION_UNRESOLVED
        operations.append(
            Operation(
                kind=kind,
                line=line,
                end_line=end_line,
                awaited=awaited,
                conditions=conditions,
                loop_interval_ms=loop_interval_ms,
                expression=source.collapsed(index, args_close + 1),
                route_path=route_path,
                route_name=route_name,
                reason=reason,
            )
        )
        return args_close + 1, tuple(operations)

    if expression in NON_STATIC_NAVIGATION:
        operations.append(
            Operation(
                kind=OP_NAVIGATION_UNRESOLVED,
                line=line,
                end_line=end_line,
                awaited=awaited,
                conditions=conditions,
                loop_interval_ms=loop_interval_ms,
                expression=source.collapsed(index, args_close + 1),
                reason=f"{expression} has no statically resolvable destination",
            )
        )
        return args_close + 1, tuple(operations)

    if expression in INTERVAL_CALLS:
        interval, callback = _interval_callback(source, cursor + 1, args_close)
        deferred = (
            _scan_statements(source, callback[0], callback[1], conditions, None, state)
            if callback is not None
            else ()
        )
        operations.append(
            Operation(
                kind=OP_INTERVAL,
                line=line,
                end_line=end_line,
                awaited=awaited,
                conditions=conditions,
                loop_interval_ms=interval,
                expression=source.collapsed(index, args_close + 1),
                then_operations=deferred,
            )
        )
        return args_close + 1, tuple(operations)

    if receiver == "this" and method:
        operations.append(
            Operation(
                kind=OP_THIS_CALL,
                line=line,
                end_line=end_line,
                awaited=awaited,
                conditions=conditions,
                loop_interval_ms=loop_interval_ms,
                expression=source.collapsed(index, args_close + 1),
                target=method,
            )
        )
        chain_cursor, _ = _scan_promise_chain(
            source, args_close + 1, end, conditions, loop_interval_ms, state
        )
        return chain_cursor, tuple(operations)

    # Any other call: its arguments may still contain awaited application calls, but this pass
    # deliberately does not enter an unknown callee's callback. Skip past it.
    return args_close + 1, ()


def _scan_promise_chain(
    source: SourceText,
    index: int,
    end: int,
    conditions: tuple[Condition, ...],
    loop_interval_ms: int | None,
    state: _ScanState,
) -> tuple[int, tuple[Operation, ...]]:
    """Follow ``.then(cb)`` / ``.catch(cb)`` / ``.finally(cb)`` after a call expression.

    Only a ``then`` callback is scanned: it runs exactly when the preceding request resolved,
    which is the same ordering guarantee ``await`` gives. A ``catch`` callback is the failure
    path and is not part of a business journey.
    """
    masked = source.masked
    operations: list[Operation] = []
    cursor = index
    while True:
        lookahead = skip_space(masked, cursor, end)
        if lookahead >= end or masked[lookahead] != ".":
            return cursor, tuple(operations)
        name_start = skip_space(masked, lookahead + 1, end)
        name = read_identifier(masked, name_start, end)
        if name not in ("then", "catch", "finally"):
            return cursor, tuple(operations)
        args_open = skip_space(masked, name_start + len(name), end)
        if args_open >= end or masked[args_open] != "(":
            return cursor, tuple(operations)
        args_close = match_pair(masked, args_open, end + 1)
        if args_close == -1:
            return end, tuple(operations)
        if name == "then":
            body = _callback_body(source, args_open + 1, args_close)
            if body is not None:
                operations.extend(
                    _scan_statements(source, body[0], body[1], conditions, loop_interval_ms, state)
                )
        cursor = args_close + 1


def _callback_body(source: SourceText, start: int, end: int) -> tuple[int, int] | None:
    """Body span of the first argument when it is a function or arrow function."""
    segments = split_top_level(source.masked, start, end)
    if not segments:
        return None
    first_start, first_end = segments[0]
    return _function_value_body(source, first_start, first_end)


def _interval_callback(
    source: SourceText, start: int, end: int
) -> tuple[int | None, tuple[int, int] | None]:
    segments = split_top_level(source.masked, start, end)
    if not segments:
        return None, None
    body = _function_value_body(source, segments[0][0], segments[0][1])
    interval = (
        number_literal_at(source, segments[1][0], segments[1][1]) if len(segments) > 1 else None
    )
    return interval, body


def _api_operation(
    source: SourceText,
    *,
    expression: str,
    statement_start: int,
    http_method: str,
    args_open: int,
    args_close: int,
    conditions: tuple[Condition, ...],
    loop_interval_ms: int | None,
    state: _ScanState,
    awaited: bool,
    line: int,
    end_line: int,
) -> Operation:
    del expression
    segments = split_top_level(source.masked, args_open + 1, args_close)
    call_text = source.collapsed(statement_start, args_close + 1)
    if not segments:
        return Operation(
            kind=OP_API_UNRESOLVED,
            line=line,
            end_line=end_line,
            awaited=awaited,
            conditions=conditions,
            loop_interval_ms=loop_interval_ms,
            expression=call_text,
            http_method=http_method,
            reason="request has no URL argument",
        )
    first_start, first_end = segments[0]
    literal = string_literal_at(source, first_start, first_end)
    if literal is not None:
        return Operation(
            kind=OP_API,
            line=line,
            end_line=end_line,
            awaited=awaited,
            conditions=conditions,
            loop_interval_ms=loop_interval_ms,
            expression=call_text,
            http_method=http_method,
            url=literal,
        )
    identifier = source.masked[first_start:first_end].strip()
    if _IDENTIFIER.fullmatch(identifier):
        if identifier in state.ambiguous:
            reason = f"URL variable {identifier!r} is assigned more than once"
        elif identifier in state.declarations:
            value_start, value_end = state.declarations[identifier]
            direct = string_literal_at(source, value_start, value_end)
            if direct is not None:
                return Operation(
                    kind=OP_API,
                    line=line,
                    end_line=end_line,
                    awaited=awaited,
                    conditions=conditions,
                    loop_interval_ms=loop_interval_ms,
                    expression=call_text,
                    http_method=http_method,
                    url=direct,
                )
            candidates = _ternary_string_candidates(source, value_start, value_end)
            if candidates:
                return Operation(
                    kind=OP_API_UNRESOLVED,
                    line=line,
                    end_line=end_line,
                    awaited=awaited,
                    conditions=conditions,
                    loop_interval_ms=loop_interval_ms,
                    expression=call_text,
                    http_method=http_method,
                    url_candidates=candidates,
                    reason=(
                        f"URL variable {identifier!r} is a conditional expression with "
                        f"{len(candidates)} literal outcomes"
                    ),
                )
            reason = f"URL variable {identifier!r} is not a static string"
        else:
            reason = f"URL variable {identifier!r} is not declared in the handler"
    else:
        reason = "URL argument is not a static string"
    return Operation(
        kind=OP_API_UNRESOLVED,
        line=line,
        end_line=end_line,
        awaited=awaited,
        conditions=conditions,
        loop_interval_ms=loop_interval_ms,
        expression=call_text,
        http_method=http_method,
        reason=reason,
    )


def _ternary_string_candidates(source: SourceText, start: int, end: int) -> tuple[str, ...]:
    """Literal outcomes of ``cond ? 'a' : 'b'``, sorted so output stays deterministic."""
    question = find_top_level(source.masked, start, end, "?")
    if question == -1:
        return ()
    colon = find_top_level(source.masked, question + 1, end, ":")
    if colon == -1:
        return ()
    first = string_literal_at(source, question + 1, colon)
    second = string_literal_at(source, colon + 1, end)
    if first is None or second is None:
        return ()
    return tuple(sorted({first, second}))


def _navigation_target(
    source: SourceText, start: int, end: int
) -> tuple[str | None, str | None, str | None]:
    """Resolve ``$router.push`` argument to a route path or a route name.

    The argument span is scanned with balanced-delimiter matching, so an object literal spread
    across several lines resolves exactly like a single-line one.
    """
    segments = split_top_level(source.masked, start, end)
    if not segments:
        return None, None, "navigation has no destination argument"
    first_start, first_end = segments[0]
    literal = string_literal_at(source, first_start, first_end)
    if literal is not None:
        return literal, None, None
    cursor = skip_space(source.masked, first_start, first_end)
    if cursor < first_end and source.masked[cursor] == "{":
        for member in object_members(source, cursor):
            if member.key != "name":
                continue
            name = string_literal_at(source, member.value_start, member.value_end)
            if name is not None:
                return None, name, None
            return None, None, "route name is not a static string"
        return None, None, "navigation object declares no static route name"
    return None, None, "navigation destination is not a static path or route name"


# ---------------------------------------------------------------------------------------
# Component, view, router and store facts
# ---------------------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class ComponentFacts:
    """One parsed single-file component."""

    relative_path: str
    source: SourceText
    has_script: bool
    has_template: bool
    handlers: dict[str, HandlerScan]
    lifecycle: dict[str, HandlerScan]
    computed_getters: dict[str, tuple[str, ...]]
    mapped_getters: tuple[str, ...]
    mapped_actions: tuple[str, ...]
    registered_components: dict[str, str]
    mounted_components: tuple[str, ...]
    template_handlers: tuple[str, ...]
    declared_role_literals: tuple[str, ...]

    @property
    def is_empty(self) -> bool:
        """A component that renders nothing and declares nothing cannot host a step."""
        return not self.has_script and not self.has_template

    def function(self, name: str) -> HandlerScan | None:
        return self.handlers.get(name) or self.lifecycle.get(name)


def _import_map(source: SourceText, limit: int) -> dict[str, str]:
    """Map locally bound default-import names to their specifier strings."""
    bindings: dict[str, str] = {}
    for match in re.finditer(
        r"\bimport\s+([A-Za-z_$][A-Za-z0-9_$]*)\s+from\s+(['\"])",
        source.masked[:limit],
    ):
        quote_index = match.end() - 1
        quote = source.masked[quote_index]
        closing = source.masked.find(quote, quote_index + 1, limit)
        if closing == -1:
            continue
        bindings[match.group(1)] = source.text[quote_index + 1 : closing]
    return bindings


def _default_export_object(source: SourceText, block: ScriptBlock) -> int | None:
    position = source.masked.find("export default", block.start, block.end)
    if position == -1:
        return None
    brace = skip_space(source.masked, position + len("export default"), block.end)
    return brace if brace < block.end and source.masked[brace] == "{" else None


def _template_handler_names(text: str, template: tuple[int, int] | None) -> tuple[str, ...]:
    """Identifiers referenced by template event bindings, in sorted order.

    A method that is never bound in the rendered template and never called from a bound method
    is unreachable, and an unreachable handler must not seed a business journey.
    """
    if template is None:
        return ()
    body = text[template[0] : template[1]]
    names: set[str] = set()
    for match in _EVENT_BINDING.finditer(body):
        for identifier in _IDENTIFIER.findall(match.group("body")):
            names.add(identifier)
    return tuple(sorted(names))


def _mounted_component_tags(text: str, template: tuple[int, int] | None) -> frozenset[str]:
    if template is None:
        return frozenset()
    body = text[template[0] : template[1]]
    return frozenset(match.lower() for match in re.findall(r"<\s*([A-Za-z][\w.-]*)", body))


def _kebab(name: str) -> str:
    return re.sub(r"(?<!^)(?=[A-Z])", "-", name).lower()


def parse_component(relative_path: str, text: str) -> ComponentFacts:
    """Parse one single-file component without importing or evaluating it."""
    source = build_source_text(relative_path, text)
    blocks = extract_script_blocks(source.text)
    template = extract_template_block(source.text)
    template_body_present = template is not None and bool(
        source.text[template[0] : template[1]].strip()
    )
    script_present = any(
        not block.is_empty and source.text[block.start : block.end].strip() for block in blocks
    )

    handlers: dict[str, HandlerScan] = {}
    lifecycle: dict[str, HandlerScan] = {}
    computed_getters: dict[str, tuple[str, ...]] = {}
    mapped_getters: list[str] = []
    mapped_actions: list[str] = []
    registered: dict[str, str] = {}
    role_literals: list[str] = []

    for block in blocks:
        imports = _import_map(source, block.end)
        export_brace = _default_export_object(source, block)
        if export_brace is None:
            continue
        for member in object_members(source, export_brace):
            if member.key in LIFECYCLE_HOOKS and member.kind == MEMBER_METHOD:
                lifecycle[member.key] = scan_handler(source, member.key, member)
            elif member.key == "methods":
                brace = skip_space(source.masked, member.value_start, member.value_end)
                if source.masked[brace : brace + 1] != "{":
                    continue
                for entry in object_members(source, brace):
                    if entry.kind == MEMBER_SPREAD:
                        helper, names = spread_helper_names(source, entry)
                        if helper == "mapActions":
                            mapped_actions.extend(names)
                        elif helper == "mapGetters":
                            mapped_getters.extend(names)
                        continue
                    if entry.kind == MEMBER_METHOD:
                        handlers[entry.key] = scan_handler(source, entry.key, entry)
            elif member.key == "computed":
                brace = skip_space(source.masked, member.value_start, member.value_end)
                if source.masked[brace : brace + 1] != "{":
                    continue
                for entry in object_members(source, brace):
                    if entry.kind == MEMBER_SPREAD:
                        helper, names = spread_helper_names(source, entry)
                        if helper == "mapGetters":
                            mapped_getters.extend(names)
                        continue
                    if entry.kind == MEMBER_METHOD:
                        computed_getters[entry.key] = _read_this_members(
                            source, entry.body_start, entry.body_end
                        )
            elif member.key == "components":
                brace = skip_space(source.masked, member.value_start, member.value_end)
                if source.masked[brace : brace + 1] != "{":
                    continue
                for entry in object_members(source, brace):
                    if entry.kind in (MEMBER_SHORTHAND, MEMBER_VALUE, MEMBER_METHOD):
                        alias = source.masked[entry.value_start : entry.value_end].strip()
                        local = entry.key if entry.kind != MEMBER_VALUE else (alias or entry.key)
                        specifier = imports.get(local) or imports.get(entry.key)
                        if specifier:
                            registered[entry.key] = specifier
            elif member.key == "data" and member.kind == MEMBER_METHOD:
                role_literals.extend(_declared_role_literals(source, member))

    return ComponentFacts(
        relative_path=relative_path,
        source=source,
        has_script=script_present,
        has_template=template_body_present,
        handlers=handlers,
        lifecycle=lifecycle,
        computed_getters=computed_getters,
        mapped_getters=tuple(sorted(set(mapped_getters))),
        mapped_actions=tuple(sorted(set(mapped_actions))),
        registered_components=registered,
        mounted_components=tuple(sorted(_mounted_component_tags(source.text, template))),
        template_handlers=_template_handler_names(source.text, template),
        declared_role_literals=tuple(sorted(set(role_literals))),
    )


def _read_this_members(source: SourceText, start: int, end: int) -> tuple[str, ...]:
    """Names read through ``this.<name>`` inside a span, sorted and de-duplicated."""
    found = set(re.findall(r"\bthis\.([A-Za-z_$][A-Za-z0-9_$]*)", source.masked[start:end]))
    return tuple(sorted(found))


def _declared_role_literals(source: SourceText, member: ObjectMember) -> tuple[str, ...]:
    """Role option values declared in ``data()``, e.g. the ``userRoles`` select options.

    Only literals under a key whose value list carries ``value:`` entries are read, so an
    unrelated string in ``data()`` is never mistaken for a role.
    """
    literals: set[str] = set()
    masked = source.masked
    for match in re.finditer(r"\bvalue\s*:", masked[member.body_start : member.body_end]):
        value_start = member.body_start + match.end()
        value_end = _member_value_end(masked, value_start, member.body_end)
        literal = string_literal_at(source, value_start, value_end)
        if literal:
            literals.add(literal)
    return tuple(sorted(literals))


@dataclass(frozen=True, slots=True)
class ViewFacts:
    """One routed view and the component it actually mounts."""

    relative_path: str
    component_path: str | None
    is_empty: bool
    reason: str | None


def resolve_view(view: ComponentFacts, component_paths: frozenset[str]) -> ViewFacts:
    """Decide whether a routed view mounts exactly one known component.

    A view that imports a component but never renders its tag mounts nothing, and a view with
    neither script nor template - which is the state of ``views/MenuPage.vue`` at the frozen
    commit - is a dead end that stops a journey.
    """
    if view.is_empty:
        return ViewFacts(view.relative_path, None, True, "view declares no script and no template")
    mounted: list[str] = []
    for local_name, specifier in sorted(view.registered_components.items()):
        tags = {_kebab(local_name), local_name.lower()}
        if not tags & set(view.mounted_components):
            continue
        resolved = _resolve_relative_specifier(view.relative_path, specifier)
        if resolved in component_paths:
            mounted.append(resolved)
    unique = sorted(set(mounted))
    if not unique:
        return ViewFacts(
            view.relative_path, None, False, "view mounts no component from the component directory"
        )
    if len(unique) > 1:
        return ViewFacts(
            view.relative_path,
            None,
            False,
            f"view mounts {len(unique)} components: {', '.join(unique)}",
        )
    return ViewFacts(view.relative_path, unique[0], False, None)


def _resolve_relative_specifier(from_path: str, specifier: str) -> str:
    base = Path(from_path).parent
    target = (base / specifier).as_posix()
    parts: list[str] = []
    for segment in target.split("/"):
        if segment in ("", "."):
            continue
        if segment == "..":
            if parts:
                parts.pop()
            continue
        parts.append(segment)
    return "/".join(parts)


@dataclass(frozen=True, slots=True)
class RouteRecord:
    """One entry of the Vue Router table."""

    path: str
    name: str
    view_path: str
    line: int


def parse_router(source: SourceText, view_paths: frozenset[str]) -> tuple[
    tuple[RouteRecord, ...], tuple[str, ...]
]:
    """Read the route table exactly: path, name and the imported view module per route."""
    imports = _import_map(source, len(source.masked))
    warnings: list[str] = []
    routes_index = re.search(r"\bconst\s+routes\s*=", source.masked)
    if routes_index is None:
        return (), ("router module declares no `routes` array",)
    array_start = skip_space(source.masked, routes_index.end(), len(source.masked))
    if source.masked[array_start : array_start + 1] != "[":
        return (), ("router `routes` is not an array literal",)
    array_end = match_pair(source.masked, array_start, len(source.masked))
    if array_end == -1:
        return (), ("router `routes` array is unbalanced",)

    records: list[RouteRecord] = []
    for start, end in split_top_level(source.masked, array_start + 1, array_end):
        brace = skip_space(source.masked, start, end)
        if source.masked[brace : brace + 1] != "{":
            continue
        entry: dict[str, str] = {}
        for member in object_members(source, brace):
            if member.kind == MEMBER_VALUE:
                entry[member.key] = source.masked[member.value_start : member.value_end].strip()
                literal = string_literal_at(source, member.value_start, member.value_end)
                if literal is not None:
                    entry[member.key] = literal
                    entry[f"{member.key}__literal"] = literal
        path = entry.get("path__literal")
        name = entry.get("name__literal")
        component = entry.get("component")
        if path is None or name is None or not component:
            warnings.append(
                f"{source.relative_path}: route at line {source.line_of(brace)} is not statically "
                f"resolvable (path, name and component must all be literal)"
            )
            continue
        specifier = imports.get(component)
        if specifier is None:
            warnings.append(
                f"{source.relative_path}: route {name!r} component {component!r} is not a "
                f"default import"
            )
            continue
        view_path = _resolve_relative_specifier(source.relative_path, specifier)
        if view_path not in view_paths:
            warnings.append(
                f"{source.relative_path}: route {name!r} resolves to {view_path!r}, which is not a "
                f"scanned view module"
            )
            continue
        records.append(
            RouteRecord(path=path, name=name, view_path=view_path, line=source.line_of(brace))
        )
    return tuple(sorted(records, key=lambda item: (item.path, item.name))), tuple(warnings)


@dataclass(frozen=True, slots=True)
class StoreFacts:
    """Vuex state reachable from getters and writable through actions."""

    getter_state: dict[str, str]
    action_state: dict[str, str]

    def state_read_by(self, getter: str) -> str | None:
        return self.getter_state.get(getter)

    def state_written_by(self, action: str) -> str | None:
        return self.action_state.get(action)


def parse_store(source: SourceText) -> StoreFacts:
    """Chain getter -> state, action -> mutation -> state from the store module."""
    masked = source.masked
    getter_state = {
        match.group(1): match.group(2)
        for match in re.finditer(
            r"\b([A-Za-z_$][A-Za-z0-9_$]*)\s*:\s*state\s*=>\s*state\.([A-Za-z_$][A-Za-z0-9_$]*)",
            masked,
        )
    }
    mutation_state = {
        match.group(1): match.group(2)
        for match in re.finditer(
            r"\b([A-Za-z_$][A-Za-z0-9_$]*)\s*\(\s*state[^)]*\)\s*\{\s*state\.([A-Za-z_$][A-Za-z0-9_$]*)\s*=",
            masked,
        )
    }
    action_state: dict[str, str] = {}
    for match in re.finditer(
        r"\b([A-Za-z_$][A-Za-z0-9_$]*)\s*\(\s*\{\s*commit\s*\}[^)]*\)\s*\{", masked
    ):
        body_open = match.end() - 1
        body_close = match_pair(masked, body_open, len(masked))
        if body_close == -1:
            continue
        commit_match = re.search(
            r"\bcommit\s*\(\s*(['\"])", masked[body_open:body_close]
        )
        if commit_match is None:
            continue
        quote_index = body_open + commit_match.end() - 1
        quote = masked[quote_index]
        closing = masked.find(quote, quote_index + 1, body_close)
        if closing == -1:
            continue
        mutation = source.text[quote_index + 1 : closing]
        state_key = mutation_state.get(mutation)
        if state_key:
            action_state[match.group(1)] = state_key
    return StoreFacts(getter_state=getter_state, action_state=action_state)


# ---------------------------------------------------------------------------------------
# Canonical Pass-5 UserFlow index and API prefix
# ---------------------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class UserFlowRef:
    """One approved Pass-5 UserFlow, addressed by HTTP method and normalized path."""

    id: str
    http_method: str
    path: str
    relative_path: str


def load_canonical_user_flows(flows_dir: Path) -> tuple[UserFlowRef, ...]:
    """Read approved ``UserFlow`` pages. Their ids are reused verbatim, never regenerated."""
    if not flows_dir.is_dir():
        raise BusinessFlowExtractionError(
            f"Canonical Pass-5 user flows not found at {flows_dir}. Pass 6 composes existing "
            f"UserFlow pages and cannot run without them."
        )
    refs: list[UserFlowRef] = []
    for page in sorted(flows_dir.glob("*.md")):
        text = page.read_text(encoding="utf-8")
        if not text.startswith("---"):
            continue
        closing = text.find("\n---", 3)
        if closing == -1:
            continue
        front = yaml.safe_load(text[3:closing]) or {}
        if str(front.get("kind") or "") != USER_FLOW_KIND:
            continue
        identifier = str(front.get("id") or "").strip()
        method = str(front.get("http_method") or "").strip().upper()
        path = str(front.get("path") or "").strip()
        if not identifier or not method or not path:
            continue
        refs.append(
            UserFlowRef(
                id=identifier,
                http_method=method,
                path=path,
                relative_path=f"{CANONICAL_FLOWS_DIR}/{page.name}",
            )
        )
    if not refs:
        raise BusinessFlowExtractionError(
            f"No approved UserFlow pages found in {flows_dir}."
        )
    return tuple(sorted(refs, key=lambda item: item.id))


@dataclass(frozen=True, slots=True)
class ApiPrefix:
    """The gateway route prefix, only usable when both halves are source-backed."""

    value: str
    resolved: bool
    config_provenance: Provenance | None
    mount_provenance: Provenance | None
    reason: str | None


def resolve_api_prefix(
    repository: str, commit: str, config_text: str | None, main_text: str | None
) -> ApiPrefix:
    """Prove the ``/api/v1`` prefix from the gateway configuration default and its mount site.

    Both halves are required. The default alone proves a value exists; the ``include_router``
    keyword proves that value is what every route is actually mounted behind. Without both,
    the prefix is not stripped and every UI URL is reported unresolved rather than guessed.
    """
    if config_text is None or main_text is None:
        return ApiPrefix("", False, None, None, "gateway configuration modules were not scanned")
    default_value: str | None = None
    config_provenance: Provenance | None = None
    try:
        config_tree = ast.parse(config_text)
    except SyntaxError as exc:
        return ApiPrefix(
            "", False, None, None, f"{GATEWAY_SERVICE_CONFIG_PATH} is not parseable: {exc}"
        )
    for node in ast.walk(config_tree):
        if not isinstance(node, ast.Call):
            continue
        callee = node.func
        name = callee.attr if isinstance(callee, ast.Attribute) else getattr(callee, "id", None)
        if name != "env_var" or not node.args:
            continue
        first = node.args[0]
        if not (isinstance(first, ast.Constant) and first.value == API_PREFIX_ENV_NAME):
            continue
        for keyword in node.keywords:
            if keyword.arg == "default" and isinstance(keyword.value, ast.Constant):
                if isinstance(keyword.value.value, str):
                    default_value = keyword.value.value
                    config_provenance = Provenance(
                        repository=repository,
                        commit=commit,
                        source_path=GATEWAY_SERVICE_CONFIG_PATH,
                        symbol=f"ServiceConfig.__init__:{API_PREFIX_ENV_NAME}",
                        line_start=node.lineno,
                        line_end=node.end_lineno or node.lineno,
                    )
    if default_value is None:
        return ApiPrefix(
            "",
            False,
            None,
            None,
            f"{API_PREFIX_ENV_NAME} has no literal default in the gateway config",
        )
    mount_provenance: Provenance | None = None
    try:
        main_tree = ast.parse(main_text)
    except SyntaxError as exc:
        return ApiPrefix(
            "", False, config_provenance, None, f"{GATEWAY_MAIN_PATH} is not parseable: {exc}"
        )
    for node in ast.walk(main_tree):
        if not isinstance(node, ast.Call):
            continue
        callee = node.func
        if not (isinstance(callee, ast.Attribute) and callee.attr == "include_router"):
            continue
        for keyword in node.keywords:
            if keyword.arg != "prefix":
                continue
            if isinstance(keyword.value, ast.Attribute) and keyword.value.attr == "api_prefix":
                mount_provenance = Provenance(
                    repository=repository,
                    commit=commit,
                    source_path=GATEWAY_MAIN_PATH,
                    symbol="app.include_router",
                    line_start=node.lineno,
                    line_end=node.end_lineno or node.lineno,
                )
    if mount_provenance is None:
        return ApiPrefix(
            default_value,
            False,
            config_provenance,
            None,
            "no include_router call mounts the router behind the configured api_prefix",
        )
    return ApiPrefix(default_value, True, config_provenance, mount_provenance, None)


@dataclass(frozen=True, slots=True)
class UrlMapping:
    """Outcome of mapping one UI request to exactly one Pass-5 UserFlow."""

    http_method: str
    raw_url: str
    path: str | None
    user_flow_id: str | None
    matches: tuple[str, ...]
    reason: str | None

    @property
    def resolved(self) -> bool:
        return self.user_flow_id is not None


def normalize_request_path(raw_url: str, prefix: ApiPrefix) -> tuple[str | None, str | None]:
    """Strip origin and the configured prefix from a UI URL, returning ``(path, reason)``."""
    without_origin = re.sub(r"^[a-zA-Z][a-zA-Z0-9+.\-]*://[^/]+", "", raw_url.strip())
    path = without_origin.split("?", 1)[0].split("#", 1)[0]
    if not path.startswith("/"):
        return None, f"request URL {raw_url!r} has no absolute path"
    if not prefix.resolved:
        return None, f"configured API prefix is not source-backed: {prefix.reason}"
    if not path.startswith(prefix.value):
        return None, (
            f"request path {path!r} does not start with the configured prefix {prefix.value!r}"
        )
    remainder = path[len(prefix.value) :] or "/"
    if not remainder.startswith("/"):
        return None, f"request path {path!r} does not split cleanly on prefix {prefix.value!r}"
    return remainder.rstrip("/") or "/", None


def map_to_user_flow(
    http_method: str, raw_url: str, prefix: ApiPrefix, index: dict[tuple[str, str], tuple[str, ...]]
) -> UrlMapping:
    """Require exactly one method/path match. Never fall back to a suffix or nearest name."""
    path, reason = normalize_request_path(raw_url, prefix)
    if path is None:
        return UrlMapping(http_method.upper(), raw_url, None, None, (), reason)
    matches = index.get((http_method.upper(), path), ())
    if len(matches) == 1:
        return UrlMapping(http_method.upper(), raw_url, path, matches[0], matches, None)
    if not matches:
        return UrlMapping(
            http_method.upper(),
            raw_url,
            path,
            None,
            (),
            f"no approved Pass-5 UserFlow declares {http_method.upper()} {path}",
        )
    return UrlMapping(
        http_method.upper(),
        raw_url,
        path,
        None,
        matches,
        f"{len(matches)} approved Pass-5 UserFlows declare {http_method.upper()} {path}",
    )


def build_user_flow_index(
    refs: tuple[UserFlowRef, ...],
) -> dict[tuple[str, str], tuple[str, ...]]:
    grouped: dict[tuple[str, str], list[str]] = {}
    for ref in refs:
        grouped.setdefault((ref.http_method, ref.path), []).append(ref.id)
    return {key: tuple(sorted(value)) for key, value in sorted(grouped.items())}


# ---------------------------------------------------------------------------------------
# Frontend model
# ---------------------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class FrontendModel:
    """Everything Pass 6 needs about the frontend, resolved once per run."""

    repository: str
    commit: str
    components: dict[str, ComponentFacts]
    views: dict[str, ComponentFacts]
    view_resolution: dict[str, ViewFacts]
    routes_by_path: dict[str, RouteRecord]
    routes_by_name: dict[str, RouteRecord]
    store: StoreFacts
    prefix: ApiPrefix
    user_flow_index: dict[tuple[str, str], tuple[str, ...]]
    reachable_handlers: dict[str, tuple[str, ...]]
    role_literals: frozenset[str]

    def component(self, relative_path: str) -> ComponentFacts | None:
        return self.components.get(relative_path)

    def route_for(self, operation: Operation) -> RouteRecord | None:
        if operation.route_path is not None:
            return self.routes_by_path.get(operation.route_path)
        if operation.route_name is not None:
            return self.routes_by_name.get(operation.route_name)
        return None

    def symbol(self, relative_path: str, function_name: str) -> str:
        return f"{Path(relative_path).stem}.{function_name}"


def compute_reachable_handlers(component: ComponentFacts) -> tuple[str, ...]:
    """Functions reachable from a template binding or a lifecycle hook, transitively.

    A method that no template binding and no lifecycle hook can reach is dead code at this
    commit and must not seed a business journey, however plausible its name looks.
    """
    frontier = [name for name in LIFECYCLE_HOOKS if name in component.lifecycle]
    frontier.extend(name for name in component.template_handlers if name in component.handlers)
    reachable: set[str] = set()
    while frontier:
        name = frontier.pop()
        if name in reachable:
            continue
        reachable.add(name)
        function = component.function(name)
        if function is None:
            continue
        for operation in _all_operations(function.operations):
            if operation.kind == OP_THIS_CALL and operation.target:
                if operation.target in component.handlers and operation.target not in reachable:
                    frontier.append(operation.target)
    return tuple(sorted(reachable))


def classify_entry_trigger(component: ComponentFacts, handler_name: str) -> str:
    """Classify how a reachable hypothesis entry handler is actually invoked.

    A method can be reachable transitively from either a rendered template event or a Vue
    lifecycle hook. The hypothesis catalog names the method but does not get to declare its
    trigger: that remains a source-derived fact.
    """

    def reachable_from(roots: tuple[str, ...]) -> frozenset[str]:
        frontier = list(roots)
        reachable: set[str] = set()
        while frontier:
            name = frontier.pop()
            if name in reachable:
                continue
            reachable.add(name)
            function = component.function(name)
            if function is None:
                continue
            for operation in _all_operations(function.operations):
                if (
                    operation.kind == OP_THIS_CALL
                    and operation.target in component.handlers
                    and operation.target not in reachable
                ):
                    frontier.append(str(operation.target))
        return frozenset(reachable)

    template_roots = tuple(
        name for name in component.template_handlers if name in component.handlers
    )
    lifecycle_roots = tuple(name for name in LIFECYCLE_HOOKS if name in component.lifecycle)
    if handler_name in reachable_from(template_roots):
        return TRIGGER_USER_ACTION
    if handler_name in reachable_from(lifecycle_roots):
        return TRIGGER_LIFECYCLE
    return TRIGGER_AUTOMATIC


def _all_operations(operations: tuple[Operation, ...]) -> tuple[Operation, ...]:
    """Flatten an operation list including ``then`` continuations, preserving order."""
    flattened: list[Operation] = []
    for operation in operations:
        flattened.append(operation)
        flattened.extend(_all_operations(operation.then_operations))
    return tuple(flattened)


def function_issues_request(
    component: ComponentFacts, name: str, *, depth: int = 0, seen: frozenset[str] = frozenset()
) -> bool:
    """True when a function transitively issues at least one HTTP request."""
    if depth > _MAX_HELPER_DEPTH or name in seen:
        return False
    function = component.function(name)
    if function is None:
        return False
    for operation in _all_operations(function.operations):
        if operation.kind in (OP_API, OP_API_UNRESOLVED):
            return True
        if operation.kind == OP_THIS_CALL and operation.target in component.handlers:
            if function_issues_request(
                component, operation.target, depth=depth + 1, seen=seen | {name}
            ):
                return True
    return False


def state_keys_consumed(
    component: ComponentFacts,
    store: StoreFacts,
    name: str,
    *,
    depth: int = 0,
    seen: frozenset[str] = frozenset(),
) -> frozenset[str]:
    """Vuex state a function reads, directly or through a computed property."""
    if depth > _MAX_HELPER_DEPTH or name in seen:
        return frozenset()
    function = component.function(name)
    if function is None:
        return frozenset()
    body_reads = _read_this_members(component.source, function.body_start, function.body_end)
    keys: set[str] = set()
    for member in body_reads:
        if member in component.mapped_getters:
            state = store.state_read_by(member)
            if state:
                keys.add(state)
        for indirect in component.computed_getters.get(member, ()):
            if indirect in component.mapped_getters:
                state = store.state_read_by(indirect)
                if state:
                    keys.add(state)
        if member in component.handlers:
            keys |= state_keys_consumed(
                component, store, member, depth=depth + 1, seen=seen | {name}
            )
    return frozenset(keys)


# ---------------------------------------------------------------------------------------
# Chain derivation
# ---------------------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class ChainStep:
    """One business step: a reference to an existing Pass-5 UserFlow, with its evidence."""

    user_flow_id: str
    http_method: str
    path: str
    raw_url: str
    component_path: str
    symbol: str
    provenance: Provenance
    trigger: str
    mechanisms: tuple[str, ...]
    conditions: tuple[Condition, ...]
    inherited_conditions: tuple[Condition, ...]
    loop_interval_ms: int | None
    ordered_from_previous: bool
    order_mechanisms: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class ChainResult:
    """Outcome of walking one entry handler in one branch world."""

    steps: tuple[ChainStep, ...]
    stop_reason: str | None
    unresolved_segments: tuple[dict[str, Any], ...]
    route_failures: tuple[dict[str, Any], ...]
    empty_views: tuple[dict[str, Any], ...]
    unknown_routes: tuple[str, ...]
    notes: tuple[str, ...]

    @property
    def user_flow_ids(self) -> tuple[str, ...]:
        return tuple(step.user_flow_id for step in self.steps)


def _dedupe(values: tuple[str, ...]) -> tuple[str, ...]:
    seen: list[str] = []
    for value in values:
        if value not in seen:
            seen.append(value)
    return tuple(seen)


def _dedupe_conditions(values: tuple[Condition, ...]) -> tuple[Condition, ...]:
    seen: list[Condition] = []
    for value in values:
        if value not in seen:
            seen.append(value)
    return tuple(seen)


def _dedupe_provenances(values: tuple[Provenance, ...]) -> tuple[Provenance, ...]:
    """Keep concrete evidence regions in first-seen order without synthesizing a span."""
    seen: list[Provenance] = []
    for value in values:
        if value not in seen:
            seen.append(value)
    return tuple(seen)


class ChainWalker:
    """Bounded walk from one reachable entry handler to a linear business-step chain."""

    def __init__(self, model: FrontendModel, world: dict[str, str]) -> None:
        self.model = model
        self.world = dict(world)
        self.steps: list[ChainStep] = []
        self.pending_order = False
        self.pending_mechanisms: tuple[str, ...] = (MECHANISM_ENTRY,)
        self.state_written: set[str] = set()
        self.navigation_hops = 0
        self.loop_stack: list[int] = []
        # Guards that enclose a helper call apply to every request that call reaches, so they
        # travel with the recursion instead of being lost at the function boundary.
        # Each inherited guard records the number of already-emitted steps when it became
        # active. It directly triggers only the first request reached through that guarded
        # call; later requests are automatic continuations unless they have their own guard.
        self.condition_stack: list[tuple[Condition, int]] = []
        self.stop_reason: str | None = None
        self.unresolved: list[dict[str, Any]] = []
        self.route_failures: list[dict[str, Any]] = []
        self.empty_views: list[dict[str, Any]] = []
        self.unknown_routes: list[str] = []
        self.notes: list[str] = []
        self.visited: set[tuple[str, str]] = set()
        self.role_branch_literals: list[str] = []

    # -- world filtering ---------------------------------------------------------------

    def _in_world(self, conditions: tuple[Condition, ...]) -> bool:
        for condition in conditions:
            subject = condition.subject
            if subject is None or subject not in self.world:
                continue
            selected = self.world[subject]
            if condition.kind == CONDITION_SWITCH_DEFAULT:
                return False
            if condition.kind == CONDITION_ELSE:
                if condition.excluded_literal == selected:
                    return False
                continue
            if condition.literal is not None and condition.literal != selected:
                return False
        return True

    def _residual_conditions(self, conditions: tuple[Condition, ...]) -> tuple[Condition, ...]:
        """Conditions that still qualify the step after the branch world is applied."""
        residual: list[Condition] = []
        for condition in conditions:
            if condition.subject is not None and condition.subject in self.world:
                if condition.literal is not None:
                    self.role_branch_literals.append(condition.literal)
                continue
            residual.append(condition)
        return tuple(residual)

    # -- entry -------------------------------------------------------------------------

    def run(self, component_path: str, handler_name: str) -> ChainResult:
        component = self.model.component(component_path)
        if component is None:
            self.stop_reason = f"entry component {component_path!r} was not scanned"
            return self._result()
        if handler_name not in self.model.reachable_handlers.get(component_path, ()):
            self.stop_reason = (
                f"entry handler {handler_name!r} is not reachable from a template binding or a "
                f"lifecycle hook in {component_path}"
            )
            return self._result()
        function = component.function(handler_name)
        if function is None:
            self.stop_reason = f"entry handler {handler_name!r} is not declared in {component_path}"
            return self._result()
        self.visited.add((component_path, handler_name))
        self.walk(function.operations, component_path, handler_name, 0)
        return self._result()

    def _result(self) -> ChainResult:
        return ChainResult(
            steps=tuple(self.steps),
            stop_reason=self.stop_reason,
            unresolved_segments=tuple(self.unresolved),
            route_failures=tuple(self.route_failures),
            empty_views=tuple(self.empty_views),
            unknown_routes=tuple(sorted(set(self.unknown_routes))),
            notes=tuple(self.notes),
        )

    # -- operation walking -------------------------------------------------------------

    def walk(
        self, operations: tuple[Operation, ...], component_path: str, function_name: str, depth: int
    ) -> bool:
        for operation in operations:
            if self.stop_reason is not None or len(self.steps) >= _MAX_CHAIN_STEPS:
                return True
            if not self._in_world(operation.conditions):
                continue
            if operation.kind in (OP_API, OP_API_UNRESOLVED):
                if self._handle_request(operation, component_path, function_name, depth):
                    return True
            elif operation.kind == OP_THIS_CALL:
                if self._handle_this_call(operation, component_path, function_name, depth):
                    return True
            elif operation.kind == OP_INTERVAL:
                if self._handle_interval(operation, component_path, function_name, depth):
                    return True
            elif operation.kind == OP_NAVIGATION:
                self._handle_navigation(operation, component_path, function_name)
                return True
            elif operation.kind == OP_NAVIGATION_UNRESOLVED:
                self.route_failures.append(
                    {
                        "path": component_path,
                        "symbol": self.model.symbol(component_path, function_name),
                        "line": operation.line,
                        "expression": operation.expression,
                        "reason": operation.reason or "navigation destination is not static",
                    }
                )
                self.stop_reason = operation.reason or "navigation destination is not static"
                return True
        return False

    def _current_loop(self, operation: Operation) -> int | None:
        if operation.loop_interval_ms is not None:
            return operation.loop_interval_ms
        return self.loop_stack[-1] if self.loop_stack else None

    def _handle_request(
        self, operation: Operation, component_path: str, function_name: str, depth: int
    ) -> bool:
        symbol = self.model.symbol(component_path, function_name)
        provenance = Provenance(
            repository=self.model.repository,
            commit=self.model.commit,
            source_path=component_path,
            symbol=symbol,
            line_start=operation.line,
            line_end=operation.end_line,
        )
        candidates = (
            operation.url_candidates
            if operation.kind == OP_API_UNRESOLVED and operation.url_candidates
            else ((operation.url,) if operation.url else ())
        )
        mappings = [
            map_to_user_flow(
                operation.http_method or "", url, self.model.prefix, self.model.user_flow_index
            )
            for url in candidates
        ]
        resolved = [mapping for mapping in mappings if mapping.resolved]
        if operation.kind == OP_API_UNRESOLVED or len(resolved) != 1:
            for mapping in mappings or [
                UrlMapping(
                    (operation.http_method or "").upper(),
                    operation.expression,
                    None,
                    None,
                    (),
                    operation.reason or "request URL is not statically resolvable",
                )
            ]:
                self.unresolved.append(
                    {
                        "http_method": mapping.http_method,
                        "request": mapping.raw_url,
                        "normalized_path": mapping.path,
                        "candidate_user_flows": list(mapping.matches),
                        "path": component_path,
                        "symbol": symbol,
                        "line_start": operation.line,
                        "line_end": operation.end_line,
                        "reason": mapping.reason or operation.reason or "unresolved request",
                    }
                )
            self.pending_order = operation.awaited
            self.pending_mechanisms = (MECHANISM_AWAIT,) if operation.awaited else ()
            return False

        mapping = resolved[0]
        ordered = bool(self.steps) and self.pending_order
        if self.steps and not ordered:
            self.stop_reason = (
                f"no ordering evidence between {self.steps[-1].user_flow_id} and "
                f"{mapping.user_flow_id}: the preceding operation is neither awaited nor "
                f"chained through a resolved promise"
            )
            return True
        inherited = self._residual_conditions(
            tuple(condition for condition, _ in self.condition_stack)
        )
        activating = self._residual_conditions(
            tuple(
                condition
                for condition, first_step_position in self.condition_stack
                if first_step_position == len(self.steps)
            )
        )
        local = self._residual_conditions(operation.conditions)
        residual = _dedupe_conditions((*activating, *local))
        inherited_only = _dedupe_conditions(
            tuple(condition for condition in inherited if condition not in activating)
        )
        loop_interval = self._current_loop(operation)
        mechanisms = _dedupe(
            (
                *self.pending_mechanisms,
                *((MECHANISM_CONDITIONAL,) if residual else ()),
                *((MECHANISM_INTERVAL,) if loop_interval is not None else ()),
            )
        )
        self.steps.append(
            ChainStep(
                user_flow_id=str(mapping.user_flow_id),
                http_method=mapping.http_method,
                path=str(mapping.path),
                raw_url=mapping.raw_url,
                component_path=component_path,
                symbol=symbol,
                provenance=provenance,
                trigger=self._trigger(residual, loop_interval, mechanisms),
                mechanisms=mechanisms,
                conditions=residual,
                inherited_conditions=inherited_only,
                loop_interval_ms=loop_interval,
                ordered_from_previous=ordered,
                order_mechanisms=_dedupe(self.pending_mechanisms) if ordered else (),
            )
        )
        if operation.then_operations:
            self.pending_order = True
            self.pending_mechanisms = (MECHANISM_THEN,)
            if self.walk(operation.then_operations, component_path, function_name, depth):
                return True
        self.pending_order = operation.awaited
        self.pending_mechanisms = (MECHANISM_AWAIT,) if operation.awaited else ()
        return False

    def _trigger(
        self,
        residual: tuple[Condition, ...],
        loop_interval: int | None,
        mechanisms: tuple[str, ...],
    ) -> str:
        if residual:
            return TRIGGER_CONDITIONAL
        if loop_interval is not None or MECHANISM_LIFECYCLE in mechanisms:
            return TRIGGER_AUTOMATIC
        if MECHANISM_ENTRY in mechanisms or MECHANISM_VUEX in mechanisms:
            return TRIGGER_USER_ACTION
        return TRIGGER_AUTOMATIC

    def _handle_this_call(
        self, operation: Operation, component_path: str, function_name: str, depth: int
    ) -> bool:
        component = self.model.component(component_path)
        target = operation.target or ""
        if component is None or not target:
            return False
        if target in component.mapped_actions:
            state = self.model.store.state_written_by(target)
            if state:
                self.state_written.add(state)
            else:
                self.notes.append(
                    f"{component_path}: mapped action {target!r} does not resolve to a store "
                    f"state key"
                )
            return False
        if component.function(target) is None:
            return False
        if depth >= _MAX_HELPER_DEPTH:
            self.notes.append(
                f"{component_path}: helper depth bound reached at {target!r}; deeper calls are "
                f"not composed"
            )
            return False
        key = (component_path, target)
        if key in self.visited:
            self.notes.append(f"{component_path}: helper cycle at {target!r}; not re-entered")
            return False
        self.visited.add(key)
        snapshot = (self.pending_order, self.pending_mechanisms)
        self.pending_mechanisms = _dedupe((*self.pending_mechanisms, MECHANISM_HELPER))
        inherited = len(self.condition_stack)
        self.condition_stack.extend(
            (condition, len(self.steps)) for condition in operation.conditions
        )
        before = len(self.steps)
        function = component.function(target)
        terminated = self.walk(
            function.operations if function else (), component_path, target, depth + 1
        )
        del self.condition_stack[inherited:]
        self.visited.discard(key)
        if terminated:
            return True
        if len(self.steps) > before:
            # The helper issued at least one request, so whether the caller awaited it decides
            # if that request has completed before the next one starts.
            self.pending_order = operation.awaited
            self.pending_mechanisms = (MECHANISM_AWAIT,) if operation.awaited else ()
        else:
            # A helper that issues no request is synchronous bookkeeping and cannot invalidate
            # ordering evidence the preceding request already established.
            self.pending_order, self.pending_mechanisms = snapshot
        return False

    def _handle_interval(
        self, operation: Operation, component_path: str, function_name: str, depth: int
    ) -> bool:
        """Enter a timer callback as a deferred entry point, never as a continuation.

        A ``setInterval`` body does not run inside the handler that scheduled it, so no await
        in that handler can order a request made in the callback. Ordering evidence is dropped
        at the boundary and the interval is recorded so every request inside carries it.
        """
        if operation.loop_interval_ms is None:
            self.notes.append(
                f"{component_path}: {self.model.symbol(component_path, function_name)} schedules a "
                f"timer with no literal interval; its callback is not composed"
            )
            return False
        self.pending_order = False
        self.pending_mechanisms = (MECHANISM_INTERVAL,)
        self.loop_stack.append(operation.loop_interval_ms)
        terminated = self.walk(
            operation.then_operations, component_path, function_name, depth
        )
        self.loop_stack.pop()
        return terminated

    def _handle_navigation(
        self, operation: Operation, component_path: str, function_name: str
    ) -> None:
        symbol = self.model.symbol(component_path, function_name)
        route = self.model.route_for(operation)
        if route is None:
            target = operation.route_name or operation.route_path or "<unknown>"
            self.unknown_routes.append(str(target))
            self.route_failures.append(
                {
                    "path": component_path,
                    "symbol": symbol,
                    "line": operation.line,
                    "target": target,
                    "reason": "no route in the router table declares this path or name",
                }
            )
            self.stop_reason = f"navigation target {target!r} is not a declared route"
            return
        resolution = self.model.view_resolution.get(route.view_path)
        if resolution is None:
            self.stop_reason = f"route {route.name!r} view {route.view_path!r} was not scanned"
            return
        if resolution.is_empty:
            self.empty_views.append(
                {
                    "route": route.name,
                    "route_path": route.path,
                    "view": route.view_path,
                    "reason": resolution.reason or "view is empty",
                }
            )
            self.stop_reason = (
                f"route {route.name!r} renders {route.view_path!r}, which mounts nothing: "
                f"{resolution.reason}"
            )
            return
        if resolution.component_path is None:
            self.route_failures.append(
                {
                    "path": route.view_path,
                    "symbol": route.name,
                    "line": route.line,
                    "target": route.name,
                    "reason": resolution.reason or "view mounts no single component",
                }
            )
            self.stop_reason = (
                f"route {route.name!r} view {route.view_path!r} does not mount exactly one "
                f"component: {resolution.reason}"
            )
            return
        if self.navigation_hops >= _MAX_NAVIGATION_HOPS:
            self.stop_reason = "navigation hop bound reached"
            return
        self.navigation_hops += 1
        destination_path = resolution.component_path
        destination = self.model.component(destination_path)
        if destination is None:
            self.stop_reason = f"destination component {destination_path!r} was not scanned"
            return
        # Only guards that still qualify the transition survive the page boundary.
        self.condition_stack = [
            (condition, len(self.steps))
            for condition in self._residual_conditions(operation.conditions)
        ]
        hooks = [
            name
            for name in LIFECYCLE_HOOKS
            if name in destination.lifecycle and function_issues_request(destination, name)
        ]
        if hooks:
            if len(hooks) > 1:
                self.notes.append(
                    f"{destination_path}: {len(hooks)} lifecycle hooks issue requests "
                    f"({', '.join(hooks)}); only {hooks[0]!r} is composed"
                )
            self.pending_order = True
            self.pending_mechanisms = (MECHANISM_NAVIGATION, MECHANISM_LIFECYCLE)
            self.visited.clear()
            self.visited.add((destination_path, hooks[0]))
            self.walk(destination.lifecycle[hooks[0]].operations, destination_path, hooks[0], 0)
            return
        # No lifecycle request: the next stage would be a user action, which arriving on a page
        # does not cause. Two conditions must both hold before it may be composed. The page must
        # offer exactly one user action that issues a request, so "the next stage" is not a guess
        # between several buttons. And that action must need data this journey produced, which is
        # what makes it the *next* stage rather than an unrelated thing the page can also do.
        offered = sorted(
            name
            for name in destination.template_handlers
            if name in destination.handlers and function_issues_request(destination, name)
        )
        if not offered:
            self.stop_reason = (
                f"route {route.name!r} has no lifecycle request and no user action that issues "
                f"a request; arriving on the page does not prove a further request"
            )
            return
        if len(offered) > 1:
            self.stop_reason = (
                f"route {route.name!r} offers {len(offered)} user actions that issue a request "
                f"({', '.join(offered)}); the next stage is ambiguous"
            )
            return
        candidate = offered[0]
        consumed = state_keys_consumed(destination, self.model.store, candidate)
        if not consumed & self.state_written:
            self.stop_reason = (
                f"route {route.name!r} offers only the user action {candidate!r}, which consumes "
                f"no state this journey wrote; arriving on the page does not prove a further "
                f"request"
            )
            return
        self.pending_order = True
        self.pending_mechanisms = (MECHANISM_NAVIGATION, MECHANISM_VUEX)
        self.visited.clear()
        self.visited.add((destination_path, candidate))
        self.walk(destination.handlers[candidate].operations, destination_path, candidate, 0)


# ---------------------------------------------------------------------------------------
# Declared journeys and rejection probes
# ---------------------------------------------------------------------------------------

ACTOR_PARAMETERIZED = "parameterized_by_user_selected_role"
ACTOR_ROLE_BRANCH = "role_branch"
ACTOR_ROLE_REGION = "role_branch_navigation_region"
ACTOR_UNRESOLVED = "unresolved"

PROBE_EMPTY_VIEW = "empty_destination_view"
PROBE_CHAIN = "chain_below_minimum"
PROBE_ABSENT_CALL_SITES = "absent_call_sites"
PROBE_DISJOINT_HANDLERS = "disjoint_handlers"


@dataclass(frozen=True, slots=True)
class BusinessFlowHypothesis:
    """A declared journey: identity and entry point only, never its steps.

    The catalog supplies what source cannot - a name and a scope. The prover supplies
    everything else and is free to reject the entry it was handed.
    """

    journey_slug: str
    title: str
    entry_component: str
    entry_handler: str
    branch_selector: tuple[tuple[str, str], ...] = ()
    expected_user_flows: tuple[str, ...] = ()
    actor_mode: str = ACTOR_ROLE_REGION

    @property
    def world(self) -> dict[str, str]:
        return dict(self.branch_selector)


@dataclass(frozen=True, slots=True)
class RejectionProbe:
    """A journey Pass 6 declines to canonicalize, with the source check that justifies it."""

    journey_slug: str
    title: str
    probe: str
    scope_note: str
    route_name: str | None = None
    entry_component: str | None = None
    entry_handler: str | None = None
    branch_selector: tuple[tuple[str, str], ...] = ()
    required_absent: tuple[tuple[str, str], ...] = ()
    disjoint_pair: tuple[tuple[str, str], ...] = ()


HYPOTHESES: tuple[BusinessFlowHypothesis, ...] = (
    BusinessFlowHypothesis(
        journey_slug="account-registration-verification",
        title="Account registration and verification",
        entry_component=f"{COMPONENTS_DIR}/SignUpComp.vue",
        entry_handler="signup",
        expected_user_flows=(
            "flow.ftgo.gateway.post.auth.register",
            "flow.ftgo.gateway.post.auth.verify",
        ),
        actor_mode=ACTOR_PARAMETERIZED,
    ),
    BusinessFlowHypothesis(
        journey_slug="customer-login-restaurant-browse",
        title="Customer login and restaurant browsing",
        entry_component=f"{COMPONENTS_DIR}/SignInComp.vue",
        entry_handler="signin",
        branch_selector=(("this.userRole", "customer"),),
        expected_user_flows=(
            "flow.ftgo.gateway.post.auth.login",
            "flow.ftgo.gateway.get.restaurant.get-all-restaurant-info",
        ),
        actor_mode=ACTOR_ROLE_BRANCH,
    ),
    BusinessFlowHypothesis(
        journey_slug="driver-login-bootstrap",
        title="Driver login bootstrap",
        entry_component=f"{COMPONENTS_DIR}/SignInComp.vue",
        entry_handler="signin",
        branch_selector=(("this.userRole", "driver"),),
        expected_user_flows=(
            "flow.ftgo.gateway.post.auth.login",
            "flow.ftgo.gateway.get.vehicle.get-info",
            "flow.ftgo.gateway.get.status.get",
        ),
        actor_mode=ACTOR_ROLE_BRANCH,
    ),
    BusinessFlowHypothesis(
        journey_slug="restaurant-admin-login-bootstrap",
        title="Restaurant admin login bootstrap",
        entry_component=f"{COMPONENTS_DIR}/SignInComp.vue",
        entry_handler="signin",
        branch_selector=(("this.userRole", "restaurant_admin"),),
        expected_user_flows=(
            "flow.ftgo.gateway.post.auth.login",
            "flow.ftgo.gateway.get.restaurant.get-supplier-restaurant-info",
            "flow.ftgo.gateway.post.menu.get-all-menu-item",
        ),
        actor_mode=ACTOR_ROLE_BRANCH,
    ),
    BusinessFlowHypothesis(
        journey_slug="driver-vehicle-onboarding",
        title="Driver vehicle onboarding",
        entry_component=f"{COMPONENTS_DIR}/RegisterVehiclePage.vue",
        entry_handler="registerVehicle",
        expected_user_flows=(
            "flow.ftgo.gateway.post.vehicle.register",
            "flow.ftgo.gateway.get.vehicle.get-info",
            "flow.ftgo.gateway.get.status.get",
        ),
    ),
    BusinessFlowHypothesis(
        journey_slug="driver-active-location-refresh",
        title="Driver active location refresh",
        entry_component=f"{COMPONENTS_DIR}/DeliveryMainPage.vue",
        entry_handler="startRefresh",
        expected_user_flows=(
            "flow.ftgo.gateway.get.status.get",
            "flow.ftgo.gateway.post.location.submit",
        ),
    ),
    BusinessFlowHypothesis(
        journey_slug="restaurant-onboarding",
        title="Restaurant onboarding",
        entry_component=f"{COMPONENTS_DIR}/RegisterRestaurantPage.vue",
        entry_handler="registerRestaurant",
        expected_user_flows=(
            "flow.ftgo.gateway.post.restaurant.register",
            "flow.ftgo.gateway.get.restaurant.get-supplier-restaurant-info",
            "flow.ftgo.gateway.post.menu.get-all-menu-item",
        ),
    ),
    BusinessFlowHypothesis(
        journey_slug="restaurant-menu-add-refresh",
        title="Restaurant menu item add and refresh",
        entry_component=f"{COMPONENTS_DIR}/SupplierMainPage.vue",
        entry_handler="addFood",
        expected_user_flows=(
            "flow.ftgo.gateway.post.menu.add",
            "flow.ftgo.gateway.post.menu.get-all-menu-item",
        ),
    ),
    BusinessFlowHypothesis(
        journey_slug="restaurant-menu-update-refresh",
        title="Restaurant menu item update and refresh",
        entry_component=f"{COMPONENTS_DIR}/SupplierMainPage.vue",
        entry_handler="updateFood",
        expected_user_flows=(
            "flow.ftgo.gateway.put.menu.update",
            "flow.ftgo.gateway.post.menu.get-all-menu-item",
        ),
    ),
    BusinessFlowHypothesis(
        journey_slug="restaurant-menu-delete-refresh",
        title="Restaurant menu item delete and refresh",
        entry_component=f"{COMPONENTS_DIR}/SupplierMainPage.vue",
        entry_handler="confirmDeleteItem",
        expected_user_flows=(
            "flow.ftgo.gateway.delete.menu.delete",
            "flow.ftgo.gateway.post.menu.get-all-menu-item",
        ),
    ),
)

REJECTION_PROBES: tuple[RejectionProbe, ...] = (
    RejectionProbe(
        journey_slug="customer-browse-menu-order-placement",
        title="Customer restaurant browse, menu view and order placement",
        probe=PROBE_EMPTY_VIEW,
        route_name="MenuPage",
        scope_note=(
            "Selecting a restaurant navigates to the MenuPage route, whose view mounts nothing at "
            "this commit, so no menu retrieval or order creation is reachable through the router."
        ),
        entry_component=f"{COMPONENTS_DIR}/CustomerMainPage.vue",
        entry_handler="selectRestaurant",
    ),
    RejectionProbe(
        journey_slug="customer-logout-login",
        title="Customer logout followed by login",
        probe=PROBE_CHAIN,
        entry_component=f"{COMPONENTS_DIR}/CustomerMainPage.vue",
        entry_handler="logout",
        scope_note=(
            "Logout navigates to the sign-in page, but nothing on that page runs automatically and "
            "its login handler consumes no state the logout wrote, so a subsequent login is not "
            "proven."
        ),
    ),
    RejectionProbe(
        journey_slug="driver-online-status-toggle",
        title="Driver online and offline status toggle",
        probe=PROBE_CHAIN,
        entry_component=f"{COMPONENTS_DIR}/DeliveryMainPage.vue",
        entry_handler="toggleActive",
        scope_note=(
            "The toggle posts to /status/online or /status/offline, and Pass 5 approved no "
            "UserFlow for either, so only the status read remains and the journey falls below "
            "the two-flow minimum."
        ),
    ),
    RejectionProbe(
        journey_slug="customer-profile-address-management",
        title="Customer profile and address management",
        probe=PROBE_CHAIN,
        entry_component=f"{COMPONENTS_DIR}/CustomerChangeInfo.vue",
        entry_handler="created",
        scope_note=(
            "The profile page loads user info and addresses from two unawaited calls in the same "
            "hook, so their relative order is not established by source."
        ),
    ),
    RejectionProbe(
        journey_slug="restaurant-vehicle-teardown",
        title="Restaurant and vehicle teardown",
        probe=PROBE_DISJOINT_HANDLERS,
        disjoint_pair=(("DELETE", "/restaurant/delete"), ("DELETE", "/vehicle/delete")),
        scope_note=(
            "Restaurant deletion and vehicle deletion live in different components behind "
            "independent buttons with no call path between them, so no single journey orders them."
        ),
    ),
    RejectionProbe(
        journey_slug="order-lifecycle-create-confirm-delivery",
        title="Order creation, confirmation and delivery",
        probe=PROBE_ABSENT_CALL_SITES,
        required_absent=(
            ("POST", "/order/confirm"),
            ("POST", "/order/reject"),
            ("POST", "/order/update"),
            ("POST", "/order/history"),
        ),
        scope_note=(
            "No reachable component issues an order confirmation, rejection, update or history "
            "request, so the order lifecycle cannot be composed from the frontend at this commit."
        ),
    ),
    RejectionProbe(
        journey_slug="feedback-rating-journey",
        title="Delivery and order feedback rating",
        probe=PROBE_ABSENT_CALL_SITES,
        required_absent=(
            ("POST", "/feedback/order/rating/create"),
            ("POST", "/feedback/delivery/rating/create"),
            ("GET", "/feedback/order/rating/get"),
            ("GET", "/feedback/delivery/rating/get"),
        ),
        scope_note=(
            "The frontend contains no feedback request at all; the Pass-5 feedback UserFlows exist "
            "only as gateway endpoints and a journey would have to be invented from their names."
        ),
    ),
)


# ---------------------------------------------------------------------------------------
# Candidates
# ---------------------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class RelationshipCandidate:
    type: str
    source: str
    target: str
    provenance: Provenance
    detail: dict[str, Any] = field(default_factory=dict)

    def summary(self) -> dict[str, Any]:
        payload: dict[str, Any] = {"type": self.type, "source": self.source, "target": self.target}
        payload.update(self.detail)
        payload.update(self.provenance.as_dict())
        return payload


@dataclass(frozen=True, slots=True)
class BusinessStepCandidate:
    id: str
    title: str
    business_flow_id: str
    position: int
    user_flow_id: str
    http_method: str
    path: str
    trigger: str
    evidence_mechanisms: tuple[str, ...]
    conditions: tuple[Condition, ...]
    inherited_conditions: tuple[Condition, ...]
    loop_interval_ms: int | None
    actor: str | None
    actors: tuple[str, ...]
    provenance: Provenance
    kind: str = FLOW_STEP_KIND

    @property
    def attributes(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "layer": BUSINESS_LAYER,
            "role": BUSINESS_STEP_ROLE,
            "position": self.position,
            "trigger": self.trigger,
            "http_method": self.http_method,
            "path": self.path,
            "evidence_mechanism": list(self.evidence_mechanisms),
        }
        if self.actor:
            payload["actor"] = self.actor
        if self.actors:
            payload["actors"] = list(self.actors)
        if self.conditions:
            payload["condition"] = [item.text for item in self.conditions]
            payload["condition_evidence"] = [item.summary() for item in self.conditions]
        if self.inherited_conditions:
            payload["inherited_condition"] = [item.text for item in self.inherited_conditions]
            payload["inherited_condition_evidence"] = [
                item.summary() for item in self.inherited_conditions
            ]
        if self.loop_interval_ms is not None:
            payload["loop_interval_ms"] = self.loop_interval_ms
        return payload

    def summary(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "business_flow": self.business_flow_id,
            "position": self.position,
            "user_flow": self.user_flow_id,
            "http_method": self.http_method,
            "path": self.path,
            "trigger": self.trigger,
            "evidence_mechanism": list(self.evidence_mechanisms),
            "condition": [item.text for item in self.conditions],
            "inherited_condition": [item.text for item in self.inherited_conditions],
            "loop_interval_ms": self.loop_interval_ms,
            "path_source": self.provenance.source_path,
            "symbol": self.provenance.symbol,
            "line_start": self.provenance.line_start,
            "line_end": self.provenance.line_end,
        }


@dataclass(frozen=True, slots=True)
class BusinessFlowCandidate:
    id: str
    title: str
    journey_slug: str
    entry_component: str
    entry_handler: str
    entry_trigger: str
    branch_selector: tuple[tuple[str, str], ...]
    user_flow_ids: tuple[str, ...]
    expected_user_flows: tuple[str, ...]
    outcome: str
    actor: str | None
    actors: tuple[str, ...]
    actor_resolution: str
    terminated_because: str | None
    unresolved_segments: tuple[str, ...]
    notes: tuple[str, ...]
    source_refs: tuple[Provenance, ...]
    kind: str = BUSINESS_FLOW_KIND

    @property
    def attributes(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "surface": UI_SURFACE,
            "step_count": len(self.user_flow_ids),
            "user_flow_count": len(set(self.user_flow_ids)),
            "entry_component": self.entry_component,
            "entry_handler": self.entry_handler,
            "entry_trigger": self.entry_trigger,
            "actor_resolution": self.actor_resolution,
        }
        if self.actor:
            payload["actor"] = self.actor
        if self.actors:
            payload["actors"] = list(self.actors)
        if self.branch_selector:
            payload["branch_selector"] = {key: value for key, value in self.branch_selector}
        if self.terminated_because:
            payload["terminated_because"] = self.terminated_because
        if self.unresolved_segments:
            payload["unresolved_business_segments"] = list(self.unresolved_segments)
        return payload

    def summary(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "outcome": self.outcome,
            "actor": self.actor,
            "actors": list(self.actors),
            "actor_resolution": self.actor_resolution,
            "entry_component": self.entry_component,
            "entry_handler": self.entry_handler,
            "entry_trigger": self.entry_trigger,
            "branch_selector": {key: value for key, value in self.branch_selector},
            "user_flows": list(self.user_flow_ids),
            "expected_user_flows": list(self.expected_user_flows),
            "terminated_because": self.terminated_because,
            "source_refs": [item.as_dict() for item in self.source_refs],
        }


@dataclass(frozen=True, slots=True)
class ApiCallSite:
    """One HTTP request expression found in the frontend, mapped or not."""

    component_path: str
    symbol: str
    line_start: int
    line_end: int
    http_method: str
    request: str
    reachable: bool
    mapping: UrlMapping
    # One physical call site can name several URLs, as a conditional request URL does. The
    # site stays a single site; the alternatives are recorded here so each can be reported.
    candidate_mappings: tuple[UrlMapping, ...] = ()

    def summary(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "path": self.component_path,
            "symbol": self.symbol,
            "line_start": self.line_start,
            "line_end": self.line_end,
            "http_method": self.mapping.http_method or self.http_method.upper(),
            "request": self.request,
            "normalized_path": self.mapping.path,
            "user_flow": self.mapping.user_flow_id,
            "candidate_user_flows": list(self.mapping.matches),
            "reachable": self.reachable,
            "reason": self.mapping.reason,
        }
        if self.candidate_mappings:
            payload["conditional_requests"] = [
                {
                    "request": mapping.raw_url,
                    "normalized_path": mapping.path,
                    "user_flow": mapping.user_flow_id,
                    "reason": mapping.reason,
                }
                for mapping in self.candidate_mappings
            ]
        return payload

    def unresolved_entries(self) -> list[dict[str, Any]]:
        """One report entry per URL this site can actually request."""
        base = self.summary()
        if not self.candidate_mappings:
            return [base]
        entries: list[dict[str, Any]] = []
        for mapping in self.candidate_mappings:
            entry = dict(base)
            entry.pop("conditional_requests", None)
            entry["request"] = mapping.raw_url
            entry["normalized_path"] = mapping.path
            entry["user_flow"] = mapping.user_flow_id
            entry["candidate_user_flows"] = list(mapping.matches)
            entry["reason"] = mapping.reason
            entries.append(entry)
        return entries


@dataclass(frozen=True, slots=True)
class BusinessFlowExtraction:
    """Immutable result of one Pass-6 run."""

    repository: str
    commit: str
    owner: str | None
    api_prefix: ApiPrefix
    source_files: tuple[str, ...]
    routes: tuple[RouteRecord, ...]
    views: tuple[str, ...]
    components: tuple[str, ...]
    canonical_user_flows: tuple[str, ...]
    call_sites: tuple[ApiCallSite, ...]
    flows: tuple[BusinessFlowCandidate, ...]
    steps: tuple[BusinessStepCandidate, ...]
    relationships: tuple[RelationshipCandidate, ...]
    rejected: tuple[dict[str, Any], ...]
    deferred: tuple[dict[str, Any], ...]
    unresolved_segments: tuple[dict[str, Any], ...]
    route_failures: tuple[dict[str, Any], ...]
    empty_views: tuple[dict[str, Any], ...]
    unknown_routes: tuple[str, ...]
    identity_collisions: tuple[str, ...]
    cycles_detected: tuple[str, ...]
    warnings: tuple[str, ...]

    def steps_of(self, business_flow_id: str) -> tuple[BusinessStepCandidate, ...]:
        return tuple(
            step
            for step in sorted(self.steps, key=lambda item: item.position)
            if step.business_flow_id == business_flow_id
        )

    def relations_for(self, identifier: str) -> tuple[RelationshipCandidate, ...]:
        return tuple(
            relation
            for relation in sorted(
                self.relationships, key=lambda item: (item.type, item.target)
            )
            if relation.source == identifier
        )

    def inbound_relations_for(self, identifier: str) -> tuple[RelationshipCandidate, ...]:
        return tuple(
            relation
            for relation in sorted(
                self.relationships, key=lambda item: (item.type, item.source)
            )
            if relation.target == identifier
        )

    def flows_with_outcome(self, outcome: str) -> tuple[BusinessFlowCandidate, ...]:
        return tuple(flow for flow in self.flows if flow.outcome == outcome)


# ---------------------------------------------------------------------------------------
# Branch worlds and actor resolution
# ---------------------------------------------------------------------------------------


def collect_branch_literals(
    model: FrontendModel,
    component_path: str,
    handler: str,
    *,
    depth: int = 0,
    seen: frozenset[str] = frozenset(),
) -> dict[str, tuple[str, ...]]:
    """Equality-tested literals reachable from one handler, grouped by tested expression."""
    component = model.component(component_path)
    if component is None or depth > _MAX_HELPER_DEPTH or handler in seen:
        return {}
    function = component.function(handler)
    if function is None:
        return {}
    grouped: dict[str, set[str]] = {}
    for operation in _all_operations(function.operations):
        for condition in operation.conditions:
            if condition.subject and condition.literal:
                grouped.setdefault(condition.subject, set()).add(condition.literal)
        if operation.kind == OP_THIS_CALL and operation.target in component.handlers:
            nested = collect_branch_literals(
                model, component_path, operation.target, depth=depth + 1, seen=seen | {handler}
            )
            for subject, literals in nested.items():
                grouped.setdefault(subject, set()).update(literals)
    return {subject: tuple(sorted(values)) for subject, values in sorted(grouped.items())}


def branch_worlds(
    model: FrontendModel, component_path: str, handler: str
) -> tuple[tuple[dict[str, str], list[str]], ...]:
    """Enumerate the mutually exclusive branch worlds of one entry handler.

    Only one tested expression is split at a time. Two independent multi-valued tests would
    make the number of worlds a product rather than a fact, so the second is left in place as
    an ordinary condition on the step and reported.
    """
    grouped = collect_branch_literals(model, component_path, handler)
    multi = {subject: values for subject, values in grouped.items() if len(values) > 1}
    if not multi:
        return (({}, []),)
    chosen = sorted(multi, key=lambda subject: (-len(multi[subject]), subject))[0]
    notes: list[str] = []
    if len(multi) > 1:
        others = ", ".join(sorted(subject for subject in multi if subject != chosen))
        notes.append(
            f"{component_path}.{handler}: split on {chosen!r} only; {others} remain as step "
            f"conditions"
        )
    return tuple(({chosen: literal}, list(notes)) for literal in multi[chosen])


@dataclass(frozen=True, slots=True)
class NavigationEdge:
    source_component: str
    destination_component: str
    role_literals: tuple[str, ...]


def build_navigation_graph(model: FrontendModel) -> tuple[NavigationEdge, ...]:
    """Component-to-component transitions the router can actually perform."""
    edges: set[NavigationEdge] = set()
    for component_path in sorted(model.components):
        component = model.components[component_path]
        for handler in model.reachable_handlers.get(component_path, ()):
            function = component.function(handler)
            if function is None:
                continue
            for operation in _all_operations(function.operations):
                if operation.kind != OP_NAVIGATION:
                    continue
                route = model.route_for(operation)
                if route is None:
                    continue
                resolution = model.view_resolution.get(route.view_path)
                if resolution is None or resolution.component_path is None:
                    continue
                literals = tuple(
                    sorted(
                        {
                            condition.literal
                            for condition in operation.conditions
                            if condition.literal in model.role_literals
                        }
                    )
                )
                edges.add(
                    NavigationEdge(
                        source_component=component_path,
                        destination_component=resolution.component_path,
                        role_literals=literals,
                    )
                )
    return tuple(
        sorted(edges, key=lambda item: (item.source_component, item.destination_component))
    )


def build_role_regions(edges: tuple[NavigationEdge, ...]) -> dict[str, str]:
    """Map each component to the single role branch whose region reaches it, if any.

    A role branch in the login handler sends each role to a different landing page. Walking
    *forward* from those landing pages, without re-entering the component that performs the
    branch, gives the set of pages a role can be on. Walking backwards instead would be
    useless here: every page's logout returns to the sign-in page, so backward reachability
    collapses the whole application into one region and proves nothing.
    """
    branch_sources = {edge.source_component for edge in edges if edge.role_literals}
    roots: dict[str, set[str]] = {}
    forward: dict[str, list[str]] = {}
    for edge in edges:
        forward.setdefault(edge.source_component, []).append(edge.destination_component)
        for literal in edge.role_literals:
            roots.setdefault(literal, set()).add(edge.destination_component)

    owners: dict[str, set[str]] = {}
    for literal, starts in sorted(roots.items()):
        seen: set[str] = set()
        frontier = [(start, 0) for start in sorted(starts)]
        while frontier:
            node, depth = frontier.pop()
            if node in seen or node in branch_sources or depth > _MAX_ACTOR_TRACE_DEPTH:
                continue
            seen.add(node)
            for following in sorted(forward.get(node, ())):
                frontier.append((following, depth + 1))
        for member in seen:
            owners.setdefault(member, set()).add(literal)
    return {
        component: next(iter(literals))
        for component, literals in sorted(owners.items())
        if len(literals) == 1
    }


def resolve_actor_by_navigation(
    edges: tuple[NavigationEdge, ...], component_path: str
) -> tuple[str | None, str]:
    """Resolve the actor of one component from the role-branch region that reaches it."""
    regions = build_role_regions(edges)
    actor = regions.get(component_path)
    return (actor, ACTOR_ROLE_REGION) if actor else (None, ACTOR_UNRESOLVED)


# ---------------------------------------------------------------------------------------
# Extraction
# ---------------------------------------------------------------------------------------


def _frontend_sources(record: RepositoryRecord) -> tuple[str, ...]:
    candidates = resolve_source_files(record, FRONTEND_SOURCE_KIND)
    return tuple(
        path
        for path in candidates
        if path.startswith(f"{UI_ROOT}/") and path.endswith((VUE_SUFFIX, JS_SUFFIX))
    )


def _read(record: RepositoryRecord, relative_path: str) -> str | None:
    target = record.path / relative_path
    if not target.is_file():
        return None
    return target.read_text(encoding="utf-8")


def _canonical_step_ids(knowledge_root: Path) -> frozenset[str]:
    steps_dir = knowledge_root / "wiki" / "steps"
    if not steps_dir.is_dir():
        return frozenset()
    return frozenset(page.stem for page in steps_dir.glob("*.md"))


def build_frontend_model(
    record: RepositoryRecord,
    commit: str,
    *,
    canonical_flows: tuple[UserFlowRef, ...],
    warnings: list[str],
) -> FrontendModel:
    """Parse the frontend once and resolve routes, views, store and the API prefix."""
    frontend_files = _frontend_sources(record)
    component_paths = frozenset(
        path
        for path in frontend_files
        if path.startswith(f"{COMPONENTS_DIR}/") and path.endswith(VUE_SUFFIX)
    )
    view_paths = frozenset(
        path
        for path in frontend_files
        if path.startswith(f"{VIEWS_DIR}/") and path.endswith(VUE_SUFFIX)
    )

    components: dict[str, ComponentFacts] = {}
    for path in sorted(component_paths):
        text = _read(record, path)
        if text is None:
            warnings.append(f"{path}: declared by the manifest but not readable")
            continue
        components[path] = parse_component(path, text)

    views: dict[str, ComponentFacts] = {}
    for path in sorted(view_paths):
        text = _read(record, path)
        if text is None:
            warnings.append(f"{path}: declared by the manifest but not readable")
            continue
        views[path] = parse_component(path, text)

    resolution = {
        path: resolve_view(view, frozenset(components)) for path, view in sorted(views.items())
    }
    for path, resolved in sorted(resolution.items()):
        if resolved.component_path is None:
            warnings.append(f"{path}: {resolved.reason}")

    router_text = _read(record, ROUTER_PATH)
    if router_text is None:
        raise BusinessFlowExtractionError(
            f"{ROUTER_PATH} is missing; route reachability cannot be proven without the router "
            f"table."
        )
    routes, router_warnings = parse_router(
        build_source_text(ROUTER_PATH, router_text), frozenset(views)
    )
    warnings.extend(router_warnings)

    store_text = _read(record, STORE_PATH)
    store = (
        parse_store(build_source_text(STORE_PATH, store_text))
        if store_text is not None
        else StoreFacts({}, {})
    )
    if store_text is None:
        warnings.append(f"{STORE_PATH} is missing; no Vuex data dependency can be proven")

    prefix = resolve_api_prefix(
        record.id,
        commit,
        _read(record, GATEWAY_SERVICE_CONFIG_PATH),
        _read(record, GATEWAY_MAIN_PATH),
    )
    if not prefix.resolved:
        warnings.append(f"API prefix is not source-backed: {prefix.reason}")

    reachable = {
        path: compute_reachable_handlers(facts) for path, facts in sorted(components.items())
    }
    role_literals = frozenset(
        literal for facts in components.values() for literal in facts.declared_role_literals
    )

    mounted_components = {
        resolved.component_path
        for resolved in resolution.values()
        if resolved.component_path is not None
    }
    for path in sorted(set(components) - mounted_components):
        warnings.append(
            f"{path}: no routed view mounts this component, so nothing in it is reachable through "
            f"the router"
        )

    return FrontendModel(
        repository=record.id,
        commit=commit,
        components=components,
        views=views,
        view_resolution=resolution,
        routes_by_path={route.path: route for route in routes},
        routes_by_name={route.name: route for route in routes},
        store=store,
        prefix=prefix,
        user_flow_index=build_user_flow_index(canonical_flows),
        reachable_handlers=reachable,
        role_literals=role_literals,
    )


def collect_call_sites(model: FrontendModel) -> tuple[ApiCallSite, ...]:
    """Inventory every HTTP request expression in the frontend, mapped or not."""
    sites: list[ApiCallSite] = []
    for path in sorted(model.components) + sorted(model.views):
        component = model.components.get(path) or model.views[path]
        reachable = set(model.reachable_handlers.get(path, ()))
        functions = {**component.handlers, **component.lifecycle}
        for name in sorted(functions):
            for operation in _all_operations(functions[name].operations):
                if operation.kind not in (OP_API, OP_API_UNRESOLVED):
                    continue
                urls = operation.url_candidates or ((operation.url,) if operation.url else ())
                candidates = tuple(
                    map_to_user_flow(
                        operation.http_method or "", url, model.prefix, model.user_flow_index
                    )
                    for url in urls
                )
                opaque = UrlMapping(
                    (operation.http_method or "").upper(),
                    operation.expression,
                    None,
                    None,
                    (),
                    operation.reason or "request URL is not statically resolvable",
                )
                single = len(candidates) == 1 and operation.kind == OP_API
                sites.append(
                    ApiCallSite(
                        component_path=path,
                        symbol=model.symbol(path, name),
                        line_start=operation.line,
                        line_end=operation.end_line,
                        http_method=operation.http_method or "",
                        request=urls[0] if single else operation.expression,
                        reachable=name in reachable,
                        mapping=candidates[0] if single else opaque,
                        candidate_mappings=() if single else candidates,
                    )
                )
    return tuple(
        sorted(sites, key=lambda item: (item.component_path, item.line_start, item.request))
    )


def _assign_step_slugs(user_flow_ids: tuple[str, ...]) -> tuple[str, ...]:
    """Derive short step slugs from UserFlow ids, qualifying only on collision."""
    parts = [user_flow_step_slug(identifier) for identifier in user_flow_ids]
    actions = [action for _, action in parts]
    slugs: list[str] = []
    for position, (resource, action) in enumerate(parts):
        if actions.count(action) == 1:
            slugs.append(action)
            continue
        qualified = f"{resource}.{action}" if resource else action
        if [f"{r}.{a}" if r else a for r, a in parts].count(qualified) == 1:
            slugs.append(qualified)
            continue
        slugs.append(f"{qualified}.{position + 1}")
    return tuple(slugs)


def _outcome(chain: ChainResult, expected: tuple[str, ...]) -> str:
    derived = chain.user_flow_ids
    if len(set(derived)) < MIN_USER_FLOWS_PER_BUSINESS_FLOW:
        return OUTCOME_REJECTED
    if expected and derived != expected:
        return OUTCOME_PARTIAL
    return OUTCOME_RESOLVED


def _resolve_actor(
    hypothesis: BusinessFlowHypothesis,
    chain: ChainResult,
    walker: ChainWalker,
    model: FrontendModel,
    edges: tuple[NavigationEdge, ...],
) -> tuple[str | None, tuple[str, ...], str]:
    del chain
    if hypothesis.actor_mode == ACTOR_PARAMETERIZED:
        entry = model.component(hypothesis.entry_component)
        declared = entry.declared_role_literals if entry else ()
        roles = tuple(role for role in declared if role in model.role_literals)
        return None, roles, ACTOR_PARAMETERIZED
    if hypothesis.actor_mode == ACTOR_ROLE_BRANCH:
        literals = sorted(
            {literal for literal in walker.role_branch_literals if literal in model.role_literals}
        )
        if len(literals) == 1:
            return literals[0], (), ACTOR_ROLE_BRANCH
        return None, tuple(literals), ACTOR_UNRESOLVED
    actor, resolution = resolve_actor_by_navigation(edges, hypothesis.entry_component)
    return actor, (), resolution


def _count_sites(call_sites: tuple[ApiCallSite, ...], method: str, path: str) -> int:
    return sum(
        1
        for site in call_sites
        if (site.mapping.http_method, site.mapping.path) == (method, path)
    )


def _run_probe(
    probe: RejectionProbe, model: FrontendModel, call_sites: tuple[ApiCallSite, ...]
) -> dict[str, Any]:
    """Verify from source that a declared-but-withheld journey really is not provable."""
    evidence: dict[str, Any] = {
        "id": business_flow_id(model.repository, probe.journey_slug),
        "title": probe.title,
        "probe": probe.probe,
        "scope_note": probe.scope_note,
        "verified": False,
        "evidence": [],
    }
    if probe.probe == PROBE_EMPTY_VIEW:
        route = model.routes_by_name.get(probe.route_name or "")
        if route is None:
            evidence["evidence"] = [f"route {probe.route_name!r} is not declared"]
            evidence["verified"] = True
            return evidence
        resolved = model.view_resolution.get(route.view_path)
        empty = resolved is not None and (resolved.is_empty or resolved.component_path is None)
        evidence["verified"] = bool(empty)
        evidence["evidence"] = [
            f"route {route.name!r} -> {route.view_path}: "
            f"{resolved.reason if resolved else 'view was not scanned'}"
        ]
        return evidence
    if probe.probe == PROBE_CHAIN:
        walker = ChainWalker(model, dict(probe.branch_selector))
        chain = walker.run(probe.entry_component or "", probe.entry_handler or "")
        evidence["derived_user_flows"] = list(chain.user_flow_ids)
        evidence["terminated_because"] = chain.stop_reason
        evidence["verified"] = len(set(chain.user_flow_ids)) < MIN_USER_FLOWS_PER_BUSINESS_FLOW
        evidence["evidence"] = [
            f"{probe.entry_component}#{probe.entry_handler} composes "
            f"{len(set(chain.user_flow_ids))} distinct approved UserFlow(s)"
        ]
        return evidence
    if probe.probe == PROBE_ABSENT_CALL_SITES:
        present = [
            site.summary()
            for site in call_sites
            if (site.mapping.http_method, site.mapping.path) in set(probe.required_absent)
        ]
        evidence["verified"] = not present
        evidence["evidence"] = [
            f"{method} {path}: {_count_sites(call_sites, method, path)} frontend call sites"
            for method, path in probe.required_absent
        ]
        return evidence
    owners: dict[tuple[str, str], set[str]] = {}
    for site in call_sites:
        key = (site.mapping.http_method, site.mapping.path or "")
        if key in set(probe.disjoint_pair):
            owners.setdefault(key, set()).add(site.component_path)
    components = sorted({path for paths in owners.values() for path in paths})
    evidence["verified"] = len(owners) == len(probe.disjoint_pair) and len(components) > 1
    evidence["evidence"] = [
        f"{method} {path}: {', '.join(sorted(owners.get((method, path), {'<absent>'})))}"
        for method, path in probe.disjoint_pair
    ]
    return evidence


def collect_route_findings(model: FrontendModel) -> tuple[
    tuple[dict[str, Any], ...], tuple[dict[str, Any], ...], tuple[str, ...]
]:
    """Check every navigation a reachable handler can perform, wherever it sits.

    The chain walker stops at the first transition, so a defective navigation further down a
    handler would never be reported by composition alone. This sweep is independent of
    composition: it looks at every navigation expression in every reachable handler.
    """
    failures: list[dict[str, Any]] = []
    empty: list[dict[str, Any]] = []
    unknown: set[str] = set()
    for component_path in sorted(model.components):
        component = model.components[component_path]
        for handler in model.reachable_handlers.get(component_path, ()):
            function = component.function(handler)
            if function is None:
                continue
            symbol = model.symbol(component_path, handler)
            for operation in _all_operations(function.operations):
                if operation.kind == OP_NAVIGATION_UNRESOLVED:
                    failures.append(
                        {
                            "path": component_path,
                            "symbol": symbol,
                            "line": operation.line,
                            "expression": operation.expression,
                            "reason": operation.reason or "navigation destination is not static",
                        }
                    )
                    continue
                if operation.kind != OP_NAVIGATION:
                    continue
                route = model.route_for(operation)
                if route is None:
                    target = operation.route_name or operation.route_path or "<unknown>"
                    unknown.add(str(target))
                    failures.append(
                        {
                            "path": component_path,
                            "symbol": symbol,
                            "line": operation.line,
                            "target": target,
                            "reason": "no route in the router table declares this path or name",
                        }
                    )
                    continue
                resolved = model.view_resolution.get(route.view_path)
                if resolved is None or resolved.component_path is not None:
                    continue
                entry = {
                    "route": route.name,
                    "route_path": route.path,
                    "view": route.view_path,
                    "reason": resolved.reason or "view mounts nothing",
                }
                if entry not in empty:
                    empty.append(entry)
    return tuple(failures), tuple(empty), tuple(sorted(unknown))


@dataclass(slots=True)
class ReachabilityFindings:
    """Route and view defects seen while sweeping every reachable entry point."""

    route_failures: list[dict[str, Any]] = field(default_factory=list)
    empty_views: list[dict[str, Any]] = field(default_factory=list)
    unknown_routes: list[str] = field(default_factory=list)

    def absorb(self, chain: ChainResult) -> None:
        for failure in chain.route_failures:
            if failure not in self.route_failures:
                self.route_failures.append(failure)
        for view in chain.empty_views:
            if view not in self.empty_views:
                self.empty_views.append(view)
        for route in chain.unknown_routes:
            if route not in self.unknown_routes:
                self.unknown_routes.append(route)


def _discover_deferred(
    model: FrontendModel, claimed: set[tuple[str, ...]], findings: ReachabilityFindings
) -> tuple[tuple[dict[str, Any], ...], tuple[str, ...]]:
    """Report every other provable composition without canonicalizing it.

    Pass 6 canonicalizes a bounded, named set of journeys. Anything else the source proves is
    still surfaced here so the difference between "not provable" and "out of this pass's scope"
    stays visible instead of silently disappearing.
    """
    found: dict[tuple[str, ...], dict[str, Any]] = {}
    notes: list[str] = []
    for component_path in sorted(model.components):
        for handler in model.reachable_handlers.get(component_path, ()):
            for world, world_notes in branch_worlds(model, component_path, handler):
                notes.extend(world_notes)
                walker = ChainWalker(model, world)
                chain = walker.run(component_path, handler)
                findings.absorb(chain)
                identity = chain.user_flow_ids
                if len(set(identity)) < MIN_USER_FLOWS_PER_BUSINESS_FLOW or identity in claimed:
                    continue
                if identity in found:
                    found[identity]["entry_points"].append(f"{component_path}#{handler}")
                    continue
                found[identity] = {
                    "user_flows": list(identity),
                    "entry_points": [f"{component_path}#{handler}"],
                    "branch_selector": dict(world),
                    "terminated_because": chain.stop_reason,
                    "reason": (
                        "provable composition outside the declared Pass-6 journey catalog; "
                        "deferred to a later reviewed pass rather than canonicalized here"
                    ),
                }
    for entry in found.values():
        entry["entry_points"] = sorted(set(entry["entry_points"]))
    ordered = tuple(found[key] for key in sorted(found))
    return ordered, tuple(sorted(set(notes)))


def _detect_cycles(relationships: tuple[RelationshipCandidate, ...]) -> tuple[str, ...]:
    """A business journey is a linear order; a PRECEDES cycle would mean the walk lied."""
    graph: dict[str, set[str]] = {}
    for relation in relationships:
        if relation.type == PRECEDES:
            graph.setdefault(relation.source, set()).add(relation.target)
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
    return tuple(sorted(set(cycles)))


def extract_business_flow(
    record: RepositoryRecord,
    commit: str,
    *,
    knowledge_root: Path | None = None,
) -> BusinessFlowExtraction:
    """Compose approved Pass-5 UserFlows into deterministic business journeys."""
    from ..settings import settings

    root = knowledge_root or settings.knowledge_root
    canonical_flows = load_canonical_user_flows(root / CANONICAL_FLOWS_DIR)
    canonical_steps = _canonical_step_ids(root)

    warnings: list[str] = []
    model = build_frontend_model(record, commit, canonical_flows=canonical_flows, warnings=warnings)
    edges = build_navigation_graph(model)
    call_sites = collect_call_sites(model)

    flows: list[BusinessFlowCandidate] = []
    steps: list[BusinessStepCandidate] = []
    relationships: list[RelationshipCandidate] = []
    rejected: list[dict[str, Any]] = []
    collisions: list[str] = []
    claimed: set[tuple[str, ...]] = set()
    findings = ReachabilityFindings()

    for hypothesis in HYPOTHESES:
        walker = ChainWalker(model, hypothesis.world)
        chain = walker.run(hypothesis.entry_component, hypothesis.entry_handler)
        findings.absorb(chain)
        warnings.extend(chain.notes)
        outcome = _outcome(chain, hypothesis.expected_user_flows)
        identifier = business_flow_id(model.repository, hypothesis.journey_slug)
        if outcome == OUTCOME_REJECTED:
            rejected.append(
                {
                    "id": identifier,
                    "title": hypothesis.title,
                    "probe": "declared_journey",
                    "entry_component": hypothesis.entry_component,
                    "entry_handler": hypothesis.entry_handler,
                    "branch_selector": hypothesis.world,
                    "derived_user_flows": list(chain.user_flow_ids),
                    "expected_user_flows": list(hypothesis.expected_user_flows),
                    "terminated_because": chain.stop_reason,
                    "verified": True,
                    "reason": (
                        f"source composes {len(set(chain.user_flow_ids))} distinct approved "
                        f"UserFlow(s); at least {MIN_USER_FLOWS_PER_BUSINESS_FLOW} are required"
                    ),
                }
            )
            continue

        actor, actors, actor_resolution = _resolve_actor(hypothesis, chain, walker, model, edges)
        entry_component = model.component(hypothesis.entry_component)
        entry_trigger = (
            classify_entry_trigger(entry_component, hypothesis.entry_handler)
            if entry_component is not None
            else TRIGGER_AUTOMATIC
        )
        candidate = BusinessFlowCandidate(
            id=identifier,
            title=hypothesis.title,
            journey_slug=hypothesis.journey_slug,
            entry_component=hypothesis.entry_component,
            entry_handler=hypothesis.entry_handler,
            entry_trigger=entry_trigger,
            branch_selector=hypothesis.branch_selector,
            user_flow_ids=chain.user_flow_ids,
            expected_user_flows=hypothesis.expected_user_flows,
            outcome=outcome,
            actor=actor,
            actors=actors,
            actor_resolution=actor_resolution,
            terminated_because=chain.stop_reason,
            unresolved_segments=tuple(
                sorted(
                    {
                        f"{item['http_method']} {item['request']}"
                        for item in chain.unresolved_segments
                    }
                )
            ),
            notes=chain.notes,
            source_refs=_dedupe_provenances(tuple(step.provenance for step in chain.steps)),
        )
        flows.append(candidate)
        claimed.add(chain.user_flow_ids)

        slugs = _assign_step_slugs(chain.user_flow_ids)
        previous_id: str | None = None
        for position, (step, slug) in enumerate(zip(chain.steps, slugs, strict=True), start=1):
            step_identifier = business_step_id(model.repository, hypothesis.journey_slug, slug)
            step_candidate = BusinessStepCandidate(
                id=step_identifier,
                title=f"{hypothesis.title}: {step.http_method} {step.path}",
                business_flow_id=identifier,
                position=position,
                user_flow_id=step.user_flow_id,
                http_method=step.http_method,
                path=step.path,
                trigger=step.trigger,
                evidence_mechanisms=step.mechanisms,
                conditions=step.conditions,
                inherited_conditions=step.inherited_conditions,
                loop_interval_ms=step.loop_interval_ms,
                actor=actor,
                actors=actors,
                provenance=step.provenance,
            )
            steps.append(step_candidate)
            relationships.append(
                RelationshipCandidate(
                    type=CONTAINS,
                    source=identifier,
                    target=step_identifier,
                    provenance=step.provenance,
                    detail={"position": position, "layer": BUSINESS_LAYER},
                )
            )
            relationships.append(
                RelationshipCandidate(
                    type=DERIVED_FROM,
                    source=step_identifier,
                    target=step.user_flow_id,
                    provenance=step.provenance,
                    detail={"evidence_mechanism": list(step.mechanisms)},
                )
            )
            if previous_id is not None:
                relationships.append(
                    RelationshipCandidate(
                        type=PRECEDES,
                        source=previous_id,
                        target=step_identifier,
                        provenance=step.provenance,
                        detail={"evidence_mechanism": list(step.order_mechanisms)},
                    )
                )
            previous_id = step_identifier

    for probe in REJECTION_PROBES:
        rejected.append(_run_probe(probe, model, call_sites))

    deferred, deferred_notes = _discover_deferred(model, claimed, findings)
    warnings.extend(deferred_notes)

    static_failures, static_empty, static_unknown = collect_route_findings(model)
    for failure in static_failures:
        if failure not in findings.route_failures:
            findings.route_failures.append(failure)
    for view in static_empty:
        if view not in findings.empty_views:
            findings.empty_views.append(view)
    findings.unknown_routes.extend(static_unknown)

    seen_ids: set[str] = set()
    for identifier in [flow.id for flow in flows] + [step.id for step in steps]:
        if identifier in seen_ids:
            collisions.append(f"duplicate candidate id {identifier}")
        seen_ids.add(identifier)
        if collides_with_pass5(identifier):
            collisions.append(f"{identifier} lands in a Pass-5 identity namespace")
        if identifier in canonical_steps:
            collisions.append(f"{identifier} collides with an approved Pass-5 FlowStep page")

    unresolved_from_sites = [
        entry
        for site in call_sites
        if not site.mapping.resolved
        for entry in site.unresolved_entries()
    ]

    return BusinessFlowExtraction(
        repository=model.repository,
        commit=model.commit,
        owner=record.owner,
        api_prefix=model.prefix,
        source_files=tuple(
            sorted(
                {
                    *model.components,
                    *model.views,
                    ROUTER_PATH,
                    STORE_PATH,
                    GATEWAY_SERVICE_CONFIG_PATH,
                    GATEWAY_MAIN_PATH,
                }
            )
        ),
        routes=tuple(sorted(model.routes_by_path.values(), key=lambda item: item.path)),
        views=tuple(sorted(model.views)),
        components=tuple(sorted(model.components)),
        canonical_user_flows=tuple(ref.id for ref in canonical_flows),
        call_sites=call_sites,
        flows=tuple(flows),
        steps=tuple(steps),
        relationships=tuple(
            sorted(relationships, key=lambda item: (item.type, item.source, item.target))
        ),
        rejected=tuple(rejected),
        deferred=deferred,
        unresolved_segments=tuple(
            sorted(
                unresolved_from_sites,
                key=lambda item: (item["path"], item["line_start"], str(item["request"])),
            )
        ),
        route_failures=tuple(
            sorted(
                findings.route_failures,
                key=lambda item: (item["path"], item["line"], str(item["reason"])),
            )
        ),
        empty_views=tuple(
            sorted(findings.empty_views, key=lambda item: (item["route"], item["view"]))
        ),
        unknown_routes=tuple(sorted(set(findings.unknown_routes))),
        identity_collisions=tuple(sorted(set(collisions))),
        cycles_detected=_detect_cycles(tuple(relationships)),
        warnings=tuple(sorted(set(warnings))),
    )


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
    *, identifier: str, kind: str, title: str, extraction: BusinessFlowExtraction
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


def render_business_flow_markdown(
    flow: BusinessFlowCandidate, extraction: BusinessFlowExtraction
) -> str:
    frontmatter = _base_frontmatter(
        identifier=flow.id, kind=flow.kind, title=flow.title, extraction=extraction
    )
    frontmatter["surface"] = UI_SURFACE
    frontmatter["completeness"] = flow.outcome
    frontmatter["entry_component"] = flow.entry_component
    frontmatter["entry_handler"] = flow.entry_handler
    if flow.actor:
        frontmatter["actor"] = flow.actor
    if flow.actors:
        frontmatter["actors"] = list(flow.actors)
    frontmatter["actor_resolution"] = flow.actor_resolution
    frontmatter["user_flows"] = list(flow.user_flow_ids)
    if flow.unresolved_segments:
        frontmatter["unresolved_business_segments"] = list(flow.unresolved_segments)
    frontmatter["source_refs"] = [item.as_dict() for item in flow.source_refs]
    outbound = extraction.relations_for(flow.id)
    if outbound:
        frontmatter["relations"] = _relation_entries(outbound)
    frontmatter["attributes"] = flow.attributes

    body = [
        f"# {flow.title}",
        "",
        f"Candidate business journey composed from approved Pass-5 UserFlow pages using "
        f"reachability evidence in `{extraction.repository}` at commit `{extraction.commit}`.",
        "",
        f"- Surface: `{UI_SURFACE}`",
        f"- Entry: `{flow.entry_component}` handler `{flow.entry_handler}`",
        f"- Completeness: `{flow.outcome}`",
        f"- Actor: `{flow.actor or ', '.join(flow.actors) or 'unresolved'}` "
        f"(`{flow.actor_resolution}`)",
        f"- Evidence class: `{EVIDENCE_TYPE}`",
        "",
        "## Ordered user flows",
        "",
    ]
    for step in extraction.steps_of(flow.id):
        marker = f" `{step.trigger}`"
        body.append(f"{step.position}. `{step.user_flow_id}`{marker} via `{step.id}`")
    body.append("")
    if flow.terminated_because:
        body.extend(
            [
                "## Where the journey stops",
                "",
                "The composition ends here because source does not carry it further:",
                "",
                f"- {flow.terminated_because}",
                "",
            ]
        )
    if flow.unresolved_segments:
        body.extend(
            [
                "## Unresolved business segments",
                "",
                "These requests happen on the same path but map to no approved Pass-5 UserFlow, so "
                "they are recorded rather than turned into steps:",
                "",
            ]
        )
        body.extend(f"- `{segment}`" for segment in flow.unresolved_segments)
        body.append("")
    body.extend(
        [
            "## Review notes",
            "",
            "This page is a candidate awaiting review. It adds no technical detail: every step "
            "is a reference to an existing approved UserFlow, and every ordering edge carries "
            "the reachability evidence that established it.",
            "",
        ]
    )
    return _render_page(frontmatter, body)


def render_business_step_markdown(
    step: BusinessStepCandidate, extraction: BusinessFlowExtraction
) -> str:
    frontmatter = _base_frontmatter(
        identifier=step.id, kind=step.kind, title=step.title, extraction=extraction
    )
    frontmatter["layer"] = BUSINESS_LAYER
    frontmatter["role"] = BUSINESS_STEP_ROLE
    frontmatter["business_flow"] = step.business_flow_id
    frontmatter["position"] = step.position
    frontmatter["user_flow"] = step.user_flow_id
    frontmatter["http_method"] = step.http_method
    frontmatter["path"] = step.path
    frontmatter["trigger"] = step.trigger
    frontmatter["evidence_mechanism"] = list(step.evidence_mechanisms)
    if step.conditions:
        frontmatter["condition"] = [item.text for item in step.conditions]
    if step.loop_interval_ms is not None:
        frontmatter["loop_interval_ms"] = step.loop_interval_ms
    frontmatter["source_refs"] = [step.provenance.as_dict()]
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
        f"Candidate business step referencing an approved Pass-5 UserFlow, extracted from "
        f"reachability evidence in `{extraction.repository}` at commit `{extraction.commit}`.",
        "",
        f"- Layer: `{BUSINESS_LAYER}`",
        f"- Role: `{BUSINESS_STEP_ROLE}`",
        f"- Business flow: `{step.business_flow_id}` (position {step.position})",
        f"- References user flow: `{step.user_flow_id}`",
        f"- Trigger: `{step.trigger}`",
        f"- Evidence mechanism: {', '.join(f'`{item}`' for item in step.evidence_mechanisms)}",
        f"- Declared in: `{step.provenance.source_path}` "
        f"(lines {step.provenance.line_start}-{step.provenance.line_end})",
        f"- Evidence class: `{EVIDENCE_TYPE}`",
        "",
    ]
    if step.conditions:
        body.extend(["## Guards", ""])
        body.extend(f"- `{item.text}` (`{item.kind}`)" for item in step.conditions)
        body.append("")
    if step.loop_interval_ms is not None:
        body.extend(
            [
                "## Repetition",
                "",
                f"This step runs on a timer every {step.loop_interval_ms} ms, so its position in "
                f"the journey is a repeating stage rather than a one-off transition.",
                "",
            ]
        )
    body.extend(
        [
            "## Review notes",
            "",
            "This page is a candidate awaiting review. It carries no endpoint, event or "
            "persistence detail of its own: that evidence already lives on the referenced "
            "UserFlow page and is not duplicated here.",
            "",
        ]
    )
    return _render_page(frontmatter, body)


def render_all(extraction: BusinessFlowExtraction) -> dict[str, str]:
    rendered: dict[str, str] = {}
    for flow in extraction.flows:
        rendered[f"business-flows/{flow.id}.md"] = render_business_flow_markdown(flow, extraction)
    for step in extraction.steps:
        rendered[f"business-steps/{step.id}.md"] = render_business_step_markdown(step, extraction)
    return rendered


def build_report(extraction: BusinessFlowExtraction) -> dict[str, Any]:
    """Assemble extraction-report.json. Contains no timestamp, so runs stay comparable."""
    counts: dict[str, int] = {}
    for relation in extraction.relationships:
        counts[relation.type] = counts.get(relation.type, 0) + 1
    mapped = [site for site in extraction.call_sites if site.mapping.resolved]
    unresolved_sites = [site for site in extraction.call_sites if not site.mapping.resolved]
    return {
        "version": 1,
        "extractor": EXTRACTOR_KIND,
        "repository": extraction.repository,
        "commit": extraction.commit,
        "commit_verified": True,
        "evidence_type": EVIDENCE_TYPE,
        "analysis": "vue-sfc/static",
        "ontology_kinds_introduced": [BUSINESS_FLOW_KIND],
        "ontology_kinds_reused": [FLOW_STEP_KIND, USER_FLOW_KIND],
        "relationship_types_introduced": [],
        "relationship_types_used": [CONTAINS, DERIVED_FROM, PRECEDES],
        "candidate_subdirectories": list(CANDIDATE_SUBDIRECTORIES),
        "api_prefix": {
            "value": extraction.api_prefix.value,
            "resolved": extraction.api_prefix.resolved,
            "reason": extraction.api_prefix.reason,
            "source_refs": [
                provenance.as_dict()
                for provenance in (
                    extraction.api_prefix.config_provenance,
                    extraction.api_prefix.mount_provenance,
                )
                if provenance is not None
            ],
        },
        "source_files_scanned": list(extraction.source_files),
        "routes_scanned": [
            {"path": route.path, "name": route.name, "view": route.view_path}
            for route in extraction.routes
        ],
        "views_scanned": list(extraction.views),
        "components_scanned": list(extraction.components),
        "canonical_user_flows_available": len(extraction.canonical_user_flows),
        "api_call_sites": [site.summary() for site in extraction.call_sites],
        "api_calls_mapped": [site.summary() for site in mapped],
        "api_calls_unresolved": [site.summary() for site in unresolved_sites],
        "business_flows": [flow.summary() for flow in extraction.flows],
        "business_steps": [step.summary() for step in extraction.steps],
        "relationships": [relation.summary() for relation in extraction.relationships],
        "relationship_counts": dict(sorted(counts.items())),
        "resolved_business_flows": [
            flow.id for flow in extraction.flows_with_outcome(OUTCOME_RESOLVED)
        ],
        "partial_business_flows": [
            flow.summary() for flow in extraction.flows_with_outcome(OUTCOME_PARTIAL)
        ],
        "rejected_business_flow_hypotheses": list(extraction.rejected),
        "unresolved_business_segments": list(extraction.unresolved_segments),
        "deferred_composable_segments": list(extraction.deferred),
        "route_resolution_failures": list(extraction.route_failures),
        "empty_destination_views": list(extraction.empty_views),
        "unknown_routes": list(extraction.unknown_routes),
        "identity_collisions": list(extraction.identity_collisions),
        "cycles_detected": list(extraction.cycles_detected),
        "warnings": list(extraction.warnings),
        "counts": {
            "source_files_scanned": len(extraction.source_files),
            "routes_scanned": len(extraction.routes),
            "views_scanned": len(extraction.views),
            "components_scanned": len(extraction.components),
            "api_call_sites": len(extraction.call_sites),
            "api_calls_mapped": len(mapped),
            "api_calls_unresolved": len(unresolved_sites),
            "business_flows": len(extraction.flows),
            "business_steps": len(extraction.steps),
            "relationships": len(extraction.relationships),
            "resolved_business_flows": len(extraction.flows_with_outcome(OUTCOME_RESOLVED)),
            "partial_business_flows": len(extraction.flows_with_outcome(OUTCOME_PARTIAL)),
            "rejected_business_flow_hypotheses": len(extraction.rejected),
            "unresolved_business_segments": len(extraction.unresolved_segments),
            "deferred_composable_segments": len(extraction.deferred),
            "route_resolution_failures": len(extraction.route_failures),
            "empty_destination_views": len(extraction.empty_views),
            "unknown_routes": len(extraction.unknown_routes),
            "identity_collisions": len(extraction.identity_collisions),
            "cycles_detected": len(extraction.cycles_detected),
            "warnings": len(extraction.warnings),
        },
        "modules_imported": 0,
        "modules_executed": 0,
        "runtime_connections_opened": 0,
        "graph_mutations": 0,
        "wiki_writes": 0,
        "neo4j_mutations": 0,
        "graphiti_mutations": 0,
        "graphiti": "disabled",
    }


def render_report_json(report: dict[str, Any]) -> str:
    return json.dumps(report, indent=2, ensure_ascii=False) + "\n"


def render_bundle(extraction: BusinessFlowExtraction) -> tuple[dict[str, str], dict[str, Any]]:
    return render_all(extraction), build_report(extraction)


def summarize(extraction: BusinessFlowExtraction, report: dict[str, Any]) -> dict[str, Any]:
    """CLI-facing summary of one extraction run."""
    return {
        "extractor": report["extractor"],
        "repository": extraction.repository,
        "commit": extraction.commit,
        "commit_verified": True,
        "analysis": report["analysis"],
        "api_prefix": report["api_prefix"]["value"],
        "api_prefix_resolved": report["api_prefix"]["resolved"],
        "counts": report["counts"],
        "business_flows": [
            {
                "id": flow.id,
                "outcome": flow.outcome,
                "actor": flow.actor or ", ".join(flow.actors) or None,
                "user_flows": list(flow.user_flow_ids),
            }
            for flow in extraction.flows
        ],
        "resolved_business_flows": report["resolved_business_flows"],
        "partial_business_flows": [item["id"] for item in report["partial_business_flows"]],
        "rejected_business_flow_hypotheses": [
            {"id": item["id"], "probe": item["probe"], "verified": item["verified"]}
            for item in extraction.rejected
        ],
        "unresolved_business_segments": report["unresolved_business_segments"],
        "deferred_composable_segments": report["deferred_composable_segments"],
        "route_resolution_failures": report["route_resolution_failures"],
        "empty_destination_views": report["empty_destination_views"],
        "unknown_routes": report["unknown_routes"],
        "relationship_counts": report["relationship_counts"],
        "identity_collisions": report["identity_collisions"],
        "cycles_detected": report["cycles_detected"],
        "warnings": report["warnings"],
        "modules_imported": 0,
        "modules_executed": 0,
        "runtime_connections_opened": 0,
        "graph_mutations": 0,
        "wiki_writes": 0,
        "neo4j_mutations": 0,
        "graphiti": "disabled",
    }
