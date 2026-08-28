"""Deterministic tests for the RabbitMQ/RPC extractor (Graph Engineering Pass 3).

The main fixture is a synthetic repository that mirrors FTGO's real shape: a gateway that
publishes through an inherited ``_call_rpc`` wrapper, a microservice that registers handlers
from a literal ``{event: handler}`` map, and decoy classes with ``publish()``/``send()``
methods that are not brokers at all. Smaller fixtures cover ``aio_pika``, identity
collisions, and module-level usage. The suite is hermetic; opt-in tests at the end verify
the same guarantees against the real frozen FTGO checkout when it is available.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest
import yaml

from knowledge_plane.extract import run
from knowledge_plane.extractors.rabbitmq import (
    DELTAS_FILENAME,
    build_service_relation_deltas,
    count_secret_leaks,
    event_id,
    extract_rabbitmq,
    is_credential_name,
    normalize_identity,
    redact_amqp,
    render_bundle,
    skip_reason,
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

# The six application services approved in Pass 1. This pass reuses them and adds none.
PASS_ONE_SERVICE_IDS = {
    "service.ftgo.gateway",
    "service.ftgo.user",
    "service.ftgo.restaurant",
    "service.ftgo.location",
    "service.ftgo.order",
    "service.ftgo.feedback",
}

# Credential values present in the fixtures. None may appear in generated output.
FIXTURE_SECRETS = ("rabbitmq_password", "hunter2-broker-secret")

BROKER_MODULE = """\
from rabbitmq_rpc import RPCClient, RabbitMQConfig


class RPCBroker:
    _instance = None

    def __init__(self, rpc_client: RPCClient):
        self._rpc_client = rpc_client

    @classmethod
    async def initialize(cls) -> None:
        config = RabbitMQConfig(
            host="localhost",
            user="rabbitmq_user",
            password="rabbitmq_password",
        )
        rpc_client = await RPCClient.create(config=config)
        cls._instance = cls(rpc_client)

    @classmethod
    def get_instance(cls) -> 'RPCBroker':
        return cls._instance

    @classmethod
    def get_client(cls) -> RPCClient:
        return cls._instance._rpc_client
"""

GATEWAY_EVENT_CONSTANTS = """\
from enum import Enum

ORDER_CANCEL_EVENT = "order.cancel"
ORDER_PREFIX = "order."
ARCHIVE_SUFFIX = "archive"


class EventNames(str, Enum):
    ORDER_GET_DETAILS = "order.get_details"
    ORDER_STATUS_CHANGE = "order.status.change"
"""

GATEWAY_BASE = """\
from data_access.broker import RPCBroker


class Microservice:
    _service_name = ''

    @classmethod
    async def _call_rpc(cls, event_name, data):
        rpc_client = RPCBroker.get_client()
        return await rpc_client.call(event_name, data=data)
"""

GATEWAY_ORDER_SERVICE = """\
import os

from config.events import ARCHIVE_SUFFIX, ORDER_CANCEL_EVENT, ORDER_PREFIX, EventNames
from services.base import Microservice


def build_event(action):
    return os.getenv("EVENT_PREFIX", "order") + "." + action


class OrderService(Microservice):
    _service_name = 'order'

    @classmethod
    async def create_order(cls, data):
        return await cls._call_rpc('order.create', data=data)

    @classmethod
    async def cancel_order(cls, data):
        return await cls._call_rpc(ORDER_CANCEL_EVENT, data=data)

    @classmethod
    async def get_details(cls, data):
        return await cls._call_rpc(EventNames.ORDER_GET_DETAILS, data=data)

    @classmethod
    async def status_change(cls, data):
        return await cls._call_rpc(EventNames.ORDER_STATUS_CHANGE.value, data=data)

    @classmethod
    async def archive_order(cls, data):
        return await cls._call_rpc(ORDER_PREFIX + ARCHIVE_SUFFIX, data=data)

    @classmethod
    async def dynamic_order(cls, data, action):
        return await cls._call_rpc(build_event(action), data=data)
"""

# Decoys: ordinary objects that happen to expose publish/send/subscribe. None of these may
# ever be reported, because none traces back to a broker library.
GATEWAY_NOTIFICATIONS = """\
class EmailSender:
    def publish(self, event_name, payload=None):
        return None

    def send(self, event_name):
        return None


class InMemoryBus:
    def subscribe(self, event, handler=None):
        return None

    def register_event(self, event=None, handler=None):
        return None


class Notifier:
    def notify(self):
        sender = EmailSender()
        sender.publish('email.welcome', payload={})
        sender.send('email.reset')
        bus = InMemoryBus()
        bus.subscribe('email.bounced')
        bus.register_event(event='email.complaint', handler=self.notify)
"""

# Valid Python that would explode on import. Proof that nothing is ever imported.
GATEWAY_BOOBY_TRAP = """\
raise RuntimeError("this module must never be imported by the extractor")
"""

ORDER_EVENTS = """\
from application.middleware import event_middleware
from application.order import OrderService
from data_access.broker import RPCBroker


async def register_events():
    rpc_broker = RPCBroker.get_instance()
    rpc_client = rpc_broker.get_client()
    events_handlers = {
        'order.create': OrderService.create_order,
        'order.cancel': OrderService.cancel_order,
        'order.get_details': OrderService.get_order_details,
        'order.status.change': OrderService.change_status,
        'order.delivery.driver_found': OrderService.assign_driver,
    }

    for event, _handler in events_handlers.items():
        try:
            handler = event_middleware(event, _handler)
            await rpc_client.register_event(event=event, handler=handler)
        except Exception:
            continue
"""

ORDER_APPLICATION = """\
class OrderService:
    @classmethod
    async def create_order(cls, **kwargs):
        return None

    @classmethod
    async def cancel_order(cls, **kwargs):
        return None

    @classmethod
    async def get_order_details(cls, **kwargs):
        return None

    @classmethod
    async def change_status(cls, **kwargs):
        return None

    @classmethod
    async def assign_driver(cls, **kwargs):
        return None
"""

ORDER_MIDDLEWARE = """\
def event_middleware(event, handler):
    return handler
"""

# A microservice with source but no broker usage at all.
RESTAURANT_MODEL = """\
class Restaurant:
    def __init__(self, name):
        self.name = name
"""

FIXTURE_FILES = {
    "backend/gateway/src/__init__.py": "",
    "backend/gateway/src/config/__init__.py": "",
    "backend/gateway/src/config/events.py": GATEWAY_EVENT_CONSTANTS,
    "backend/gateway/src/data_access/__init__.py": "",
    "backend/gateway/src/data_access/broker.py": BROKER_MODULE,
    "backend/gateway/src/services/__init__.py": "",
    "backend/gateway/src/services/base.py": GATEWAY_BASE,
    "backend/gateway/src/services/order.py": GATEWAY_ORDER_SERVICE,
    "backend/gateway/src/services/notifications.py": GATEWAY_NOTIFICATIONS,
    "backend/gateway/src/services/booby_trap.py": GATEWAY_BOOBY_TRAP,
    "backend/microservices/order/src/__init__.py": "",
    "backend/microservices/order/src/events.py": ORDER_EVENTS,
    "backend/microservices/order/src/application/__init__.py": "",
    "backend/microservices/order/src/application/order.py": ORDER_APPLICATION,
    "backend/microservices/order/src/application/middleware.py": ORDER_MIDDLEWARE,
    "backend/microservices/order/src/data_access/__init__.py": "",
    "backend/microservices/order/src/data_access/broker.py": BROKER_MODULE,
    "backend/microservices/restaurant/src/__init__.py": "",
    "backend/microservices/restaurant/src/models.py": RESTAURANT_MODEL,
    # Out-of-scope trees that declare broker usage; none may reach the output.
    "backend/microservices/order/tests/test_events.py": ORDER_EVENTS,
    "backend/microservices/order/migrations/env.py": ORDER_EVENTS,
    "backend/gateway/Dockerfile": "FROM python:3.12\n",
}

EVENT_CREATE = "event.ftgo.rabbitmq.order.create"
EVENT_CANCEL = "event.ftgo.rabbitmq.order.cancel"
EVENT_DETAILS = "event.ftgo.rabbitmq.order.get-details"
EVENT_STATUS = "event.ftgo.rabbitmq.order.status.change"
EVENT_ARCHIVE = "event.ftgo.rabbitmq.order.archive"
EVENT_DRIVER_FOUND = "event.ftgo.rabbitmq.order.delivery.driver-found"


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
        sources={"code": ("backend/gateway/**/*", "backend/microservices/**/*")},
    )


@pytest.fixture
def extraction(tmp_path: Path):
    return extract_rabbitmq(make_record(build_repository(tmp_path / "repo")), FROZEN_COMMIT)


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
                        "sources": {"code": ["backend/gateway/**/*", "backend/microservices/**/*"]},
                    }
                ],
            },
            sort_keys=False,
        ),
        encoding="utf-8",
    )
    return manifest


def events_by_id(extraction) -> dict[str, object]:
    return {item.id: item for item in extraction.events}


def identities(interactions) -> set[str]:
    return {item.identity for item in interactions}


# --------------------------------------------------------------------------------------
# Identity normalization and scope
# --------------------------------------------------------------------------------------


def test_event_ids_follow_the_documented_shape() -> None:
    assert event_id("ftgo", "order.create") == "event.ftgo.rabbitmq.order.create"
    assert event_id("ftgo", "user.profile.get_info") == "event.ftgo.rabbitmq.user.profile.get-info"


def test_event_ids_are_byte_stable_and_case_insensitive() -> None:
    assert event_id("ftgo", "Order.Create") == event_id("ftgo", "order.create")
    first = event_id("ftgo", "a.b")
    assert first == event_id("ftgo", "a.b")


def test_identity_normalization_collapses_separators_per_segment() -> None:
    assert normalize_identity("order.get_details") == "order.get-details"
    assert normalize_identity("driver.availability.available") == "driver.availability.available"


def test_amqp_credentials_are_redacted() -> None:
    redacted = redact_amqp("amqp://rabbitmq_user:hunter2-broker-secret@rabbitmq:5672/")
    assert "hunter2-broker-secret" not in redacted
    assert redacted == "amqp://[redacted]@rabbitmq:5672/"
    assert redact_amqp("amqp://rabbitmq:5672/") == "amqp://rabbitmq:5672/"


def test_only_service_src_python_files_are_in_scope() -> None:
    assert skip_reason("backend/gateway/src/services/order.py") is None
    assert skip_reason("backend/microservices/order/src/events.py") is None
    assert "not a Python source file" in skip_reason("backend/gateway/Dockerfile")
    # Sibling trees of ``src`` are out of scope before any other rule applies.
    assert "src" in skip_reason("backend/microservices/order/tests/test_events.py")
    assert "src" in skip_reason("backend/microservices/order/migrations/env.py")
    assert "src" in skip_reason("backend/gateway/setup.py")
    # Excluded and test trees nested *inside* src are rejected by name.
    assert "test directory" in skip_reason("backend/gateway/src/tests/test_events.py")
    assert "excluded directory" in skip_reason("backend/gateway/src/migrations/env.py")
    assert "excluded directory" in skip_reason("backend/gateway/src/__pycache__/events.py")
    assert "test module" in skip_reason("backend/gateway/src/services/test_order.py")
    assert "generated module" in skip_reason("backend/gateway/src/api_pb2.py")
    assert skip_reason("ui/src/app.py") is not None


# --------------------------------------------------------------------------------------
# Static analysis guarantees
# --------------------------------------------------------------------------------------


def test_no_fixture_module_is_ever_imported(extraction) -> None:
    # The fixture contains a module that raises on import; extraction still succeeded.
    assert "backend/gateway/src/services/booby_trap.py" in extraction.source_files
    for module_name in ("services.order", "services.base", "data_access.broker", "events"):
        assert module_name not in sys.modules


def test_report_records_zero_imports_executions_and_connections(extraction) -> None:
    _, report = render_bundle(extraction)

    assert report["analysis"] == "python-ast"
    assert report["modules_imported"] == 0
    assert report["modules_executed"] == 0
    assert report["broker_connections_opened"] == 0
    assert report["graph_mutations"] == 0
    assert report["neo4j_mutations"] == 0
    assert report["wiki_writes"] == 0
    assert report["graphiti"] == "disabled"


# --------------------------------------------------------------------------------------
# Broker rooting
# --------------------------------------------------------------------------------------


def test_broker_library_is_detected_from_imports(extraction) -> None:
    assert extraction.broker_libraries == ("rabbitmq_rpc",)


def test_local_wrapper_is_traced_to_the_broker_library(extraction) -> None:
    wrappers = {wrapper.symbol: wrapper for wrapper in extraction.wrappers}

    assert "services.base.Microservice._call_rpc" in wrappers
    wrapper = wrappers["services.base.Microservice._call_rpc"]
    assert wrapper.direction == "PUBLISHES"
    assert wrapper.operation == "call"
    assert wrapper.library == "rabbitmq_rpc"
    # The identity is the wrapper's first parameter after the implicit ``cls``.
    assert wrapper.parameter_name == "event_name"
    assert wrapper.parameter_index == 0
    assert wrapper.hops == 1


def test_generic_publish_and_subscribe_methods_are_rejected(extraction) -> None:
    # EmailSender.publish, EmailSender.send, InMemoryBus.subscribe and
    # InMemoryBus.register_event are not broker-rooted, so nothing may be reported.
    all_identities = identities(extraction.publisher_calls) | identities(
        extraction.consumer_bindings
    )
    assert not any(identity.startswith("email.") for identity in all_identities)
    assert not any("email" in item.id for item in extraction.events)
    assert not any(
        "notifications" in item.provenance.source_path for item in extraction.unresolved_identifiers
    )
    assert not any(
        wrapper.symbol.startswith("services.notifications") for wrapper in extraction.wrappers
    )


def test_broker_construction_is_not_mistaken_for_an_interaction(extraction) -> None:
    # RPCClient.create / RabbitMQConfig(...) set the client up; they publish nothing.
    assert not any(
        "data_access/broker.py" in item.provenance.source_path
        for item in extraction.publisher_calls
    )
    assert not any(
        "data_access/broker.py" in item.provenance.source_path
        for item in extraction.consumer_bindings
    )


def test_wrapper_forwarding_call_is_not_reported_as_unresolved(extraction) -> None:
    # ``rpc_client.call(event_name, ...)`` inside the wrapper is bookkeeping: its identity
    # belongs to each caller, so it must not appear as an unresolved interaction.
    assert not any(
        item.provenance.source_path.endswith("services/base.py")
        for item in extraction.unresolved_identifiers
    )


# --------------------------------------------------------------------------------------
# Publisher extraction
# --------------------------------------------------------------------------------------


def test_publishers_are_extracted_through_the_inherited_wrapper(extraction) -> None:
    published = identities(extraction.publisher_calls)

    assert published == {
        "order.create",
        "order.cancel",
        "order.get_details",
        "order.status.change",
        "order.archive",
    }
    assert all(item.service == "gateway" for item in extraction.publisher_calls)
    assert all(item.role == "publisher" for item in extraction.publisher_calls)
    assert all(item.mechanism == "rpc" for item in extraction.publisher_calls)
    assert all(
        item.via_wrapper == "services.base.Microservice._call_rpc"
        for item in extraction.publisher_calls
    )


def test_publisher_provenance_points_at_the_application_call_site(extraction) -> None:
    call = next(item for item in extraction.publisher_calls if item.identity == "order.create")

    assert call.provenance.source_path == "backend/gateway/src/services/order.py"
    assert call.provenance.symbol == "services.order.OrderService.create_order"
    assert call.provenance.repository == "ftgo"
    assert call.provenance.commit == FROZEN_COMMIT
    assert call.provenance.evidence_type == "implemented"
    assert call.provenance.line_start is not None
    assert "order.create" in (call.call_expression or "")


def test_identity_sources_are_recorded_for_each_resolution_kind(extraction) -> None:
    sources = {item.identity: item.identity_source for item in extraction.publisher_calls}

    assert sources["order.create"] == "literal"
    assert sources["order.cancel"] == "imported_constant"
    assert sources["order.get_details"] == "enum_member"
    assert sources["order.status.change"] == "enum_member"
    assert sources["order.archive"] == "concatenation"


def test_module_and_imported_string_constants_resolve(extraction) -> None:
    assert "order.cancel" in identities(extraction.publisher_calls)
    assert "order.archive" in identities(extraction.publisher_calls)


def test_enum_string_members_resolve_with_and_without_dot_value(extraction) -> None:
    assert "order.get_details" in identities(extraction.publisher_calls)
    assert "order.status.change" in identities(extraction.publisher_calls)


def test_dynamic_identifier_is_reported_unresolved_and_never_guessed(extraction) -> None:
    assert len(extraction.unresolved_identifiers) == 1
    unresolved = extraction.unresolved_identifiers[0]

    assert unresolved.service == "gateway"
    assert unresolved.role == "publisher"
    assert unresolved.operation == "call"
    assert unresolved.library == "rabbitmq_rpc"
    assert "build_event(action)" in (unresolved.expression or "")
    assert "call" in unresolved.reason or "statically" in unresolved.reason
    assert unresolved.provenance.symbol == "services.order.OrderService.dynamic_order"
    # No event was invented for it.
    assert not any("dynamic" in item.id for item in extraction.events)


# --------------------------------------------------------------------------------------
# Consumer extraction
# --------------------------------------------------------------------------------------


def test_consumers_are_extracted_from_the_literal_handler_map(extraction) -> None:
    consumed = identities(extraction.consumer_bindings)

    assert consumed == {
        "order.create",
        "order.cancel",
        "order.get_details",
        "order.status.change",
        "order.delivery.driver_found",
    }
    assert all(item.service == "order" for item in extraction.consumer_bindings)
    assert all(item.role == "consumer" for item in extraction.consumer_bindings)
    assert all(item.identity_source == "iteration" for item in extraction.consumer_bindings)
    assert all(item.operation == "register_event" for item in extraction.consumer_bindings)


def test_consumer_binding_records_the_paired_handler(extraction) -> None:
    handlers = {item.identity: item.handler for item in extraction.consumer_bindings}

    assert handlers["order.create"] == "OrderService.create_order"
    assert handlers["order.delivery.driver_found"] == "OrderService.assign_driver"


def test_consumer_provenance_points_at_the_registration_site(extraction) -> None:
    binding = next(item for item in extraction.consumer_bindings if item.identity == "order.create")

    assert binding.provenance.source_path == "backend/microservices/order/src/events.py"
    assert binding.provenance.symbol == "events.register_events"
    assert binding.provenance.commit == FROZEN_COMMIT
    assert "register_event" in (binding.call_expression or "")


# --------------------------------------------------------------------------------------
# Correlation
# --------------------------------------------------------------------------------------


def test_publisher_and_consumer_share_one_event_identity(extraction) -> None:
    events = events_by_id(extraction)
    matched = events[EVENT_CREATE]

    assert matched.status == "matched"
    assert matched.publishers == ("service.ftgo.gateway",)
    assert matched.consumers == ("service.ftgo.order",)
    assert matched.identity == "order.create"


def test_all_four_shared_identities_are_matched(extraction) -> None:
    matched = {item.id for item in extraction.events if item.status == "matched"}

    assert matched == {EVENT_CREATE, EVENT_CANCEL, EVENT_DETAILS, EVENT_STATUS}


def test_publisher_only_interaction_is_recorded_without_inventing_a_consumer(extraction) -> None:
    event = events_by_id(extraction)[EVENT_ARCHIVE]

    assert event.status == "publisher_only"
    assert event.publishers == ("service.ftgo.gateway",)
    assert event.consumers == ()
    assert not any(
        item.type == "CONSUMES" and item.target == EVENT_ARCHIVE
        for item in extraction.relationships
    )


def test_consumer_only_interaction_is_recorded_without_inventing_a_publisher(extraction) -> None:
    event = events_by_id(extraction)[EVENT_DRIVER_FOUND]

    assert event.status == "consumer_only"
    assert event.consumers == ("service.ftgo.order",)
    assert event.publishers == ()
    assert not any(
        item.type == "PUBLISHES" and item.target == EVENT_DRIVER_FOUND
        for item in extraction.relationships
    )


def test_correlation_is_exact_and_never_by_similar_name(tmp_path: Path) -> None:
    # ``order.get_details`` is consumed but the publisher says ``order.get`` instead. A
    # near-match must stay two unmatched sides, not one matched interaction.
    files = dict(FIXTURE_FILES)
    files["backend/gateway/src/services/order.py"] = GATEWAY_ORDER_SERVICE.replace(
        'ORDER_GET_DETAILS = "order.get_details"', 'ORDER_GET_DETAILS = "order.get"'
    )
    files["backend/gateway/src/config/events.py"] = GATEWAY_EVENT_CONSTANTS.replace(
        'ORDER_GET_DETAILS = "order.get_details"', 'ORDER_GET_DETAILS = "order.get"'
    )
    result = extract_rabbitmq(
        make_record(build_repository(tmp_path / "repo", files)), FROZEN_COMMIT
    )

    statuses = {item.identity: item.status for item in result.events}
    assert statuses["order.get"] == "publisher_only"
    assert statuses["order.get_details"] == "consumer_only"


def test_event_counts_are_exactly_the_proven_interactions(extraction) -> None:
    assert len(extraction.events) == 6
    assert len(extraction.publisher_calls) == 5
    assert len(extraction.consumer_bindings) == 5
    assert len([item for item in extraction.events if item.status == "matched"]) == 4
    assert len([item for item in extraction.events if item.status == "publisher_only"]) == 1
    assert len([item for item in extraction.events if item.status == "consumer_only"]) == 1


# --------------------------------------------------------------------------------------
# Relationships and ontology scope
# --------------------------------------------------------------------------------------


def test_only_publishes_and_consumes_relationships_are_created(extraction) -> None:
    document = yaml.safe_load(
        (AIDE_ROOT / "ontology/relationship-types.yaml").read_text(encoding="utf-8")
    )
    allowed = {item["type"] for item in document["relationship_types"]}
    emitted = {item.type for item in extraction.relationships}

    assert emitted <= allowed
    assert emitted == {"PUBLISHES", "CONSUMES"}
    assert not emitted & {"CALLS", "DEPENDS_ON", "READS", "WRITES", "USES_SCHEMA"}


def test_only_event_entities_are_emitted(extraction) -> None:
    allowed = set(
        yaml.safe_load((AIDE_ROOT / "ontology/entity-types.yaml").read_text(encoding="utf-8"))[
            "entity_types"
        ]
    )
    emitted = {item.kind for item in extraction.events}

    assert emitted <= allowed
    assert emitted == {"Event"}


def test_relationships_connect_existing_services_to_events(extraction) -> None:
    known_events = {item.id for item in extraction.events}

    assert extraction.relationships
    for relation in extraction.relationships:
        assert relation.source in PASS_ONE_SERVICE_IDS
        assert relation.target in known_events
        assert relation.provenance.commit == FROZEN_COMMIT
        assert relation.provenance.evidence_type == "implemented"
        assert relation.provenance.source_path.endswith(".py")
        assert relation.provenance.line_start is not None


def test_service_ownership_comes_from_the_source_path(extraction) -> None:
    scans = {scan.slug: scan for scan in extraction.services_scanned}

    assert set(scans) == {"gateway", "order", "restaurant"}
    assert scans["gateway"].entity_id == "service.ftgo.gateway"
    assert scans["gateway"].publisher_calls == 5
    assert scans["gateway"].consumer_bindings == 0
    assert scans["order"].entity_id == "service.ftgo.order"
    assert scans["order"].consumer_bindings == 5
    assert scans["order"].publisher_calls == 0
    # A scanned service with no broker usage is reported, not omitted.
    assert scans["restaurant"].publisher_calls == 0
    assert scans["restaurant"].consumer_bindings == 0
    assert any("no broker-rooted" in warning for warning in extraction.warnings)


def test_out_of_scope_trees_never_contribute(extraction) -> None:
    joined = " ".join(extraction.source_files)

    assert "tests/" not in joined
    assert "migrations/" not in joined
    assert not any("tests" in item.provenance.source_path for item in extraction.consumer_bindings)


# --------------------------------------------------------------------------------------
# aio_pika, module-level usage, and identity collisions
# --------------------------------------------------------------------------------------

AIO_PIKA_MODULE = """\
import aio_pika

QUEUE_NAME = "driver.location.submit"
DRIVER_EXCHANGE = "drivers"


def build_key(value):
    return value


async def bind() -> None:
    connection = await aio_pika.connect_robust(
        "amqp://rabbitmq_user:hunter2-broker-secret@rabbitmq:5672/"
    )
    channel = await connection.channel()
    await channel.basic_consume(queue=QUEUE_NAME)
    await channel.basic_publish(
        exchange=DRIVER_EXCHANGE,
        routing_key="driver.status.online",
    )
    await channel.basic_publish(
        exchange=DRIVER_EXCHANGE,
        routing_key=build_key("amqp://rabbitmq_user:hunter2-broker-secret@rabbitmq:5672/"),
    )
"""


def test_aio_pika_operations_are_rooted_and_composed(tmp_path: Path) -> None:
    files = {"backend/microservices/location/src/bindings.py": AIO_PIKA_MODULE}
    result = extract_rabbitmq(
        make_record(build_repository(tmp_path / "repo", files)), FROZEN_COMMIT
    )

    assert result.broker_libraries == ("aio_pika",)
    assert identities(result.consumer_bindings) == {"driver.location.submit"}
    assert identities(result.publisher_calls) == {"drivers.driver.status.online"}
    publisher = result.publisher_calls[0]
    assert publisher.exchange == "drivers"
    assert publisher.routing_key == "driver.status.online"
    assert publisher.mechanism == "message"
    assert publisher.service == "location"
    consumer = result.consumer_bindings[0]
    assert consumer.queue == "driver.location.submit"


def test_amqp_credentials_never_reach_the_output(tmp_path: Path) -> None:
    files = {"backend/microservices/location/src/bindings.py": AIO_PIKA_MODULE}
    result = extract_rabbitmq(
        make_record(build_repository(tmp_path / "repo", files)), FROZEN_COMMIT
    )
    rendered, report = render_bundle(result)
    blob = "\n".join(rendered.values()) + json.dumps(report)

    # The unresolved routing key embeds an AMQP URL; it must be redacted, not dropped.
    assert len(result.unresolved_identifiers) == 1
    assert "hunter2-broker-secret" not in blob
    assert "[redacted]" in json.dumps(report)
    assert report["secret_values_emitted"] == 0


MODULE_LEVEL_PUBLISHER = """\
from rabbitmq_rpc import RPCClient

client = RPCClient()
client.publish("order.created")
"""


def test_module_level_broker_calls_are_extracted(tmp_path: Path) -> None:
    files = {"backend/gateway/src/bootstrap.py": MODULE_LEVEL_PUBLISHER}
    result = extract_rabbitmq(
        make_record(build_repository(tmp_path / "repo", files)), FROZEN_COMMIT
    )

    assert identities(result.publisher_calls) == {"order.created"}
    assert result.publisher_calls[0].provenance.symbol == "bootstrap"


COLLIDING_MODULE = """\
from rabbitmq_rpc import RPCClient

client = RPCClient()
client.publish("order.create")
client.publish("Order.Create")
"""


def test_identity_collision_is_reported_and_no_event_is_created(tmp_path: Path) -> None:
    files = {"backend/gateway/src/collide.py": COLLIDING_MODULE}
    result = extract_rabbitmq(
        make_record(build_repository(tmp_path / "repo", files)), FROZEN_COMMIT
    )

    assert len(result.identity_collisions) == 1
    collision = result.identity_collisions[0]
    assert collision.event_id == EVENT_CREATE
    assert collision.raw_identities == ("Order.Create", "order.create")
    assert len(collision.sites) == 2
    # Nothing was guessed: neither the event nor its relationships exist.
    assert result.events == ()
    assert result.relationships == ()


# --------------------------------------------------------------------------------------
# Rendering, deltas, and report
# --------------------------------------------------------------------------------------


def test_event_candidates_are_never_approved(extraction) -> None:
    rendered, _ = render_bundle(extraction)

    assert len(rendered) == len(extraction.events)
    for path, content in rendered.items():
        frontmatter = yaml.safe_load(content.split("---")[1])
        assert frontmatter["status"] == "candidate"
        assert frontmatter["review_status"] == "pending"
        assert frontmatter["kind"] == frontmatter["type"] == "Event"
        assert "status: approved" not in content
        assert path.startswith("events/")


def test_event_page_shows_verified_publishers_and_consumers(extraction) -> None:
    rendered, _ = render_bundle(extraction)
    content = rendered[f"events/{EVENT_CREATE}.md"]
    frontmatter = yaml.safe_load(content.split("---")[1])

    assert frontmatter["publishers"] == ["service.ftgo.gateway"]
    assert frontmatter["consumers"] == ["service.ftgo.order"]
    inbound = {(item["type"], item["source"]) for item in frontmatter["inbound_relations"]}
    assert inbound == {
        ("PUBLISHES", "service.ftgo.gateway"),
        ("CONSUMES", "service.ftgo.order"),
    }
    assert FROZEN_COMMIT in content


def test_no_service_candidate_pages_are_written(extraction) -> None:
    rendered, _ = render_bundle(extraction)

    assert all(path.startswith("events/") for path in rendered)
    assert not any("service.ftgo" in path for path in rendered)


def test_service_relation_deltas_hold_the_outgoing_relations(extraction) -> None:
    deltas = build_service_relation_deltas(extraction)

    assert deltas["status"] == "candidate"
    assert deltas["review_status"] == "pending"
    assert "not canonical knowledge" in deltas["note"]
    by_service = {item["service"]: item for item in deltas["services"]}
    assert set(by_service) == {"service.ftgo.gateway", "service.ftgo.order"}
    gateway_types = {item["type"] for item in by_service["service.ftgo.gateway"]["relations"]}
    order_types = {item["type"] for item in by_service["service.ftgo.order"]["relations"]}
    assert gateway_types == {"PUBLISHES"}
    assert order_types == {"CONSUMES"}
    total = sum(item["relation_count"] for item in deltas["services"])
    assert total == len(extraction.relationships)


def test_report_contains_the_required_fields(extraction) -> None:
    _, report = render_bundle(extraction)

    for key in (
        "repository",
        "commit",
        "commit_verified",
        "analysis",
        "modules_imported",
        "modules_executed",
        "source_files",
        "services_scanned",
        "broker_libraries_detected",
        "publisher_calls",
        "consumer_bindings",
        "events",
        "matched_interactions",
        "publisher_only",
        "consumer_only",
        "relationships",
        "identity_collisions",
        "unresolved_identifiers",
        "warnings",
        "secret_values_emitted",
        "graph_mutations",
        "wiki_writes",
        "neo4j_mutations",
        "graphiti",
    ):
        assert key in report, f"missing report key {key!r}"
    assert report["commit"] == FROZEN_COMMIT
    assert report["counts"]["matched_interactions"] == 4


def test_credential_names_exempt_broker_and_cache_vocabulary() -> None:
    # Credentials.
    assert is_credential_name("password")
    assert is_credential_name("RABBITMQ_PASS")
    assert is_credential_name("TOKEN_SECRET_KEY")
    assert is_credential_name("api_key")
    # Broker topology, not credentials: these are the subject of this pass.
    assert not is_credential_name("routing_key")
    assert not is_credential_name("queue")
    assert not is_credential_name("exchange")
    assert not is_credential_name("event")
    # A bare cache key is not a credential either.
    assert not is_credential_name("DRIVER_STATUS_KEY")
    assert not is_credential_name("cache_key")


def test_leak_scan_matches_whole_tokens_not_substrings(extraction) -> None:
    # A credential value that merely occurs inside a longer identifier has not leaked.
    # FTGO's cache value ``driver_status`` sits inside the handler name ``get_driver_status``,
    # and ``secret`` sits inside this report's own ``secret_values_emitted`` field.
    assert count_secret_leaks(extraction, {"a": "def get_driver_status(self):"}) == 0
    assert count_secret_leaks(extraction, {"a": '"secret_values_emitted": 0'}) == 0
    # A standalone emission is a real leak and must be counted.
    leaked = {"a": "password: rabbitmq_password\n"}
    assert count_secret_leaks(extraction, leaked) == 1


def test_broker_credentials_are_never_emitted(extraction) -> None:
    rendered, report = render_bundle(extraction)
    blob = "\n".join(rendered.values()) + json.dumps(report)

    for secret in FIXTURE_SECRETS:
        assert secret not in blob, f"secret {secret!r} leaked into candidate output"
    assert report["secret_values_emitted"] == 0


# --------------------------------------------------------------------------------------
# CLI behavior: dry-run, commit gate, determinism
# --------------------------------------------------------------------------------------


def test_dry_run_writes_nothing(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    manifest = write_manifest(tmp_path, build_repository(tmp_path / "repo"))
    output_dir = tmp_path / "candidates"
    monkeypatch.setattr("knowledge_plane.extract.read_git_head", lambda path: FROZEN_COMMIT)

    summary = run("ftgo", "rabbitmq", manifest_path=manifest, output_dir=output_dir, dry_run=True)

    assert summary["status"] == "dry-run"
    assert summary["dry_run"] is True
    assert summary["commit"] == FROZEN_COMMIT
    assert summary["commit_verified"] is True
    assert summary["counts"]["events"] == 6
    assert summary["modules_imported"] == 0
    assert summary["modules_executed"] == 0
    assert summary["broker_connections_opened"] == 0
    assert summary["secret_values_emitted"] == 0
    assert summary["graph_mutations"] == 0
    assert summary["wiki_writes"] == 0
    assert summary["neo4j_mutations"] == 0
    assert summary["graphiti"] == "disabled"
    # Zero filesystem candidate changes, including the sidecar.
    assert not output_dir.exists()


def test_commit_mismatch_aborts_before_writing_anything(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    manifest = write_manifest(tmp_path, build_repository(tmp_path / "repo"))
    output_dir = tmp_path / "candidates"
    monkeypatch.setattr("knowledge_plane.extract.read_git_head", lambda path: WRONG_COMMIT)

    with pytest.raises(CommitMismatchError) as excinfo:
        run("ftgo", "rabbitmq", manifest_path=manifest, output_dir=output_dir, dry_run=False)

    assert excinfo.value.expected == FROZEN_COMMIT
    assert excinfo.value.actual == WRONG_COMMIT
    assert not output_dir.exists()


def test_expected_output_structure_is_written(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    manifest = write_manifest(tmp_path, build_repository(tmp_path / "repo"))
    output_dir = tmp_path / "candidates"
    monkeypatch.setattr("knowledge_plane.extract.read_git_head", lambda path: FROZEN_COMMIT)

    summary = run("ftgo", "rabbitmq", manifest_path=manifest, output_dir=output_dir)

    assert summary["status"] == "ok"
    assert (output_dir / "extraction-report.json").is_file()
    assert (output_dir / DELTAS_FILENAME).is_file()
    assert len(list((output_dir / "events").glob("*.md"))) == 6

    report = json.loads((output_dir / "extraction-report.json").read_text(encoding="utf-8"))
    assert report["commit"] == FROZEN_COMMIT
    assert report["secret_values_emitted"] == 0
    assert report["graph_mutations"] == 0

    deltas = json.loads((output_dir / DELTAS_FILENAME).read_text(encoding="utf-8"))
    assert {item["service"] for item in deltas["services"]} == {
        "service.ftgo.gateway",
        "service.ftgo.order",
    }


def test_repeat_extraction_is_byte_identical(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    manifest = write_manifest(tmp_path, build_repository(tmp_path / "repo"))
    monkeypatch.setattr("knowledge_plane.extract.read_git_head", lambda path: FROZEN_COMMIT)
    first = tmp_path / "run-one"
    second = tmp_path / "run-two"

    run("ftgo", "rabbitmq", manifest_path=manifest, output_dir=first)
    run("ftgo", "rabbitmq", manifest_path=manifest, output_dir=second)

    first_files = sorted(path.relative_to(first) for path in first.rglob("*") if path.is_file())
    second_files = sorted(path.relative_to(second) for path in second.rglob("*") if path.is_file())
    assert first_files == second_files
    assert first_files, "extraction produced no files"
    for relative_path in first_files:
        assert (first / relative_path).read_bytes() == (second / relative_path).read_bytes(), (
            f"{relative_path} differs between runs"
        )


def test_rerun_prunes_orphans_and_leaves_sibling_passes_alone(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    manifest = write_manifest(tmp_path, build_repository(tmp_path / "repo"))
    monkeypatch.setattr("knowledge_plane.extract.read_git_head", lambda path: FROZEN_COMMIT)
    output_dir = tmp_path / "candidates"

    run("ftgo", "rabbitmq", manifest_path=manifest, output_dir=output_dir)
    orphan = output_dir / "events" / "event.ftgo.rabbitmq.retired.md"
    orphan.write_text("stale", encoding="utf-8")
    foreign = output_dir / "services" / "service.ftgo.gateway.md"
    foreign.parent.mkdir(parents=True, exist_ok=True)
    foreign.write_text("owned by the compose pass", encoding="utf-8")

    run("ftgo", "rabbitmq", manifest_path=manifest, output_dir=output_dir)

    assert not orphan.exists()
    assert foreign.read_text(encoding="utf-8") == "owned by the compose pass"


# --------------------------------------------------------------------------------------
# Opt-in verification against the real frozen FTGO checkout
# --------------------------------------------------------------------------------------


def _real_ftgo_record() -> RepositoryRecord | None:
    try:
        records = load_repository_manifest(AIDE_ROOT / DEFAULT_MANIFEST_RELATIVE_PATH)
    except Exception:  # pragma: no cover - manifest problems are covered elsewhere
        return None
    record = records.get("ftgo")
    if record is None or not record.path.is_dir():
        return None
    try:
        if read_git_head(record.path) != FROZEN_COMMIT:
            return None
    except Exception:  # pragma: no cover - git absent or repository unreadable
        return None
    return record


@pytest.fixture(scope="module")
def real_extraction():
    record = _real_ftgo_record()
    if record is None:
        pytest.skip("FTGO checkout at the frozen commit is not available")
    return extract_rabbitmq(record, FROZEN_COMMIT)


def test_real_ftgo_uses_rabbitmq_rpc_only(real_extraction) -> None:
    assert real_extraction.broker_libraries == ("rabbitmq_rpc",)
    assert real_extraction.identity_collisions == ()


def test_real_ftgo_gateway_is_the_only_publisher(real_extraction) -> None:
    publishing = {item.service for item in real_extraction.publisher_calls}
    consuming = {item.service for item in real_extraction.consumer_bindings}

    assert publishing == {"gateway"}
    assert consuming == {"user", "order", "restaurant", "location", "feedback"}
    scanned = {scan.entity_id for scan in real_extraction.services_scanned}
    assert scanned == PASS_ONE_SERVICE_IDS


def test_real_ftgo_wrapper_tracing_finds_the_gateway_rpc_helper(real_extraction) -> None:
    symbols = {wrapper.symbol for wrapper in real_extraction.wrappers}

    assert "services.base.Microservice._call_rpc" in symbols
    wrapper = next(item for item in real_extraction.wrappers if item.symbol.endswith("._call_rpc"))
    assert wrapper.direction == "PUBLISHES"
    assert wrapper.operation == "call"
    assert wrapper.hops == 1


def test_real_ftgo_cross_service_paths_are_established(real_extraction) -> None:
    events = {item.id: item for item in real_extraction.events}
    create = events["event.ftgo.rabbitmq.order.create"]

    assert create.status == "matched"
    assert create.publishers == ("service.ftgo.gateway",)
    assert create.consumers == ("service.ftgo.order",)

    login = events["event.ftgo.rabbitmq.user.profile.login"]
    assert login.publishers == ("service.ftgo.gateway",)
    assert login.consumers == ("service.ftgo.user",)


def test_real_ftgo_naming_drift_is_surfaced_not_hidden(real_extraction) -> None:
    statuses = {item.identity: item.status for item in real_extraction.events}

    # The gateway asks for ``delivery.rating.get`` but feedback registers
    # ``delivery.rating.get_details``. Exact correlation keeps both sides visible.
    assert statuses["delivery.rating.get"] == "publisher_only"
    assert statuses["delivery.rating.get_details"] == "consumer_only"
    assert statuses["order.rating.get"] == "publisher_only"
    assert statuses["order.rating.get_details"] == "consumer_only"
    # order.history is published by the gateway; its handler is commented out.
    assert statuses["order.history"] == "publisher_only"


def test_real_ftgo_relationships_are_in_scope(real_extraction) -> None:
    known = {item.id for item in real_extraction.events}

    assert {item.type for item in real_extraction.relationships} == {"PUBLISHES", "CONSUMES"}
    for relation in real_extraction.relationships:
        assert relation.source in PASS_ONE_SERVICE_IDS
        assert relation.target in known


def test_real_ftgo_emits_no_secret_values(real_extraction) -> None:
    rendered, report = render_bundle(real_extraction)
    blob = "\n".join(rendered.values()) + json.dumps(report)

    assert report["secret_values_emitted"] == 0
    assert "rabbitmq_password" not in blob
    assert report["graph_mutations"] == 0


def test_real_ftgo_extraction_is_deterministic(real_extraction) -> None:
    record = _real_ftgo_record()
    assert record is not None
    repeated = extract_rabbitmq(record, FROZEN_COMMIT)

    first, _ = render_bundle(real_extraction)
    second, _ = render_bundle(repeated)
    assert first.keys() == second.keys()
    for key in first:
        assert first[key] == second[key], f"{key} differs between identical runs"
