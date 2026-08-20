from __future__ import annotations

import argparse
import asyncio
import json
import logging
from pathlib import Path

from .graph_store import Neo4jKnowledgeGraph
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


async def ingest(include_graphiti: bool | None = None) -> dict:
    pages = load_pages(settings.canonical_path, settings.knowledge_root)
    entity_types = load_entity_types(settings.knowledge_root / "ontology/entity-types.yaml")
    relation_types = load_relationship_types(
        settings.knowledge_root / "ontology/relationship-types.yaml"
    )
    errors = validate_pages(pages, entity_types, relation_types)
    if errors:
        raise ValueError("Knowledge validation failed:\n- " + "\n- ".join(errors))

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
        deterministic_counts = await deterministic.sync_pages(pages)

        requested = settings.enable_graphiti if include_graphiti is None else include_graphiti
        graphiti_count = 0
        graphiti_status = "disabled"
        pending_graphiti_pages = [
            page for page in pages if prior_graphiti_hashes.get(page.id) != page.source_hash
        ]
        if requested:
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
        "canonical_pages": len(pages),
        "deterministic_graph": deterministic_counts,
        "graphiti": {
            "status": graphiti_status,
            "episodes_added": graphiti_count,
            "pending_before_run": len(pending_graphiti_pages),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Ingest approved Markdown into the knowledge plane"
    )
    parser.add_argument(
        "--graphiti",
        choices=["auto", "on", "off"],
        default="auto",
        help="Override ENABLE_GRAPHITI for this run",
    )
    args = parser.parse_args()
    include_graphiti = {"auto": None, "on": True, "off": False}[args.graphiti]

    logging.basicConfig(
        level=getattr(logging, settings.log_level.upper(), logging.INFO),
        format="%(asctime)s %(levelname)s %(name)s - %(message)s",
    )
    result = asyncio.run(ingest(include_graphiti))
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
