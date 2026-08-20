from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass(slots=True)
class Relation:
    type: str
    target: str
    evidence: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class KnowledgePage:
    id: str
    kind: str
    title: str
    status: str
    review_status: str
    path: Path
    relative_path: str
    body: str
    metadata: dict[str, Any]
    relations: list[Relation]
    source_refs: list[dict[str, Any]]
    source_hash: str

    @property
    def body_excerpt(self) -> str:
        text = " ".join(line.strip() for line in self.body.splitlines() if line.strip())
        return text[:4000]

    def public_dict(self, include_body: bool = False) -> dict[str, Any]:
        result: dict[str, Any] = {
            "id": self.id,
            "kind": self.kind,
            "title": self.title,
            "status": self.status,
            "review_status": self.review_status,
            "path": self.relative_path,
            "relations": [
                {"type": relation.type, "target": relation.target, **relation.evidence}
                for relation in self.relations
            ],
            "source_refs": self.source_refs,
            "source_hash": self.source_hash,
            "owner": self.metadata.get("owner"),
            "last_verified_at": self.metadata.get("last_verified_at"),
            "valid_from": self.metadata.get("valid_from"),
            "valid_to": self.metadata.get("valid_to"),
        }
        if include_body:
            result["body"] = self.body
        return result
