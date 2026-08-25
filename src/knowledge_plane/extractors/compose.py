"""Deterministic Docker Compose extractor (Graph Engineering Pass 1).

Scope and non-goals
-------------------
This extractor reads Compose YAML and emits *candidates* only. It never writes canonical
knowledge, never touches Neo4j or Graphiti, and never uses an LLM. It records only what
Compose states explicitly: application services, infrastructure instances, and runtime
dependencies declared through ``*_HOST`` configuration. APIs, events, and business
relationships are out of scope for this pass and are not inferred.

Classification is evidence-based rather than name-based, so no application service name is
hard-coded:

* a Compose service with a ``build`` section is built from the repository -> Service
* a Compose service with only ``image`` is a pulled dependency -> classified by image name

Image classification matches the *exact* image name, never a substring. This matters:
``redislabs/redisinsight`` and ``mongo-express`` are admin UIs, not a Redis cache or a
Mongo database, and a substring match would misclassify both.

Identity uses the canonical network alias (``hostname``, else ``container_name``, else the
Compose service key), which is also what a dependent service dials. That is why RabbitMQ,
declared as service ``message_broker`` with ``hostname: rabbitmq``, is identified as
``component.<repo>.rabbitmq`` and resolves from ``RABBITMQ_HOST=rabbitmq``.

Output carries no timestamp anywhere, so re-running against an unchanged repository
produces byte-identical candidates.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

from ..repository_manifest import RepositoryRecord, resolve_source_files

EXTRACTOR_KIND = "compose"
CANDIDATE_STATUS = "candidate"
CANDIDATE_REVIEW_STATUS = "pending"
EVIDENCE_TYPE = "implemented"
DEPENDS_ON = "DEPENDS_ON"
REDACTED_PLACEHOLDER = "[redacted]"

# Any environment key containing one of these markers is redacted before emission.
SECRET_KEY_MARKERS = ("PASSWORD", "PASS", "SECRET", "TOKEN", "KEY", "CREDENTIAL")
# Compose keys whose values may embed credentials (for example a redis --requirepass
# argument) are never copied into candidate output.
UNSAFE_COMPOSE_KEYS = ("command", "entrypoint")

HOST_KEY_SUFFIX = "_HOST"
# A bind address configures where a service listens; it is not a reference to a dependency.
LOCAL_BIND_VALUES = frozenset(
    {"0.0.0.0", "127.0.0.1", "::", "::1", "localhost", "host.docker.internal"}
)
_IPV4_PATTERN = re.compile(r"^\d{1,3}(?:\.\d{1,3}){3}$")
# Short or purely numeric values behind secret-looking keys are configuration knobs such as
# MB_PASSWORD_LENGTH=8, not credentials. Scanning output for "8" would produce false leak
# reports against ports, so only distinctive values enter the leak scan. Redaction itself
# stays broad and applies to every secret-looking key regardless of value.
_MIN_SCANNABLE_SECRET_LENGTH = 4
_APPLICATION_SERVICE_SUFFIXES = ("_service", "-service", "_svc", "-svc")

# Exact image name -> (ontology entity kind, engine). Only kinds already present in
# ontology/entity-types.yaml are used; no Network, Cache, or Broker kind is introduced.
INFRASTRUCTURE_IMAGES: dict[str, tuple[str, str]] = {
    "postgres": ("Database", "postgresql"),
    "postgresql": ("Database", "postgresql"),
    "mongo": ("Database", "mongodb"),
    "mongodb": ("Database", "mongodb"),
    "redis": ("Component", "redis"),
    "rabbitmq": ("Component", "rabbitmq"),
}
KIND_ID_PREFIXES = {"Service": "service", "Database": "database", "Component": "component"}

APPLICATION_ROLE = "application"
INFRASTRUCTURE_ROLE = "infrastructure"


# ---------------------------------------------------------------------------------------
# Normalization helpers
# ---------------------------------------------------------------------------------------


def normalize_token(value: str) -> str:
    """Lowercase ``value`` and reduce every run of non-alphanumerics to a single hyphen."""
    lowered = str(value).strip().lower()
    return re.sub(r"[^a-z0-9]+", "-", lowered).strip("-")


def image_name(image: str) -> str:
    """Return the bare image name, dropping registry, namespace, tag, and digest.

    ``localhost:5000/library/redis:7.2.5`` -> ``redis``. The final path segment is taken
    before the tag is split so a registry port is never mistaken for a tag.
    """
    reference = str(image).strip()
    if "@" in reference:
        reference = reference.split("@", 1)[0]
    final_segment = reference.rsplit("/", 1)[-1]
    if ":" in final_segment:
        final_segment = final_segment.split(":", 1)[0]
    return final_segment.strip().lower()


def classify_image(image: str) -> tuple[str, str] | None:
    """Map an image to an (entity kind, engine) pair, or None when unrecognized."""
    return INFRASTRUCTURE_IMAGES.get(image_name(image))


def application_service_id(repository_slug: str, compose_key: str) -> str:
    """Normalize a Compose service key into a stable Service id.

    A trailing ``_service`` style suffix is dropped because it restates the entity kind:
    ``gateway_service`` -> ``service.<repo>.gateway``.
    """
    token = str(compose_key).strip()
    lowered = token.lower()
    for suffix in _APPLICATION_SERVICE_SUFFIXES:
        if lowered.endswith(suffix) and len(lowered) > len(suffix):
            token = token[: -len(suffix)]
            break
    normalized = normalize_token(token) or normalize_token(compose_key)
    return f"service.{repository_slug}.{normalized}"


def canonical_alias(compose_key: str, definition: dict[str, Any]) -> str:
    """Return the name dependents dial: hostname, else container_name, else service key."""
    for field_name in ("hostname", "container_name"):
        value = definition.get(field_name)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return str(compose_key).strip()


def infrastructure_id(repository_slug: str, kind: str, alias: str) -> str:
    return f"{KIND_ID_PREFIXES[kind]}.{repository_slug}.{normalize_token(alias)}"


def json_pointer(*segments: str) -> str:
    """Build an RFC 6901 JSON pointer, escaping ``~`` and ``/`` inside segments."""
    escaped = (str(segment).replace("~", "~0").replace("/", "~1") for segment in segments)
    return "".join(f"/{segment}" for segment in escaped)


def parse_environment(raw: Any) -> dict[str, str]:
    """Normalize both Compose environment forms (``KEY=value`` list and mapping)."""
    result: dict[str, str] = {}
    if isinstance(raw, dict):
        for key, value in raw.items():
            result[str(key).strip()] = "" if value is None else str(value)
    elif isinstance(raw, list):
        for item in raw:
            text = str(item)
            if "=" in text:
                key, value = text.split("=", 1)
                result[key.strip()] = value
            elif text.strip():
                result[text.strip()] = ""
    return result


def is_secret_key(key: str) -> bool:
    upper = str(key).upper()
    return any(marker in upper for marker in SECRET_KEY_MARKERS)


def redact_environment(environment: dict[str, str]) -> dict[str, str]:
    """Keep every key visible while replacing secret-looking values with a placeholder."""
    return {
        key: (REDACTED_PLACEHOLDER if is_secret_key(key) else value)
        for key, value in environment.items()
    }


def scannable_secret_values(environment: dict[str, str]) -> set[str]:
    """Distinctive secret values used to verify that nothing leaked into the output."""
    values: set[str] = set()
    for key, value in environment.items():
        if not is_secret_key(key):
            continue
        text = str(value).strip()
        if len(text) < _MIN_SCANNABLE_SECRET_LENGTH or text.isdigit():
            continue
        values.add(text)
    return values


def _is_bind_address(value: str) -> bool:
    text = value.strip()
    return text in LOCAL_BIND_VALUES or bool(_IPV4_PATTERN.match(text))


# ---------------------------------------------------------------------------------------
# Candidate model
# ---------------------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class Provenance:
    """Where a candidate came from: repository, frozen commit, file, and YAML pointer."""

    repository: str
    commit: str
    source_path: str
    pointer: str
    evidence_type: str = EVIDENCE_TYPE

    def as_dict(self) -> dict[str, str]:
        return {
            "repository": self.repository,
            "commit": self.commit,
            "path": self.source_path,
            "pointer": self.pointer,
            "evidence_type": self.evidence_type,
        }


@dataclass(frozen=True, slots=True)
class EntityCandidate:
    id: str
    kind: str
    title: str
    role: str
    compose_service: str
    provenance: Provenance
    engine: str | None = None
    aliases: tuple[str, ...] = ()
    attributes: dict[str, Any] = field(default_factory=dict)

    def summary(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "id": self.id,
            "kind": self.kind,
            "role": self.role,
            "compose_service": self.compose_service,
        }
        if self.engine:
            payload["engine"] = self.engine
        if self.aliases:
            payload["aliases"] = list(self.aliases)
        payload["source"] = self.provenance.as_dict()
        return payload


@dataclass(frozen=True, slots=True)
class RelationshipCandidate:
    source: str
    type: str
    target: str
    config_key: str
    referenced_host: str
    provenance: Provenance

    def summary(self) -> dict[str, Any]:
        return {
            "source": self.source,
            "type": self.type,
            "target": self.target,
            "config_key": self.config_key,
            "referenced_host": self.referenced_host,
            "source_evidence": self.provenance.as_dict(),
        }


@dataclass(frozen=True, slots=True)
class UnresolvedDependency:
    """A declared host reference with no matching infrastructure entity.

    Reported rather than invented: no entity is created for an unresolved target.
    """

    source: str
    config_key: str
    referenced_host: str
    provenance: Provenance

    def summary(self) -> dict[str, Any]:
        return {
            "source": self.source,
            "config_key": self.config_key,
            "referenced_host": self.referenced_host,
            "reason": "no infrastructure service, hostname, or container_name alias matched",
            "source_evidence": self.provenance.as_dict(),
        }


@dataclass(frozen=True, slots=True)
class ComposeExtraction:
    repository: str
    commit: str
    owner: str | None
    source_files: tuple[str, ...]
    services: tuple[EntityCandidate, ...]
    infrastructure: tuple[EntityCandidate, ...]
    relationships: tuple[RelationshipCandidate, ...]
    unresolved_dependencies: tuple[UnresolvedDependency, ...]
    warnings: tuple[str, ...]
    secret_values: frozenset[str]

    @property
    def entities(self) -> tuple[EntityCandidate, ...]:
        return self.services + self.infrastructure

    def relations_for(self, entity_id: str) -> tuple[RelationshipCandidate, ...]:
        return tuple(item for item in self.relationships if item.source == entity_id)


# ---------------------------------------------------------------------------------------
# Extraction
# ---------------------------------------------------------------------------------------


def _safe_attributes(definition: dict[str, Any]) -> dict[str, Any]:
    """Project a Compose service into attributes that cannot carry a credential."""
    attributes: dict[str, Any] = {}

    image = definition.get("image")
    if isinstance(image, str) and image.strip():
        attributes["image"] = image.strip()

    build = definition.get("build")
    if isinstance(build, str) and build.strip():
        attributes["build_context"] = build.strip()
    elif isinstance(build, dict):
        context = build.get("context")
        dockerfile = build.get("dockerfile")
        if isinstance(context, str) and context.strip():
            attributes["build_context"] = context.strip()
        if isinstance(dockerfile, str) and dockerfile.strip():
            attributes["build_dockerfile"] = dockerfile.strip()

    for source_key, target_key in (
        ("container_name", "container_name"),
        ("hostname", "hostname"),
        ("restart", "restart"),
    ):
        value = definition.get(source_key)
        if isinstance(value, str) and value.strip():
            attributes[target_key] = value.strip()

    for source_key, target_key in (
        ("ports", "ports"),
        ("networks", "networks"),
        ("volumes", "volumes"),
        ("env_file", "env_file"),
        ("depends_on", "compose_depends_on"),
    ):
        value = definition.get(source_key)
        if isinstance(value, list) and value:
            attributes[target_key] = [str(item) for item in value]
        elif isinstance(value, dict) and value:
            attributes[target_key] = sorted(str(item) for item in value)

    environment = parse_environment(definition.get("environment"))
    if environment:
        attributes["environment"] = redact_environment(environment)

    # Record only that a command exists; its text may embed a password.
    present = [key for key in UNSAFE_COMPOSE_KEYS if definition.get(key)]
    if present:
        attributes["omitted_for_secret_safety"] = present

    return attributes


def _load_compose_documents(
    repository_path: Path, source_files: tuple[str, ...], warnings: list[str]
) -> list[tuple[str, dict[str, Any]]]:
    """Parse each source file with yaml.safe_load, skipping anything that is not Compose."""
    documents: list[tuple[str, dict[str, Any]]] = []
    for relative_path in source_files:
        absolute = repository_path / relative_path
        try:
            document = yaml.safe_load(absolute.read_text(encoding="utf-8"))
        except (OSError, yaml.YAMLError) as exc:
            warnings.append(f"{relative_path}: unreadable or invalid YAML, skipped ({exc})")
            continue
        if not isinstance(document, dict):
            warnings.append(f"{relative_path}: not a YAML mapping, skipped")
            continue
        if "include" in document:
            warnings.append(
                f"{relative_path}: Compose 'include' directives are not traversed; the "
                f"manifest source patterns already enumerate the included files"
            )
        services = document.get("services")
        if not isinstance(services, dict) or not services:
            warnings.append(f"{relative_path}: no Compose 'services' mapping, skipped")
            continue
        documents.append((relative_path, services))
    return documents


def extract_compose(
    record: RepositoryRecord,
    commit: str,
    *,
    source_kind: str = EXTRACTOR_KIND,
) -> ComposeExtraction:
    """Extract Compose services, infrastructure, and runtime dependencies.

    ``commit`` must already be verified against the manifest baseline by the caller.
    """
    repository_slug = normalize_token(record.id)
    source_files = resolve_source_files(record, source_kind)
    warnings: list[str] = []
    documents = _load_compose_documents(record.path, source_files, warnings)

    # Deterministic traversal: sorted by file, then by Compose service key.
    ordered: list[tuple[str, str, dict[str, Any]]] = []
    for relative_path, services in documents:
        for compose_key in sorted(services):
            definition = services[compose_key]
            if not isinstance(definition, dict):
                warnings.append(
                    f"{relative_path}: service {compose_key!r} is not a mapping, skipped"
                )
                continue
            ordered.append((relative_path, str(compose_key), definition))
    ordered.sort(key=lambda item: (item[0], item[1]))

    services: list[EntityCandidate] = []
    infrastructure: list[EntityCandidate] = []
    secret_values: set[str] = set()

    for relative_path, compose_key, definition in ordered:
        provenance = Provenance(
            repository=record.id,
            commit=commit,
            source_path=relative_path,
            pointer=json_pointer("services", compose_key),
        )
        environment = parse_environment(definition.get("environment"))

        if definition.get("build"):
            # Built from this repository, therefore an application service.
            services.append(
                EntityCandidate(
                    id=application_service_id(repository_slug, compose_key),
                    kind="Service",
                    title=compose_key,
                    role=APPLICATION_ROLE,
                    compose_service=compose_key,
                    provenance=provenance,
                    attributes=_safe_attributes(definition),
                )
            )
            secret_values |= scannable_secret_values(environment)
            continue

        image = definition.get("image")
        if not isinstance(image, str) or not image.strip():
            warnings.append(
                f"{relative_path}: service {compose_key!r} declares neither 'build' nor "
                f"'image'; not classifiable from Compose evidence, skipped"
            )
            continue

        classification = classify_image(image)
        if classification is None:
            warnings.append(
                f"{relative_path}: service {compose_key!r} uses unrecognized image "
                f"{image.strip()!r}; no entity created (infrastructure is never invented)"
            )
            continue

        kind, engine = classification
        alias = canonical_alias(compose_key, definition)
        aliases = {compose_key, alias}
        for field_name in ("hostname", "container_name"):
            value = definition.get(field_name)
            if isinstance(value, str) and value.strip():
                aliases.add(value.strip())
        infrastructure.append(
            EntityCandidate(
                id=infrastructure_id(repository_slug, kind, alias),
                kind=kind,
                title=alias,
                role=INFRASTRUCTURE_ROLE,
                compose_service=compose_key,
                provenance=provenance,
                engine=engine,
                aliases=tuple(sorted(aliases)),
                attributes=_safe_attributes(definition),
            )
        )
        secret_values |= scannable_secret_values(environment)

    # Alias index: every name a dependent service could dial -> infrastructure entity id.
    alias_index: dict[str, str] = {}
    for entity in infrastructure:
        for alias in entity.aliases:
            existing = alias_index.get(alias)
            if existing is None:
                alias_index[alias] = entity.id
            elif existing != entity.id:
                warnings.append(
                    f"Alias {alias!r} is claimed by both {existing} and {entity.id}; kept "
                    f"{existing} (first in deterministic order)"
                )

    relationships: list[RelationshipCandidate] = []
    unresolved: list[UnresolvedDependency] = []

    for entity in services:
        definition_environment = entity.attributes.get("environment") or {}
        for config_key in sorted(definition_environment):
            if not config_key.upper().endswith(HOST_KEY_SUFFIX):
                continue
            raw_value = definition_environment[config_key]
            referenced_host = str(raw_value).strip()
            pointer = json_pointer("services", entity.compose_service, "environment", config_key)
            provenance = Provenance(
                repository=record.id,
                commit=commit,
                source_path=entity.provenance.source_path,
                pointer=pointer,
            )
            if not referenced_host or referenced_host == REDACTED_PLACEHOLDER:
                warnings.append(
                    f"{entity.compose_service}: {config_key} has no usable value, skipped"
                )
                continue
            if _is_bind_address(referenced_host):
                warnings.append(
                    f"{entity.compose_service}: {config_key}={referenced_host} is a local "
                    f"bind address, not a dependency reference; skipped"
                )
                continue
            target = alias_index.get(referenced_host)
            if target is None:
                unresolved.append(
                    UnresolvedDependency(
                        source=entity.id,
                        config_key=config_key,
                        referenced_host=referenced_host,
                        provenance=provenance,
                    )
                )
                continue
            relationships.append(
                RelationshipCandidate(
                    source=entity.id,
                    type=DEPENDS_ON,
                    target=target,
                    config_key=config_key,
                    referenced_host=referenced_host,
                    provenance=provenance,
                )
            )

    services.sort(key=lambda item: item.id)
    infrastructure.sort(key=lambda item: item.id)
    relationships.sort(key=lambda item: (item.source, item.config_key, item.target))
    unresolved.sort(key=lambda item: (item.source, item.config_key, item.referenced_host))

    return ComposeExtraction(
        repository=record.id,
        commit=commit,
        owner=record.owner,
        source_files=source_files,
        services=tuple(services),
        infrastructure=tuple(infrastructure),
        relationships=tuple(relationships),
        unresolved_dependencies=tuple(unresolved),
        warnings=tuple(warnings),
        secret_values=frozenset(secret_values),
    )


# ---------------------------------------------------------------------------------------
# Candidate rendering
# ---------------------------------------------------------------------------------------


def render_candidate_markdown(entity: EntityCandidate, extraction: ComposeExtraction) -> str:
    """Render one candidate page. Always ``status: candidate`` / ``review_status: pending``."""
    frontmatter: dict[str, Any] = {
        "id": entity.id,
        "kind": entity.kind,
        # The canonical loader requires kind and OKF type to agree.
        "type": entity.kind,
        "title": entity.title,
        "status": CANDIDATE_STATUS,
        "review_status": CANDIDATE_REVIEW_STATUS,
        "candidate_of": f"{EXTRACTOR_KIND}-extraction",
        "repository": extraction.repository,
        "commit": extraction.commit,
        "evidence_type": EVIDENCE_TYPE,
        "extractor": EXTRACTOR_KIND,
        "role": entity.role,
        "compose_service": entity.compose_service,
    }
    if entity.engine:
        frontmatter["engine"] = entity.engine
    if entity.aliases:
        frontmatter["network_aliases"] = list(entity.aliases)
    if extraction.owner:
        frontmatter["owner"] = extraction.owner
    frontmatter["source_refs"] = [entity.provenance.as_dict()]

    relations = extraction.relations_for(entity.id)
    if relations:
        frontmatter["relations"] = [
            {
                "type": relation.type,
                "target": relation.target,
                "config_key": relation.config_key,
                "referenced_host": relation.referenced_host,
                **relation.provenance.as_dict(),
            }
            for relation in relations
        ]
    if entity.attributes:
        frontmatter["attributes"] = entity.attributes

    rendered_frontmatter = yaml.safe_dump(
        frontmatter,
        sort_keys=False,
        default_flow_style=False,
        allow_unicode=True,
        width=100,
    ).rstrip("\n")

    lines = [
        "---",
        rendered_frontmatter,
        "---",
        "",
        f"# {entity.title}",
        "",
        f"Candidate extracted from Docker Compose evidence in `{extraction.repository}` at "
        f"commit `{extraction.commit}`.",
        "",
        f"- Compose service: `{entity.compose_service}`",
        f"- Declared in: `{entity.provenance.source_path}`",
        f"- YAML pointer: `{entity.provenance.pointer}`",
        f"- Evidence class: `{EVIDENCE_TYPE}`",
        "",
    ]
    if relations:
        lines.append("## Runtime dependencies")
        lines.append("")
        for relation in relations:
            lines.append(
                f"- `{relation.type}` -> `{relation.target}` "
                f"(from `{relation.config_key}={relation.referenced_host}`)"
            )
        lines.append("")
    lines.extend(
        [
            "## Review notes",
            "",
            "This page is a candidate awaiting review. It is not canonical knowledge and "
            "secret values are redacted at extraction time.",
            "",
        ]
    )
    return "\n".join(lines)


def build_report(extraction: ComposeExtraction, secret_values_emitted: int) -> dict[str, Any]:
    """Assemble extraction-report.json. Contains no timestamp, so runs stay comparable."""
    return {
        "version": 1,
        "extractor": EXTRACTOR_KIND,
        "repository": extraction.repository,
        "commit": extraction.commit,
        "evidence_type": EVIDENCE_TYPE,
        "source_files": list(extraction.source_files),
        "counts": {
            "source_files": len(extraction.source_files),
            "application_services": len(extraction.services),
            "infrastructure_entities": len(extraction.infrastructure),
            "relationships": len(extraction.relationships),
            "unresolved_dependencies": len(extraction.unresolved_dependencies),
            "warnings": len(extraction.warnings),
        },
        "application_services": [entity.summary() for entity in extraction.services],
        "infrastructure_entities": [entity.summary() for entity in extraction.infrastructure],
        "relationships": [relation.summary() for relation in extraction.relationships],
        "unresolved_dependencies": [
            item.summary() for item in extraction.unresolved_dependencies
        ],
        "warnings": list(extraction.warnings),
        "secret_values_emitted": secret_values_emitted,
    }


def count_secret_leaks(extraction: ComposeExtraction, rendered: dict[str, str]) -> int:
    """Verify redaction by scanning rendered output for distinctive secret values.

    ``secret_values_emitted`` in the report is this measured count, not a constant.
    """
    leaks = 0
    for content in rendered.values():
        for secret in sorted(extraction.secret_values):
            leaks += content.count(secret)
    return leaks


def render_all(extraction: ComposeExtraction) -> dict[str, str]:
    """Render every candidate page keyed by output-relative POSIX path."""
    rendered: dict[str, str] = {}
    for entity in extraction.services:
        rendered[f"services/{entity.id}.md"] = render_candidate_markdown(entity, extraction)
    for entity in extraction.infrastructure:
        rendered[f"infrastructure/{entity.id}.md"] = render_candidate_markdown(
            entity, extraction
        )
    return rendered


def render_report_json(report: dict[str, Any]) -> str:
    return json.dumps(report, indent=2, ensure_ascii=False) + "\n"


def render_bundle(extraction: ComposeExtraction) -> tuple[dict[str, str], dict[str, Any]]:
    """Render candidates plus the report, with the leak count measured over all output.

    The count is computed over the candidate pages and over a provisional report body, so
    a secret surfacing through a warning or an unresolved host name is caught too.
    """
    rendered = render_all(extraction)
    provisional = build_report(extraction, 0)
    scanned = {**rendered, "extraction-report.json": render_report_json(provisional)}
    leaks = count_secret_leaks(extraction, scanned)
    return rendered, build_report(extraction, leaks)
