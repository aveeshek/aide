"""Deterministic regression tests for the graph synchronization deletion guard.

These tests drive the real ``Neo4jKnowledgeGraph.sync_pages`` code path against a
recording fake driver, so they assert the actual statements the sync would send to Neo4j
rather than a reimplementation of the decision logic. No live database is required.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest

from knowledge_plane.graph_store import (
    DestructiveSyncError,
    Neo4jKnowledgeGraph,
    build_sync_plan,
)
from knowledge_plane.ingest import build_parser
from knowledge_plane.models import KnowledgePage, Relation

# Any statement containing one of these keywords changes graph state or schema.
_MUTATING_KEYWORDS = ("CREATE", "MERGE", "SET ", "DELETE", "REMOVE", "DROP")

NINE_IDS = [f"service.order-{index}" for index in range(1, 10)]


def make_page(page_id: str, relations: list[Relation] | None = None) -> KnowledgePage:
    return KnowledgePage(
        id=page_id,
        kind="Service",
        title=f"Title {page_id}",
        status="approved",
        review_status="approved",
        path=Path(f"wiki/services/{page_id}.md"),
        relative_path=f"wiki/services/{page_id}.md",
        body="Body line one.",
        metadata={"owner": "team-order"},
        relations=relations or [],
        source_refs=[],
        source_hash=f"hash-{page_id}",
    )


class _FakeResult:
    def __init__(self, records: list[dict[str, Any]]) -> None:
        self._records = records

    def __aiter__(self):
        return self._iterate()

    async def _iterate(self):
        for record in self._records:
            yield record

    async def single(self) -> dict[str, Any] | None:
        return self._records[0] if self._records else None


class _RecordingSession:
    def __init__(self, driver: _RecordingDriver) -> None:
        self._driver = driver

    async def __aenter__(self) -> _RecordingSession:
        return self

    async def __aexit__(self, *exc_info: object) -> bool:
        return False

    async def run(
        self, query: str, parameters: dict[str, Any] | None = None, **kwargs: Any
    ) -> _FakeResult:
        params = dict(parameters or {})
        params.update(kwargs)
        self._driver.statements.append((query.strip(), params))
        if "RETURN n.id AS id" in query:
            return _FakeResult([{"id": value} for value in sorted(self._driver.existing_ids)])
        return _FakeResult([])


class _RecordingDriver:
    """Minimal AsyncDriver stand-in that records every statement it is asked to run."""

    def __init__(self, existing_ids: list[str]) -> None:
        self.existing_ids = set(existing_ids)
        self.statements: list[tuple[str, dict[str, Any]]] = []

    def session(self, database: str | None = None) -> _RecordingSession:
        return _RecordingSession(self)

    async def close(self) -> None:
        return None

    async def verify_connectivity(self) -> None:
        return None

    @property
    def mutating_statements(self) -> list[str]:
        return [
            query
            for query, _ in self.statements
            if any(keyword in query.upper() for keyword in _MUTATING_KEYWORDS)
        ]

    def deletion_parameters(self) -> list[dict[str, Any]]:
        return [
            params
            for query, params in self.statements
            if "DETACH DELETE" in query.upper() and "deletions" in params
        ]


def make_graph(existing_ids: list[str]) -> tuple[Neo4jKnowledgeGraph, _RecordingDriver]:
    driver = _RecordingDriver(existing_ids)
    graph = Neo4jKnowledgeGraph("bolt://unused", "neo4j", "unused", driver=driver)
    return graph, driver


# --------------------------------------------------------------------------------------
# Plan arithmetic
# --------------------------------------------------------------------------------------


def test_plan_reports_creates_retained_and_deletions() -> None:
    plan = build_sync_plan(["a", "b", "c"], ["b", "c", "d"])

    assert plan.creates == ("d",)
    assert plan.retained == ("b", "c")
    assert plan.deletions == ("a",)
    assert plan.is_destructive is True


def test_plan_is_deterministic_regardless_of_input_order() -> None:
    first = build_sync_plan(["c", "a", "b"], ["b", "z", "a"])
    second = build_sync_plan(["b", "c", "a"], ["z", "a", "b"])

    assert first == second
    assert first.creates == ("z",)
    assert first.retained == ("a", "b")
    assert first.deletions == ("c",)


# --------------------------------------------------------------------------------------
# 9 -> 9 : allowed
# --------------------------------------------------------------------------------------


async def test_nine_to_nine_is_allowed_and_deletes_nothing() -> None:
    graph, driver = make_graph(NINE_IDS)
    pages = [make_page(page_id) for page_id in NINE_IDS]

    result = await graph.sync_pages(pages)

    assert result["plan"]["create_count"] == 0
    assert result["plan"]["retained_count"] == 9
    assert result["plan"]["deletion_count"] == 0
    assert result["entities"] == 9
    assert result["entities_deleted"] == 0
    assert result["applied"] is True
    assert driver.deletion_parameters() == []


# --------------------------------------------------------------------------------------
# 9 -> 10 : allowed
# --------------------------------------------------------------------------------------


async def test_nine_to_ten_is_allowed_and_reports_one_create() -> None:
    graph, driver = make_graph(NINE_IDS)
    pages = [make_page(page_id) for page_id in [*NINE_IDS, "service.order-10"]]

    result = await graph.sync_pages(pages)

    assert result["plan"]["creates"] == ["service.order-10"]
    assert result["plan"]["retained_count"] == 9
    assert result["plan"]["deletion_count"] == 0
    assert result["entities"] == 10
    assert result["entities_deleted"] == 0
    assert driver.deletion_parameters() == []


# --------------------------------------------------------------------------------------
# 9 -> 1 : blocked
# --------------------------------------------------------------------------------------


async def test_nine_to_one_is_blocked_before_any_mutation() -> None:
    graph, driver = make_graph(NINE_IDS)
    pages = [make_page(NINE_IDS[0])]

    with pytest.raises(DestructiveSyncError) as excinfo:
        await graph.sync_pages(pages)

    assert len(excinfo.value.plan.deletions) == 8
    assert excinfo.value.plan.retained == (NINE_IDS[0],)
    assert "--allow-delete" in str(excinfo.value)
    # The abort must precede setup(), every MERGE, and every DELETE.
    assert driver.mutating_statements == []


async def test_blocked_sync_message_lists_stale_ids() -> None:
    graph, _ = make_graph(NINE_IDS)

    with pytest.raises(DestructiveSyncError) as excinfo:
        await graph.sync_pages([make_page(NINE_IDS[0])])

    message = str(excinfo.value)
    assert "8 existing KP_Entity node(s)" in message
    assert "service.order-2" in message


# --------------------------------------------------------------------------------------
# 9 -> 1 with --allow-delete : allowed
# --------------------------------------------------------------------------------------


async def test_nine_to_one_with_allow_delete_removes_only_stale_nodes() -> None:
    graph, driver = make_graph(NINE_IDS)
    pages = [make_page(NINE_IDS[0])]

    result = await graph.sync_pages(pages, allow_delete=True)

    assert result["entities"] == 1
    assert result["entities_deleted"] == 8
    assert result["allow_delete"] is True
    assert result["applied"] is True

    deletions = driver.deletion_parameters()
    assert len(deletions) == 1
    # Exactly the planned stale set, never "everything not in the canonical set".
    assert deletions[0]["deletions"] == sorted(NINE_IDS[1:])
    assert NINE_IDS[0] not in deletions[0]["deletions"]


# --------------------------------------------------------------------------------------
# dry-run : no mutation
# --------------------------------------------------------------------------------------


async def test_dry_run_reports_plan_without_mutating_neo4j() -> None:
    graph, driver = make_graph(NINE_IDS)
    pages = [make_page(page_id) for page_id in [*NINE_IDS, "service.order-10"]]

    result = await graph.sync_pages(pages, dry_run=True)

    assert result["dry_run"] is True
    assert result["applied"] is False
    assert result["plan"]["creates"] == ["service.order-10"]
    assert result["plan"]["retained_count"] == 9
    assert result["plan"]["deletion_count"] == 0
    assert result["entities_deleted"] == 0
    # No schema setup, no MERGE, no DELETE: only the read-only id probe ran.
    assert driver.mutating_statements == []
    assert len(driver.statements) == 1


async def test_dry_run_still_reports_a_blocked_destructive_plan() -> None:
    graph, driver = make_graph(NINE_IDS)

    with pytest.raises(DestructiveSyncError):
        await graph.sync_pages([make_page(NINE_IDS[0])], dry_run=True)

    assert driver.mutating_statements == []


async def test_dry_run_with_allow_delete_still_mutates_nothing() -> None:
    graph, driver = make_graph(NINE_IDS)

    result = await graph.sync_pages([make_page(NINE_IDS[0])], allow_delete=True, dry_run=True)

    assert result["applied"] is False
    assert result["plan"]["deletion_count"] == 8
    assert driver.mutating_statements == []


# --------------------------------------------------------------------------------------
# Empty canonical set must never silently clear a populated graph
# --------------------------------------------------------------------------------------


async def test_zero_pages_cannot_clear_a_non_empty_graph() -> None:
    graph, driver = make_graph(NINE_IDS)

    with pytest.raises(DestructiveSyncError) as excinfo:
        await graph.sync_pages([])

    assert len(excinfo.value.plan.deletions) == 9
    assert excinfo.value.plan.creates == ()
    assert excinfo.value.plan.retained == ()
    assert driver.mutating_statements == []


async def test_zero_pages_clears_graph_only_with_allow_delete() -> None:
    graph, driver = make_graph(NINE_IDS)

    result = await graph.sync_pages([], allow_delete=True)

    assert result["entities"] == 0
    assert result["entities_deleted"] == 9
    assert driver.deletion_parameters()[0]["deletions"] == sorted(NINE_IDS)


async def test_zero_pages_against_empty_graph_is_a_safe_no_op() -> None:
    graph, driver = make_graph([])

    result = await graph.sync_pages([])

    assert result["entities"] == 0
    assert result["entities_deleted"] == 0
    assert result["applied"] is True
    assert driver.deletion_parameters() == []


# --------------------------------------------------------------------------------------
# Relationships still sync on the non-destructive path
# --------------------------------------------------------------------------------------


async def test_relationships_are_written_when_the_plan_is_safe() -> None:
    graph, driver = make_graph(NINE_IDS)
    pages = [make_page(page_id) for page_id in NINE_IDS]
    pages[0].relations.append(Relation(type="EXPOSES", target=NINE_IDS[1]))

    result = await graph.sync_pages(pages)

    assert result["relationships"] == 1
    assert any("MERGE (source)-[r:KP_REL" in query for query in driver.mutating_statements)


# --------------------------------------------------------------------------------------
# CLI surface
# --------------------------------------------------------------------------------------


def test_cli_exposes_allow_delete_and_dry_run() -> None:
    parser = build_parser()

    default = parser.parse_args([])
    assert default.allow_delete is False
    assert default.dry_run is False
    assert default.graphiti == "auto"

    explicit = parser.parse_args(["--allow-delete", "--dry-run", "--graphiti", "off"])
    assert explicit.allow_delete is True
    assert explicit.dry_run is True
    assert explicit.graphiti == "off"
