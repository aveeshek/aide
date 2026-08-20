from __future__ import annotations

import json
import sys

from .markdown_loader import KnowledgeValidationError, load_pages, validate_pages
from .ontology import load_entity_types, load_relationship_types
from .settings import settings


def validate_repository() -> tuple[list[dict], list[str]]:
    pages = load_pages(settings.canonical_path, settings.knowledge_root)
    entity_types = load_entity_types(settings.knowledge_root / "ontology/entity-types.yaml")
    relation_types = load_relationship_types(
        settings.knowledge_root / "ontology/relationship-types.yaml"
    )
    errors = validate_pages(pages, entity_types, relation_types)
    return [page.public_dict() for page in pages], errors


def main() -> None:
    try:
        pages, errors = validate_repository()
    except (KnowledgeValidationError, OSError, ValueError) as exc:
        print(f"Knowledge validation failed: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc

    if errors:
        print("Knowledge validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        raise SystemExit(1)

    print(json.dumps({"status": "ok", "pages": len(pages)}, indent=2))


if __name__ == "__main__":
    main()
