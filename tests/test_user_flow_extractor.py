"""Deterministic tests for the user-flow / execution-path extractor (Graph Engineering Pass 5).

The fixture is a synthetic repository shaped like FTGO end to end: a FastAPI gateway whose
handlers reach an RPC publisher through inherited wrappers, a microservice that registers the
matching consumer from a literal handler map, and a domain layer that reaches a Beanie
document and a SQLAlchemy table. It also contains the cases that must *not* stitch: an
endpoint whose handler publishes nothing, a published identity nobody consumes, a consumer
whose persistence hop is one call too deep, and a handler-shaped name that only looks like a
publisher. Opt-in tests at the end assert the same guarantees against the real frozen FTGO
checkout, including the order-create path end to end.
"""

from __future__ import annotations

import ast
import json
import sys
from pathlib import Path

import pytest
import yaml

from knowledge_plane.extract import run
from knowledge_plane.extractors.user_flow import (
    COMPLETENESS_PARTIAL,
    COMPLETENESS_RESOLVED,
    COMPLETENESS_TRIVIAL,
    CONTAINS,
    DERIVED_FROM,
    ENUMERATED_RESOLUTION,
    IMPLEMENTS,
    PARTICIPATES_IN,
    PRECEDES,
    SERVICE_DELTAS_FILENAME,
    UNRESOLVED_CONSUMER,
    UNRESOLVED_DISPATCH,
    UNRESOLVED_PERSISTENCE,
    CalleeResolver,
    RelationshipCandidate,
    _detect_cycles,
    _returns_own_instance,
    _unwrap_optional,
    analyze_module,
    build_service_relation_deltas,
    build_source_index,
    count_secret_leaks,
    extract_user_flow,
    flow_id,
    is_sensitive_name,
    local_scope,
    redact_expression,
    render_bundle,
    skip_reason,
    step_id,
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

# The six application services approved in Pass 1. Pass 5 reuses them and adds none.
PASS_ONE_SERVICE_IDS = {
    "service.ftgo.gateway",
    "service.ftgo.user",
    "service.ftgo.restaurant",
    "service.ftgo.location",
    "service.ftgo.order",
    "service.ftgo.feedback",
}

# Credential values present in the fixture. None may appear in generated output.
FIXTURE_SECRETS = ("rabbitmq_password", "fixture_pg_password", "fixture_mongo_password")

# --------------------------------------------------------------------------------------
# Fixture: gateway HTTP surface
# --------------------------------------------------------------------------------------

GATEWAY_MAIN = '''\
from fastapi import FastAPI

from application.app import init_router

app = FastAPI(title="Fixture Gateway")
app.include_router(init_router(), prefix="/api")
'''

GATEWAY_APP = '''\
from fastapi import APIRouter

from application.routes.order import router as order_router


def init_router() -> APIRouter:
    router = APIRouter()
    router.include_router(order_router)
    return router
'''

# Every handler below is a deliberate case:
#   create_order   depth-1 call to a proven publisher, persistence proven end to end
#   deep_order     depth-2 call to the same publisher through a helper
#   cancel_order   publishes an identity that nobody consumes
#   archive_order  publishes and is consumed, but the write is one hop past the bound
#   report_order   handler-shaped local call that never reaches a publisher
GATEWAY_ORDER_ROUTES = '''\
from fastapi import APIRouter, Request

from application.schemas.order import CreateOrderRequest
from services.order import OrderService

router = APIRouter(prefix="/orders", tags=["orders"])


def dispatch_create(data):
    return OrderService.create_order(data=data)


@router.post("/create")
async def create_order(request: Request, payload: CreateOrderRequest):
    data = {"customer_id": payload.customer_id}
    response = await OrderService.create_order(data=data)
    return {"status": response.get("status"), "code": response.pop("error_code", None)}


@router.post("/deep")
async def deep_order(request: Request, payload: CreateOrderRequest):
    data = {"customer_id": payload.customer_id}
    return await dispatch_create(data)


@router.post("/cancel")
async def cancel_order(request: Request, payload: CreateOrderRequest):
    return await OrderService.cancel_order(data={"id": payload.customer_id})


@router.post("/archive")
async def archive_order(request: Request, payload: CreateOrderRequest):
    return await OrderService.archive_order(data={"id": payload.customer_id})


@router.post("/report")
async def report_order(request: Request, payload: CreateOrderRequest):
    summary = Reporter().publish("order.report", payload={})
    return summary


class Reporter:
    def publish(self, event_name, payload=None):
        return None
'''

GATEWAY_SCHEMAS_ORDER = '''\
from pydantic import BaseModel


class CreateOrderRequest(BaseModel):
    customer_id: str
'''

GATEWAY_BROKER = '''\
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
        cls._instance = cls(await RPCClient.create(config=config))

    @classmethod
    def get_client(cls) -> RPCClient:
        return cls._instance._rpc_client
'''

GATEWAY_SERVICE_BASE = '''\
from data_access.broker import RPCBroker


class Microservice:
    _service_name = ''

    @classmethod
    async def _call_rpc(cls, event_name, data):
        rpc_client = RPCBroker.get_client()
        return await rpc_client.call(event_name, data=data)
'''

GATEWAY_ORDER_SERVICE = '''\
from services.base import Microservice


class OrderService(Microservice):
    _service_name = 'order'

    @classmethod
    async def create_order(cls, data):
        return await cls._call_rpc('order.create', data=data)

    @classmethod
    async def cancel_order(cls, data):
        return await cls._call_rpc('order.cancel', data=data)

    @classmethod
    async def archive_order(cls, data):
        return await cls._call_rpc('order.archive', data=data)
'''

# --------------------------------------------------------------------------------------
# Fixture: order microservice (document persistence, proven end to end)
# --------------------------------------------------------------------------------------

ORDER_EVENTS = '''\
from application.order import OrderService
from data_access.broker import RPCBroker


async def register_events():
    rpc_client = RPCBroker.get_client()
    events_handlers = {
        'order.create': OrderService.create_order,
        'order.archive': OrderService.archive_order,
    }
    for event, handler in events_handlers.items():
        await rpc_client.register_event(event=event, handler=handler)
'''

ORDER_APPLICATION = '''\
from domain.order import OrderHandler


class OrderService:
    @classmethod
    async def create_order(cls, **kwargs):
        return await OrderHandler.create_order(**kwargs)

    @classmethod
    async def archive_order(cls, **kwargs):
        return await OrderHandler.archive_order(**kwargs)
'''

# ``create_order`` proves a read and a write at depth 2 from the consumer handler.
# ``archive_order`` needs four hops, one past the contract bound, so it must stay unresolved.
ORDER_DOMAIN = '''\
from domain.entities import Order


class OrderHandler:
    @classmethod
    async def create_order(cls, customer_id=None, **kwargs):
        existing = await Order.fetch(customer_id)
        order = Order.create(customer_id=customer_id)
        await order.save()
        return order or existing

    @classmethod
    async def archive_order(cls, order_id=None, **kwargs):
        return await cls.stage_one(order_id)

    @classmethod
    async def stage_one(cls, order_id):
        return await cls.stage_two(order_id)

    @classmethod
    async def stage_two(cls, order_id):
        order = Order.create(customer_id=order_id)
        return await order.save()
'''

ORDER_ENTITIES_INIT = "from domain.entities.order import Order\n"

ORDER_ENTITY_BASE = '''\
from beanie import Document


class BaseEntity:
    document_cls = None

    def __init__(self, document: Document):
        self.document: Document = document

    @classmethod
    async def fetch_document(cls, **kwargs):
        return await cls.document_cls.find_one(kwargs)
'''

ORDER_ENTITY = '''\
from domain.entities.base import BaseEntity
from models.order import Order as OrderDocument


class Order(BaseEntity):
    document_cls = OrderDocument

    def __init__(self, document: OrderDocument):
        super().__init__(document)

    @classmethod
    def create(cls, customer_id: str) -> "Order":
        return cls(document=OrderDocument(customer_id=customer_id))

    @classmethod
    async def fetch(cls, customer_id: str):
        return await OrderDocument.find_one(customer_id=customer_id)

    async def save(self):
        # ``insert_one`` is the Beanie operation Pass 4 already resolved to the collection.
        # ``setattr`` is a dynamic construct and must stay reported even in the same function.
        setattr(self.document, "saved", True)
        await OrderDocument.insert_one(self.document)
'''

ORDER_DOCUMENT = '''\
from beanie import Document
from pydantic import Field


class Order(Document):
    customer_id: str = Field(...)

    class Settings:
        name = "orders"
'''

# --------------------------------------------------------------------------------------
# Fixture: user microservice (relational read, proven end to end)
# --------------------------------------------------------------------------------------

USER_EVENTS = '''\
from application.profile import ProfileService
from data_access.broker import RPCBroker


async def register_events():
    rpc_client = RPCBroker.get_client()
    events_handlers = {
        'user.profile.get_info': ProfileService.get_info,
        'user.profile.opaque': ProfileService.opaque,
    }
    for event, handler in events_handlers.items():
        await rpc_client.register_event(event=event, handler=handler)
'''

USER_APPLICATION = '''\
from domain.profile import ProfileManager


class ProfileService:
    @classmethod
    async def get_info(cls, **kwargs):
        return await ProfileManager.load(**kwargs)

    @classmethod
    async def opaque(cls, handler=None, **kwargs):
        return await handler(**kwargs)
'''

USER_DOMAIN = '''\
from data_access.repository import DatabaseRepository
from data_access.models.profile import Profile


class ProfileManager:
    @staticmethod
    async def load(user_id=None, **kwargs):
        return await DatabaseRepository.fetch_profile(user_id)
'''

USER_REPOSITORY = '''\
from sqlalchemy.future import select

from asyncpg_client import AsyncPostgres
from data_access.models.profile import Profile


class DatabaseRepository:
    _data_access: AsyncPostgres = None

    @classmethod
    async def fetch_profile(cls, user_id):
        async with cls._data_access.get_or_create_session() as session:
            result = await session.execute(select(Profile).filter_by(id=user_id))
            return result.scalars().first()
'''

USER_MODEL_BASE = '''\
import sqlalchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    __abstract__ = True
    metadata = sqlalchemy.MetaData()

    id: Mapped[str] = mapped_column(sqlalchemy.String, primary_key=True)
'''

USER_MODEL = '''\
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from data_access.models.base import Base


class Profile(Base):
    __tablename__ = "user_profile"

    phone_number: Mapped[str] = mapped_column(String, nullable=False)
'''

# --------------------------------------------------------------------------------------
# Fixture: compose topology, so Pass 1 and Pass 4 have real evidence to correlate
# --------------------------------------------------------------------------------------

APP_COMPOSE = """\
services:
  gateway_service:
    build:
      context: ./gateway
    environment:
      - RABBITMQ_HOST=rabbitmq
  user_service:
    build:
      context: ./microservices/user
    environment:
      - POSTGRES_HOST=user_postgres
      - POSTGRES_PASSWORD=fixture_pg_password
  order_service:
    build:
      context: ./microservices/order
    environment:
      - MONGO_HOST=order_mongo
      - MONGO_PASSWORD=fixture_mongo_password
"""

INFRA_COMPOSE = """\
services:
  user_postgres:
    image: postgres:16.3
    hostname: "user_postgres"
  order_mongo:
    image: mongo:latest
    hostname: "order_mongo"
  rabbitmq:
    image: rabbitmq:3.13-management
    hostname: "rabbitmq"
"""

# Valid Python that would explode on import. Proof that nothing is ever imported.
BOOBY_TRAP = 'raise RuntimeError("this module must never be imported by the extractor")\n'

FIXTURE_FILES = {
    "backend/docker-compose.yaml": APP_COMPOSE,
    "backend/infra/docker-compose.yaml": INFRA_COMPOSE,
    # Gateway.
    "backend/gateway/src/__init__.py": "",
    "backend/gateway/src/main.py": GATEWAY_MAIN,
    "backend/gateway/src/application/__init__.py": "",
    "backend/gateway/src/application/app.py": GATEWAY_APP,
    "backend/gateway/src/application/routes/__init__.py": "",
    "backend/gateway/src/application/routes/order.py": GATEWAY_ORDER_ROUTES,
    "backend/gateway/src/application/schemas/__init__.py": "",
    "backend/gateway/src/application/schemas/order.py": GATEWAY_SCHEMAS_ORDER,
    "backend/gateway/src/data_access/__init__.py": "",
    "backend/gateway/src/data_access/broker.py": GATEWAY_BROKER,
    "backend/gateway/src/services/__init__.py": "",
    "backend/gateway/src/services/base.py": GATEWAY_SERVICE_BASE,
    "backend/gateway/src/services/order.py": GATEWAY_ORDER_SERVICE,
    "backend/gateway/src/services/booby_trap.py": BOOBY_TRAP,
    # Order microservice.
    "backend/microservices/order/src/__init__.py": "",
    "backend/microservices/order/src/events.py": ORDER_EVENTS,
    "backend/microservices/order/src/data_access/__init__.py": "",
    "backend/microservices/order/src/data_access/broker.py": GATEWAY_BROKER,
    "backend/microservices/order/src/application/__init__.py": "",
    "backend/microservices/order/src/application/order.py": ORDER_APPLICATION,
    "backend/microservices/order/src/domain/__init__.py": "",
    "backend/microservices/order/src/domain/order.py": ORDER_DOMAIN,
    "backend/microservices/order/src/domain/entities/__init__.py": ORDER_ENTITIES_INIT,
    "backend/microservices/order/src/domain/entities/base.py": ORDER_ENTITY_BASE,
    "backend/microservices/order/src/domain/entities/order.py": ORDER_ENTITY,
    "backend/microservices/order/src/models/__init__.py": "",
    "backend/microservices/order/src/models/order.py": ORDER_DOCUMENT,
    # User microservice.
    "backend/microservices/user/src/__init__.py": "",
    "backend/microservices/user/src/events.py": USER_EVENTS,
    "backend/microservices/user/src/data_access/__init__.py": "",
    "backend/microservices/user/src/data_access/broker.py": GATEWAY_BROKER,
    "backend/microservices/user/src/data_access/repository.py": USER_REPOSITORY,
    "backend/microservices/user/src/data_access/models/__init__.py": "",
    "backend/microservices/user/src/data_access/models/base.py": USER_MODEL_BASE,
    "backend/microservices/user/src/data_access/models/profile.py": USER_MODEL,
    "backend/microservices/user/src/application/__init__.py": "",
    "backend/microservices/user/src/application/profile.py": USER_APPLICATION,
    "backend/microservices/user/src/domain/__init__.py": "",
    "backend/microservices/user/src/domain/profile.py": USER_DOMAIN,
    # Out-of-scope trees that would stitch a flow if they were ever read.
    "backend/gateway/tests/test_routes.py": GATEWAY_ORDER_ROUTES,
    "backend/gateway/src/__pycache__/order.py": GATEWAY_ORDER_ROUTES,
    "backend/gateway/Dockerfile": "FROM python:3.12\n",
}

CREATE_ENDPOINT = "endpoint.ftgo.gateway.post.api.orders.create"
DEEP_ENDPOINT = "endpoint.ftgo.gateway.post.api.orders.deep"
CANCEL_ENDPOINT = "endpoint.ftgo.gateway.post.api.orders.cancel"
ARCHIVE_ENDPOINT = "endpoint.ftgo.gateway.post.api.orders.archive"
REPORT_ENDPOINT = "endpoint.ftgo.gateway.post.api.orders.report"

CREATE_FLOW = "flow.ftgo.gateway.post.api.orders.create"
DEEP_FLOW = "flow.ftgo.gateway.post.api.orders.deep"
CANCEL_FLOW = "flow.ftgo.gateway.post.api.orders.cancel"
ARCHIVE_FLOW = "flow.ftgo.gateway.post.api.orders.archive"
REPORT_FLOW = "flow.ftgo.gateway.post.api.orders.report"

EVENT_CREATE = "event.ftgo.rabbitmq.order.create"
EVENT_CANCEL = "event.ftgo.rabbitmq.order.cancel"
EVENT_ARCHIVE = "event.ftgo.rabbitmq.order.archive"
ORDERS_COLLECTION = "collection.ftgo.order.orders"
PUBLISHER_SYMBOL = "services.order.OrderService.create_order"

# --------------------------------------------------------------------------------------
# Sibling-method fixture: one service class, four methods, four different events.
#
# This is the shape that would expose a resolver that collapses sibling methods onto the
# first one declared in the class. Each handler calls exactly one method, each method
# publishes exactly one identity, and only two of the four identities have a consumer, so a
# collapse would show up either as a shared dispatch symbol, a shared event, or as
# ``create``'s consumer and persistence leaking into a sibling flow.
# --------------------------------------------------------------------------------------

SIBLING_ROUTES = '''\
from fastapi import APIRouter, Request

from application.schemas.order import CreateOrderRequest
from services.order import OrderService

router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("/create")
async def create_order(request: Request, payload: CreateOrderRequest):
    return await OrderService.create_order(data={"id": payload.customer_id})


@router.post("/update")
async def update_order(request: Request, payload: CreateOrderRequest):
    return await OrderService.update_order(data={"id": payload.customer_id})


@router.post("/confirm")
async def restaurant_confirm(request: Request, payload: CreateOrderRequest):
    return await OrderService.restaurant_confirm(data={"id": payload.customer_id})


@router.post("/reject")
async def restaurant_reject(request: Request, payload: CreateOrderRequest):
    return await OrderService.restaurant_reject(data={"id": payload.customer_id})
'''

SIBLING_SERVICE = '''\
from services.base import Microservice


class OrderService(Microservice):
    _service_name = 'order'

    @classmethod
    async def create_order(cls, data):
        return await cls._call_rpc('order.create', data=data)

    @classmethod
    async def update_order(cls, data):
        return await cls._call_rpc('order.update', data=data)

    @classmethod
    async def restaurant_confirm(cls, data):
        return await cls._call_rpc('order.restaurant.confirm', data=data)

    @classmethod
    async def restaurant_reject(cls, data):
        return await cls._call_rpc('order.restaurant.reject', data=data)
'''

# Only ``order.create`` and ``order.update`` are consumed, and they land on different
# handlers with different persistence: create writes, update only reads.
SIBLING_CONSUMER_EVENTS = '''\
from application.order import OrderService
from data_access.broker import RPCBroker


async def register_events():
    rpc_client = RPCBroker.get_client()
    events_handlers = {
        'order.create': OrderService.create_order,
        'order.update': OrderService.update_order,
    }
    for event, handler in events_handlers.items():
        await rpc_client.register_event(event=event, handler=handler)
'''

SIBLING_CONSUMER_APPLICATION = '''\
from domain.order import OrderHandler


class OrderService:
    @classmethod
    async def create_order(cls, **kwargs):
        return await OrderHandler.create_order(**kwargs)

    @classmethod
    async def update_order(cls, **kwargs):
        return await OrderHandler.update_order(**kwargs)
'''

SIBLING_CONSUMER_DOMAIN = '''\
from domain.entities import Order


class OrderHandler:
    @classmethod
    async def create_order(cls, customer_id=None, **kwargs):
        order = Order.create(customer_id=customer_id)
        await order.save()
        return order

    @classmethod
    async def update_order(cls, customer_id=None, **kwargs):
        return await Order.fetch(customer_id)
'''

SIBLING_FIXTURE_FILES = {
    **FIXTURE_FILES,
    "backend/gateway/src/application/routes/order.py": SIBLING_ROUTES,
    "backend/gateway/src/services/order.py": SIBLING_SERVICE,
    "backend/microservices/order/src/events.py": SIBLING_CONSUMER_EVENTS,
    "backend/microservices/order/src/application/order.py": SIBLING_CONSUMER_APPLICATION,
    "backend/microservices/order/src/domain/order.py": SIBLING_CONSUMER_DOMAIN,
}

SIBLING_EXPECTATIONS = {
    # flow suffix: (dispatch symbol, event id)
    "create": ("services.order.OrderService.create_order", "event.ftgo.rabbitmq.order.create"),
    "update": ("services.order.OrderService.update_order", "event.ftgo.rabbitmq.order.update"),
    "confirm": (
        "services.order.OrderService.restaurant_confirm",
        "event.ftgo.rabbitmq.order.restaurant.confirm",
    ),
    "reject": (
        "services.order.OrderService.restaurant_reject",
        "event.ftgo.rabbitmq.order.restaurant.reject",
    ),
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
        sources={
            "code": ("backend/gateway/**/*", "backend/microservices/**/*"),
            "compose": ("backend/docker-compose.yaml", "backend/infra/**/*.yaml"),
        },
    )


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
                            "code": ["backend/gateway/**/*", "backend/microservices/**/*"],
                            "compose": [
                                "backend/docker-compose.yaml",
                                "backend/infra/**/*.yaml",
                            ],
                        },
                    }
                ],
            },
            sort_keys=False,
        ),
        encoding="utf-8",
    )
    return manifest


@pytest.fixture
def extraction(tmp_path: Path):
    return extract_user_flow(make_record(build_repository(tmp_path / "repo")), FROZEN_COMMIT)


@pytest.fixture
def sibling_extraction(tmp_path: Path):
    record = make_record(build_repository(tmp_path / "repo", SIBLING_FIXTURE_FILES))
    return extract_user_flow(record, FROZEN_COMMIT)


def flows_by_id(result) -> dict[str, object]:
    return {item.id: item for item in result.flows}


def steps_by_role(result, flow_identifier: str) -> dict[str, list]:
    grouped: dict[str, list] = {}
    for step in result.steps_of(flow_identifier):
        grouped.setdefault(step.role, []).append(step)
    return grouped


def relations(result, relation_type: str) -> set[tuple[str, str]]:
    return {
        (item.source, item.target) for item in result.relationships if item.type == relation_type
    }


def classification_of(result, endpoint_identifier: str):
    return next(
        item for item in result.classifications if item.endpoint_id == endpoint_identifier
    )


# --------------------------------------------------------------------------------------
# 1-4. Identity construction
# --------------------------------------------------------------------------------------


# --------------------------------------------------------------------------------------
# Receiver typing: what a call's return value may and may not be assumed to be
# --------------------------------------------------------------------------------------


def index_of(sources: dict[str, str], service: str = "order"):
    """Build a SourceIndex from inline modules, for direct receiver-typing checks."""
    warnings: list[str] = []
    modules = [
        analyze_module(
            text,
            ast.parse(text),
            relative_path=f"backend/microservices/{service}/src/{name.replace('.', '/')}.py",
            service=service,
            module=name,
            is_package=False,
            warnings=warnings,
        )
        for name, text in sources.items()
    ]
    return build_source_index(modules)


def receiver_class(sources: dict[str, str], caller: str, expression: str, service: str = "order"):
    """Statically type the receiver of ``expression`` inside the function ``caller``."""
    index = index_of(sources, service)
    resolver = CalleeResolver(index)
    module_name, function_name = caller.rsplit(".", 1)
    facts = index.facts(service, module_name)
    assert facts is not None, f"module {module_name} not indexed"
    declaration = facts.functions[function_name]
    scope = local_scope(declaration)
    target = next(
        site for site in declaration.calls if site.callee_expression == expression
    )
    return resolver.instance_class(
        service,
        module_name,
        target.node.func.value,
        scope,
        declaration.owner_class,
    )


def annotation_of(text: str):
    return _unwrap_optional(ast.parse(text, mode="eval").body)


def dotted_of(node) -> str | None:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        head = dotted_of(node.value)
        return f"{head}.{node.attr}" if head else node.attr
    return None


def test_optional_annotations_are_unwrapped_to_the_single_real_type() -> None:
    assert dotted_of(annotation_of("Optional[User]")) == "User"
    assert dotted_of(annotation_of("typing.Optional[User]")) == "User"
    assert dotted_of(annotation_of("Union[User, None]")) == "User"
    assert dotted_of(annotation_of("typing.Union[User, None]")) == "User"
    assert dotted_of(annotation_of("Optional[domain.user.User]")) == "domain.user.User"


def test_pep604_optionals_are_unwrapped_in_either_order() -> None:
    assert dotted_of(annotation_of("User | None")) == "User"
    assert dotted_of(annotation_of("None | User")) == "User"


def test_a_union_of_two_real_types_is_left_ambiguous() -> None:
    # Two candidates means the receiver is genuinely undecidable; guessing one is forbidden.
    assert dotted_of(annotation_of("User | Driver")) is None
    assert dotted_of(annotation_of("Union[User, Driver]")) is None


USER_SOURCES = {
    "domain.user": (
        "class User:\n"
        "    def is_verified(self):\n"
        "        return True\n"
        "\n"
        "    def load_private_attributes(self):\n"
        "        return None\n"
    ),
    "domain.manager": (
        "from typing import Optional\n"
        "\n"
        "from domain.user import User\n"
        "\n"
        "\n"
        "class UserManager:\n"
        "    def is_verified(self):\n"
        "        return 'manager-not-user'\n"
        "\n"
        "    @staticmethod\n"
        "    async def load(user_id=None) -> Optional[User]:\n"
        "        return User()\n"
        "\n"
        "    @staticmethod\n"
        "    async def opaque(user_id=None):\n"
        "        return _build(user_id)\n"
        "\n"
        "    @classmethod\n"
        "    def build(cls, user_id=None):\n"
        "        return cls(user_id)\n"
        "\n"
        "\n"
        "def _build(user_id):\n"
        "    return User()\n"
        "\n"
        "\n"
        "async def handler(user_id=None):\n"
        "    user = await UserManager.load(user_id=user_id)\n"
        "    user.is_verified()\n"
        "    unknown = await UserManager.opaque(user_id=user_id)\n"
        "    unknown.is_verified()\n"
        "    made = UserManager.build(user_id)\n"
        "    made.is_verified()\n"
    ),
}


def test_an_awaited_call_keeps_the_declared_return_type() -> None:
    """``user = await UserManager.load(...)`` types ``user`` as ``User``, not ``UserManager``."""
    resolved = receiver_class(USER_SOURCES, "domain.manager.handler", "user.is_verified")

    assert resolved == ("domain.user", "User")


def test_a_service_method_result_is_not_typed_as_that_service() -> None:
    """With no provable return type the receiver stays untyped rather than becoming the owner."""
    resolved = receiver_class(USER_SOURCES, "domain.manager.handler", "unknown.is_verified")

    assert resolved is None


def test_return_cls_still_infers_the_owning_class() -> None:
    resolved = receiver_class(USER_SOURCES, "domain.manager.handler", "made.is_verified")

    assert resolved == ("domain.manager", "UserManager")


def test_an_explicit_annotation_overrides_owner_class_inference() -> None:
    """A factory that annotates ``User`` and returns ``cls(...)`` must follow the annotation."""
    sources = {
        "domain.user": "class User:\n    def ping(self):\n        return None\n",
        "domain.manager": (
            "from domain.user import User\n"
            "\n"
            "\n"
            "class UserManager:\n"
            "    def ping(self):\n"
            "        return None\n"
            "\n"
            "    @classmethod\n"
            "    def make(cls) -> User:\n"
            "        return cls()\n"
            "\n"
            "\n"
            "def handler():\n"
            "    made = UserManager.make()\n"
            "    made.ping()\n"
        ),
    }

    assert receiver_class(sources, "domain.manager.handler", "made.ping") == (
        "domain.user",
        "User",
    )


def test_returns_own_instance_only_looks_at_the_methods_own_scope() -> None:
    index = index_of(
        {
            "domain.factory": (
                "class Widget:\n"
                "    @classmethod\n"
                "    def build(cls):\n"
                "        def inner():\n"
                "            return cls()\n"
                "        return inner\n"
                "\n"
                "    @classmethod\n"
                "    def direct(cls):\n"
                "        return cls()\n"
            )
        }
    )
    declaration = index.facts("order", "domain.factory").classes["Widget"]

    assert _returns_own_instance(declaration.methods["direct"], "Widget") is True
    # The nested closure returns ``cls()``; the method itself returns a function.
    assert _returns_own_instance(declaration.methods["build"], "Widget") is False


def test_flow_id_is_derived_mechanically_from_the_endpoint_id() -> None:
    assert flow_id(CREATE_ENDPOINT) == CREATE_FLOW
    # Only the leading kind changes; nothing else about the endpoint id is rewritten.
    assert flow_id("endpoint.ftgo.gateway.get.health") == "flow.ftgo.gateway.get.health"


def test_flow_ids_are_byte_stable() -> None:
    assert flow_id(CREATE_ENDPOINT) == flow_id(CREATE_ENDPOINT)


def test_step_ids_encode_the_role_and_the_subject() -> None:
    assert step_id(CREATE_FLOW, "http-ingress", "") == f"step.{CREATE_FLOW[5:]}.http-ingress"
    assert step_id(CREATE_FLOW, "write", "ftgo.order.orders") == (
        f"step.{CREATE_FLOW[5:]}.write.ftgo.order.orders"
    )


def test_step_ids_normalize_symbol_subjects() -> None:
    # Case and underscores collapse so a symbol and its normalized form share one id.
    assert step_id(CREATE_FLOW, "dispatch", PUBLISHER_SYMBOL) == (
        f"step.{CREATE_FLOW[5:]}.dispatch.services.order.orderservice.create-order"
    )


# --------------------------------------------------------------------------------------
# 5-7. Scope and safety
# --------------------------------------------------------------------------------------


def test_only_service_src_python_files_are_in_scope() -> None:
    assert skip_reason("backend/gateway/src/application/routes/order.py") is None
    assert skip_reason("backend/microservices/order/src/events.py") is None
    assert "not a Python source file" in skip_reason("backend/gateway/Dockerfile")
    assert "src" in skip_reason("backend/gateway/tests/test_routes.py")
    assert "excluded directory" in skip_reason("backend/gateway/src/__pycache__/order.py")
    assert "test module" in skip_reason("backend/gateway/src/services/test_order.py")


def test_no_fixture_module_is_ever_imported(extraction) -> None:
    # The fixture contains a module that raises on import; extraction still succeeded.
    assert "backend/gateway/src/services/booby_trap.py" in extraction.source_files
    for module_name in ("services.order", "domain.order", "domain.entities.order", "events"):
        assert module_name not in sys.modules


def test_report_records_a_static_analysis_with_no_side_effects(extraction) -> None:
    _, report = render_bundle(extraction)

    assert report["analysis"] == "python-ast/static"
    assert report["modules_imported"] == 0
    assert report["modules_executed"] == 0
    assert report["runtime_connections_opened"] == 0
    assert report["graph_mutations"] == 0
    assert report["wiki_writes"] == 0
    assert report["neo4j_mutations"] == 0
    assert report["graphiti"] == "disabled"
    assert report["secret_values_emitted"] == 0


def test_credential_names_and_values_are_withheld() -> None:
    assert is_sensitive_name("password") is True
    assert is_sensitive_name("MONGO_PASSWORD") is True
    assert is_sensitive_name("customer_id") is False
    assert redact_expression("amqp://user:secret@rabbitmq:5672/") == "amqp://[redacted]@rabbitmq:5672/"


def test_no_fixture_secret_reaches_the_output(extraction) -> None:
    rendered, report = render_bundle(extraction)
    blob = "\n".join(rendered.values()) + json.dumps(report)

    for secret in FIXTURE_SECRETS:
        assert secret not in blob


# --------------------------------------------------------------------------------------
# 8-14. The proven flow, stitched only from call evidence
# --------------------------------------------------------------------------------------


def test_a_depth_one_dispatch_produces_a_fully_resolved_flow(extraction) -> None:
    flow = flows_by_id(extraction)[CREATE_FLOW]

    assert flow.completeness == COMPLETENESS_RESOLVED
    assert flow.endpoint_id == CREATE_ENDPOINT
    assert flow.events == (EVENT_CREATE,)
    assert flow.persistence_targets == (ORDERS_COLLECTION,)
    assert flow.unresolved_segments == ()
    assert flow.services == ("service.ftgo.gateway", "service.ftgo.order")


def test_the_resolved_flow_has_one_step_per_stage(extraction) -> None:
    grouped = steps_by_role(extraction, CREATE_FLOW)

    assert set(grouped) == {
        "http_ingress",
        "service_dispatch",
        "event_publish",
        "event_consume",
        "persistence_read",
        "persistence_write",
    }
    assert len(grouped["http_ingress"]) == 1
    assert grouped["service_dispatch"][0].attributes["gateway_symbol"] == PUBLISHER_SYMBOL
    assert grouped["event_publish"][0].anchor_id == EVENT_CREATE
    assert grouped["event_consume"][0].service == "order"
    assert grouped["persistence_read"][0].anchor_id == ORDERS_COLLECTION
    assert grouped["persistence_write"][0].anchor_id == ORDERS_COLLECTION


def test_every_stitched_step_carries_its_call_site_evidence(extraction) -> None:
    grouped = steps_by_role(extraction, CREATE_FLOW)
    dispatch = grouped["service_dispatch"][0]
    write = grouped["persistence_write"][0]

    assert dispatch.traces
    hops = dispatch.traces[0].hops
    assert hops[0].caller_symbol == "application.routes.order.create_order"
    assert hops[0].callee_symbol == PUBLISHER_SYMBOL
    assert hops[0].provenance.source_path == "backend/gateway/src/application/routes/order.py"

    # The write is proven through the domain handler into the entity, not assumed from the
    # fact that the order service happens to write the orders collection somewhere.
    chains = [[hop.callee_symbol for hop in trace.hops] for trace in write.traces]
    assert [
        "domain.order.OrderHandler.create_order",
        "domain.entities.order.Order.save",
    ] in chains


def test_a_deeper_dispatch_is_still_traced_within_the_bound(extraction) -> None:
    flow = flows_by_id(extraction)[DEEP_FLOW]
    dispatch = steps_by_role(extraction, DEEP_FLOW)["service_dispatch"][0]

    assert flow.completeness == COMPLETENESS_RESOLVED
    assert dispatch.attributes["call_depth"] == 2
    chain = [hop.callee_symbol for hop in dispatch.traces[0].hops]
    assert chain == ["application.routes.order.dispatch_create", PUBLISHER_SYMBOL]


def test_relationship_types_are_limited_to_the_five_declared_types(extraction) -> None:
    assert {item.type for item in extraction.relationships} == {
        CONTAINS,
        PRECEDES,
        IMPLEMENTS,
        DERIVED_FROM,
        PARTICIPATES_IN,
    }


def test_the_flow_contains_its_steps_and_precedes_only_proven_stages(extraction) -> None:
    contains = relations(extraction, CONTAINS)
    precedes = relations(extraction, PRECEDES)
    grouped = steps_by_role(extraction, CREATE_FLOW)
    ingress = grouped["http_ingress"][0].id
    dispatch = grouped["service_dispatch"][0].id
    publish = grouped["event_publish"][0].id
    consume = grouped["event_consume"][0].id
    write = grouped["persistence_write"][0].id

    for step in extraction.steps_of(CREATE_FLOW):
        assert (CREATE_FLOW, step.id) in contains
    assert (ingress, dispatch) in precedes
    assert (dispatch, publish) in precedes
    assert (publish, consume) in precedes
    assert (consume, write) in precedes
    # No edge is invented between stages that share no call evidence.
    assert (ingress, write) not in precedes
    assert (ingress, publish) not in precedes


def test_steps_derive_from_the_entities_the_earlier_passes_proved(extraction) -> None:
    derived = relations(extraction, DERIVED_FROM)
    grouped = steps_by_role(extraction, CREATE_FLOW)

    assert (grouped["http_ingress"][0].id, CREATE_ENDPOINT) in derived
    assert (grouped["event_publish"][0].id, EVENT_CREATE) in derived
    assert (grouped["event_consume"][0].id, EVENT_CREATE) in derived
    assert (grouped["persistence_write"][0].id, ORDERS_COLLECTION) in derived


def test_participating_services_are_only_pass_one_services(extraction) -> None:
    participants = {source for source, _ in relations(extraction, PARTICIPATES_IN)}

    assert participants
    assert participants <= PASS_ONE_SERVICE_IDS
    assert ("service.ftgo.order", CREATE_FLOW) in relations(extraction, PARTICIPATES_IN)


def test_a_consumer_with_no_publishing_endpoint_yields_no_flow(extraction) -> None:
    """The user service consumes and reads, but no gateway endpoint publishes to it."""
    assert "service.ftgo.user" in extraction.services_scanned
    assert not any(step.service == "user" for step in extraction.steps)
    assert not any(
        target.startswith("table.ftgo.user")
        for flow in extraction.flows
        for target in flow.persistence_targets
    )


# --------------------------------------------------------------------------------------
# 15-21. What must not be stitched
# --------------------------------------------------------------------------------------


def test_a_handler_that_reaches_no_publisher_yields_no_flow(extraction) -> None:
    assert REPORT_FLOW not in flows_by_id(extraction)
    classification = classification_of(extraction, REPORT_ENDPOINT)

    assert classification.completeness == COMPLETENESS_TRIVIAL
    assert "no bounded call path" in classification.reason


def test_a_lookalike_publish_method_is_never_treated_as_a_broker_call(extraction) -> None:
    """``Reporter.publish`` is an ordinary method, so it may not become a publish step."""
    assert not any(
        step.attributes.get("event_identity") == "order.report" for step in extraction.steps
    )
    assert "event.ftgo.rabbitmq.order.report" not in {
        event for flow in extraction.flows for event in flow.events
    }
    rendered, _ = render_bundle(extraction)
    assert "event.ftgo.rabbitmq.order.report" not in "\n".join(rendered.values())


def test_a_published_identity_with_no_consumer_stays_partial(extraction) -> None:
    flow = flows_by_id(extraction)[CANCEL_FLOW]
    grouped = steps_by_role(extraction, CANCEL_FLOW)

    assert flow.completeness == COMPLETENESS_PARTIAL
    assert flow.events == (EVENT_CANCEL,)
    assert flow.persistence_targets == ()
    assert "consume:order.cancel" in flow.unresolved_segments
    assert "event_consume" not in grouped
    assert "persistence_write" not in grouped


def test_a_persistence_hop_past_the_depth_bound_is_reported_not_invented(extraction) -> None:
    """``order.archive`` needs four hops to reach the same write the create path proves."""
    flow = flows_by_id(extraction)[ARCHIVE_FLOW]
    grouped = steps_by_role(extraction, ARCHIVE_FLOW)

    assert flow.completeness == COMPLETENESS_PARTIAL
    assert flow.events == (EVENT_ARCHIVE,)
    # The collection is reachable in the source but not within the contract, so the flow
    # says so instead of borrowing the target from the create path.
    assert flow.persistence_targets == ()
    assert "persistence:order.archive" in flow.unresolved_segments
    assert "event_consume" in grouped
    assert "persistence_write" not in grouped


# --------------------------------------------------------------------------------------
# Sibling methods on one service class must never collapse onto one another
# --------------------------------------------------------------------------------------


@pytest.mark.parametrize("suffix", sorted(SIBLING_EXPECTATIONS))
def test_each_sibling_method_resolves_to_its_own_dispatch_and_event(
    sibling_extraction, suffix: str
) -> None:
    """Four handlers, four methods on one class, four identities: no two may share either."""
    expected_symbol, expected_event = SIBLING_EXPECTATIONS[suffix]
    flow = flows_by_id(sibling_extraction)[f"flow.ftgo.gateway.post.api.orders.{suffix}"]
    dispatch = steps_by_role(sibling_extraction, flow.id)["service_dispatch"]

    assert len(dispatch) == 1
    assert dispatch[0].attributes["gateway_symbol"] == expected_symbol
    assert flow.events == (expected_event,)


def test_no_sibling_flow_borrows_another_siblings_dispatch_or_event(sibling_extraction) -> None:
    flows = flows_by_id(sibling_extraction)
    dispatches: dict[str, str] = {}
    events: dict[str, tuple[str, ...]] = {}
    for suffix in SIBLING_EXPECTATIONS:
        flow = flows[f"flow.ftgo.gateway.post.api.orders.{suffix}"]
        dispatches[suffix] = steps_by_role(sibling_extraction, flow.id)["service_dispatch"][
            0
        ].attributes["gateway_symbol"]
        events[suffix] = flow.events

    # Four distinct symbols and four distinct identities: a collapse would create duplicates.
    assert len(set(dispatches.values())) == 4
    assert len({item for value in events.values() for item in value}) == 4
    for suffix in ("update", "confirm", "reject"):
        assert EVENT_CREATE not in events[suffix]
        assert dispatches[suffix] != PUBLISHER_SYMBOL


def test_the_traced_call_site_names_the_method_the_handler_actually_calls(
    sibling_extraction,
) -> None:
    """The dispatch trace's last hop is the exact AST callee, not a sibling of it."""
    for suffix, (expected_symbol, _) in SIBLING_EXPECTATIONS.items():
        flow_identifier = f"flow.ftgo.gateway.post.api.orders.{suffix}"
        dispatch = steps_by_role(sibling_extraction, flow_identifier)["service_dispatch"][0]

        assert dispatch.traces
        for trace in dispatch.traces:
            assert trace.target_symbol == expected_symbol
            assert trace.hops[-1].callee_symbol == expected_symbol


def test_a_corrected_event_uses_its_own_consumer_and_persistence(sibling_extraction) -> None:
    """``order.update`` gets its own consumer and read; it must not inherit create's write."""
    flows = flows_by_id(sibling_extraction)
    create = flows["flow.ftgo.gateway.post.api.orders.create"]
    update = flows["flow.ftgo.gateway.post.api.orders.update"]
    create_steps = steps_by_role(sibling_extraction, create.id)
    update_steps = steps_by_role(sibling_extraction, update.id)

    assert create.completeness == COMPLETENESS_RESOLVED
    assert "persistence_write" in create_steps
    assert create.persistence_targets == (ORDERS_COLLECTION,)

    assert update.completeness == COMPLETENESS_RESOLVED
    assert update.persistence_targets == (ORDERS_COLLECTION,)
    # Update only reads. The write proven for create must not be carried over.
    assert "persistence_read" in update_steps
    assert "persistence_write" not in update_steps
    assert update_steps["event_consume"][0].attributes["event_identity"] == "order.update"


def test_an_event_with_no_consumer_stays_partial_instead_of_borrowing_one(
    sibling_extraction,
) -> None:
    """``order.restaurant.confirm`` and ``.reject`` have no binding, so nothing downstream."""
    flows = flows_by_id(sibling_extraction)
    for suffix in ("confirm", "reject"):
        flow = flows[f"flow.ftgo.gateway.post.api.orders.{suffix}"]
        grouped = steps_by_role(sibling_extraction, flow.id)

        assert flow.completeness == COMPLETENESS_PARTIAL
        assert flow.persistence_targets == ()
        assert "event_consume" not in grouped
        assert "persistence_read" not in grouped
        assert "persistence_write" not in grouped
        assert flow.unresolved_segments == (
            f"consume:order.restaurant.{suffix}",
        )


def test_a_method_that_cannot_be_resolved_is_never_replaced_by_a_sibling(tmp_path: Path) -> None:
    """When the called method does not exist, the flow is dropped, not re-pointed."""
    files = dict(SIBLING_FIXTURE_FILES)
    files["backend/gateway/src/application/routes/order.py"] = '''\
from fastapi import APIRouter, Request

from application.schemas.order import CreateOrderRequest
from services.order import OrderService

router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("/missing")
async def missing_method(request: Request, payload: CreateOrderRequest):
    # ``OrderService.publish_order`` is not defined anywhere in the class or its bases.
    return await OrderService.publish_order(data={"id": payload.customer_id})
'''
    record = make_record(build_repository(tmp_path / "repo", files))
    result = extract_user_flow(record, FROZEN_COMMIT)

    assert result.flows == ()
    classification = classification_of(
        result, "endpoint.ftgo.gateway.post.api.orders.missing"
    )
    assert classification.completeness == COMPLETENESS_TRIVIAL
    reasons = {item.reason for item in result.unresolved_of(UNRESOLVED_DISPATCH)}
    assert "OrderService.publish_order is not defined in scanned source" in reasons


def test_a_response_value_is_never_reported_as_a_method_of_the_called_service(
    extraction,
) -> None:
    """``response = await OrderService.create_order(...)`` does not make ``response`` an
    ``OrderService``, so ``response.get`` must not be reported as ``OrderService.get``."""
    reasons = {
        item.reason
        for item in (
            *extraction.unresolved_of(UNRESOLVED_DISPATCH),
            *extraction.unresolved_of(UNRESOLVED_PERSISTENCE),
        )
    }

    for forbidden in (
        "OrderService.get is not defined in scanned source",
        "OrderService.pop is not defined in scanned source",
    ):
        assert forbidden not in reasons
    # The honest outcome is a receiver whose type is simply not provable.
    untyped = {item.expression for item in extraction.receiver_typing_gaps}
    assert {"response.get", "response.pop"} <= untyped


def test_a_framework_call_an_earlier_pass_resolved_is_not_an_unresolved_gap(
    extraction,
) -> None:
    """Pass 3 named the broker call and Pass 4 named the Beanie write; neither is a gap."""
    reasons = {
        item.reason
        for item in (
            *extraction.unresolved_of(UNRESOLVED_DISPATCH),
            *extraction.unresolved_of(UNRESOLVED_PERSISTENCE),
        )
    }
    boundary = {
        (item.caller_symbol, item.expression) for item in extraction.interpreted_boundary_calls
    }

    assert not any("insert_one is not defined" in reason for reason in reasons)
    assert not any("find_one is not defined" in reason for reason in reasons)
    assert ("domain.entities.order.Order.save", "OrderDocument.insert_one") in boundary
    assert ("domain.entities.order.Order.fetch", "OrderDocument.find_one") in boundary
    # The broker wrapper Pass 3 proved forwards to the publisher is filtered the same way.
    assert ("services.base.Microservice._call_rpc", "rpc_client.call") in boundary


def test_a_dynamic_construct_stays_unresolved_inside_a_resolved_boundary(extraction) -> None:
    """``setattr`` sits in the same function as the resolved Beanie write and still surfaces."""
    findings = [
        item
        for item in extraction.unresolved_of(UNRESOLVED_PERSISTENCE)
        if "setattr" in item.reason
    ]

    assert findings
    assert all("dynamic call construct" in item.reason for item in findings)
    assert any(
        item.provenance.symbol == "domain.entities.order.Order.save" for item in findings
    )
    # Filtering the framework call did not swallow the dynamic one at the same site.
    assert not any(
        "setattr" in item.expression for item in extraction.interpreted_boundary_calls
    )


def test_every_unresolved_finding_names_a_reason_and_a_source_line(extraction) -> None:
    findings = [
        *extraction.unresolved_of(UNRESOLVED_PERSISTENCE),
        *extraction.unresolved_of(UNRESOLVED_DISPATCH),
        *extraction.unresolved_of(UNRESOLVED_CONSUMER),
    ]

    for finding in findings:
        assert finding.reason
        assert finding.provenance.source_path
        assert finding.provenance.line_start


def test_text_similarity_never_creates_a_link(tmp_path: Path) -> None:
    """An endpoint path that reads like an event identity must not stitch to it."""
    files = dict(FIXTURE_FILES)
    # The handler no longer calls the publisher; only the names still line up.
    files["backend/gateway/src/application/routes/order.py"] = '''\
from fastapi import APIRouter, Request

from application.schemas.order import CreateOrderRequest

router = APIRouter(prefix="/order", tags=["orders"])


@router.post("/create")
async def create_order(request: Request, payload: CreateOrderRequest):
    return {"ok": True}
'''
    record = make_record(build_repository(tmp_path / "repo", files))
    result = extract_user_flow(record, FROZEN_COMMIT)

    assert result.flows == ()
    assert all(item.completeness == COMPLETENESS_TRIVIAL for item in result.classifications)


def test_identity_collisions_and_cycles_are_empty_for_a_clean_fixture(extraction) -> None:
    assert extraction.identity_collisions == ()
    assert extraction.cycles_detected == ()
    assert extraction.warnings == ()


def test_precedes_cycles_are_detected_and_reported() -> None:
    from knowledge_plane.extractors.user_flow import Provenance

    provenance = Provenance(
        repository="ftgo",
        commit=FROZEN_COMMIT,
        source_path="a.py",
        symbol="a",
        line_start=1,
        line_end=1,
        evidence_type="implemented",
    )
    edges = [
        RelationshipCandidate("step.a", PRECEDES, "step.b", provenance),
        RelationshipCandidate("step.b", PRECEDES, "step.a", provenance),
    ]

    cycles = _detect_cycles(edges)

    assert cycles
    assert "step.a" in cycles[0]


# --------------------------------------------------------------------------------------
# 22-27. Rendering and candidate discipline
# --------------------------------------------------------------------------------------


def test_candidate_pages_are_never_approved(extraction) -> None:
    rendered, _ = render_bundle(extraction)

    assert rendered
    for path, content in rendered.items():
        frontmatter = yaml.safe_load(content.split("---")[1])
        assert frontmatter["status"] == "candidate"
        assert frontmatter["review_status"] == "pending"
        assert frontmatter["kind"] == frontmatter["type"]
        assert "status: approved" not in content
        assert path.startswith(("flows/", "steps/"))


def test_one_page_is_rendered_per_flow_and_per_step(extraction) -> None:
    rendered, _ = render_bundle(extraction)

    assert len([path for path in rendered if path.startswith("flows/")]) == len(extraction.flows)
    assert len([path for path in rendered if path.startswith("steps/")]) == len(extraction.steps)


def test_no_page_is_written_for_an_entity_an_earlier_pass_owns(extraction) -> None:
    rendered, _ = render_bundle(extraction)

    assert not any("endpoint.ftgo" in path for path in rendered)
    assert not any("event.ftgo" in path for path in rendered)
    assert not any("service.ftgo" in path for path in rendered)
    assert not any("collection.ftgo" in path for path in rendered)


def test_step_pages_keep_separate_call_chains_separate(extraction) -> None:
    rendered, _ = render_bundle(extraction)
    write = steps_by_role(extraction, CREATE_FLOW)["persistence_write"][0]
    content = rendered[f"steps/{write.id}.md"]
    frontmatter = yaml.safe_load(content.split("---")[1])

    assert isinstance(frontmatter["traces"], list)
    for trace in frontmatter["traces"]:
        assert trace["depth"] == len(trace["hops"])


def test_service_deltas_are_additive_and_never_canonical(extraction) -> None:
    deltas = build_service_relation_deltas(extraction)

    assert deltas["review_status"] == "pending"
    assert "not canonical knowledge" in deltas["note"]
    services = {item["service"] for item in deltas["services"]}
    assert services <= PASS_ONE_SERVICE_IDS
    for entry in deltas["services"]:
        assert {relation["type"] for relation in entry["relations"]} == {PARTICIPATES_IN}


def test_secret_leak_counting_uses_whole_token_matches(extraction) -> None:
    rendered, _ = render_bundle(extraction)

    assert count_secret_leaks(extraction, rendered) == 0


# --------------------------------------------------------------------------------------
# 28-33. CLI behaviour
# --------------------------------------------------------------------------------------


def test_dry_run_writes_nothing(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    manifest = write_manifest(tmp_path, build_repository(tmp_path / "repo"))
    output_dir = tmp_path / "candidates"
    monkeypatch.setattr("knowledge_plane.extract.read_git_head", lambda path: FROZEN_COMMIT)

    summary = run("ftgo", "user-flow", manifest_path=manifest, output_dir=output_dir, dry_run=True)

    assert summary["status"] == "dry-run"
    assert summary["dry_run"] is True
    assert summary["commit_verified"] is True
    assert summary["analysis"] == "python-ast/static"
    assert summary["modules_imported"] == 0
    assert summary["modules_executed"] == 0
    assert summary["runtime_connections_opened"] == 0
    assert summary["secret_values_emitted"] == 0
    assert summary["graph_mutations"] == 0
    assert summary["wiki_writes"] == 0
    assert summary["neo4j_mutations"] == 0
    assert summary["graphiti"] == "disabled"
    assert summary["counts"]["flows"] == 4
    assert not output_dir.exists()


def test_dry_run_leaves_the_inspected_repository_untouched(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    repo_root = build_repository(tmp_path / "repo")
    manifest = write_manifest(tmp_path, repo_root)
    monkeypatch.setattr("knowledge_plane.extract.read_git_head", lambda path: FROZEN_COMMIT)
    before = {path: path.read_bytes() for path in sorted(repo_root.rglob("*")) if path.is_file()}

    run("ftgo", "user-flow", manifest_path=manifest, dry_run=True)

    after = {path: path.read_bytes() for path in sorted(repo_root.rglob("*")) if path.is_file()}
    assert after == before


def test_normal_run_writes_only_the_candidate_tree(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    repo_root = build_repository(tmp_path / "repo")
    manifest = write_manifest(tmp_path, repo_root)
    output_dir = tmp_path / "candidates"
    monkeypatch.setattr("knowledge_plane.extract.read_git_head", lambda path: FROZEN_COMMIT)
    before = {path: path.read_bytes() for path in sorted(repo_root.rglob("*")) if path.is_file()}

    summary = run("ftgo", "user-flow", manifest_path=manifest, output_dir=output_dir)

    assert summary["status"] == "ok"
    assert (output_dir / "extraction-report.json").is_file()
    assert (output_dir / SERVICE_DELTAS_FILENAME).is_file()
    assert len(list((output_dir / "flows").glob("*.md"))) == 4
    assert list((output_dir / "steps").glob("*.md"))
    after = {path: path.read_bytes() for path in sorted(repo_root.rglob("*")) if path.is_file()}
    assert after == before

    report = json.loads((output_dir / "extraction-report.json").read_text(encoding="utf-8"))
    assert report["commit"] == FROZEN_COMMIT
    assert report["max_call_depth"] == 3
    assert report["graph_mutations"] == 0


def test_commit_mismatch_aborts_before_writing_anything(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    manifest = write_manifest(tmp_path, build_repository(tmp_path / "repo"))
    output_dir = tmp_path / "candidates"
    monkeypatch.setattr("knowledge_plane.extract.read_git_head", lambda path: WRONG_COMMIT)

    with pytest.raises(CommitMismatchError) as excinfo:
        run("ftgo", "user-flow", manifest_path=manifest, output_dir=output_dir, dry_run=False)

    assert excinfo.value.expected == FROZEN_COMMIT
    assert excinfo.value.actual == WRONG_COMMIT
    assert not output_dir.exists()


def test_repeat_extraction_is_byte_identical(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    manifest = write_manifest(tmp_path, build_repository(tmp_path / "repo"))
    monkeypatch.setattr("knowledge_plane.extract.read_git_head", lambda path: FROZEN_COMMIT)
    first = tmp_path / "run-one"
    second = tmp_path / "run-two"

    run("ftgo", "user-flow", manifest_path=manifest, output_dir=first)
    run("ftgo", "user-flow", manifest_path=manifest, output_dir=second)

    first_files = sorted(path.relative_to(first) for path in first.rglob("*") if path.is_file())
    second_files = sorted(path.relative_to(second) for path in second.rglob("*") if path.is_file())
    assert first_files == second_files
    assert first_files
    for relative_path in first_files:
        assert (first / relative_path).read_bytes() == (second / relative_path).read_bytes(), (
            f"{relative_path} differs between runs"
        )


def test_sibling_pass_output_is_not_pruned(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    manifest = write_manifest(tmp_path, build_repository(tmp_path / "repo"))
    monkeypatch.setattr("knowledge_plane.extract.read_git_head", lambda path: FROZEN_COMMIT)
    output_dir = tmp_path / "candidates"
    foreign = output_dir / "endpoints" / f"{CREATE_ENDPOINT}.md"
    foreign.parent.mkdir(parents=True, exist_ok=True)
    foreign.write_text("owned by the fastapi pass", encoding="utf-8")

    run("ftgo", "user-flow", manifest_path=manifest, output_dir=output_dir)
    orphan = output_dir / "flows" / "flow.ftgo.gateway.get.retired.md"
    orphan.write_text("stale", encoding="utf-8")
    run("ftgo", "user-flow", manifest_path=manifest, output_dir=output_dir)

    assert not orphan.exists()
    assert foreign.read_text(encoding="utf-8") == "owned by the fastapi pass"


def test_earlier_passes_still_behave_the_same(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    manifest = write_manifest(tmp_path, build_repository(tmp_path / "repo"))
    monkeypatch.setattr("knowledge_plane.extract.read_git_head", lambda path: FROZEN_COMMIT)

    compose = run("ftgo", "compose", manifest_path=manifest, dry_run=True)
    fastapi = run("ftgo", "fastapi", manifest_path=manifest, dry_run=True)
    rabbitmq = run("ftgo", "rabbitmq", manifest_path=manifest, dry_run=True)
    data_model = run("ftgo", "data-model", manifest_path=manifest, dry_run=True)

    assert "database.ftgo.user-postgres" in compose["infrastructure_entities"]
    assert fastapi["counts"]["endpoints"] == 5
    assert any(entry.endswith(EVENT_CREATE) for entry in rabbitmq["events"])
    assert data_model["counts"]["collections"] == 1


# --------------------------------------------------------------------------------------
# Opt-in verification against the real frozen FTGO checkout
# --------------------------------------------------------------------------------------


def _real_ftgo_record() -> RepositoryRecord | None:
    try:
        records = load_repository_manifest(AIDE_ROOT / DEFAULT_MANIFEST_RELATIVE_PATH)
    except Exception:  # pragma: no cover
        return None
    record = records.get("ftgo")
    if record is None or not record.path.is_dir():
        return None
    try:
        if read_git_head(record.path) != FROZEN_COMMIT:
            return None
    except Exception:  # pragma: no cover
        return None
    return record


@pytest.fixture(scope="module")
def real_extraction():
    record = _real_ftgo_record()
    if record is None:
        pytest.skip("FTGO checkout at the frozen commit is not available")
    return extract_user_flow(record, FROZEN_COMMIT)


def test_real_ftgo_order_create_reaches_the_orders_collection(real_extraction) -> None:
    """The one path Pass 5 was asked to prove, asserted hop by hop."""
    flow = flows_by_id(real_extraction)["flow.ftgo.gateway.post.order.create"]

    assert flow.completeness == COMPLETENESS_RESOLVED
    assert flow.endpoint_id == "endpoint.ftgo.gateway.post.order.create"
    assert flow.events == (EVENT_CREATE,)
    assert flow.persistence_targets == (ORDERS_COLLECTION,)
    assert flow.enumerated_persistence_targets == ()
    assert flow.unresolved_segments == ()
    assert flow.services == ("service.ftgo.gateway", "service.ftgo.order")

    grouped = steps_by_role(real_extraction, flow.id)
    dispatch = grouped["service_dispatch"][0]
    assert [hop.callee_symbol for hop in dispatch.traces[0].hops] == [
        "services.order.OrderService.create_order"
    ]
    write = grouped["persistence_write"][0]
    chains = [[hop.callee_symbol for hop in trace.hops] for trace in write.traces]
    assert [
        "domain.order.OrderHandler.create_order",
        "domain.entities.order.Order.save",
    ] in chains


def test_real_ftgo_order_dispatches_match_the_handler_call_sites_exactly(
    real_extraction,
) -> None:
    """Every order flow's dispatch is the method its handler literally calls.

    At the frozen commit the gateway's ``/order`` handlers all call
    ``OrderService.create_order``: see ``backend/gateway/src/application/routes/order/order.py``
    lines 52, 78, 103 and 128. ``update_order``, ``restaurant_confirm`` and
    ``restaurant_reject`` are declared in ``backend/gateway/src/services/order.py`` but are
    never called from any handler. This test pins the extractor to that source fact rather
    than to the names of the handlers, so a future resolver that guessed
    ``update_order`` from the ``update_order`` handler name would fail here.
    """
    expected_symbol = "services.order.OrderService.create_order"
    for suffix in ("create", "update", "confirm", "reject"):
        flow = flows_by_id(real_extraction)[f"flow.ftgo.gateway.post.order.{suffix}"]
        dispatch = steps_by_role(real_extraction, flow.id)["service_dispatch"]

        assert len(dispatch) == 1, suffix
        assert dispatch[0].attributes["gateway_symbol"] == expected_symbol, suffix
        assert flow.events == (EVENT_CREATE,), suffix
        for trace in dispatch[0].traces:
            assert trace.hops[-1].callee_symbol == expected_symbol


def test_real_ftgo_never_invents_an_event_for_an_uncalled_service_method(
    real_extraction,
) -> None:
    """The three uncalled gateway methods publish identities no endpoint can reach.

    Pass 3 sees their ``_call_rpc`` sites, so the Events exist. Pass 5 must not attach them
    to a flow, because no handler call chain reaches them.
    """
    reachable = {event for flow in real_extraction.flows for event in flow.events}

    for identity in (
        "event.ftgo.rabbitmq.order.update",
        "event.ftgo.rabbitmq.order.restaurant.confirm",
        "event.ftgo.rabbitmq.order.restaurant.reject",
    ):
        assert identity not in reachable
    assert not any(
        step.attributes.get("gateway_symbol")
        in (
            "services.order.OrderService.update_order",
            "services.order.OrderService.restaurant_confirm",
            "services.order.OrderService.restaurant_reject",
        )
        for step in real_extraction.steps
    )


def test_real_ftgo_order_flows_share_a_downstream_because_they_share_a_publisher(
    real_extraction,
) -> None:
    """Sharing the identity is a source fact, so sharing the consumer and write follows."""
    for suffix in ("create", "update", "confirm", "reject"):
        flow = flows_by_id(real_extraction)[f"flow.ftgo.gateway.post.order.{suffix}"]
        grouped = steps_by_role(real_extraction, flow.id)

        assert flow.completeness == COMPLETENESS_RESOLVED, suffix
        assert grouped["event_consume"][0].attributes["event_identity"] == "order.create"
        assert flow.persistence_targets == (ORDERS_COLLECTION,), suffix


def test_real_ftgo_flows_only_enter_through_the_gateway(real_extraction) -> None:
    assert real_extraction.flows
    for flow in real_extraction.flows:
        assert flow.endpoint_id.startswith("endpoint.ftgo.gateway.")
        assert flow.id.startswith("flow.ftgo.gateway.")


def test_real_ftgo_uses_only_existing_kinds_and_relationship_types(real_extraction) -> None:
    assert {item.kind for item in real_extraction.flows} == {"UserFlow"}
    assert {item.kind for item in real_extraction.steps} == {"FlowStep"}
    assert {item.type for item in real_extraction.relationships} == {
        CONTAINS,
        PRECEDES,
        IMPLEMENTS,
        DERIVED_FROM,
        PARTICIPATES_IN,
    }


def test_real_ftgo_every_contained_step_has_a_page(real_extraction) -> None:
    rendered, _ = render_bundle(real_extraction)
    known = {item.id for item in real_extraction.steps}

    for flow in real_extraction.flows:
        for step_identifier in flow.step_ids:
            assert step_identifier in known
            assert f"steps/{step_identifier}.md" in rendered


def test_real_ftgo_participating_services_are_pass_one_services(real_extraction) -> None:
    participants = {source for source, _ in relations(real_extraction, PARTICIPATES_IN)}

    assert participants <= PASS_ONE_SERVICE_IDS
    assert "service.ftgo.gateway" in participants
    assert "service.ftgo.order" in participants


def test_real_ftgo_does_not_report_already_resolved_framework_calls(real_extraction) -> None:
    """Pass 3 turned ``rpc_client.call`` into an Event, so it is not an unresolved dispatch."""
    reasons = {item.reason for item in real_extraction.unresolved_of(UNRESOLVED_DISPATCH)}

    assert not any("RPCBroker.call" in reason for reason in reasons)
    assert real_extraction.unresolved_of(UNRESOLVED_CONSUMER) == ()


def test_real_ftgo_does_not_mistype_gateway_response_values(real_extraction) -> None:
    """``response = await XService.method(...)`` is not an ``XService``."""
    reasons = {
        item.reason
        for item in (
            *real_extraction.unresolved_of(UNRESOLVED_DISPATCH),
            *real_extraction.unresolved_of(UNRESOLVED_PERSISTENCE),
        )
    }
    services = (
        "OrderService",
        "UserService",
        "RestaurantService",
        "FeedbackService",
        "LocationService",
        "MenuService",
        "VehicleService",
    )

    for service in services:
        for method in ("get", "pop"):
            assert f"{service}.{method} is not defined in scanned source" not in reasons


def test_real_ftgo_resolves_an_optional_return_to_the_declared_class(real_extraction) -> None:
    """``UserManager.load(...) -> Optional[User]`` types the result as ``User``, not a manager."""
    reasons = {item.reason for item in real_extraction.unresolved_of(UNRESOLVED_PERSISTENCE)}

    assert "UserManager.is_verified is not defined in scanned source" not in reasons
    assert "UserManager.load_private_attributes is not defined in scanned source" not in reasons


def test_real_ftgo_still_reports_genuine_dynamic_dispatch(real_extraction) -> None:
    reasons = {item.reason for item in real_extraction.unresolved_of(UNRESOLVED_PERSISTENCE)}

    assert any("dynamic call construct" in reason for reason in reasons)


def test_real_ftgo_discloses_targets_the_call_site_does_not_pin(real_extraction) -> None:
    # The user service reaches persistence through a repository that takes the model as an
    # argument. Pass 4 enumerates every mapped model there, so Pass 5 must not present the
    # specific table as pinned by the source.
    disclosed = {
        flow.id: flow.enumerated_persistence_targets
        for flow in real_extraction.flows
        if flow.enumerated_persistence_targets
    }

    assert disclosed
    for flow_identifier, targets in disclosed.items():
        del flow_identifier
        assert all(target.startswith("table.ftgo.user.") for target in targets)
    for step in real_extraction.steps:
        if step.role.startswith("persistence") and step.anchor_id in {
            target for targets in disclosed.values() for target in targets
        }:
            assert step.attributes["resolution"] == ENUMERATED_RESOLUTION


def test_real_ftgo_has_no_collisions_or_cycles(real_extraction) -> None:
    assert real_extraction.identity_collisions == ()
    assert real_extraction.cycles_detected == ()


def test_real_ftgo_emits_no_secret_values(real_extraction) -> None:
    rendered, report = render_bundle(real_extraction)

    assert report["secret_values_emitted"] == 0
    blob = "\n".join(rendered.values()) + json.dumps(report)
    for secret in ("rabbitmq_password", "user_password", "order_password"):
        assert secret not in blob


def test_real_ftgo_extraction_is_deterministic(real_extraction) -> None:
    record = _real_ftgo_record()
    assert record is not None
    repeated = extract_user_flow(record, FROZEN_COMMIT)

    first, first_report = render_bundle(real_extraction)
    second, second_report = render_bundle(repeated)
    assert first.keys() == second.keys()
    for key in first:
        assert first[key] == second[key], f"{key} differs between identical runs"
    assert first_report == second_report
