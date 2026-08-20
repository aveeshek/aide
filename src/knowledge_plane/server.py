from __future__ import annotations

import argparse
import asyncio
import json
import logging
import platform
import re
from datetime import UTC, datetime
from typing import Any

from mcp.server.fastmcp import FastMCP

from . import __version__
from .graph_store import Neo4jKnowledgeGraph
from .graphiti_store import GraphitiContextGraph
from .markdown_loader import load_pages
from .settings import settings

logging.basicConfig(
    level=getattr(logging, settings.log_level.upper(), logging.INFO),
    format="%(asctime)s %(levelname)s %(name)s - %(message)s",
)
logger = logging.getLogger(__name__)

mcp = FastMCP(
    "Engineering Knowledge Plane",
    instructions=(
        "Use approved canonical Markdown and deterministic graph facts first. "
        "Treat OpenWiki and temporal episodes as derived context. Surface contradictions. "
        "Never invent contracts, schemas, owners, or code symbols."
    ),
    host=settings.mcp_host,
    port=settings.mcp_port,
    stateless_http=True,
    json_response=True,
)


def _graph() -> Neo4jKnowledgeGraph:
    return Neo4jKnowledgeGraph(
        settings.neo4j_uri,
        settings.neo4j_user,
        settings.neo4j_password,
        settings.neo4j_database,
    )


def _safe_candidate_name(value: str) -> str:
    value = re.sub(r"[^a-zA-Z0-9._-]+", "-", value).strip("-.").lower()
    return value[:80] or "knowledge-delta"


def _read_markdown(relative_path: str) -> str:
    candidate = (settings.knowledge_root / relative_path).resolve()
    allowed_roots = [settings.canonical_path.resolve(), settings.openwiki_path.resolve()]
    if not any(candidate == root or root in candidate.parents for root in allowed_roots):
        raise ValueError("Path must be inside wiki/ or openwiki/")
    if candidate.suffix.lower() != ".md" or not candidate.is_file():
        raise FileNotFoundError(relative_path)
    return candidate.read_text(encoding="utf-8")


@mcp.tool()
async def health() -> dict[str, Any]:
    """Check repository and Neo4j connectivity without modifying data."""
    graph = _graph()
    try:
        await graph.verify()
        stats = await graph.stats()
        return {
            "status": "ok",
            "knowledge_plane_version": __version__,
            "python_version": platform.python_version(),
            "canonical_path": str(settings.canonical_path),
            "neo4j": stats,
            "graphiti_enabled": settings.enable_graphiti,
        }
    finally:
        await graph.close()


@mcp.tool()
def list_knowledge_pages(kind: str | None = None, status: str = "approved") -> list[dict[str, Any]]:
    """List canonical Markdown concepts, optionally filtered by kind and status."""
    pages = load_pages(settings.canonical_path, settings.knowledge_root)
    return [
        page.public_dict()
        for page in pages
        if (not kind or page.kind.lower() == kind.lower())
        and (not status or page.status.lower() == status.lower())
    ]


@mcp.tool()
def read_knowledge_page(relative_path: str) -> str:
    """Read a Markdown page from wiki/ or openwiki/ after path safety checks."""
    return _read_markdown(relative_path)


@mcp.tool()
async def get_entity(entity_id: str) -> dict[str, Any]:
    """Return one canonical graph entity, provenance properties, and outgoing relationships."""
    graph = _graph()
    try:
        result = await graph.get_entity(entity_id)
        return result or {"found": False, "entity_id": entity_id}
    finally:
        await graph.close()


@mcp.tool()
async def search_knowledge(query: str, limit: int = 10) -> dict[str, Any]:
    """Search deterministic canonical entities and optional Graphiti temporal facts."""
    limit = max(1, min(limit, settings.max_search_results))
    graph = _graph()
    try:
        deterministic = await graph.search(query, limit)
    finally:
        await graph.close()

    temporal: list[dict[str, Any]] = []
    temporal_status = "disabled"
    if settings.enable_graphiti and GraphitiContextGraph.is_configured():
        context_graph = GraphitiContextGraph(
            settings.neo4j_uri,
            settings.neo4j_user,
            settings.neo4j_password,
            settings.graph_group_id,
        )
        try:
            temporal = await context_graph.search(query, limit)
            temporal_status = "ok"
        except Exception as exc:  # Keep canonical retrieval available if Graphiti is degraded.
            logger.exception("Graphiti search failed")
            temporal_status = f"degraded: {type(exc).__name__}"
        finally:
            await context_graph.close()

    return {
        "query": query,
        "canonical_results": deterministic,
        "temporal_results": temporal,
        "temporal_status": temporal_status,
        "trust_note": "Canonical results outrank temporal results.",
    }


@mcp.tool()
async def trace_dependencies(
    entity_id: str,
    depth: int = 2,
    direction: str = "both",
    relationship_types: list[str] | None = None,
) -> list[dict[str, Any]]:
    """Traverse typed canonical relationships for dependency and flow analysis."""
    depth = max(1, min(depth, settings.max_graph_depth))
    graph = _graph()
    try:
        return await graph.traverse(entity_id, depth, relationship_types, direction)
    finally:
        await graph.close()


@mcp.tool()
async def analyze_change_impact(
    entity_id: str,
    change_summary: str,
    depth: int = 3,
) -> dict[str, Any]:
    """Build an evidence-backed impact slice around an entity without changing the graph."""
    graph = _graph()
    try:
        entity, neighborhood = await asyncio.gather(
            graph.get_entity(entity_id),
            graph.traverse(entity_id, min(depth, settings.max_graph_depth), None, "both"),
        )
    finally:
        await graph.close()
    return {
        "change_summary": change_summary,
        "anchor": entity,
        "affected_neighborhood": neighborhood,
        "required_checks": [
            "Confirm current contract and schema pointers.",
            "Trace synchronous callers and asynchronous consumers.",
            "Identify governing ADRs, constraints, and NFRs.",
            "Locate existing unit, integration, contract, and E2E tests.",
            (
                "Surface contradictions between declared, contracted, "
                "implemented, and observed evidence."
            ),
        ],
    }


@mcp.tool()
async def resolve_task_context(
    story_text: str,
    target_entities: list[str] | None = None,
    token_budget: int = 24000,
) -> dict[str, Any]:
    """Assemble a bounded E2E context pack for Kiro.

    Sources are canonical search results and target graph neighborhoods.
    """
    targets = target_entities or []
    search = await search_knowledge(story_text, min(12, settings.max_search_results))

    neighborhoods: dict[str, Any] = {}
    for entity_id in targets[:10]:
        neighborhoods[entity_id] = await trace_dependencies(
            entity_id,
            depth=min(3, settings.max_graph_depth),
            direction="both",
        )

    contradictions_path = settings.operations_path / "contradictions.md"
    contradictions = (
        contradictions_path.read_text(encoding="utf-8")
        if contradictions_path.exists()
        else "No contradiction register found."
    )

    return {
        "normalized_objective": story_text.strip(),
        "token_budget": max(4000, min(token_budget, 100000)),
        "search": search,
        "target_neighborhoods": neighborhoods,
        "contradiction_register": contradictions[:12000],
        "generation_rules": [
            "Use current approved facts unless historical state is explicitly requested.",
            "Cite canonical page paths and source_refs for architectural claims.",
            "Do not invent endpoints, events, schema fields, tables, owners, or symbols.",
            "Treat temporal and OpenWiki results as advisory synthesis.",
            "Generate requirements, design, tasks, code, and tests within the discovered scope.",
        ],
    }


@mcp.tool()
def list_contradictions() -> str:
    """Return the governed contradiction register."""
    path = settings.operations_path / "contradictions.md"
    return path.read_text(encoding="utf-8") if path.exists() else "No contradiction register found."


@mcp.tool()
def propose_knowledge_delta(
    title: str,
    rationale: str,
    affected_entity_ids: list[str],
    proposed_markdown: str,
) -> dict[str, Any]:
    """Write a candidate delta only; a PR and human approval are still required for publication."""
    candidate_dir = settings.generated_path / "candidates"
    candidate_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    filename = f"{timestamp}-{_safe_candidate_name(title)}.md"
    path = candidate_dir / filename
    document = f"""---
kind: KnowledgeDeltaCandidate
status: candidate
created_at: {datetime.now(UTC).isoformat()}
affected_entity_ids: {json.dumps(affected_entity_ids)}
---

# {title.strip()}

## Rationale

{rationale.strip()}

## Proposed canonical Markdown

{proposed_markdown.strip()}

## Required governance

This candidate is not authoritative. Validate source references, run knowledge-plane validation,
open a pull request, obtain CODEOWNER approval, and merge through the protected branch
before ingesting.
"""
    path.write_text(document, encoding="utf-8")
    return {
        "status": "candidate_written",
        "path": path.relative_to(settings.knowledge_root).as_posix(),
        "authoritative": False,
        "next_action": "Open a reviewed pull request; do not ingest this file directly.",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the engineering knowledge-plane MCP server")
    parser.add_argument(
        "--transport",
        choices=["stdio", "streamable-http"],
        default=settings.mcp_transport,
        help=(
            "Use stdio for Kiro-local launch; HTTP is intended for "
            "diagnostics or managed gateways."
        ),
    )
    args = parser.parse_args()
    mcp.run(transport=args.transport)


if __name__ == "__main__":
    main()
