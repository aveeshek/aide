from __future__ import annotations

import asyncio
import json
import platform

from knowledge_plane import __version__
from knowledge_plane.graph_store import Neo4jKnowledgeGraph
from knowledge_plane.settings import settings


async def main() -> None:
    graph = Neo4jKnowledgeGraph(
        settings.neo4j_uri,
        settings.neo4j_user,
        settings.neo4j_password,
        settings.neo4j_database,
    )
    try:
        await graph.verify()
        stats = await graph.stats()
        print(
            json.dumps(
                {
                    "status": "ok",
                    "knowledge_plane_version": __version__,
                    "python_version": platform.python_version(),
                    "canonical_path": str(settings.canonical_path),
                    "neo4j": stats,
                    "graphiti_enabled": settings.enable_graphiti,
                },
                indent=2,
            )
        )
    finally:
        await graph.close()


if __name__ == "__main__":
    asyncio.run(main())
