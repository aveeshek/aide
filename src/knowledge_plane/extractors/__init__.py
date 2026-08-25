"""Deterministic source extractors for Graph Engineering passes.

Extractors read a registered repository at a frozen commit and emit review candidates.
They never write canonical knowledge, never touch Neo4j or Graphiti, and never call an LLM.
"""

from __future__ import annotations

from .compose import EXTRACTOR_KIND as COMPOSE_KIND
from .compose import (
    ComposeExtraction,
    EntityCandidate,
    Provenance,
    RelationshipCandidate,
    UnresolvedDependency,
    extract_compose,
)

# Extractor kinds available to `python -m knowledge_plane.extract --kind ...`.
AVAILABLE_KINDS: tuple[str, ...] = (COMPOSE_KIND,)

__all__ = [
    "AVAILABLE_KINDS",
    "COMPOSE_KIND",
    "ComposeExtraction",
    "EntityCandidate",
    "Provenance",
    "RelationshipCandidate",
    "UnresolvedDependency",
    "extract_compose",
]
