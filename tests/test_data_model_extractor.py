"""Deterministic tests for the persistence / data-model extractor (Pass 4).

The fixture is a synthetic repository shaped like FTGO: a relational service with an
abstract declarative base, an aliased base, a foreign key and a ``{DTO: Model}`` repository;
a document service with Beanie models; decoy classes that look persistent but are not; and
Compose files so the service-to-database correlation has real evidence to work from.
Opt-in tests at the end verify the same guarantees against the real frozen FTGO checkout.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest
import yaml

from knowledge_plane.extract import run
from knowledge_plane.extractors.data_model import (
    DATABASE_DELTAS_FILENAME,
    SERVICE_DELTAS_FILENAME,
    build_database_relation_deltas,
    build_service_relation_deltas,
    classify_model,
    collection_id,
    is_sensitive_name,
    render_bundle,
    skip_reason,
    table_id,
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

PASS_ONE_SERVICE_IDS = {
    "service.ftgo.gateway",
    "service.ftgo.user",
    "service.ftgo.restaurant",
    "service.ftgo.location",
    "service.ftgo.order",
    "service.ftgo.feedback",
}
FIXTURE_SECRETS = ("fixture_pg_password", "fixture_mongo_password")

# --------------------------------------------------------------------------------------
# Fixture sources
# --------------------------------------------------------------------------------------

RELATIONAL_BASE = '''\
import sqlalchemy
from sqlalchemy import DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    __abstract__ = True
    metadata = sqlalchemy.MetaData()

    id: Mapped[str] = mapped_column(sqlalchemy.String, primary_key=True, default=uuid4)
    created_at: Mapped[str] = mapped_column(DateTime(timezone=True), server_default=func.now())
'''

PROFILE_MODEL = '''\
from typing import List, Optional
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from data_access.models.base import Base


class Profile(Base):
    __tablename__ = "user_profile"

    phone_number: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    national_id: Mapped[Optional[str]] = mapped_column(String, nullable=True, index=True)

    addresses: Mapped[List["Address"]] = relationship("Address", back_populates="profile")
'''

ADDRESS_MODEL = '''\
from sqlalchemy import Boolean, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from data_access.models.base import Base


class Address(Base):
    __tablename__ = "customer_address"

    user_id: Mapped[str] = mapped_column(String, ForeignKey("user_profile.id"), nullable=False)
    is_default: Mapped[bool] = mapped_column(Boolean, nullable=True, default=False)

    profile: Mapped["Profile"] = relationship("Profile", back_populates="addresses")
'''

# A mapped class whose physical name is computed: the table must not be invented.
DYNAMIC_TABLE_MODEL = '''\
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from data_access.models.base import Base

SUFFIX = "audit"


class AuditLog(Base):
    __tablename__ = "log_" + SUFFIX.upper()

    message: Mapped[str] = mapped_column(String, nullable=False)
'''

RELATIONAL_REPOSITORY = '''\
from typing import Dict, Type
from sqlalchemy.future import select

from asyncpg_client import AsyncPostgres
from data_access.models.address import Address
from data_access.models.profile import Profile
from dto import AddressDTO, ProfileDTO


class DatabaseRepository:
    _data_access: AsyncPostgres = None

    _dto_model_mapping: Dict[Type, Type] = {
        ProfileDTO: Profile,
        AddressDTO: Address,
    }

    @classmethod
    async def fetch(cls, dto_class, query):
        model_class = cls._get_model_class(dto_class)
        async with cls._data_access.get_or_create_session() as session:
            return await session.execute(select(model_class).filter_by(**query))

    @classmethod
    async def fetch_again(cls, dto_class, query):
        model_class = cls._get_model_class(dto_class)
        async with cls._data_access.get_or_create_session() as session:
            return await session.execute(select(model_class).filter_by(**query))

    @classmethod
    async def insert(cls, dto_instances):
        model_class = cls._get_model_class(type(dto_instances[0]))
        instances = [model_class.from_dto(dto) for dto in dto_instances]
        async with cls._data_access.get_or_create_session() as session:
            session.add_all(instances)
            await session.commit()

    @classmethod
    def _get_model_class(cls, dto):
        return cls._dto_model_mapping[dto]
'''

# A generic repository whose model arrives as an argument: wrapper tracing must resolve it.
WRAPPER_REPOSITORY = '''\
from sqlalchemy.future import select

from asyncpg_client import AsyncPostgres


class GenericRepository:
    _data_access: AsyncPostgres = None

    @classmethod
    async def load(cls, model, query):
        async with cls._data_access.get_or_create_session() as session:
            return await session.execute(select(model).filter_by(**query))
'''

WRAPPER_CALLER = '''\
from data_access.models.profile import Profile
from data_access.repository.generic import GenericRepository


async def load_profile(query):
    return await GenericRepository.load(Profile, query)
'''

# Decoys. None of these root in a persistence library, so none may be reported.
DECOYS = '''\
from dataclasses import dataclass

from pydantic import BaseModel


class ProfileRequest(BaseModel):
    phone_number: str
    hashed_password: str


@dataclass
class ProfileDomain:
    user_id: str
    phone_number: str


class InMemoryStore:
    def __init__(self):
        self._items = {}

    def get_order(self, key):
        return self._items.get(key)

    def save(self, key, value):
        self._items[key] = value

    def delete(self, key):
        self._items.pop(key, None)

    def select(self, key):
        return self._items.get(key)


class CacheService:
    def __init__(self):
        self.store = InMemoryStore()

    def run(self):
        self.store.get_order("a")
        self.store.save("a", 1)
        self.store.delete("a")
        self.store.select("a")
'''

DTO_MODULE = '''\
from dataclasses import dataclass


@dataclass
class ProfileDTO:
    user_id: str


@dataclass
class AddressDTO:
    address_id: str
'''

DB_CONFIG = '''\
class PostgresConfig:
    def __init__(self):
        self.host = "user_postgres"
        self.db = "user_database"
        self.user = "fixture_pg_user"
        self.password = "fixture_pg_password"

    @property
    def async_url(self):
        return "postgresql+asyncpg://fixture_pg_user:fixture_pg_password@user_postgres:5432/db"
'''

MIGRATION_MODULE = '''\
"""create initial tables

Revision ID: aaa111bbb222
Revises:
"""
from alembic import op
import sqlalchemy as sa

revision = 'aaa111bbb222'
down_revision = None


def upgrade() -> None:
    op.create_table(
        'user_profile',
        sa.Column('id', sa.String(), nullable=False),
    )
    op.create_table('unknown_table', sa.Column('id', sa.String()))


def downgrade() -> None:
    op.drop_table('user_profile')
'''

DOCUMENT_MODEL = '''\
import pymongo

from typing import List, Optional
from beanie import Document, Link
from pydantic import Field
from pymongo import IndexModel

from models.order_item import OrderItem


class Order(Document):
    customer_id: str
    total_amount: float = Field(..., gt=0)
    order_items: List[Link[OrderItem]] = []
    payment_id: Optional[str] = None

    class Settings:
        name = "orders"
        indexes = [
            IndexModel([("customer_id", pymongo.ASCENDING)], name="order_customer_id_index"),
        ]
'''

DOCUMENT_ITEM_MODEL = '''\
from beanie import Document
from pydantic import Field


class OrderItem(Document):
    order_id: str
    quantity: int = Field(..., gt=0)

    class Settings:
        name = "order_items"
'''

DYNAMIC_COLLECTION_MODEL = '''\
from beanie import Document

PREFIX = "archive"


class ArchivedOrder(Document):
    order_id: str

    class Settings:
        name = PREFIX.upper() + "_orders"
'''

DOCUMENT_REPOSITORY = '''\
from beanie import init_beanie
from mongo_motors import AsyncMongo

from models.order import Order
from models.order_item import OrderItem


class DatabaseRepository:
    _data_access: AsyncMongo = None

    @classmethod
    async def initialize(cls):
        mongo = await AsyncMongo.create(
            host="order_mongo",
            username="fixture_mongo_user",
            password="fixture_mongo_password",
        )
        await init_beanie(database=mongo.get_database(), document_models=[Order, OrderItem])
        cls._data_access = mongo
'''

DOCUMENT_APPLICATION = '''\
from models.order import Order


async def read_order(order_id):
    return await Order.find_one(Order.customer_id == order_id)


async def read_order_again(order_id):
    return await Order.find_one(Order.customer_id == order_id)


async def create_order(customer_id):
    order = Order(customer_id=customer_id, total_amount=1.0)
    await order.insert()
    return order
'''

# A relational service with models but no Compose database: the mapping must stay unresolved.
ORPHAN_MODEL = '''\
import sqlalchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    metadata = sqlalchemy.MetaData()


class DriverLocation(Base):
    __tablename__ = "driver_location"

    driver_id: Mapped[str] = mapped_column(sqlalchemy.String, primary_key=True)
'''

APP_COMPOSE = """\
services:
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
  location_service:
    build:
      context: ./microservices/location
    environment:
      - REDIS_HOST=location_redis
  gateway_service:
    build:
      context: ./gateway
    environment:
      - REDIS_HOST=gateway_redis
"""

INFRA_COMPOSE = """\
services:
  user_postgres:
    image: postgres:16.3
    hostname: "user_postgres"
  order_mongo:
    image: mongo:latest
    hostname: "order_mongo"
  gateway_redis:
    image: redis:7.2.5
    hostname: "gateway_redis"
  location_redis:
    image: redis:7.2.5
    hostname: "location_redis"
"""

FIXTURE_FILES = {
    "backend/docker-compose.yaml": APP_COMPOSE,
    "backend/infra/docker-compose.yaml": INFRA_COMPOSE,
    # Relational service.
    "backend/microservices/user/src/__init__.py": "",
    "backend/microservices/user/src/dto.py": DTO_MODULE,
    "backend/microservices/user/src/schemas.py": DECOYS,
    "backend/microservices/user/src/config/__init__.py": "",
    "backend/microservices/user/src/config/db.py": DB_CONFIG,
    "backend/microservices/user/src/data_access/__init__.py": "",
    "backend/microservices/user/src/data_access/models/__init__.py": "",
    "backend/microservices/user/src/data_access/models/base.py": RELATIONAL_BASE,
    "backend/microservices/user/src/data_access/models/profile.py": PROFILE_MODEL,
    "backend/microservices/user/src/data_access/models/address.py": ADDRESS_MODEL,
    "backend/microservices/user/src/data_access/models/audit.py": DYNAMIC_TABLE_MODEL,
    "backend/microservices/user/src/data_access/repository/__init__.py": "",
    "backend/microservices/user/src/data_access/repository/db_repository.py": (
        RELATIONAL_REPOSITORY
    ),
    "backend/microservices/user/src/data_access/repository/generic.py": WRAPPER_REPOSITORY,
    "backend/microservices/user/src/application/__init__.py": "",
    "backend/microservices/user/src/application/profile.py": WRAPPER_CALLER,
    "backend/microservices/user/migrations/versions/aaa111_initial.py": MIGRATION_MODULE,
    # Document service.
    "backend/microservices/order/src/__init__.py": "",
    "backend/microservices/order/src/models/__init__.py": "",
    "backend/microservices/order/src/models/order.py": DOCUMENT_MODEL,
    "backend/microservices/order/src/models/order_item.py": DOCUMENT_ITEM_MODEL,
    "backend/microservices/order/src/models/archived.py": DYNAMIC_COLLECTION_MODEL,
    "backend/microservices/order/src/data_access/__init__.py": "",
    "backend/microservices/order/src/data_access/db_repository.py": DOCUMENT_REPOSITORY,
    "backend/microservices/order/src/application/__init__.py": "",
    "backend/microservices/order/src/application/order.py": DOCUMENT_APPLICATION,
    # Relational service with no Compose database.
    "backend/microservices/location/src/__init__.py": "",
    "backend/microservices/location/src/models.py": ORPHAN_MODEL,
    # Service with no persistence at all.
    "backend/gateway/src/__init__.py": "",
    "backend/gateway/src/main.py": "app = object()\n",
    # Out-of-scope trees that declare models; none may reach the output.
    "backend/microservices/user/tests/test_models.py": PROFILE_MODEL,
    "backend/microservices/user/src/__pycache__/profile.py": PROFILE_MODEL,
}

USER_PROFILE_TABLE = "table.ftgo.user.user-profile"
CUSTOMER_ADDRESS_TABLE = "table.ftgo.user.customer-address"
DRIVER_LOCATION_TABLE = "table.ftgo.location.driver-location"
ORDER_SCHEMA = "schema.ftgo.order.persistence.models.order.order"
ORDER_ITEM_SCHEMA = "schema.ftgo.order.persistence.models.order-item.orderitem"
ORDERS_COLLECTION = "collection.ftgo.order.orders"
ORDER_ITEMS_COLLECTION = "collection.ftgo.order.order-items"


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
    from knowledge_plane.extractors.data_model import extract_data_model

    return extract_data_model(make_record(build_repository(tmp_path / "repo")), FROZEN_COMMIT)


def tables_by_id(extraction) -> dict[str, object]:
    return {item.id: item for item in extraction.tables}


def columns_of(extraction, identifier: str) -> dict[str, object]:
    return {
        item.column.name: item.column
        for item in extraction.columns
        if item.table_id == identifier
    }


def accesses(extraction, role: str) -> set[tuple[str, str]]:
    return {
        (item.service, item.target) for item in extraction.accesses if item.role == role
    }


# --------------------------------------------------------------------------------------
# 1-2. Library detection rooted in imports
# --------------------------------------------------------------------------------------


def test_relational_library_is_detected_from_imports(extraction) -> None:
    assert "sqlalchemy" in extraction.libraries
    assert "asyncpg_client" in extraction.libraries
    scans = {scan.slug: scan for scan in extraction.services_scanned}
    assert "sqlalchemy" in scans["user"].libraries


def test_document_library_is_detected_from_imports(extraction) -> None:
    assert "beanie" in extraction.libraries
    assert "pymongo" in extraction.libraries
    assert "mongo_motors" in extraction.libraries
    scans = {scan.slug: scan for scan in extraction.services_scanned}
    assert "beanie" in scans["order"].libraries


def test_service_without_persistence_reports_none(extraction) -> None:
    scans = {scan.slug: scan for scan in extraction.services_scanned}
    assert scans["gateway"].libraries == ()
    assert scans["gateway"].tables == 0
    assert scans["gateway"].document_models == 0
    assert any("no persistence library import found" in item for item in extraction.warnings)


# --------------------------------------------------------------------------------------
# 3-4. Non-persistence classes are not models
# --------------------------------------------------------------------------------------


def test_pydantic_api_schema_is_not_a_persistence_model(extraction) -> None:
    titles = {item.title for item in extraction.tables} | {
        item.title for item in extraction.document_schemas
    }
    assert "ProfileRequest" not in titles
    assert not any("profilerequest" in item.id for item in extraction.document_schemas)


def test_domain_dataclass_is_not_a_persistence_model(extraction) -> None:
    titles = {item.title for item in extraction.tables} | {
        item.title for item in extraction.document_schemas
    }
    assert "ProfileDomain" not in titles
    assert "ProfileDTO" not in titles
    assert "InMemoryStore" not in titles


# --------------------------------------------------------------------------------------
# 5-9. Relational structure
# --------------------------------------------------------------------------------------


def test_tables_come_from_explicit_tablenames(extraction) -> None:
    identifiers = set(tables_by_id(extraction))

    assert identifiers == {USER_PROFILE_TABLE, CUSTOMER_ADDRESS_TABLE, DRIVER_LOCATION_TABLE}
    assert table_id("ftgo", "user", "user_profile") == USER_PROFILE_TABLE
    profile = tables_by_id(extraction)[USER_PROFILE_TABLE]
    assert profile.table_name == "user_profile"
    assert profile.library == "sqlalchemy"
    assert profile.engine == "postgresql"
    # The abstract declarative base is not a physical table.
    assert not any(item.model_class.endswith(".Base") for item in extraction.tables)


def test_dynamic_table_name_is_reported_not_invented(extraction) -> None:
    unresolved = extraction.unresolved_of("unresolved_table_names")

    assert any("AuditLog" in item.subject for item in unresolved)
    assert not any("audit" in item.id for item in extraction.tables)


def test_columns_include_inherited_base_columns(extraction) -> None:
    columns = columns_of(extraction, USER_PROFILE_TABLE)

    assert {"id", "created_at", "phone_number", "hashed_password", "national_id"} <= set(columns)
    inherited = next(
        item
        for item in extraction.columns
        if item.table_id == USER_PROFILE_TABLE and item.column.name == "id"
    )
    # Provenance points at the base class that actually declares the column.
    assert inherited.provenance.source_path.endswith("models/base.py")
    assert inherited.declaring_class.endswith("Base")


def test_primary_key_is_extracted(extraction) -> None:
    profile = tables_by_id(extraction)[USER_PROFILE_TABLE]

    assert profile.primary_key == ("id",)
    assert columns_of(extraction, USER_PROFILE_TABLE)["id"].primary_key is True


def test_foreign_key_is_extracted_and_becomes_a_table_dependency(extraction) -> None:
    address = tables_by_id(extraction)[CUSTOMER_ADDRESS_TABLE]

    assert address.foreign_keys == ({"column": "user_id", "references": "user_profile.id"},)
    edges = {
        (item.source, item.target)
        for item in extraction.relationships
        if item.type == "DEPENDS_ON"
    }
    assert (CUSTOMER_ADDRESS_TABLE, USER_PROFILE_TABLE) in edges


def test_nullable_unique_and_index_metadata_is_captured(extraction) -> None:
    columns = columns_of(extraction, USER_PROFILE_TABLE)

    assert columns["phone_number"].nullable is False
    assert columns["phone_number"].unique is True
    assert columns["national_id"].nullable is True
    assert columns["national_id"].indexed is True
    assert columns["id"].has_default is True
    assert columns["created_at"].has_server_default is True
    # Table-level rollups agree with the column metadata.
    profile = tables_by_id(extraction)[USER_PROFILE_TABLE]
    assert profile.unique_columns == ("phone_number",)
    assert profile.indexed_columns == ("national_id",)


def test_table_contains_column_relationships_are_generated(extraction) -> None:
    contained = {
        item.target
        for item in extraction.relationships
        if item.type == "CONTAINS" and item.source == USER_PROFILE_TABLE
    }

    assert "column.ftgo.user.user-profile.phone-number" in contained
    assert len(contained) == len(columns_of(extraction, USER_PROFILE_TABLE))


# --------------------------------------------------------------------------------------
# 10-12. Document models
# --------------------------------------------------------------------------------------


def test_document_models_are_extracted_as_persistence_schemas(extraction) -> None:
    schemas = {item.id: item for item in extraction.document_schemas}

    assert ORDER_SCHEMA in schemas
    order = schemas[ORDER_SCHEMA]
    assert order.kind == "Schema"
    assert order.library == "beanie"
    assert order.engine == "mongodb"
    assert order.attributes["persistence_role"] == "document_model"
    fields = {item.name for item in order.fields}
    assert {"customer_id", "total_amount", "order_items", "payment_id"} <= fields
    # No Column entity is ever created for a document field.
    assert not any(item.table_name == "orders" for item in extraction.columns)


def test_explicit_collection_name_and_indexes_are_captured(extraction) -> None:
    schemas = {item.id: item for item in extraction.document_schemas}

    assert schemas[ORDER_SCHEMA].collection_name == "orders"
    assert schemas[ORDER_ITEM_SCHEMA].collection_name == "order_items"
    assert schemas[ORDER_SCHEMA].declared_indexes == ("order_customer_id_index",)


# --------------------------------------------------------------------------------------
# Collection: the approved first-class document-persistence kind
# --------------------------------------------------------------------------------------


def test_collection_is_an_allowed_ontology_kind() -> None:
    allowed = set(
        yaml.safe_load((AIDE_ROOT / "ontology/entity-types.yaml").read_text(encoding="utf-8"))[
            "entity_types"
        ]
    )

    assert "Collection" in allowed


def test_collection_candidates_are_generated_for_proven_collection_names(extraction) -> None:
    collections = {item.id: item for item in extraction.collections}

    assert set(collections) == {ORDERS_COLLECTION, ORDER_ITEMS_COLLECTION}
    orders = collections[ORDERS_COLLECTION]
    assert orders.kind == "Collection"
    assert orders.collection_name == "orders"
    assert orders.service == "order"
    assert orders.library == "beanie"
    assert orders.engine == "mongodb"
    assert orders.schema_id == ORDER_SCHEMA
    assert orders.declared_indexes == ("order_customer_id_index",)


def test_collection_ids_are_deterministic() -> None:
    assert collection_id("ftgo", "order", "orders") == ORDERS_COLLECTION
    assert collection_id("ftgo", "order", "order_items") == ORDER_ITEMS_COLLECTION
    assert collection_id("ftgo", "feedback", "delivery_ratings") == (
        "collection.ftgo.feedback.delivery-ratings"
    )
    # Repeating the call cannot introduce a hash or counter.
    assert collection_id("ftgo", "order", "orders") == collection_id("ftgo", "order", "orders")


def test_database_contains_collection(extraction) -> None:
    contains = {
        (item.source, item.target)
        for item in extraction.relationships
        if item.type == "CONTAINS"
    }

    assert ("database.ftgo.order-mongo", ORDERS_COLLECTION) in contains
    assert ("database.ftgo.order-mongo", ORDER_ITEMS_COLLECTION) in contains
    # The Schema is no longer contained directly by the Database.
    assert ("database.ftgo.order-mongo", ORDER_SCHEMA) not in contains
    assert {item.id: item.database for item in extraction.collections}[ORDERS_COLLECTION] == (
        "database.ftgo.order-mongo"
    )


def test_collection_uses_schema(extraction) -> None:
    uses = {
        (item.source, item.target)
        for item in extraction.relationships
        if item.type == "USES_SCHEMA"
    }

    assert (ORDERS_COLLECTION, ORDER_SCHEMA) in uses
    assert (ORDER_ITEMS_COLLECTION, ORDER_ITEM_SCHEMA) in uses
    relation = next(
        item
        for item in extraction.relationships
        if item.type == "USES_SCHEMA" and item.source == ORDERS_COLLECTION
    )
    assert relation.detail["persistence_role"] == "document_model"
    assert relation.provenance.commit == FROZEN_COMMIT


def test_relational_side_keeps_its_shape(extraction) -> None:
    contains = {
        (item.source, item.target)
        for item in extraction.relationships
        if item.type == "CONTAINS"
    }

    assert ("database.ftgo.user-postgres", USER_PROFILE_TABLE) in contains
    assert (USER_PROFILE_TABLE, "column.ftgo.user.user-profile.phone-number") in contains
    # A Table never uses a Schema; only a Collection does.
    assert not any(
        item.type == "USES_SCHEMA" and item.source.startswith("table.")
        for item in extraction.relationships
    )


def test_explicit_document_reference_is_captured(extraction) -> None:
    order = next(item for item in extraction.document_schemas if item.id == ORDER_SCHEMA)

    assert any("OrderItem" in reference for reference in order.references)
    items_field = next(item for item in order.fields if item.name == "order_items")
    assert items_field.references == ("OrderItem",)


def test_dynamic_collection_name_creates_no_collection_and_is_reported(extraction) -> None:
    unresolved = extraction.unresolved_of("unresolved_collection_names")

    assert any("ArchivedOrder" in item.subject for item in unresolved)
    archived = next(
        item for item in extraction.document_schemas if item.title == "ArchivedOrder"
    )
    assert archived.collection_name is None
    # No Collection is invented, and nothing contains the Schema either.
    assert not any("archive" in item.id for item in extraction.collections)
    assert not any(
        item.target == archived.id and item.type == "CONTAINS"
        for item in extraction.relationships
    )
    # The table-name category is not reused for a collection finding.
    assert not any(
        "ArchivedOrder" in item.subject
        for item in extraction.unresolved_of("unresolved_table_names")
    )


# --------------------------------------------------------------------------------------
# 13-15. Ownership and database mapping
# --------------------------------------------------------------------------------------


def test_service_ownership_comes_from_the_source_path(extraction) -> None:
    scans = {scan.slug: scan for scan in extraction.services_scanned}

    assert set(scans) == {"gateway", "location", "order", "user"}
    for scan in extraction.services_scanned:
        assert scan.entity_id in PASS_ONE_SERVICE_IDS
    assert tables_by_id(extraction)[USER_PROFILE_TABLE].service == "user"
    assert tables_by_id(extraction)[DRIVER_LOCATION_TABLE].service == "location"


def test_database_mapping_is_derived_from_compose_evidence(extraction) -> None:
    mappings = {item.service: item for item in extraction.database_mappings}

    assert mappings["user"].database == "database.ftgo.user-postgres"
    assert mappings["user"].engine == "postgresql"
    assert mappings["order"].database == "database.ftgo.order-mongo"
    assert mappings["order"].engine == "mongodb"
    # The mapping flows through to the entities and to Database -CONTAINS-> Table.
    assert tables_by_id(extraction)[USER_PROFILE_TABLE].database == "database.ftgo.user-postgres"
    contains = {
        (item.source, item.target)
        for item in extraction.relationships
        if item.type == "CONTAINS"
    }
    assert ("database.ftgo.user-postgres", USER_PROFILE_TABLE) in contains
    assert ("database.ftgo.order-mongo", ORDERS_COLLECTION) in contains


def test_unmappable_database_is_reported_and_no_duplicate_is_created(extraction) -> None:
    unresolved = extraction.unresolved_of("unresolved_database_mappings")

    assert any(item.subject.startswith("location") for item in unresolved)
    assert tables_by_id(extraction)[DRIVER_LOCATION_TABLE].database is None
    # No Database entity is invented for the unmapped service.
    assert not any(
        item.source.startswith("database.ftgo.location")
        for item in extraction.relationships
    )


# --------------------------------------------------------------------------------------
# 16-20. Access relationships
# --------------------------------------------------------------------------------------


def test_relational_read_relation_is_source_backed(extraction) -> None:
    reads = accesses(extraction, "read")

    assert ("service.ftgo.user", USER_PROFILE_TABLE) in reads
    assert ("service.ftgo.user", CUSTOMER_ADDRESS_TABLE) in reads
    relation = next(
        item
        for item in extraction.relationships
        if item.type == "READS" and item.target == USER_PROFILE_TABLE
    )
    assert relation.source == "service.ftgo.user"
    assert relation.detail["persistence_library"] == "sqlalchemy"


def test_relational_write_relation_is_source_backed(extraction) -> None:
    writes = accesses(extraction, "write")

    assert ("service.ftgo.user", USER_PROFILE_TABLE) in writes
    operations = {
        site.operation
        for item in extraction.accesses
        if item.role == "write" and item.target == USER_PROFILE_TABLE
        for site in item.call_sites
    }
    assert "add_all" in operations


def test_service_reads_and_writes_the_collection_not_the_schema(extraction) -> None:
    assert ("service.ftgo.order", ORDERS_COLLECTION) in accesses(extraction, "read")
    assert ("service.ftgo.order", ORDERS_COLLECTION) in accesses(extraction, "write")
    write = next(
        item
        for item in extraction.accesses
        if item.role == "write" and item.target == ORDERS_COLLECTION
    )
    assert write.library == "beanie"
    assert write.target_kind == "Collection"
    assert {site.operation for site in write.call_sites} == {"insert"}


def test_no_duplicate_service_access_edge_to_the_schema(extraction) -> None:
    schema_ids = {item.id for item in extraction.document_schemas}

    # Every document access resolves to the Collection; the Schema is reached only through
    # Collection -USES_SCHEMA-> Schema.
    assert not any(item.target in schema_ids for item in extraction.accesses)
    assert not any(
        item.type in ("READS", "WRITES") and item.target in schema_ids
        for item in extraction.relationships
    )
    inbound_types = {
        item.type for item in extraction.relationships if item.target == ORDER_SCHEMA
    }
    assert inbound_types == {"USES_SCHEMA"}


def test_generic_get_save_delete_methods_are_rejected(extraction) -> None:
    # InMemoryStore/CacheService expose get_order, save, delete and even select, but none of
    # them roots in a persistence library.
    for item in extraction.accesses:
        for site in item.call_sites:
            assert "schemas.py" not in site.path
    assert not any(
        "schemas.py" in (item.provenance.source_path if item.provenance else "")
        for item in extraction.unresolved_of("unresolved_accesses")
    )
    assert not any("inmemorystore" in item.id for item in extraction.tables)


def test_wrapper_tracing_resolves_the_model_from_the_call_site(extraction) -> None:
    assert any(
        symbol.endswith("GenericRepository.load") for symbol in extraction.wrappers
    )
    read = next(
        item
        for item in extraction.accesses
        if item.role == "read" and item.target == USER_PROFILE_TABLE
    )
    resolutions = {site.resolution for site in read.call_sites}
    assert "wrapper_argument" in resolutions or "model_map_enumeration" in resolutions
    # The application call site is retained, not just the repository implementation.
    assert any("application/profile.py" in site.path for site in read.call_sites)


def test_duplicate_call_sites_collapse_to_one_relation(extraction) -> None:
    relations = [
        item
        for item in extraction.relationships
        if item.type == "READS" and item.target == ORDERS_COLLECTION
    ]

    # Two identical reads in application/order.py, one semantic relationship.
    assert len(relations) == 1
    access = next(
        item
        for item in extraction.accesses
        if item.role == "read" and item.target == ORDERS_COLLECTION
    )
    assert len(access.call_sites) >= 2
    assert relations[0].detail["call_site_count"] == len(access.call_sites)


def test_no_endpoint_or_event_edges_are_created(extraction) -> None:
    for relation in extraction.relationships:
        assert not relation.source.startswith(("endpoint.", "event."))
        assert not relation.target.startswith(("endpoint.", "event."))


# --------------------------------------------------------------------------------------
# 21-24. Provenance, secrets, and static-analysis guarantees
# --------------------------------------------------------------------------------------


def test_every_entity_carries_full_provenance(extraction) -> None:
    entities = (
        list(extraction.tables)
        + list(extraction.columns)
        + list(extraction.document_schemas)
        + list(extraction.migrations)
    )

    assert entities
    for entity in entities:
        provenance = entity.provenance
        assert provenance.repository == "ftgo"
        assert provenance.commit == FROZEN_COMMIT
        assert provenance.evidence_type == "implemented"
        assert provenance.source_path.endswith(".py")
        assert not Path(provenance.source_path).is_absolute()
        assert provenance.symbol
        assert provenance.line_start is not None and provenance.line_start > 0


def test_access_relations_retain_every_call_site_with_provenance(extraction) -> None:
    for access in extraction.accesses:
        assert access.call_sites
        for site in access.call_sites:
            assert site.provenance.commit == FROZEN_COMMIT
            assert site.provenance.source_path.endswith(".py")
            assert site.provenance.line_start
            assert site.operation


def test_connection_credentials_are_never_emitted(extraction) -> None:
    rendered, report = render_bundle(extraction)
    blob = "\n".join(rendered.values()) + json.dumps(report)

    for secret in FIXTURE_SECRETS:
        assert secret not in blob, f"secret {secret!r} leaked into candidate output"
    assert report["secret_values_emitted"] == 0
    # A domain column named hashed_password still appears, without any value.
    assert "hashed_password" in blob


def test_sensitive_name_detection_spares_domain_columns() -> None:
    assert is_sensitive_name("password")
    assert is_sensitive_name("DB_PASSWORD")
    assert is_sensitive_name("secret_key")
    assert is_sensitive_name("dsn")
    assert is_sensitive_name("url")
    # Ambiguous words are sensitive only as whole names, so ordinary domain columns are not
    # swept up. Column *names* are always emitted either way; this governs only whether a
    # literal bound to the name is treated as a credential.
    assert not is_sensitive_name("user_id")
    assert not is_sensitive_name("owner_user_id")
    assert not is_sensitive_name("restaurant_licence_id")
    assert not is_sensitive_name("menu_item_id")
    assert not is_sensitive_name("national_id")


def test_no_fixture_module_is_imported_or_executed(extraction) -> None:
    _, report = render_bundle(extraction)

    assert report["analysis"] == "python-ast/static"
    assert report["modules_imported"] == 0
    assert report["modules_executed"] == 0
    assert report["database_connections_opened"] == 0
    for module_name in ("data_access.models.profile", "models.order", "dto"):
        assert module_name not in sys.modules


def test_out_of_scope_trees_never_contribute(extraction) -> None:
    joined = " ".join(extraction.source_files)

    assert "tests/" not in joined
    assert "__pycache__" not in joined
    assert "test directory" in skip_reason("backend/microservices/user/src/tests/test_x.py")
    assert "src and migrations" in skip_reason("backend/microservices/user/docs/notes.py")
    # Migrations are deliberately in scope for this pass.
    assert skip_reason("backend/microservices/user/migrations/versions/aaa111_initial.py") is None


# --------------------------------------------------------------------------------------
# Migrations and ontology
# --------------------------------------------------------------------------------------


def test_migrations_are_extracted_with_their_own_revision_identity(extraction) -> None:
    assert len(extraction.migrations) == 1
    migration = extraction.migrations[0]

    assert migration.id == "migration.ftgo.user.aaa111bbb222"
    assert migration.revision == "aaa111bbb222"
    assert migration.tool == "alembic"
    assert "user_profile" in migration.touched_tables
    changed_by = {
        (item.source, item.target)
        for item in extraction.relationships
        if item.type == "CHANGED_BY"
    }
    assert (USER_PROFILE_TABLE, migration.id) in changed_by


def test_migration_table_that_does_not_exist_is_reported(extraction) -> None:
    unresolved = extraction.unresolved_of("unresolved_model_references")

    assert any("unknown_table" in item.subject for item in unresolved)


def test_the_collection_ontology_gap_is_resolved_and_no_longer_reported(extraction) -> None:
    _, report = render_bundle(extraction)

    assert [item.requested_kind for item in extraction.ontology_gaps] == []
    assert report["ontology_gaps"] == []
    assert report["counts"]["ontology_gaps"] == 0


def test_only_approved_entity_kinds_are_emitted(extraction) -> None:
    allowed = set(
        yaml.safe_load((AIDE_ROOT / "ontology/entity-types.yaml").read_text(encoding="utf-8"))[
            "entity_types"
        ]
    )
    emitted = (
        {item.kind for item in extraction.tables}
        | {item.kind for item in extraction.columns}
        | {item.kind for item in extraction.collections}
        | {item.kind for item in extraction.document_schemas}
        | {item.kind for item in extraction.migrations}
    )

    assert emitted <= allowed
    assert emitted == {"Table", "Column", "Collection", "Schema", "Migration"}


def test_document_fields_never_become_column_entities(extraction) -> None:
    # Mongo field names must not leak into the relational Column space.
    column_names = {item.column.name for item in extraction.columns}
    relational_tables = {item.table_name for item in extraction.tables}

    assert "orders" not in relational_tables
    assert "order_items" not in relational_tables
    assert not any(item.table_name in ("orders", "order_items") for item in extraction.columns)
    assert "total_amount" not in column_names
    assert "customer_id" not in column_names
    # Document fields stay structured attributes on the Schema.
    order = next(item for item in extraction.document_schemas if item.id == ORDER_SCHEMA)
    assert {"customer_id", "total_amount"} <= {field.name for field in order.fields}


def test_only_approved_relationship_types_are_emitted(extraction) -> None:
    document = yaml.safe_load(
        (AIDE_ROOT / "ontology/relationship-types.yaml").read_text(encoding="utf-8")
    )
    allowed = {item["type"] for item in document["relationship_types"]}
    emitted = {item.type for item in extraction.relationships}

    assert emitted <= allowed
    assert emitted <= {"CONTAINS", "DEPENDS_ON", "USES_SCHEMA", "READS", "WRITES", "CHANGED_BY"}


def test_identity_collision_is_reported_and_no_entity_is_created(tmp_path: Path) -> None:
    from knowledge_plane.extractors.data_model import extract_data_model

    files = dict(FIXTURE_FILES)
    files["backend/microservices/user/src/data_access/models/duplicate.py"] = '''\
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from data_access.models.base import Base


class ProfileCopy(Base):
    __tablename__ = "USER_PROFILE"

    nickname: Mapped[str] = mapped_column(String, nullable=True)
'''
    result = extract_data_model(
        make_record(build_repository(tmp_path / "repo", files)), FROZEN_COMMIT
    )

    collisions = {item.entity_id: item for item in result.identity_collisions}
    assert USER_PROFILE_TABLE in collisions
    assert len(collisions[USER_PROFILE_TABLE].participants) == 2
    assert USER_PROFILE_TABLE not in tables_by_id(result)


# --------------------------------------------------------------------------------------
# 25-28. CLI behaviour
# --------------------------------------------------------------------------------------


def test_dry_run_writes_nothing(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    manifest = write_manifest(tmp_path, build_repository(tmp_path / "repo"))
    output_dir = tmp_path / "candidates"
    monkeypatch.setattr("knowledge_plane.extract.read_git_head", lambda path: FROZEN_COMMIT)

    summary = run("ftgo", "data-model", manifest_path=manifest, output_dir=output_dir, dry_run=True)

    assert summary["status"] == "dry-run"
    assert summary["dry_run"] is True
    assert summary["commit_verified"] is True
    assert summary["analysis"] == "python-ast/static"
    assert summary["modules_imported"] == 0
    assert summary["modules_executed"] == 0
    assert summary["database_connections_opened"] == 0
    assert summary["secret_values_emitted"] == 0
    assert summary["graph_mutations"] == 0
    assert summary["wiki_writes"] == 0
    assert summary["neo4j_mutations"] == 0
    assert summary["graphiti"] == "disabled"
    assert summary["counts"]["tables"] == 3
    assert not output_dir.exists()


def test_normal_run_writes_only_the_candidate_tree(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    repo_root = build_repository(tmp_path / "repo")
    manifest = write_manifest(tmp_path, repo_root)
    output_dir = tmp_path / "candidates"
    monkeypatch.setattr("knowledge_plane.extract.read_git_head", lambda path: FROZEN_COMMIT)
    before = {
        path: path.read_bytes() for path in sorted(repo_root.rglob("*")) if path.is_file()
    }

    summary = run("ftgo", "data-model", manifest_path=manifest, output_dir=output_dir)

    assert summary["status"] == "ok"
    assert (output_dir / "extraction-report.json").is_file()
    assert (output_dir / DATABASE_DELTAS_FILENAME).is_file()
    assert (output_dir / SERVICE_DELTAS_FILENAME).is_file()
    assert len(list((output_dir / "tables").glob("*.md"))) == 3
    assert len(list((output_dir / "schemas").glob("*.md"))) == 3
    assert len(list((output_dir / "collections").glob("*.md"))) == 2
    assert len(list((output_dir / "migrations").glob("*.md"))) == 1
    assert list((output_dir / "columns").glob("*.md"))
    # The inspected repository is untouched.
    after = {path: path.read_bytes() for path in sorted(repo_root.rglob("*")) if path.is_file()}
    assert after == before

    report = json.loads((output_dir / "extraction-report.json").read_text(encoding="utf-8"))
    assert report["commit"] == FROZEN_COMMIT
    assert report["secret_values_emitted"] == 0
    assert report["graph_mutations"] == 0


def test_candidate_pages_are_never_approved(extraction) -> None:
    rendered, _ = render_bundle(extraction)

    assert rendered
    for path, content in rendered.items():
        frontmatter = yaml.safe_load(content.split("---")[1])
        assert frontmatter["status"] == "candidate"
        assert frontmatter["review_status"] == "pending"
        assert frontmatter["kind"] == frontmatter["type"]
        assert "status: approved" not in content
        assert path.startswith(
            ("tables/", "columns/", "collections/", "schemas/", "migrations/")
        )


def test_no_duplicate_service_or_database_pages_are_written(extraction) -> None:
    rendered, _ = render_bundle(extraction)

    assert not any("service.ftgo" in path for path in rendered)
    assert not any("database.ftgo" in path for path in rendered)


def test_delta_files_carry_relations_for_existing_pages(extraction) -> None:
    database_deltas = build_database_relation_deltas(extraction)
    service_deltas = build_service_relation_deltas(extraction)

    assert database_deltas["review_status"] == "pending"
    assert "not canonical knowledge" in database_deltas["note"]
    assert {item["database"] for item in database_deltas["databases"]} == {
        "database.ftgo.user-postgres",
        "database.ftgo.order-mongo",
    }
    assert "not canonical knowledge" in service_deltas["note"]
    services = {item["service"] for item in service_deltas["services"]}
    assert services <= PASS_ONE_SERVICE_IDS
    for entry in service_deltas["services"]:
        assert {relation["type"] for relation in entry["relations"]} <= {"READS", "WRITES"}


def test_commit_mismatch_aborts_before_writing_anything(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    manifest = write_manifest(tmp_path, build_repository(tmp_path / "repo"))
    output_dir = tmp_path / "candidates"
    monkeypatch.setattr("knowledge_plane.extract.read_git_head", lambda path: WRONG_COMMIT)

    with pytest.raises(CommitMismatchError) as excinfo:
        run("ftgo", "data-model", manifest_path=manifest, output_dir=output_dir, dry_run=False)

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

    run("ftgo", "data-model", manifest_path=manifest, output_dir=first)
    run("ftgo", "data-model", manifest_path=manifest, output_dir=second)

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
    foreign = output_dir / "events" / "event.ftgo.rabbitmq.order.create.md"
    foreign.parent.mkdir(parents=True, exist_ok=True)
    foreign.write_text("owned by the rabbitmq pass", encoding="utf-8")

    run("ftgo", "data-model", manifest_path=manifest, output_dir=output_dir)
    orphan = output_dir / "tables" / "table.ftgo.user.retired.md"
    orphan.write_text("stale", encoding="utf-8")
    run("ftgo", "data-model", manifest_path=manifest, output_dir=output_dir)

    assert not orphan.exists()
    assert foreign.read_text(encoding="utf-8") == "owned by the rabbitmq pass"


def test_other_extractor_kinds_still_work(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    # Pass 4 must not change compose behaviour.
    manifest = write_manifest(tmp_path, build_repository(tmp_path / "repo"))
    monkeypatch.setattr("knowledge_plane.extract.read_git_head", lambda path: FROZEN_COMMIT)

    summary = run("ftgo", "compose", manifest_path=manifest, dry_run=True)

    assert summary["status"] == "dry-run"
    assert "database.ftgo.user-postgres" in summary["infrastructure_entities"]


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
    from knowledge_plane.extractors.data_model import extract_data_model

    record = _real_ftgo_record()
    if record is None:
        pytest.skip("FTGO checkout at the frozen commit is not available")
    return extract_data_model(record, FROZEN_COMMIT)


def test_real_ftgo_persistence_stack(real_extraction) -> None:
    assert {"sqlalchemy", "beanie", "pymongo", "alembic"} <= set(real_extraction.libraries)
    assert real_extraction.identity_collisions == ()


def test_real_ftgo_tables_and_documents(real_extraction) -> None:
    tables = {item.table_name for item in real_extraction.tables}

    assert tables == {
        "user_profile",
        "customer_address",
        "vehicle_info",
        "driver_location",
        "supplier_profile",
        "menu_item",
    }
    assert real_extraction.columns


def test_real_ftgo_collections_match_the_approved_identities(real_extraction) -> None:
    # These six ids are the exact collection names the extractor proved from source.
    assert {item.id for item in real_extraction.collections} == {
        "collection.ftgo.feedback.delivery-ratings",
        "collection.ftgo.feedback.order-ratings",
        "collection.ftgo.order.delivery-details",
        "collection.ftgo.order.order-items",
        "collection.ftgo.order.order-status",
        "collection.ftgo.order.orders",
    }
    assert {item.collection_name for item in real_extraction.collections} == {
        "delivery_ratings",
        "order_ratings",
        "delivery_details",
        "order_items",
        "order_status",
        "orders",
    }
    # Every Collection is contained by its mapped Database and uses its document Schema.
    schema_ids = {item.id for item in real_extraction.document_schemas}
    assert len(real_extraction.document_schemas) == 6
    for collection in real_extraction.collections:
        assert collection.database in (
            "database.ftgo.order-mongo",
            "database.ftgo.feedback-mongo",
        )
        assert collection.schema_id in schema_ids
    contains = {
        (item.source, item.target)
        for item in real_extraction.relationships
        if item.type == "CONTAINS"
    }
    uses = {
        (item.source, item.target)
        for item in real_extraction.relationships
        if item.type == "USES_SCHEMA"
    }
    assert ("database.ftgo.order-mongo", "collection.ftgo.order.orders") in contains
    assert len(uses) == 6
    assert real_extraction.unresolved_of("unresolved_collection_names") == ()


def test_real_ftgo_database_mappings_are_all_resolved(real_extraction) -> None:
    mappings = {item.service: item.database for item in real_extraction.database_mappings}

    assert mappings == {
        "user": "database.ftgo.user-postgres",
        "location": "database.ftgo.location-postgres",
        "restaurant": "database.ftgo.restaurant-postgres",
        "order": "database.ftgo.order-mongo",
        "feedback": "database.ftgo.feedback-mongo",
    }
    assert real_extraction.unresolved_of("unresolved_database_mappings") == ()


def test_real_ftgo_foreign_keys_and_accesses(real_extraction) -> None:
    edges = {
        (item.source, item.target)
        for item in real_extraction.relationships
        if item.type == "DEPENDS_ON"
    }
    assert ("table.ftgo.user.customer-address", "table.ftgo.user.user-profile") in edges
    assert ("table.ftgo.restaurant.menu-item", "table.ftgo.restaurant.supplier-profile") in edges

    reads = {
        (item.service, item.target) for item in real_extraction.accesses if item.role == "read"
    }
    writes = {
        (item.service, item.target) for item in real_extraction.accesses if item.role == "write"
    }
    assert ("service.ftgo.user", "table.ftgo.user.user-profile") in reads
    assert ("service.ftgo.user", "table.ftgo.user.user-profile") in writes
    # Document accesses land on the Collection, never on the Schema.
    assert ("service.ftgo.order", "collection.ftgo.order.orders") in writes
    assert ("service.ftgo.feedback", "collection.ftgo.feedback.delivery-ratings") in reads
    schema_ids = {item.id for item in real_extraction.document_schemas}
    assert not (reads | writes) & schema_ids


def test_real_ftgo_gateway_uses_cache_only_and_owns_no_data_model(real_extraction) -> None:
    assert not any(item.service == "gateway" for item in real_extraction.tables)
    assert not any(item.service == "gateway" for item in real_extraction.document_schemas)

    scans = {scan.slug: scan for scan in real_extraction.services_scanned}
    # The gateway caches through Redis but persists nothing, so the library is reported while
    # no entity is created: the ontology has no cache kind.
    assert "aredis_client" in scans["gateway"].libraries
    assert "aredis_client" in real_extraction.libraries
    assert scans["gateway"].database is None
    assert any(
        "no relational or document model is declared" in item and "gateway" in item
        for item in real_extraction.warnings
    )


def test_real_ftgo_emits_no_secret_values(real_extraction) -> None:
    rendered, report = render_bundle(real_extraction)
    blob = "\n".join(rendered.values()) + json.dumps(report)

    assert report["secret_values_emitted"] == 0
    for secret in ("user_password", "order_password", "feedback_password"):
        assert secret not in blob
    assert report["graph_mutations"] == 0
    assert report["neo4j_mutations"] == 0
    assert report["graphiti"] == "disabled"


def test_real_ftgo_has_no_remaining_ontology_gap(real_extraction) -> None:
    assert real_extraction.ontology_gaps == ()


def test_real_ftgo_keeps_the_unrelated_unresolved_findings(real_extraction) -> None:
    # Resolving the Collection gap must not quietly resolve anything else: the two
    # restaurant repository accesses whose model arrives as an untraced parameter stay open.
    unresolved = real_extraction.unresolved_of("unresolved_accesses")

    assert len(unresolved) == 2
    assert all("restaurant" in (item.service or "") for item in unresolved)


def test_real_ftgo_extraction_is_deterministic(real_extraction) -> None:
    from knowledge_plane.extractors.data_model import extract_data_model

    record = _real_ftgo_record()
    assert record is not None
    repeated = extract_data_model(record, FROZEN_COMMIT)

    first, _ = render_bundle(real_extraction)
    second, _ = render_bundle(repeated)
    assert first.keys() == second.keys()
    for key in first:
        assert first[key] == second[key], f"{key} differs between identical runs"


def test_classify_model_requires_a_library_base(tmp_path: Path) -> None:
    """Direct check of the rooting rule the whole pass depends on."""
    import ast

    from knowledge_plane.extractors.data_model import analyze_module, build_source_index

    sources = {
        "models": (
            "from sqlalchemy.orm import DeclarativeBase\n"
            "from pydantic import BaseModel\n"
            "\n"
            "class Mapped(DeclarativeBase):\n"
            "    __tablename__ = 't'\n"
            "\n"
            "class ApiSchema(BaseModel):\n"
            "    field: str\n"
            "\n"
            "class Plain:\n"
            "    field = 1\n"
        )
    }
    del tmp_path
    modules = []
    warnings: list[str] = []
    for module, text in sources.items():
        modules.append(
            analyze_module(
                text,
                ast.parse(text),
                relative_path=f"backend/microservices/user/src/{module}.py",
                service="user",
                service_root="backend/microservices/user",
                module=module,
                is_package=False,
                warnings=warnings,
            )
        )
    index = build_source_index(modules)

    assert classify_model(index, "user", "models", "Mapped") is not None
    assert classify_model(index, "user", "models", "Mapped").role == "relational_table"
    # Pydantic is not a persistence library and a bare class has no library base at all.
    assert classify_model(index, "user", "models", "ApiSchema") is None
    assert classify_model(index, "user", "models", "Plain") is None
