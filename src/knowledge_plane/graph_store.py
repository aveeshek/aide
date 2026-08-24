from __future__ import annotations

import json
import logging
from collections.abc import Iterable
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any

from neo4j import AsyncDriver, AsyncGraphDatabase
from neo4j.exceptions import Neo4jError

from .models import KnowledgePage

logger = logging.getLogger(__name__)

# Deletion previews are truncated so an accidental full-graph wipe produces a readable
# error instead of thousands of ids.
_DELETION_PREVIEW_LIMIT = 10


@dataclass(frozen=True, slots=True)
class SyncPlan:
    """Deterministic diff between the live graph and the incoming canonical set.

    ``retained`` holds ids present on both sides; those nodes are re-merged (updated)
    in place rather than recreated, so retained and updated are the same set here.
    All tuples are sorted so the same inputs always produce the same reported plan.
    """

    creates: tuple[str, ...]
    retained: tuple[str, ...]
    deletions: tuple[str, ...]

    @property
    def is_destructive(self) -> bool:
        return bool(self.deletions)

    def as_dict(self) -> dict[str, Any]:
        return {
            "creates": list(self.creates),
            "retained": list(self.retained),
            "deletions": list(self.deletions),
            "create_count": len(self.creates),
            "retained_count": len(self.retained),
            "deletion_count": len(self.deletions),
        }

    def ensure_safe(self, allow_delete: bool) -> None:
        """Raise unless the plan is non-destructive or deletion was authorized."""
        if self.deletions and not allow_delete:
            raise DestructiveSyncError(self)


class DestructiveSyncError(RuntimeError):
    """Raised when a sync would remove KP_Entity nodes without explicit authorization."""

    def __init__(self, plan: SyncPlan) -> None:
        self.plan = plan
        preview = ", ".join(plan.deletions[:_DELETION_PREVIEW_LIMIT])
        hidden = len(plan.deletions) - _DELETION_PREVIEW_LIMIT
        if hidden > 0:
            preview = f"{preview}, ... (+{hidden} more)"
        super().__init__(
            f"Refusing to synchronize: {len(plan.deletions)} existing KP_Entity node(s) "
            f"are not backed by the incoming canonical set and would be deleted "
            f"[{preview}]. The graph was left unchanged. Re-run with --allow-delete to "
            f"authorize intentional stale-node removal."
        )


def build_sync_plan(existing_ids: Iterable[str], canonical_ids: Iterable[str]) -> SyncPlan:
    """Compare live KP_Entity ids with incoming canonical ids.

    Pure and side-effect free: this is the decision input for the deletion guard and is
    computed before any graph mutation so an unsafe plan can abort without touching Neo4j.
    """
    existing = set(existing_ids)
    canonical = set(canonical_ids)
    return SyncPlan(
        creates=tuple(sorted(canonical - existing)),
        retained=tuple(sorted(canonical & existing)),
        deletions=tuple(sorted(existing - canonical)),
    )


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

    def __init__(
        self,
        uri: str,
        user: str,
        password: str,
        database: str = "neo4j",
        *,
        driver: AsyncDriver | None = None,
    ) -> None:
        # ``driver`` is an injection seam: it lets deterministic tests observe the exact
        # order of statements the sync issues without a live Neo4j instance.
        if driver is None:
            driver = AsyncGraphDatabase.driver(uri, auth=(user, password))
        self._driver: AsyncDriver = driver
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

    async def get_entity_ids(self) -> set[str]:
        """Read the ids of every KP_Entity currently in the graph. Read-only."""
        async with self._driver.session(database=self._database) as session:
            result = await session.run("MATCH (n:KP_Entity) RETURN n.id AS id")
            return {record["id"] async for record in result}

    async def plan_sync(self, pages: list[KnowledgePage]) -> SyncPlan:
        """Diff the live graph against ``pages`` without modifying anything."""
        return build_sync_plan(await self.get_entity_ids(), {page.id for page in pages})

    async def sync_pages(
        self,
        pages: list[KnowledgePage],
        *,
        allow_delete: bool = False,
        dry_run: bool = False,
    ) -> dict[str, Any]:
        """Rebuild the deterministic graph from ``pages`` behind a deletion guard.

        The plan is computed and checked before ``setup()`` and before any MERGE, so a
        rejected sync (including an empty canonical set against a populated graph) leaves
        the graph untouched. ``dry_run`` reports the plan and issues no statement that
        modifies Neo4j.
        """
        plan = await self.plan_sync(pages)
        plan.ensure_safe(allow_delete)

        result: dict[str, Any] = {
            "entities": len(pages),
            "relationships": sum(len(page.relations) for page in pages),
            "entities_deleted": 0,
            "allow_delete": allow_delete,
            "dry_run": dry_run,
            "plan": plan.as_dict(),
        }
        if dry_run:
            result["applied"] = False
            return result

        await self.setup()
        sync_id = datetime.now(UTC).isoformat()

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

            if plan.deletions:
                # Delete exactly the authorized set instead of "everything not in the
                # canonical set", so the mutation can never exceed the reported plan.
                logger.warning(
                    "Deleting %d stale KP_Entity node(s) authorized by --allow-delete: %s",
                    len(plan.deletions),
                    ", ".join(plan.deletions[:_DELETION_PREVIEW_LIMIT]),
                )
                await session.run(
                    "MATCH (n:KP_Entity) WHERE n.id IN $deletions DETACH DELETE n",
                    deletions=list(plan.deletions),
                )

        result["entities_deleted"] = len(plan.deletions)
        result["applied"] = True
        return result

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
