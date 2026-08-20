from __future__ import annotations

import json
import os
from datetime import UTC, datetime
from typing import Any

from graphiti_core import Graphiti
from graphiti_core.nodes import EpisodeType

from .models import KnowledgePage


class GraphitiContextGraph:
    """Thin wrapper around Graphiti for temporal semantic episodes and hybrid search."""

    def __init__(
        self,
        uri: str,
        user: str,
        password: str,
        group_id: str,
    ) -> None:
        self._graphiti = Graphiti(uri, user, password)
        self._group_id = group_id

    @staticmethod
    def is_configured() -> bool:
        return bool(os.getenv("OPENAI_API_KEY"))

    async def close(self) -> None:
        await self._graphiti.close()

    async def setup(self) -> None:
        await self._graphiti.build_indices_and_constraints()

    @staticmethod
    def _reference_time(page: KnowledgePage) -> datetime:
        raw = page.metadata.get("last_verified_at") or page.metadata.get("valid_from")
        if raw:
            try:
                parsed = datetime.fromisoformat(str(raw).replace("Z", "+00:00"))
                if parsed.tzinfo is None:
                    parsed = parsed.replace(tzinfo=UTC)
                return parsed.astimezone(UTC)
            except ValueError:
                pass
        return datetime.now(UTC)

    async def add_pages(self, pages: list[KnowledgePage]) -> int:
        await self.setup()
        count = 0
        for page in pages:
            payload = page.public_dict(include_body=True)
            payload["knowledge_class"] = "approved_canonical_markdown"
            await self._graphiti.add_episode(
                name=f"canonical:{page.id}:{page.source_hash[:12]}",
                episode_body=json.dumps(payload, default=str),
                source=EpisodeType.json,
                source_description=f"Approved canonical Markdown: {page.relative_path}",
                reference_time=self._reference_time(page),
                group_id=self._group_id,
                custom_extraction_instructions=(
                    "Extract software-engineering entities and relationships. Preserve "
                    "canonical IDs, source paths, status, evidence classes, and temporal "
                    "validity. Do not infer an endpoint, schema field, owner, or dependency "
                    "that is not present in the episode."
                ),
            )
            count += 1
        return count

    async def search(self, query: str, limit: int = 10) -> list[dict[str, Any]]:
        results = await self._graphiti.search(
            query,
            group_ids=[self._group_id],
            num_results=limit,
        )
        return [
            {
                "uuid": result.uuid,
                "fact": result.fact,
                "source_node_uuid": result.source_node_uuid,
                "target_node_uuid": result.target_node_uuid,
                "valid_at": str(getattr(result, "valid_at", "") or ""),
                "invalid_at": str(getattr(result, "invalid_at", "") or ""),
            }
            for result in results
        ]
