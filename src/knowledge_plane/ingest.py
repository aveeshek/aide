from __future__ import annotations

import argparse
import asyncio
import json
import logging
from pathlib import Path

from .graph_store import DestructiveSyncError, Neo4jKnowledgeGraph
from .graphiti_store import GraphitiContextGraph
from .markdown_loader import load_pages, validate_pages
from .ontology import load_entity_types, load_relationship_types
from .settings import settings

logger = logging.getLogger(__name__)


def _write_index(pages: list, output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "version": 1,
        "pages": [page.public_dict(include_body=False) for page in pages],
    }
    output.write_text(json.dumps(payload, indent=2, default=str), encoding="utf-8")


async def ingest(
    include_graphiti: bool | None = None,
    *,
    allow_delete: bool = False,
    dry_run: bool = False,
) -> dict:
    """Validate canonical Markdown and synchronize it into the graph.

    Raises ``DestructiveSyncError`` before any graph mutation when the incoming canonical
    set would delete existing KP_Entity nodes and ``allow_delete`` is False.
    """
    pages = load_pages(settings.canonical_path, settings.knowledge_root)
    entity_types = load_entity_types(settings.knowledge_root / "ontology/entity-types.yaml")
    relation_types = load_relationship_types(
        settings.knowledge_root / "ontology/relationship-types.yaml"
    )
    errors = validate_pages(pages, entity_types, relation_types)
    if errors:
        raise ValueError("Knowledge validation failed:\n- " + "\n- ".join(errors))

    # A dry run reports only; it leaves the generated index alongside Neo4j untouched.
    if not dry_run:
        _write_index(pages, settings.generated_path / "knowledge_index.json")

    deterministic = Neo4jKnowledgeGraph(
        settings.neo4j_uri,
        settings.neo4j_user,
        settings.neo4j_password,
        settings.neo4j_database,
    )
    try:
        await deterministic.verify()
        prior_graphiti_hashes = await deterministic.get_graphiti_hashes()
        deterministic_counts = await deterministic.sync_pages(
            pages, allow_delete=allow_delete, dry_run=dry_run
        )

        requested = settings.enable_graphiti if include_graphiti is None else include_graphiti
        graphiti_count = 0
        graphiti_status = "disabled"
        pending_graphiti_pages = [
            page for page in pages if prior_graphiti_hashes.get(page.id) != page.source_hash
        ]
        if requested and dry_run:
            # Graphiti episodes are written into the same Neo4j instance, so a dry run must
            # skip them. The Graphiti-off path above is left exactly as-is.
            graphiti_status = "skipped: dry-run"
        elif requested:
            if not GraphitiContextGraph.is_configured():
                graphiti_status = "skipped: OPENAI_API_KEY is not configured"
                logger.warning(graphiti_status)
            elif not pending_graphiti_pages:
                graphiti_status = "up-to-date"
            else:
                context_graph = GraphitiContextGraph(
                    settings.neo4j_uri,
                    settings.neo4j_user,
                    settings.neo4j_password,
                    settings.graph_group_id,
                )
                try:
                    graphiti_count = await context_graph.add_pages(pending_graphiti_pages)
                    await deterministic.mark_graphiti_synced(pending_graphiti_pages)
                    graphiti_status = "ok"
                finally:
                    await context_graph.close()
    finally:
        await deterministic.close()

    return {
        "status": "ok",
        "dry_run": dry_run,
        "allow_delete": allow_delete,
        "canonical_pages": len(pages),
        "deterministic_graph": deterministic_counts,
        "graphiti": {
            "status": graphiti_status,
            "episodes_added": graphiti_count,
            "pending_before_run": len(pending_graphiti_pages),
        },
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Ingest approved Markdown into the knowledge plane"
    )
    parser.add_argument(
        "--graphiti",
        choices=["auto", "on", "off"],
        default="auto",
        help="Override ENABLE_GRAPHITI for this run",
    )
    parser.add_argument(
        "--allow-delete",
        action="store_true",
        help=(
            "Authorize removal of stale KP_Entity nodes that the incoming canonical set "
            "no longer contains. Without this flag a sync that would delete nodes aborts "
            "before any graph mutation."
        ),
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Report the synchronization plan without modifying Neo4j",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()
    include_graphiti = {"auto": None, "on": True, "off": False}[args.graphiti]

    logging.basicConfig(
        level=getattr(logging, settings.log_level.upper(), logging.INFO),
        format="%(asctime)s %(levelname)s %(name)s - %(message)s",
    )
    try:
        result = asyncio.run(
            ingest(include_graphiti, allow_delete=args.allow_delete, dry_run=args.dry_run)
        )
    except DestructiveSyncError as exc:
        print(
            json.dumps(
                {"status": "blocked", "reason": str(exc), "plan": exc.plan.as_dict()},
                indent=2,
            )
        )
        raise SystemExit(2) from exc
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
