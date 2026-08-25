"""Deterministic tests for the Docker Compose extractor (Graph Engineering Pass 1).

The fixture mirrors the frozen FTGO baseline (six built application services, five
infrastructure Compose files, admin UIs, and a deliberately absent ``feedback_redis``) so
the suite is hermetic and runs without the FTGO checkout present. One opt-in test verifies
the same expectations against the real repository when it is available locally.
"""

from __future__ import annotations

import json
import textwrap
from pathlib import Path

import pytest
import yaml

from knowledge_plane.extract import run
from knowledge_plane.extractors.compose import (
    application_service_id,
    canonical_alias,
    classify_image,
    extract_compose,
    image_name,
    json_pointer,
    normalize_token,
    parse_environment,
    render_bundle,
)
from knowledge_plane.repository_manifest import (
    DEFAULT_MANIFEST_RELATIVE_PATH,
    CommitMismatchError,
    RepositoryRecord,
    load_repository_manifest,
    read_git_head,
)

FROZEN_COMMIT = "52b1fd1b5d808e32b7925e890f560445a8460e7a"
WRONG_COMMIT = "0123456789abcdef0123456789abcdef01234567"
AIDE_ROOT = Path(__file__).resolve().parents[1]

EXPECTED_SERVICE_IDS = {
    "service.ftgo.gateway",
    "service.ftgo.user",
    "service.ftgo.restaurant",
    "service.ftgo.location",
    "service.ftgo.order",
    "service.ftgo.feedback",
}

# Secret values present in the fixture. None may appear in generated output.
FIXTURE_SECRETS = (
    "gateway_password",
    "user_password",
    "restaurant_password",
    "location_password",
    "order_password",
    "feedback_password",
    "rabbitmq_password",
    "admin_pass",
    "fdshU32U89UH324SDFHJDASFdsf2394",
)

APP_COMPOSE = """\
services:
  gateway_service:
    build:
      context: ./gateway
      dockerfile: Dockerfile
    container_name: gateway_service
    environment:
      - RABBITMQ_HOST=rabbitmq
      - RABBITMQ_PASS=rabbitmq_password
      - REDIS_HOST=gateway_redis
      - REDIS_PASSWORD=gateway_password
      - TOKEN_SECRET_KEY=fdshU32U89UH324SDFHJDASFdsf2394
      - SERVICE_HOST=0.0.0.0
      - SERVICE_PORT=8000
    ports:
      - "8000:8000"
    networks:
      - backend-network

  user_service:
    build:
      context: ./microservices/user
      dockerfile: Dockerfile
    container_name: "user_service"
    environment:
      - RABBITMQ_HOST=rabbitmq
      - REDIS_HOST=user_redis
      - REDIS_PASSWORD=user_password
      - POSTGRES_HOST=user_postgres
      - POSTGRES_PASSWORD=user_password
    networks:
      - backend-network

  restaurant_service:
    build:
      context: ./microservices/restaurant
      dockerfile: Dockerfile
    environment:
      - RABBITMQ_HOST=rabbitmq
      - REDIS_HOST=restaurant_redis
      - POSTGRES_HOST=restaurant_postgres
      - POSTGRES_PASSWORD=restaurant_password

  location_service:
    build:
      context: ./microservices/location
      dockerfile: Dockerfile
    environment:
      - RABBITMQ_HOST=rabbitmq
      - REDIS_HOST=location_redis
      - POSTGRES_HOST=location_postgres
      - POSTGRES_PASSWORD=location_password

  order_service:
    build:
      context: ./microservices/order
      dockerfile: Dockerfile
    environment:
      - RABBITMQ_HOST=rabbitmq
      - REDIS_HOST=order_redis
      - MONGO_HOST=order_mongo
      - MONGO_PASSWORD=order_password

  feedback_service:
    build:
      context: ./microservices/feedback
      dockerfile: Dockerfile
    environment:
      - RABBITMQ_HOST=rabbitmq
      - REDIS_HOST=feedback_redis
      - MONGO_HOST=feedback_mongo
      - MONGO_PASSWORD=feedback_password

networks:
  backend-network:
    external: true
"""

POSTGRES_COMPOSE = """\
services:
  user_postgres:
    image: postgres:16.3
    container_name: "user_postgres"
    hostname: "user_postgres"
    environment:
      - POSTGRES_PASSWORD=user_password
    ports:
      - "5438:5432"

  restaurant_postgres:
    image: postgres:16.3
    container_name: "restaurant_postgres"
    hostname: "restaurant_postgres"
    environment:
      - POSTGRES_PASSWORD=restaurant_password

  location_postgres:
    image: postgres:16.3
    hostname: "location_postgres"
    environment:
      - POSTGRES_PASSWORD=location_password
"""

REDIS_COMPOSE = """\
services:
  gateway_redis:
    image: redis:7.2.5
    container_name: "gateway_redis"
    hostname: "gateway_redis"
    environment:
      - REDIS_PASSWORD=gateway_password
    command: ["redis-server", "--requirepass", "gateway_password"]

  user_redis:
    image: redis:7.2.5
    hostname: "user_redis"
    environment:
      - REDIS_PASSWORD=user_password
    command: ["redis-server", "--requirepass", "user_password"]

  restaurant_redis:
    image: redis:7.2.5
    hostname: "restaurant_redis"

  location_redis:
    image: redis:7.2.5
    hostname: "location_redis"

  order_redis:
    image: redis:7.2.5
    hostname: "order_redis"
"""

RABBITMQ_COMPOSE = """\
services:
  message_broker:
    image: rabbitmq:3-management
    container_name: "message_broker"
    hostname: "rabbitmq"
    environment:
      - RABBITMQ_DEFAULT_PASS=rabbitmq_password
"""

MONGO_COMPOSE = """\
services:
  order_mongo:
    image: mongo:latest
    container_name: order_mongo
    environment:
      MONGO_INITDB_ROOT_PASSWORD: order_password

  feedback_mongo:
    image: mongo:latest
    container_name: feedback_mongo
    environment:
      MONGO_INITDB_ROOT_PASSWORD: feedback_password
"""

# Admin UIs whose image names embed "redis" and "mongo" but are not a cache or a database.
ADMIN_COMPOSE = """\
services:
  redis_insight:
    image: "redislabs/redisinsight:latest"
    container_name: redisinsight

  mongo_express:
    image: mongo-express
    environment:
      ME_CONFIG_MONGODB_ADMINPASSWORD: admin_pass

  metabase:
    image: metabase/metabase:latest
    environment:
      MB_PASSWORD_LENGTH: "8"
"""

# Not a Compose file at all; the manifest glob still matches it.
NON_COMPOSE_YAML = """\
global:
  scrape_interval: 15s
scrape_configs:
- job_name: prometheus
"""

INCLUDE_ONLY_COMPOSE = """\
include:
  - ./postgres/docker-compose.yaml
  - ./redis/docker-compose.yaml
"""

FIXTURE_FILES = {
    "backend/docker-compose.yaml": APP_COMPOSE,
    "backend/infra/docker-compose.yaml": INCLUDE_ONLY_COMPOSE,
    "backend/infra/postgres/docker-compose.yaml": POSTGRES_COMPOSE,
    "backend/infra/redis/docker-compose.yaml": REDIS_COMPOSE,
    "backend/infra/rabbitmq/docker-compose.yaml": RABBITMQ_COMPOSE,
    "backend/infra/mongo/docker-compose.yaml": MONGO_COMPOSE,
    "backend/infra/admin/docker-compose.yaml": ADMIN_COMPOSE,
    "backend/infra/monitoring/prometheus/prometheus.yaml": NON_COMPOSE_YAML,
}


def build_repository(root: Path, files: dict[str, str] | None = None) -> Path:
    for relative_path, content in (files or FIXTURE_FILES).items():
        target = root / relative_path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
    return root


def make_record(repo_root: Path) -> RepositoryRecord:
    return RepositoryRecord(
        id="ftgo",
        path=repo_root,
        url="https://example.invalid/ftgo.git",
        default_branch="main",
        expected_commit=FROZEN_COMMIT,
        owner="aide-ftgo-cohort",
        sources={"compose": ("backend/docker-compose.yaml", "backend/infra/**/*.yaml")},
    )


@pytest.fixture
def extraction(tmp_path: Path):
    return extract_compose(make_record(build_repository(tmp_path / "repo")), FROZEN_COMMIT)


def write_manifest(tmp_path: Path, repo_root: Path) -> Path:
    manifest = tmp_path / "repositories.yaml"
    manifest.write_text(
        yaml.safe_dump(
            {
                "version": 1,
                "repositories": [
                    {
                        "id": "ftgo",
                        "path": str(repo_root),
                        "expected_commit": FROZEN_COMMIT,
                        "owner": "aide-ftgo-cohort",
                        "sources": {
                            "compose": [
                                "backend/docker-compose.yaml",
                                "backend/infra/**/*.yaml",
                            ]
                        },
                    }
                ],
            },
            sort_keys=False,
        ),
        encoding="utf-8",
    )
    return manifest


# --------------------------------------------------------------------------------------
# Normalization primitives
# --------------------------------------------------------------------------------------


def test_service_ids_are_normalized_deterministically() -> None:
    expected = {
        "gateway_service": "service.ftgo.gateway",
        "user_service": "service.ftgo.user",
        "restaurant_service": "service.ftgo.restaurant",
        "location_service": "service.ftgo.location",
        "order_service": "service.ftgo.order",
        "feedback_service": "service.ftgo.feedback",
    }
    for compose_key, service_id in expected.items():
        assert application_service_id("ftgo", compose_key) == service_id


def test_service_id_normalization_is_path_independent() -> None:
    # The same Compose key always yields the same id regardless of workstation layout.
    assert application_service_id("ftgo", "order_service") == "service.ftgo.order"
    assert application_service_id("ftgo", "ORDER_SERVICE") == "service.ftgo.order"
    assert application_service_id("ftgo", "order-service") == "service.ftgo.order"
    # A key that is only the suffix must not normalize to an empty id.
    assert application_service_id("ftgo", "service") == "service.ftgo.service"


def test_normalize_token_collapses_separators() -> None:
    assert normalize_token("user_postgres") == "user-postgres"
    assert normalize_token("  Message__Broker  ") == "message-broker"


def test_image_name_ignores_registry_namespace_tag_and_digest() -> None:
    assert image_name("postgres:16.3") == "postgres"
    assert image_name("mongo") == "mongo"
    assert image_name("localhost:5000/library/redis:7.2.5") == "redis"
    assert image_name("redis@sha256:abc123") == "redis"


def test_image_classification_matches_exact_names_not_substrings() -> None:
    assert classify_image("postgres:16.3") == ("Database", "postgresql")
    assert classify_image("mongo:latest") == ("Database", "mongodb")
    assert classify_image("redis:7.2.5") == ("Component", "redis")
    assert classify_image("rabbitmq:3-management") == ("Component", "rabbitmq")
    # Admin UIs must not be mistaken for the engines their names mention.
    assert classify_image("redislabs/redisinsight:latest") is None
    assert classify_image("mongo-express") is None
    assert classify_image("metabase/metabase:latest") is None


def test_canonical_alias_prefers_hostname_then_container_then_key() -> None:
    assert canonical_alias("message_broker", {"hostname": "rabbitmq"}) == "rabbitmq"
    assert canonical_alias("order_mongo", {"container_name": "order_mongo"}) == "order_mongo"
    assert canonical_alias("bare_service", {}) == "bare_service"


def test_environment_parsing_handles_both_compose_forms() -> None:
    assert parse_environment(["A=1", "B=x=y", "C"]) == {"A": "1", "B": "x=y", "C": ""}
    assert parse_environment({"A": 1, "B": None}) == {"A": "1", "B": ""}
    assert parse_environment(None) == {}


def test_json_pointer_escapes_reserved_characters() -> None:
    assert json_pointer("services", "order_service") == "/services/order_service"
    assert json_pointer("a/b", "c~d") == "/a~1b/c~0d"


# --------------------------------------------------------------------------------------
# Service discovery
# --------------------------------------------------------------------------------------


def test_discovers_exactly_six_application_services(extraction) -> None:
    assert len(extraction.services) == 6
    assert {entity.id for entity in extraction.services} == EXPECTED_SERVICE_IDS
    assert all(entity.kind == "Service" for entity in extraction.services)


def test_application_service_names_are_not_hard_coded(tmp_path: Path) -> None:
    # Renaming every service must still discover them: classification follows `build:`.
    renamed = APP_COMPOSE.replace("_service:", "_worker:").replace(
        "REDIS_HOST=feedback_redis", "REDIS_HOST=order_redis"
    )
    files = dict(FIXTURE_FILES)
    files["backend/docker-compose.yaml"] = renamed
    record = make_record(build_repository(tmp_path / "repo", files))

    result = extract_compose(record, FROZEN_COMMIT)

    assert len(result.services) == 6
    assert {entity.id for entity in result.services} == {
        "service.ftgo.gateway-worker",
        "service.ftgo.user-worker",
        "service.ftgo.restaurant-worker",
        "service.ftgo.location-worker",
        "service.ftgo.order-worker",
        "service.ftgo.feedback-worker",
    }


def test_services_without_build_or_image_are_skipped(tmp_path: Path) -> None:
    files = dict(FIXTURE_FILES)
    files["backend/docker-compose.yaml"] = "services:\n  ghost:\n    networks: [backend-network]\n"
    record = make_record(build_repository(tmp_path / "repo", files))

    result = extract_compose(record, FROZEN_COMMIT)

    assert result.services == ()
    assert any("neither 'build' nor 'image'" in warning for warning in result.warnings)


# --------------------------------------------------------------------------------------
# Infrastructure discovery and classification
# --------------------------------------------------------------------------------------


def test_postgres_instances_become_database_candidates(extraction) -> None:
    databases = {
        entity.id: entity for entity in extraction.infrastructure if entity.kind == "Database"
    }

    for expected_id in (
        "database.ftgo.user-postgres",
        "database.ftgo.restaurant-postgres",
        "database.ftgo.location-postgres",
    ):
        assert databases[expected_id].engine == "postgresql"


def test_mongo_instances_become_database_candidates(extraction) -> None:
    databases = {
        entity.id: entity for entity in extraction.infrastructure if entity.kind == "Database"
    }

    assert databases["database.ftgo.order-mongo"].engine == "mongodb"
    assert databases["database.ftgo.feedback-mongo"].engine == "mongodb"


def test_redis_instances_become_component_candidates(extraction) -> None:
    components = {
        entity.id: entity for entity in extraction.infrastructure if entity.kind == "Component"
    }

    for expected_id in (
        "component.ftgo.gateway-redis",
        "component.ftgo.user-redis",
        "component.ftgo.restaurant-redis",
        "component.ftgo.location-redis",
        "component.ftgo.order-redis",
    ):
        assert components[expected_id].engine == "redis"


def test_rabbitmq_is_identified_by_its_hostname_alias(extraction) -> None:
    broker = next(
        entity for entity in extraction.infrastructure if entity.engine == "rabbitmq"
    )

    # Compose key is message_broker; identity follows the hostname dependents dial.
    assert broker.id == "component.ftgo.rabbitmq"
    assert broker.kind == "Component"
    assert broker.compose_service == "message_broker"
    assert set(broker.aliases) == {"message_broker", "rabbitmq"}


def test_only_ontology_approved_kinds_are_emitted(extraction) -> None:
    allowed = set(
        yaml.safe_load((AIDE_ROOT / "ontology/entity-types.yaml").read_text(encoding="utf-8"))[
            "entity_types"
        ]
    )
    emitted = {entity.kind for entity in extraction.entities}

    assert emitted <= allowed
    assert emitted == {"Service", "Database", "Component"}
    # No new ontology type is introduced for networks, caches, or brokers.
    assert not emitted & {"Network", "Cache", "Broker"}


def test_admin_uis_are_not_misclassified_as_infrastructure(extraction) -> None:
    identifiers = {entity.id for entity in extraction.entities}

    assert not any("redisinsight" in identifier for identifier in identifiers)
    assert not any("insight" in identifier for identifier in identifiers)
    assert not any("express" in identifier for identifier in identifiers)
    assert not any("metabase" in identifier for identifier in identifiers)
    assert sum("unrecognized image" in warning for warning in extraction.warnings) == 3


def test_non_compose_yaml_is_skipped_with_a_warning(extraction) -> None:
    assert any(
        "prometheus.yaml: no Compose 'services' mapping" in warning
        for warning in extraction.warnings
    )
    assert any(
        "'include' directives are not traversed" in warning for warning in extraction.warnings
    )


# --------------------------------------------------------------------------------------
# Dependency extraction
# --------------------------------------------------------------------------------------


def _edges(extraction) -> set[tuple[str, str, str]]:
    return {
        (relation.source, relation.config_key, relation.target)
        for relation in extraction.relationships
    }


def test_postgres_dependencies_come_from_explicit_host_configuration(extraction) -> None:
    assert (
        "service.ftgo.user",
        "POSTGRES_HOST",
        "database.ftgo.user-postgres",
    ) in _edges(extraction)


def test_mongo_dependencies_come_from_explicit_host_configuration(extraction) -> None:
    assert ("service.ftgo.order", "MONGO_HOST", "database.ftgo.order-mongo") in _edges(extraction)


def test_redis_dependencies_come_from_explicit_host_configuration(extraction) -> None:
    assert (
        "service.ftgo.gateway",
        "REDIS_HOST",
        "component.ftgo.gateway-redis",
    ) in _edges(extraction)


def test_rabbitmq_alias_resolves_for_every_service_that_declares_it(extraction) -> None:
    brokers = {
        relation.source
        for relation in extraction.relationships
        if relation.target == "component.ftgo.rabbitmq"
    }

    assert brokers == EXPECTED_SERVICE_IDS
    assert all(
        relation.referenced_host == "rabbitmq"
        for relation in extraction.relationships
        if relation.target == "component.ftgo.rabbitmq"
    )


def test_every_relationship_is_depends_on_with_a_known_target(extraction) -> None:
    known = {entity.id for entity in extraction.entities}

    assert all(relation.type == "DEPENDS_ON" for relation in extraction.relationships)
    assert all(relation.target in known for relation in extraction.relationships)
    assert all(relation.source in known for relation in extraction.relationships)


def test_dependencies_are_not_inferred_from_names_alone(tmp_path: Path) -> None:
    # order_service names order_mongo only in its container name, never in *_HOST config.
    files = dict(FIXTURE_FILES)
    files["backend/docker-compose.yaml"] = textwrap.dedent(
        """\
        services:
          order_service:
            build:
              context: ./microservices/order
            container_name: order_service_next_to_order_mongo
            environment:
              - MONGO_PORT=27017
        """
    )
    record = make_record(build_repository(tmp_path / "repo", files))

    result = extract_compose(record, FROZEN_COMMIT)

    assert result.relationships == ()
    assert result.unresolved_dependencies == ()


def test_unresolved_host_is_reported_and_no_entity_is_invented(extraction) -> None:
    unresolved = extraction.unresolved_dependencies

    assert len(unresolved) == 1
    missing = unresolved[0]
    assert missing.source == "service.ftgo.feedback"
    assert missing.config_key == "REDIS_HOST"
    assert missing.referenced_host == "feedback_redis"
    assert missing.provenance.pointer == "/services/feedback_service/environment/REDIS_HOST"

    # Nothing was fabricated for the missing target.
    identifiers = {entity.id for entity in extraction.entities}
    assert "component.ftgo.feedback-redis" not in identifiers
    assert not any(
        relation.referenced_host == "feedback_redis" for relation in extraction.relationships
    )


def test_bind_address_is_not_treated_as_a_dependency(extraction) -> None:
    assert not any(
        item.config_key == "SERVICE_HOST" for item in extraction.unresolved_dependencies
    )
    assert not any(
        relation.config_key == "SERVICE_HOST" for relation in extraction.relationships
    )
    assert any("local bind address" in warning for warning in extraction.warnings)


# --------------------------------------------------------------------------------------
# Provenance
# --------------------------------------------------------------------------------------


def test_every_candidate_carries_full_provenance(extraction) -> None:
    for entity in extraction.entities:
        provenance = entity.provenance
        assert provenance.repository == "ftgo"
        assert provenance.commit == FROZEN_COMMIT
        assert provenance.evidence_type == "implemented"
        assert provenance.source_path.endswith(".yaml")
        assert not Path(provenance.source_path).is_absolute()
        assert provenance.pointer == f"/services/{entity.compose_service}"

    for relation in extraction.relationships:
        assert relation.provenance.commit == FROZEN_COMMIT
        assert relation.provenance.pointer.endswith(f"/environment/{relation.config_key}")


def test_source_paths_are_repository_relative_posix(extraction) -> None:
    assert "backend/docker-compose.yaml" in extraction.source_files
    for source_path in extraction.source_files:
        assert "\\" not in source_path
        assert not Path(source_path).is_absolute()


# --------------------------------------------------------------------------------------
# Candidate rendering, secret safety, and status
# --------------------------------------------------------------------------------------


def test_candidates_are_never_approved(extraction) -> None:
    rendered, _ = render_bundle(extraction)

    assert len(rendered) == len(extraction.entities)
    for path, content in rendered.items():
        frontmatter = yaml.safe_load(content.split("---")[1])
        assert frontmatter["status"] == "candidate"
        assert frontmatter["review_status"] == "pending"
        assert "status: approved" not in content
        assert path.startswith(("services/", "infrastructure/"))


def test_candidate_output_contains_the_frozen_commit(extraction) -> None:
    rendered, report = render_bundle(extraction)

    assert report["commit"] == FROZEN_COMMIT
    for content in rendered.values():
        assert FROZEN_COMMIT in content


def test_secret_values_are_redacted_from_candidate_content(extraction) -> None:
    rendered, report = render_bundle(extraction)
    blob = "\n".join(rendered.values()) + json.dumps(report)

    for secret in FIXTURE_SECRETS:
        assert secret not in blob, f"secret {secret!r} leaked into candidate output"
    assert report["secret_values_emitted"] == 0
    # Keys stay visible so reviewers can see the shape of the configuration.
    assert "[redacted]" in blob


def test_command_strings_are_not_copied_into_candidates(extraction) -> None:
    rendered, _ = render_bundle(extraction)
    blob = "\n".join(rendered.values())

    assert "requirepass" not in blob
    assert "redis-server" not in blob
    gateway_redis = rendered["infrastructure/component.ftgo.gateway-redis.md"]
    frontmatter = yaml.safe_load(gateway_redis.split("---")[1])
    assert frontmatter["attributes"]["omitted_for_secret_safety"] == ["command"]


def test_report_contains_the_required_fields(extraction) -> None:
    _, report = render_bundle(extraction)

    for key in (
        "repository",
        "commit",
        "source_files",
        "application_services",
        "infrastructure_entities",
        "relationships",
        "unresolved_dependencies",
        "warnings",
        "secret_values_emitted",
    ):
        assert key in report
    assert report["counts"]["application_services"] == 6
    assert report["counts"]["unresolved_dependencies"] == 1


# --------------------------------------------------------------------------------------
# CLI behavior: dry-run, commit gate, determinism
# --------------------------------------------------------------------------------------


def test_dry_run_writes_nothing(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    repo_root = build_repository(tmp_path / "repo")
    manifest = write_manifest(tmp_path, repo_root)
    output_dir = tmp_path / "candidates"
    monkeypatch.setattr("knowledge_plane.extract.read_git_head", lambda path: FROZEN_COMMIT)

    summary = run("ftgo", "compose", manifest_path=manifest, output_dir=output_dir, dry_run=True)

    assert summary["status"] == "dry-run"
    assert summary["dry_run"] is True
    assert summary["commit"] == FROZEN_COMMIT
    assert summary["counts"]["application_services"] == 6
    assert summary["secret_values_emitted"] == 0
    assert summary["graph_mutations"] == 0
    assert summary["graphiti"] == "disabled"
    # Zero filesystem candidate changes.
    assert not output_dir.exists()


def test_dry_run_still_reports_unresolved_dependencies(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    manifest = write_manifest(tmp_path, build_repository(tmp_path / "repo"))
    monkeypatch.setattr("knowledge_plane.extract.read_git_head", lambda path: FROZEN_COMMIT)

    summary = run("ftgo", "compose", manifest_path=manifest, dry_run=True)

    hosts = {item["referenced_host"] for item in summary["unresolved_dependencies"]}
    assert hosts == {"feedback_redis"}


def test_real_run_requires_an_output_directory(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    manifest = write_manifest(tmp_path, build_repository(tmp_path / "repo"))
    monkeypatch.setattr("knowledge_plane.extract.read_git_head", lambda path: FROZEN_COMMIT)

    with pytest.raises(Exception, match="--output-dir is required"):
        run("ftgo", "compose", manifest_path=manifest, dry_run=False)


def test_commit_mismatch_aborts_before_writing_anything(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    manifest = write_manifest(tmp_path, build_repository(tmp_path / "repo"))
    output_dir = tmp_path / "candidates"
    monkeypatch.setattr("knowledge_plane.extract.read_git_head", lambda path: WRONG_COMMIT)

    with pytest.raises(CommitMismatchError) as excinfo:
        run("ftgo", "compose", manifest_path=manifest, output_dir=output_dir, dry_run=False)

    assert excinfo.value.expected == FROZEN_COMMIT
    assert excinfo.value.actual == WRONG_COMMIT
    assert not output_dir.exists()


def test_expected_output_structure_is_written(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    manifest = write_manifest(tmp_path, build_repository(tmp_path / "repo"))
    output_dir = tmp_path / "candidates"
    monkeypatch.setattr("knowledge_plane.extract.read_git_head", lambda path: FROZEN_COMMIT)

    summary = run("ftgo", "compose", manifest_path=manifest, output_dir=output_dir)

    assert summary["status"] == "ok"
    assert (output_dir / "extraction-report.json").is_file()
    assert len(list((output_dir / "services").glob("*.md"))) == 6
    assert len(list((output_dir / "infrastructure").glob("*.md"))) == 11

    report = json.loads((output_dir / "extraction-report.json").read_text(encoding="utf-8"))
    assert report["commit"] == FROZEN_COMMIT
    assert report["secret_values_emitted"] == 0


def test_repeat_extraction_is_byte_identical(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    manifest = write_manifest(tmp_path, build_repository(tmp_path / "repo"))
    monkeypatch.setattr("knowledge_plane.extract.read_git_head", lambda path: FROZEN_COMMIT)
    first = tmp_path / "run-one"
    second = tmp_path / "run-two"

    run("ftgo", "compose", manifest_path=manifest, output_dir=first)
    run("ftgo", "compose", manifest_path=manifest, output_dir=second)

    first_files = sorted(path.relative_to(first) for path in first.rglob("*") if path.is_file())
    second_files = sorted(path.relative_to(second) for path in second.rglob("*") if path.is_file())
    assert first_files == second_files
    assert first_files, "extraction produced no files"
    for relative_path in first_files:
        assert (first / relative_path).read_bytes() == (second / relative_path).read_bytes(), (
            f"{relative_path} differs between runs"
        )


def test_rerun_into_the_same_directory_is_stable_and_prunes_orphans(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    manifest = write_manifest(tmp_path, build_repository(tmp_path / "repo"))
    monkeypatch.setattr("knowledge_plane.extract.read_git_head", lambda path: FROZEN_COMMIT)
    output_dir = tmp_path / "candidates"

    run("ftgo", "compose", manifest_path=manifest, output_dir=output_dir)
    orphan = output_dir / "services" / "service.ftgo.retired.md"
    orphan.write_text("stale", encoding="utf-8")
    before = {
        path.relative_to(output_dir).as_posix(): path.read_bytes()
        for path in sorted(output_dir.rglob("*"))
        if path.is_file() and path.name != orphan.name
    }

    run("ftgo", "compose", manifest_path=manifest, output_dir=output_dir)

    assert not orphan.exists()
    after = {
        path.relative_to(output_dir).as_posix(): path.read_bytes()
        for path in sorted(output_dir.rglob("*"))
        if path.is_file()
    }
    # The report records the prune, so only that file may differ.
    assert set(after) == set(before)
    for relative_path, content in before.items():
        if relative_path != "extraction-report.json":
            assert after[relative_path] == content


# --------------------------------------------------------------------------------------
# Opt-in verification against the real frozen FTGO checkout
# --------------------------------------------------------------------------------------


def _real_ftgo_record() -> RepositoryRecord | None:
    try:
        records = load_repository_manifest(AIDE_ROOT / DEFAULT_MANIFEST_RELATIVE_PATH)
    except Exception:  # noqa: BLE001 - absence of the checkout must only skip the test
        return None
    record = records.get("ftgo")
    if record is None or not record.path.is_dir():
        return None
    try:
        if read_git_head(record.path) != record.expected_commit:
            return None
    except Exception:  # noqa: BLE001
        return None
    return record


@pytest.mark.skipif(
    _real_ftgo_record() is None,
    reason="FTGO checkout is absent or not at the frozen expected commit",
)
def test_real_ftgo_baseline_matches_the_expected_shape() -> None:
    record = _real_ftgo_record()
    assert record is not None
    result = extract_compose(record, FROZEN_COMMIT)

    assert {entity.id for entity in result.services} == EXPECTED_SERVICE_IDS
    assert "component.ftgo.rabbitmq" in {entity.id for entity in result.infrastructure}
    assert "database.ftgo.order-mongo" in {entity.id for entity in result.infrastructure}
    assert "database.ftgo.user-postgres" in {entity.id for entity in result.infrastructure}
    assert [item.referenced_host for item in result.unresolved_dependencies] == ["feedback_redis"]

    _, report = render_bundle(result)
    assert report["secret_values_emitted"] == 0
