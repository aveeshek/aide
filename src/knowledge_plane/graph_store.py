from __future__ import annotations

import json
import logging
from datetime import UTC, datetime
from typing import Any

from neo4j import AsyncDriver, AsyncGraphDatabase
from neo4j.exceptions import Neo4jError

from .models import KnowledgePage

logger = logging.getLogger(__name__)


def optional_str(value: Any) -> str | None:
    """Return a trimmed string, or None when the value is absent or blank.

    Frontmatter validity fields are optional and may be YAML null. Returning None
    keeps the property absent in Neo4j instead of storing an empty string, which
    would otherwise compare as a real value in validity-window checks.
    """
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def json_safe(value: Any) -> Any:
    """Coerce Neo4j driver values into JSON-serializable primitives.

    Node property bags can contain temporal types such as ``neo4j.time.DateTime``
    (written by ``datetime()`` during ingest), which the MCP JSON encoder cannot
    serialize. Temporal values are preserved as ISO 8601 strings rather than
    dropped, so provenance freshness stays visible to callers.
    """
    if value is None or isinstance(value, (str, bool, int, float)):
        return value
    # Temporal types are checked before containers: neo4j.time.Duration subclasses
    # tuple, so container handling would otherwise flatten it into raw components.
    for method_name in ("isoformat", "iso_format"):
        method = getattr(value, method_name, None)
        if callable(method):
            return method()
    if isinstance(value, dict):
        return {key: json_safe(item) for key, item in value.items()}
    if isinstance(value, (list, tuple, set)):
        return [json_safe(item) for item in value]
    return str(value)


class Neo4jKnowledgeGraph:
    """Deterministic typed graph rebuilt from approved canonical Markdown."""

    def __init__(self, uri: str, user: str, password: str, database: str = "neo4j") -> None:
        self._driver: AsyncDriver = AsyncGraphDatabase.driver(uri, auth=(user, password))
        self._database = database

    async def close(self) -> None:
        await self._driver.close()

    async def verify(self) -> None:
        await self._driver.verify_connectivity()

    async def setup(self) -> None:
        statements = [
            "CREATE CONSTRAINT kp_entity_id IF NOT EXISTS FOR (n:KP_Entity) REQUIRE n.id IS UNIQUE",
            "CREATE INDEX kp_entity_kind IF NOT EXISTS FOR (n:KP_Entity) ON (n.kind)",
            "CREATE INDEX kp_entity_status IF NOT EXISTS FOR (n:KP_Entity) ON (n.status)",
            "CREATE FULLTEXT INDEX kp_entity_search IF NOT EXISTS "
            "FOR (n:KP_Entity) ON EACH [n.id, n.title, n.body_excerpt]",
        ]
        async with self._driver.session(database=self._database) as session:
            for statement in statements:
                await session.run(statement)

    async def sync_pages(self, pages: list[KnowledgePage]) -> dict[str, int]:
        await self.setup()
        sync_id = datetime.now(UTC).isoformat()
        entity_ids = {page.id for page in pages}

        async with self._driver.session(database=self._database) as session:
            for page in pages:
                properties = {
                    "id": page.id,
                    "kind": page.kind,
                    "title": page.title,
                    "status": page.status,
                    "review_status": page.review_status,
                    "owner": page.metadata.get("owner"),
                    "path": page.relative_path,
                    "body_excerpt": page.body_excerpt,
                    "source_hash": page.source_hash,
                    "source_refs_json": json.dumps(page.source_refs, default=str),
                    "valid_from": optional_str(page.metadata.get("valid_from")),
                    "valid_to": optional_str(page.metadata.get("valid_to")),
                    "last_verified_at": optional_str(page.metadata.get("last_verified_at")),
                    "sync_id": sync_id,
                }
                await session.run(
                    """
                    MERGE (n:KP_Entity {id: $id})
                    SET n += $properties,
                        n.updated_at = datetime()
                    """,
                    id=page.id,
                    properties=properties,
                )
                await session.run(
                    "MATCH (n:KP_Entity {id: $id})-[r:KP_REL]->() DELETE r",
                    id=page.id,
                )

            for page in pages:
                for relation in page.relations:
                    await session.run(
                        """
                        MATCH (source:KP_Entity {id: $source_id})
                        MATCH (target:KP_Entity {id: $target_id})
                        MERGE (source)-[r:KP_REL {type: $relation_type}]->(target)
                        SET r.source_path = $source_path,
                            r.evidence_json = $evidence_json,
                            r.updated_at = datetime()
                        """,
                        source_id=page.id,
                        target_id=relation.target,
                        relation_type=relation.type,
                        source_path=page.relative_path,
                        evidence_json=json.dumps(relation.evidence, default=str),
                    )

            await session.run(
                "MATCH (n:KP_Entity) WHERE NOT (n.id IN $entity_ids) DETACH DELETE n",
                entity_ids=sorted(entity_ids),
            )

        relation_count = sum(len(page.relations) for page in pages)
        return {"entities": len(pages), "relationships": relation_count}

    async def get_graphiti_hashes(self) -> dict[str, str]:
        async with self._driver.session(database=self._database) as session:
            result = await session.run(
                """
                MATCH (n:KP_Entity)
                RETURN n.id AS id, coalesce(n.graphiti_hash, '') AS graphiti_hash
                """
            )
            return {record["id"]: record["graphiti_hash"] async for record in result}

    async def mark_graphiti_synced(self, pages: list[KnowledgePage]) -> None:
        async with self._driver.session(database=self._database) as session:
            for page in pages:
                await session.run(
                    """
                    MATCH (n:KP_Entity {id: $id})
                    SET n.graphiti_hash = $source_hash,
                        n.graphiti_synced_at = datetime()
                    """,
                    id=page.id,
                    source_hash=page.source_hash,
                )

    async def get_entity(self, entity_id: str) -> dict[str, Any] | None:
        async with self._driver.session(database=self._database) as session:
            result = await session.run(
                """
                MATCH (n:KP_Entity {id: $entity_id})
                OPTIONAL MATCH (n)-[r:KP_REL]->(target:KP_Entity)
                RETURN properties(n) AS entity,
                       collect(CASE WHEN target IS NULL THEN NULL ELSE {
                         type: r.type,
                         target: target.id,
                         target_title: target.title,
                         evidence_json: r.evidence_json
                       } END) AS outgoing
                """,
                entity_id=entity_id,
            )
            record = await result.single()
            if record is None:
                return None
            outgoing = [item for item in record["outgoing"] if item is not None]
            return {
                "entity": json_safe(dict(record["entity"])),
                "outgoing": json_safe(outgoing),
            }

    async def search(self, query: str, limit: int = 10) -> list[dict[str, Any]]:
        async with self._driver.session(database=self._database) as session:
            try:
                result = await session.run(
                    """
                    CALL db.index.fulltext.queryNodes('kp_entity_search', $query)
                    YIELD node, score
                    RETURN node.id AS id, node.title AS title, node.kind AS kind,
                           node.path AS path, node.body_excerpt AS excerpt, score
                    ORDER BY score DESC
                    LIMIT $limit
                    """,
                    # Cypher parameters are passed as a dict: AsyncSession.run() names its
                    # first positional argument "query", so a query= keyword would collide.
                    {"query": query, "limit": limit},
                )
                return [dict(record) async for record in result]
            except Neo4jError as exc:
                # Only a server-side failure, such as a missing or corrupt
                # kp_entity_search index, may degrade to substring matching. Python-level
                # defects must propagate instead of silently lowering search quality.
                logger.warning(
                    "Full-text search unavailable (%s: %s). Falling back to substring "
                    "matching with uniform scores; ranking will be degraded.",
                    getattr(exc, "code", None) or type(exc).__name__,
                    getattr(exc, "message", None) or str(exc),
                )
                result = await session.run(
                    """
                    MATCH (node:KP_Entity)
                    WHERE toLower(node.id) CONTAINS toLower($query)
                       OR toLower(node.title) CONTAINS toLower($query)
                       OR toLower(node.body_excerpt) CONTAINS toLower($query)
                    RETURN node.id AS id, node.title AS title, node.kind AS kind,
                           node.path AS path, node.body_excerpt AS excerpt, 1.0 AS score
                    LIMIT $limit
                    """,
                    {"query": query, "limit": limit},
                )
                return [dict(record) async for record in result]

    async def traverse(
        self,
        start_id: str,
        depth: int = 2,
        relation_types: list[str] | None = None,
        direction: str = "both",
    ) -> list[dict[str, Any]]:
        depth = max(1, min(int(depth), 5))
        direction = direction.lower()
        if direction not in {"out", "in", "both"}:
            raise ValueError("direction must be one of: out, in, both")

        if direction == "out":
            pattern = f"(start:KP_Entity)-[rels:KP_REL*1..{depth}]->(node:KP_Entity)"
        elif direction == "in":
            pattern = f"(start:KP_Entity)<-[rels:KP_REL*1..{depth}]-(node:KP_Entity)"
        else:
            pattern = f"(start:KP_Entity)-[rels:KP_REL*1..{depth}]-(node:KP_Entity)"

        query = f"""
        MATCH path={pattern}
        WHERE start.id = $start_id
          AND ($relation_types = [] OR all(rel IN rels WHERE rel.type IN $relation_types))
        RETURN DISTINCT node.id AS id, node.title AS title, node.kind AS kind,
               length(path) AS distance,
               [rel IN rels | rel.type] AS relationship_path,
               [item IN nodes(path) | item.id] AS entity_path
        ORDER BY distance, id
        LIMIT 200
        """
        async with self._driver.session(database=self._database) as session:
            result = await session.run(
                query,
                start_id=start_id,
                relation_types=[value.upper() for value in (relation_types or [])],
            )
            return [dict(record) async for record in result]

    async def stats(self) -> dict[str, int]:
        async with self._driver.session(database=self._database) as session:
            result = await session.run(
                """
                CALL { MATCH (n:KP_Entity) RETURN count(n) AS entities }
                CALL { MATCH ()-[r:KP_REL]->() RETURN count(r) AS relationships }
                RETURN entities, relationships
                """
            )
            record = await result.single()
            if record is None:
                return {"entities": 0, "relationships": 0}
            return {"entities": record["entities"], "relationships": record["relationships"]}
