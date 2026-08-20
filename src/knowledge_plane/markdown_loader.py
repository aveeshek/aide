from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any

import yaml

from .models import KnowledgePage, Relation


class KnowledgeValidationError(ValueError):
    """Raised when canonical Markdown violates the knowledge schema."""


def _normalized_relations(raw: object, path: Path) -> list[Relation]:
    if raw in (None, ""):
        return []
    if not isinstance(raw, list):
        raise KnowledgeValidationError(f"{path}: relations must be a list")

    relations: list[Relation] = []
    for index, item in enumerate(raw):
        if not isinstance(item, dict):
            raise KnowledgeValidationError(f"{path}: relations[{index}] must be a mapping")
        relation_type = str(item.get("type", "")).strip().upper()
        target = str(item.get("target", "")).strip()
        if not relation_type or not target:
            raise KnowledgeValidationError(
                f"{path}: relations[{index}] requires non-empty type and target"
            )
        evidence = {key: value for key, value in item.items() if key not in {"type", "target"}}
        relations.append(Relation(type=relation_type, target=target, evidence=evidence))
    return relations


def _split_frontmatter(path: Path) -> tuple[dict[str, Any], str]:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise KnowledgeValidationError(f"{path}: canonical Markdown requires YAML frontmatter")
    try:
        end = next(index for index, line in enumerate(lines[1:], start=1) if line.strip() == "---")
    except StopIteration as exc:
        raise KnowledgeValidationError(f"{path}: YAML frontmatter is not closed") from exc
    raw_metadata = "\n".join(lines[1:end])
    metadata = yaml.safe_load(raw_metadata) or {}
    if not isinstance(metadata, dict):
        raise KnowledgeValidationError(f"{path}: YAML frontmatter must be a mapping")
    body = "\n".join(lines[end + 1 :]).strip()
    return dict(metadata), body


def parse_page(path: Path, root: Path) -> KnowledgePage:
    metadata, body = _split_frontmatter(path)

    page_id = str(metadata.get("id", "")).strip()
    kind = str(metadata.get("kind") or metadata.get("type") or "").strip()
    page_type = str(metadata.get("type") or kind).strip()
    title = str(metadata.get("title", "")).strip()
    status = str(metadata.get("status", "")).strip().lower()
    review_status = str(metadata.get("review_status") or status).strip().lower()

    missing = [
        name
        for name, value in {
            "id": page_id,
            "kind/type": kind,
            "type": page_type,
            "title": title,
            "status": status,
            "review_status": review_status,
        }.items()
        if not value
    ]
    if missing:
        raise KnowledgeValidationError(
            f"{path}: missing required frontmatter: {', '.join(missing)}"
        )
    if kind != page_type:
        raise KnowledgeValidationError(
            f"{path}: canonical kind ({kind}) and OKF type ({page_type}) must match"
        )

    source_refs = metadata.get("source_refs") or []
    if not isinstance(source_refs, list):
        raise KnowledgeValidationError(f"{path}: source_refs must be a list")
    if status == "approved" and not source_refs:
        raise KnowledgeValidationError(f"{path}: approved pages require at least one source_ref")

    raw_bytes = path.read_bytes()
    source_hash = hashlib.sha256(raw_bytes).hexdigest()
    return KnowledgePage(
        id=page_id,
        kind=kind,
        title=title,
        status=status,
        review_status=review_status,
        path=path,
        relative_path=path.relative_to(root).as_posix(),
        body=body,
        metadata=metadata,
        relations=_normalized_relations(metadata.get("relations"), path),
        source_refs=source_refs,
        source_hash=source_hash,
    )


def load_pages(canonical_root: Path, repository_root: Path | None = None) -> list[KnowledgePage]:
    if not canonical_root.exists():
        raise KnowledgeValidationError(f"Canonical directory does not exist: {canonical_root}")
    repository_root = repository_root or canonical_root.parent

    pages = [
        parse_page(path, repository_root)
        for path in sorted(canonical_root.rglob("*.md"))
        if path.is_file()
    ]
    if not pages:
        raise KnowledgeValidationError(f"No Markdown pages found under {canonical_root}")
    return pages


def validate_pages(
    pages: list[KnowledgePage],
    allowed_kinds: set[str] | None = None,
    allowed_relations: set[str] | None = None,
) -> list[str]:
    errors: list[str] = []
    by_id: dict[str, KnowledgePage] = {}

    for page in pages:
        if page.id in by_id:
            errors.append(
                f"Duplicate id {page.id!r}: {by_id[page.id].relative_path} and {page.relative_path}"
            )
        by_id[page.id] = page

        if allowed_kinds is not None and page.kind not in allowed_kinds:
            errors.append(f"{page.relative_path}: unknown kind {page.kind!r}")
        if page.status == "approved" and page.review_status != "approved":
            errors.append(
                f"{page.relative_path}: status is approved but "
                f"review_status is {page.review_status!r}"
            )

    for page in pages:
        for relation in page.relations:
            if allowed_relations is not None and relation.type not in allowed_relations:
                errors.append(f"{page.relative_path}: unknown relationship type {relation.type!r}")
            if relation.target not in by_id:
                errors.append(
                    f"{page.relative_path}: unresolved target {relation.target!r} "
                    f"for relationship {relation.type}"
                )
    return errors
