from __future__ import annotations

from pathlib import Path

import yaml


def load_entity_types(path: Path) -> set[str]:
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    values = data.get("entity_types") or []
    return {str(value).strip() for value in values if str(value).strip()}


def load_relationship_types(path: Path) -> set[str]:
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    values = data.get("relationship_types") or []
    result: set[str] = set()
    for value in values:
        if isinstance(value, dict):
            name = str(value.get("type", "")).strip().upper()
        else:
            name = str(value).strip().upper()
        if name:
            result.add(name)
    return result
