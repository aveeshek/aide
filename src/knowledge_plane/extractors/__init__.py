"""Deterministic source extractors for Graph Engineering passes.

Extractors read a registered repository at a frozen commit and emit review candidates.
They never write canonical knowledge, never touch Neo4j or Graphiti, and never call an LLM.

Every extractor exposes the same four-function contract so the CLI stays extractor-agnostic:

``extract(record, commit)``
    Parse the repository and return an immutable extraction result.
``render_bundle(extraction)``
    Render ``{output-relative path: content}`` plus the extraction report.
``summarize(extraction, report)``
    Build the CLI-facing summary payload.
``candidate_subdirectories``
    The output subdirectories the extractor owns, so stale candidates can be pruned
    without ever deleting a directory another pass wrote.
``sidecars`` (optional)
    Extra output files the extractor owns beyond the candidate pages and the report, keyed
    by output-relative path. A dry run renders them in memory and writes none of them.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from . import compose as _compose
from . import data_model as _data_model
from . import fastapi as _fastapi
from . import rabbitmq as _rabbitmq
from .compose import EXTRACTOR_KIND as COMPOSE_KIND
from .compose import (
    ComposeExtraction,
    EntityCandidate,
    Provenance,
    RelationshipCandidate,
    UnresolvedDependency,
    extract_compose,
)
from .data_model import EXTRACTOR_KIND as DATA_MODEL_KIND
from .data_model import (
    AccessCandidate,
    CollectionCandidate,
    ColumnCandidate,
    DatabaseMapping,
    DataModelExtraction,
    DocumentSchemaCandidate,
    MigrationCandidate,
    OntologyGap,
    TableCandidate,
    extract_data_model,
)
from .fastapi import EXTRACTOR_KIND as FASTAPI_KIND
from .fastapi import (
    ApiCandidate,
    EndpointCandidate,
    FastApiExtraction,
    SchemaCandidate,
    ServiceScan,
    UnresolvedRoute,
    UnresolvedSchema,
    extract_fastapi,
)
from .rabbitmq import EXTRACTOR_KIND as RABBITMQ_KIND
from .rabbitmq import (
    BrokerInteraction,
    BrokerWrapper,
    EventCandidate,
    IdentityCollision,
    RabbitExtraction,
    UnresolvedIdentifier,
    extract_rabbitmq,
)


@dataclass(frozen=True, slots=True)
class ExtractorSpec:
    """One registered extractor and the callables the CLI needs."""

    kind: str
    extract: Callable[..., Any]
    render_bundle: Callable[[Any], tuple[dict[str, str], dict[str, Any]]]
    summarize: Callable[[Any, dict[str, Any]], dict[str, Any]]
    candidate_subdirectories: tuple[str, ...]
    sidecars: Callable[[Any, dict[str, Any]], dict[str, str]] | None = None


EXTRACTORS: dict[str, ExtractorSpec] = {
    COMPOSE_KIND: ExtractorSpec(
        kind=COMPOSE_KIND,
        extract=extract_compose,
        render_bundle=_compose.render_bundle,
        summarize=_compose.summarize,
        candidate_subdirectories=_compose.CANDIDATE_SUBDIRECTORIES,
    ),
    FASTAPI_KIND: ExtractorSpec(
        kind=FASTAPI_KIND,
        extract=extract_fastapi,
        render_bundle=_fastapi.render_bundle,
        summarize=_fastapi.summarize,
        candidate_subdirectories=_fastapi.CANDIDATE_SUBDIRECTORIES,
    ),
    RABBITMQ_KIND: ExtractorSpec(
        kind=RABBITMQ_KIND,
        extract=extract_rabbitmq,
        render_bundle=_rabbitmq.render_bundle,
        summarize=_rabbitmq.summarize,
        candidate_subdirectories=_rabbitmq.CANDIDATE_SUBDIRECTORIES,
        sidecars=_rabbitmq.render_sidecars,
    ),
    DATA_MODEL_KIND: ExtractorSpec(
        kind=DATA_MODEL_KIND,
        extract=extract_data_model,
        render_bundle=_data_model.render_bundle,
        summarize=_data_model.summarize,
        candidate_subdirectories=_data_model.CANDIDATE_SUBDIRECTORIES,
        sidecars=_data_model.render_sidecars,
    ),
}

# Extractor kinds available to `python -m knowledge_plane.extract --kind ...`.
AVAILABLE_KINDS: tuple[str, ...] = tuple(EXTRACTORS)

__all__ = [
    "AVAILABLE_KINDS",
    "COMPOSE_KIND",
    "DATA_MODEL_KIND",
    "EXTRACTORS",
    "FASTAPI_KIND",
    "RABBITMQ_KIND",
    "AccessCandidate",
    "ApiCandidate",
    "BrokerInteraction",
    "BrokerWrapper",
    "CollectionCandidate",
    "ColumnCandidate",
    "ComposeExtraction",
    "DataModelExtraction",
    "DatabaseMapping",
    "DocumentSchemaCandidate",
    "EndpointCandidate",
    "EntityCandidate",
    "EventCandidate",
    "ExtractorSpec",
    "FastApiExtraction",
    "IdentityCollision",
    "MigrationCandidate",
    "OntologyGap",
    "Provenance",
    "RabbitExtraction",
    "TableCandidate",
    "RelationshipCandidate",
    "SchemaCandidate",
    "ServiceScan",
    "UnresolvedDependency",
    "UnresolvedIdentifier",
    "UnresolvedRoute",
    "UnresolvedSchema",
    "extract_compose",
    "extract_data_model",
    "extract_fastapi",
    "extract_rabbitmq",
]
