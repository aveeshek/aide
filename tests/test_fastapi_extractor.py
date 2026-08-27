"""Deterministic tests for the FastAPI extractor (Graph Engineering Pass 2).

The fixture is a synthetic repository that mirrors the FTGO layout and exercises every
construct this pass claims to support, including the ones FTGO itself does not contain
(path parameters, ``PATCH``/``OPTIONS``/``HEAD``, statically resolvable mount prefixes).
The suite is hermetic and runs without the FTGO checkout present. Opt-in tests at the end
verify the same guarantees against the real frozen FTGO repository when it is available.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest
import yaml

from knowledge_plane.extract import run
from knowledge_plane.extractors.fastapi import (
    endpoint_id,
    endpoint_path_tokens,
    extract_fastapi,
    is_generated_source,
    join_route_path,
    module_dotted_name,
    normalize_path_segment,
    render_bundle,
    schema_id,
    service_location,
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

# Secret values present in the fixture. None may appear in generated output.
FIXTURE_SECRETS = (
    "super-secret-token-value",
    "another-secret-value",
    "leaked-token-value",
)

GATEWAY_MAIN = '''\
from fastapi import FastAPI

from application.app import init_router
from application.schemas.common import HealthResponse

app = FastAPI(title="Fixture Gateway")
app.include_router(init_router(), prefix="/api/v1")


@app.get("/health", response_model=HealthResponse)
async def health():
    return HealthResponse()
'''

GATEWAY_APP = '''\
from fastapi import APIRouter
from third_party.routers import external_router

from application.routes.order import order_router
from application.routes.user import user_router


def init_router() -> APIRouter:
    router = APIRouter()
    router.include_router(order_router, prefix="/v2")
    router.include_router(user_router)
    router.include_router(external_router)
    return router
'''

ORDER_ROUTES = '''\
from typing import Annotated, Optional

from fastapi import APIRouter, Depends, Request, status

from application.dependencies import AccessManager
from application.schemas.common import SuccessResponse
from application.schemas.order import CreateOrderRequest, OrderFilters, OrderSummary

ROUTE_PATH = "/computed"

router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("/", response_model=SuccessResponse, status_code=status.HTTP_201_CREATED)
async def create_order(request: Request, payload: CreateOrderRequest):
    return SuccessResponse()


@router.post("/bulk", response_model=SuccessResponse, status_code=201)
async def bulk_create(
    request: Request,
    payload: CreateOrderRequest,
    actor: AccessManager = Depends(AccessManager),
):
    return SuccessResponse()


@router.get("/list", response_model=list[OrderSummary])
async def list_orders(request: Request, limit: int = 10):
    return []


@router.get("/search", response_model=Optional[OrderSummary])
async def search_orders(request: Request, filters: Annotated[OrderFilters, Depends()]):
    return None


@router.get("/{order_id}", response_model=OrderSummary)
async def get_order(request: Request, order_id: str):
    return OrderSummary()


@router.put("/{order_id}", response_model=OrderSummary)
async def replace_order(request: Request, order_id: str, payload: CreateOrderRequest):
    return OrderSummary()


@router.patch("/{order_id}", response_model=OrderSummary, operation_id="patchOrder")
async def patch_order(request: Request, order_id: str, payload: CreateOrderRequest):
    return OrderSummary()


@router.delete("/{order_id}", response_model=SuccessResponse, deprecated=True)
async def delete_order(request: Request, order_id: str):
    return SuccessResponse()


@router.options("/{order_id}")
async def options_order(request: Request, order_id: str):
    return None


@router.head("/{order_id}")
async def head_order(request: Request, order_id: str):
    return None


@router.get(ROUTE_PATH, response_model=SuccessResponse)
async def computed_route(request: Request):
    return SuccessResponse()
'''

USER_ROUTES = '''\
from fastapi import APIRouter, Request
from vendor_schemas import ExternalPayload, ExternalSummary

from application.schemas.user import UserProfile
from config import ServiceConfig

service_config = ServiceConfig()

router = APIRouter(prefix=service_config.user_prefix, tags=["users"])


@router.get("/me", response_model=UserProfile)
async def current_user(request: Request):
    return UserProfile()


@router.get("/external", response_model=ExternalSummary)
async def external_summary(request: Request):
    return None


@router.post("/external", response_model=UserProfile)
async def create_external(request: Request, payload: ExternalPayload):
    return UserProfile()
'''

SCHEMAS_COMMON = '''\
from pydantic import BaseModel as PydanticBase


class SuccessResponse(PydanticBase):
    success: bool = True


class HealthResponse(PydanticBase):
    status: str = "ok"
'''

SCHEMAS_BASE = '''\
from pydantic import BaseModel


class ProjectBase(BaseModel):
    pass
'''

SCHEMAS_ORDER = '''\
from pydantic import Field

from application.schemas.base import ProjectBase


class CreateOrderRequest(ProjectBase):
    restaurant_id: str
    items: list[dict]
    note: str = "plain-note"
    quantity: int = 3
    api_token: str = "super-secret-token-value"
    auth_key: str = Field(default="another-secret-value")


class OrderSummary(ProjectBase):
    order_id: str
    total: float = Field(..., gt=0)


class OrderFilters(ProjectBase):
    term: str
'''

SCHEMAS_USER = '''\
from vendor_schemas import ExternalBase


class UserProfile(ExternalBase):
    user_id: str
    secret_token: str = "leaked-token-value"
'''

DEPENDENCIES = '''\
class AccessManager:
    def __init__(self, roles=None):
        self.roles = roles
'''

CONFIG_INIT = "from config.service import ServiceConfig\n"

CONFIG_SERVICE = '''\
import os


class ServiceConfig:
    def __init__(self):
        self.api_prefix = os.getenv("API_PREFIX", "/api/v1")
        self.user_prefix = os.getenv("USER_PREFIX", "/users")
'''

# A microservice with no HTTP surface at all: an RPC worker, like real FTGO microservices.
WORKER_MAIN = '''\
import asyncio


async def startup():
    await asyncio.sleep(0)
'''

WORKER_MODEL = '''\
from pydantic import BaseModel


class OrderRecord(BaseModel):
    order_id: str
'''

GENERATED_MODULE = '''\
# @generated by a code generator; do not edit
from fastapi import APIRouter

router = APIRouter(prefix="/generated")


@router.get("/ghost")
async def ghost():
    return None
'''

TEST_MODULE = '''\
from fastapi import APIRouter

router = APIRouter(prefix="/in-tests")


@router.get("/ghost")
async def ghost():
    return None
'''

MIGRATION_MODULE = '''\
from fastapi import APIRouter

router = APIRouter(prefix="/migration")


@router.get("/ghost")
async def ghost():
    return None
'''

BROKEN_MODULE = "def broken(:\n    pass\n"

FIXTURE_FILES = {
    "backend/gateway/src/__init__.py": "",
    "backend/gateway/src/main.py": GATEWAY_MAIN,
    "backend/gateway/src/application/__init__.py": "",
    "backend/gateway/src/application/app.py": GATEWAY_APP,
    "backend/gateway/src/application/dependencies.py": DEPENDENCIES,
    "backend/gateway/src/application/routes/__init__.py": "",
    "backend/gateway/src/application/routes/order/__init__.py": (
        "from application.routes.order.order import router as order_router\n"
    ),
    "backend/gateway/src/application/routes/order/order.py": ORDER_ROUTES,
    "backend/gateway/src/application/routes/user/__init__.py": (
        "from application.routes.user.user import router as user_router\n"
    ),
    "backend/gateway/src/application/routes/user/user.py": USER_ROUTES,
    "backend/gateway/src/application/schemas/__init__.py": "",
    "backend/gateway/src/application/schemas/base.py": SCHEMAS_BASE,
    "backend/gateway/src/application/schemas/common.py": SCHEMAS_COMMON,
    "backend/gateway/src/application/schemas/order.py": SCHEMAS_ORDER,
    "backend/gateway/src/application/schemas/user.py": SCHEMAS_USER,
    "backend/gateway/src/config/__init__.py": CONFIG_INIT,
    "backend/gateway/src/config/service.py": CONFIG_SERVICE,
    # Out-of-scope trees that all declare routes; none may appear in the output.
    "backend/gateway/src/application/routes/order/auto_pb2.py": GENERATED_MODULE,
    "backend/gateway/src/application/routes/order/auto_client.py": GENERATED_MODULE,
    "backend/gateway/tests/test_routes.py": TEST_MODULE,
    "backend/microservices/order/migrations/env.py": MIGRATION_MODULE,
    # RPC-only microservices: scanned, reported, but no API candidate.
    "backend/microservices/order/src/__init__.py": "",
    "backend/microservices/order/src/main.py": WORKER_MAIN,
    "backend/microservices/order/src/models/__init__.py": "",
    "backend/microservices/order/src/models/order.py": WORKER_MODEL,
    "backend/microservices/feedback/src/__init__.py": "",
    "backend/microservices/feedback/src/main.py": WORKER_MAIN,
    "backend/microservices/feedback/src/broken.py": BROKEN_MODULE,
}

GATEWAY_ORDER_PREFIX = "/api/v1/v2/orders"


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
    return extract_fastapi(make_record(build_repository(tmp_path / "repo")), FROZEN_COMMIT)


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
                            "code": ["backend/gateway/**/*", "backend/microservices/**/*"]
                        },
                    }
                ],
            },
            sort_keys=False,
        ),
        encoding="utf-8",
    )
    return manifest


def endpoints_by_id(extraction) -> dict[str, object]:
    return {item.id: item for item in extraction.endpoints}


def endpoint_for(extraction, method: str, path: str):
    for item in extraction.endpoints:
        if item.method == method and item.effective_path == path:
            return item
    raise AssertionError(f"no endpoint for {method} {path}")


# --------------------------------------------------------------------------------------
# Normalization primitives
# --------------------------------------------------------------------------------------


def test_endpoint_ids_follow_the_documented_shape() -> None:
    assert endpoint_id("ftgo", "order", "POST", "/orders") == "endpoint.ftgo.order.post.orders"
    assert (
        endpoint_id("ftgo", "user", "GET", "/users/{user_id}")
        == "endpoint.ftgo.user.get.users.user-id"
    )


def test_endpoint_ids_are_byte_stable_and_case_insensitive() -> None:
    assert endpoint_id("ftgo", "order", "post", "/Orders") == endpoint_id(
        "ftgo", "order", "POST", "/orders"
    )
    # Repeating the call cannot introduce a hash or counter.
    first = endpoint_id("ftgo", "order", "get", "/a/b")
    assert first == endpoint_id("ftgo", "order", "get", "/a/b")


def test_path_tokens_normalize_parameters_and_separators() -> None:
    assert endpoint_path_tokens("/orders") == ("orders",)
    assert endpoint_path_tokens("/orders/") == ("orders",)
    assert endpoint_path_tokens("/order/set-preferred") == ("order", "set-preferred")
    assert endpoint_path_tokens("/users/{user_id}") == ("users", "user-id")
    assert endpoint_path_tokens("/files/{file_path:path}") == ("files", "file-path")
    assert endpoint_path_tokens("/") == ("root",)
    assert endpoint_path_tokens("") == ("root",)


def test_path_parameter_segments_lose_braces_and_converters() -> None:
    assert normalize_path_segment("{user_id}") == "user-id"
    assert normalize_path_segment("{file_path:path}") == "file-path"
    assert normalize_path_segment("get_all_info") == "get-all-info"


def test_route_paths_are_concatenated_the_way_fastapi_does() -> None:
    assert join_route_path("/orders", "/") == "/orders/"
    assert join_route_path("/api/v1/orders", "/list") == "/api/v1/orders/list"
    assert join_route_path("", "/health") == "/health"
    assert join_route_path("", "") == "/"


def test_schema_ids_normalize_the_python_qualified_name() -> None:
    assert (
        schema_id("ftgo", "gateway", "application.schemas.order.CreateOrderRequest")
        == "schema.ftgo.gateway.application.schemas.order.createorderrequest"
    )


def test_service_ownership_follows_repository_layout_only() -> None:
    assert service_location("backend/gateway/src/main.py") == ("gateway", "backend/gateway")
    assert service_location("backend/microservices/order/src/main.py") == (
        "order",
        "backend/microservices/order",
    )
    assert service_location("backend/microservices/feedback/src/a/b.py") == (
        "feedback",
        "backend/microservices/feedback",
    )
    assert service_location("ui/src/index.py") is None
    assert service_location("backend/README.py") is None


def test_module_names_match_the_dotted_name_the_application_imports() -> None:
    assert (
        module_dotted_name("backend/gateway/src/application/app.py", "backend/gateway")
        == "application.app"
    )
    package_init = "backend/gateway/src/application/routes/order/__init__.py"
    assert module_dotted_name(package_init, "backend/gateway") == "application.routes.order"
    assert module_dotted_name("backend/gateway/src/main.py", "backend/gateway") == "main"


def test_out_of_scope_files_are_identified_before_parsing() -> None:
    assert skip_reason("backend/gateway/src/main.py") is None
    assert skip_reason("backend/gateway/Dockerfile") is not None
    assert "test directory" in skip_reason("backend/gateway/tests/test_routes.py")
    assert "excluded directory" in skip_reason("backend/microservices/order/migrations/env.py")
    assert "excluded directory" in skip_reason("backend/gateway/.venv/lib/thing.py")
    assert "excluded directory" in skip_reason("backend/gateway/src/__pycache__/main.py")
    assert "generated" in skip_reason("backend/gateway/src/api_pb2.py")


def test_generated_headers_are_detected() -> None:
    assert is_generated_source("# @generated by tool\nimport os\n")
    assert is_generated_source("# Generated by protoc\n")
    # Only the header is inspected, so a mention deep in the body is not a marker.
    assert not is_generated_source("import os\n" * 10 + "# @generated appears far below\n")


# --------------------------------------------------------------------------------------
# Source discovery and service scanning
# --------------------------------------------------------------------------------------


def test_only_in_scope_python_files_are_scanned(extraction) -> None:
    assert all(path.endswith(".py") for path in extraction.source_files)
    for path in extraction.source_files:
        assert "\\" not in path
        assert not Path(path).is_absolute()
    joined = " ".join(extraction.source_files)
    assert "tests/" not in joined
    assert "migrations/" not in joined
    assert "_pb2.py" not in joined
    assert "auto_client.py" not in joined


def test_out_of_scope_route_declarations_never_become_endpoints(extraction) -> None:
    paths = {item.effective_path for item in extraction.endpoints}
    assert not any("ghost" in path for path in paths)
    assert not any(path.startswith("/generated") for path in paths)
    assert not any(path.startswith("/in-tests") for path in paths)
    assert not any(path.startswith("/migration") for path in paths)


def test_unparseable_module_is_reported_and_skipped(extraction) -> None:
    assert "backend/microservices/feedback/src/broken.py" not in extraction.source_files
    assert any("invalid Python syntax" in warning for warning in extraction.warnings)


def test_every_scanned_service_is_reported_even_without_a_surface(extraction) -> None:
    scans = {scan.slug: scan for scan in extraction.services_scanned}

    assert set(scans) == {"gateway", "order", "feedback"}
    assert scans["gateway"].entity_id == "service.ftgo.gateway"
    assert scans["gateway"].api == "api.ftgo.gateway"
    # RPC-only microservices are reported with zero surfaces and no invented API.
    assert scans["order"].surfaces == 0
    assert scans["order"].endpoints == 0
    assert scans["order"].api is None
    assert scans["feedback"].api is None
    assert any("no FastAPI or APIRouter construct found" in item for item in extraction.warnings)


def test_service_entity_ids_reuse_the_pass_one_model(extraction) -> None:
    for scan in extraction.services_scanned:
        assert scan.entity_id in PASS_ONE_SERVICE_IDS
    for api in extraction.apis:
        assert api.service_entity_id in PASS_ONE_SERVICE_IDS


# --------------------------------------------------------------------------------------
# API surfaces
# --------------------------------------------------------------------------------------


def test_only_the_gateway_exposes_an_api(extraction) -> None:
    assert [api.id for api in extraction.apis] == ["api.ftgo.gateway"]
    api = extraction.apis[0]
    assert api.kind == "API"
    assert api.title == "Fixture Gateway"
    assert api.attributes["application_symbol"] == "main.app"
    assert api.attributes["application_count"] == 1
    assert api.provenance.source_path == "backend/gateway/src/main.py"


def test_service_exposes_api_relationship_is_generated(extraction) -> None:
    exposes = [item for item in extraction.relationships if item.type == "EXPOSES"]

    assert len(exposes) == 1
    assert exposes[0].source == "service.ftgo.gateway"
    assert exposes[0].target == "api.ftgo.gateway"


def test_api_contains_every_endpoint_of_its_service(extraction) -> None:
    contains = {
        item.target for item in extraction.relationships if item.type == "CONTAINS"
    }

    assert contains == {item.id for item in extraction.endpoints}
    assert all(
        item.source == "api.ftgo.gateway"
        for item in extraction.relationships
        if item.type == "CONTAINS"
    )


# --------------------------------------------------------------------------------------
# Endpoint discovery: methods, prefixes, paths
# --------------------------------------------------------------------------------------


def test_app_level_decorator_is_extracted(extraction) -> None:
    endpoint = endpoint_for(extraction, "GET", "/health")

    assert endpoint.id == "endpoint.ftgo.gateway.get.health"
    assert endpoint.path_resolution == "complete"
    assert endpoint.attributes["router"] == "main:app"
    assert endpoint.attributes["handler"] == "main.health"


def test_router_level_decorator_is_extracted(extraction) -> None:
    endpoint = endpoint_for(extraction, "POST", f"{GATEWAY_ORDER_PREFIX}/bulk")

    assert endpoint.id == "endpoint.ftgo.gateway.post.api.v1.v2.orders.bulk"
    assert endpoint.attributes["handler"] == "application.routes.order.order.bulk_create"
    assert endpoint.attributes["status_code"] == 201


def test_aliased_and_module_qualified_constructors_are_recognized(tmp_path: Path) -> None:
    files = {
        "backend/gateway/src/main.py": (
            "import fastapi\n"
            "from fastapi import APIRouter as Router\n"
            "\n"
            "app = fastapi.FastAPI(title='Aliased')\n"
            "inner = Router(prefix='/inner')\n"
            "app.include_router(inner, prefix='/outer')\n"
            "\n"
            "\n"
            "@inner.get('/ping')\n"
            "async def ping():\n"
            "    return None\n"
        ),
    }
    result = extract_fastapi(make_record(build_repository(tmp_path / "repo", files)), FROZEN_COMMIT)

    assert [item.id for item in result.apis] == ["api.ftgo.gateway"]
    assert result.apis[0].title == "Aliased"
    endpoint = endpoint_for(result, "GET", "/outer/inner/ping")
    assert endpoint.id == "endpoint.ftgo.gateway.get.outer.inner.ping"
    assert endpoint.path_resolution == "complete"


def test_every_supported_http_method_is_discovered(extraction) -> None:
    methods = {item.method for item in extraction.endpoints}

    assert methods == {"GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS", "HEAD"}


def test_all_methods_on_one_path_become_distinct_endpoints(extraction) -> None:
    parameterized = f"{GATEWAY_ORDER_PREFIX}/{{order_id}}"
    methods = {
        item.method for item in extraction.endpoints if item.effective_path == parameterized
    }

    assert methods == {"GET", "PUT", "PATCH", "DELETE", "OPTIONS", "HEAD"}
    for method in methods:
        expected = f"endpoint.ftgo.gateway.{method.lower()}.api.v1.v2.orders.order-id"
        assert endpoint_for(extraction, method, parameterized).id == expected


def test_apirouter_prefix_is_applied(extraction) -> None:
    endpoint = endpoint_for(extraction, "GET", f"{GATEWAY_ORDER_PREFIX}/list")

    assert endpoint.attributes["decorator_path"] == "/list"
    assert endpoint.attributes["router_prefix"] == GATEWAY_ORDER_PREFIX


def test_include_router_prefix_and_nested_chain_are_composed(extraction) -> None:
    endpoint = endpoint_for(extraction, "POST", f"{GATEWAY_ORDER_PREFIX}/")

    # app("") + include("/api/v1") + init_router("") + include("/v2") + APIRouter("/orders")
    assert endpoint.effective_path == "/api/v1/v2/orders/"
    assert endpoint.path_resolution == "complete"
    assert endpoint.attributes["mount_path"] == [
        "main:app",
        "application.app:router",
        "application.routes.order.order:router",
    ]
    # A declared trailing slash survives into the path but not into the id.
    assert endpoint.id == "endpoint.ftgo.gateway.post.api.v1.v2.orders"


def test_path_parameters_are_recorded_and_normalized(extraction) -> None:
    endpoint = endpoint_for(extraction, "GET", f"{GATEWAY_ORDER_PREFIX}/{{order_id}}")

    assert endpoint.attributes["path_parameters"] == ["order_id"]
    assert endpoint.id.endswith(".order-id")


def test_router_tags_and_decorator_metadata_are_captured(extraction) -> None:
    patched = endpoint_for(extraction, "PATCH", f"{GATEWAY_ORDER_PREFIX}/{{order_id}}")
    deleted = endpoint_for(extraction, "DELETE", f"{GATEWAY_ORDER_PREFIX}/{{order_id}}")
    created = endpoint_for(extraction, "POST", f"{GATEWAY_ORDER_PREFIX}/")

    assert patched.attributes["operation_id"] == "patchOrder"
    assert patched.attributes["tags"] == ["orders"]
    assert deleted.attributes["deprecated"] is True
    # A non-literal status_code is recorded as an expression, never evaluated.
    assert created.attributes["status_code_expression"] == "status.HTTP_201_CREATED"
    assert "status_code" not in created.attributes


# --------------------------------------------------------------------------------------
# Unresolved constructs are reported, never guessed
# --------------------------------------------------------------------------------------


def test_dynamic_route_path_yields_no_endpoint_and_is_reported(extraction) -> None:
    handlers = {item.attributes["handler"] for item in extraction.endpoints}
    assert not any("computed" in item.effective_path for item in extraction.endpoints)
    assert not any(handler.endswith("computed_route") for handler in handlers)

    reported = [
        item for item in extraction.unresolved_routes if item.reason_code == "dynamic_route_path"
    ]
    assert len(reported) == 1
    assert reported[0].expression == "ROUTE_PATH"
    assert reported[0].method == "GET"
    assert reported[0].provenance.source_path.endswith("routes/order/order.py")


def test_dynamic_router_prefix_is_reported_and_path_is_partial(extraction) -> None:
    reported = [
        item
        for item in extraction.unresolved_routes
        if item.reason_code == "dynamic_router_prefix"
    ]
    assert len(reported) == 1
    assert reported[0].expression == "service_config.user_prefix"

    endpoint = endpoint_for(extraction, "GET", "/api/v1/me")
    assert endpoint.path_resolution == "partial"
    assert endpoint.attributes["unresolved_prefix_expressions"] == ["service_config.user_prefix"]


def test_untraceable_included_router_is_reported_without_a_mount(extraction) -> None:
    reported = [
        item
        for item in extraction.unresolved_routes
        if item.reason_code == "unresolved_include_target"
    ]

    assert len(reported) == 1
    assert reported[0].expression == "external_router"
    assert reported[0].provenance.source_path == "backend/gateway/src/application/app.py"


def test_fully_resolved_endpoints_are_marked_complete(extraction) -> None:
    def paths(resolution: str) -> set[str]:
        return {
            item.effective_path
            for item in extraction.endpoints
            if item.path_resolution == resolution
        }

    complete = paths("complete")
    partial = paths("partial")

    assert "/health" in complete
    assert f"{GATEWAY_ORDER_PREFIX}/list" in complete
    assert partial == {"/api/v1/me", "/api/v1/external"}


# --------------------------------------------------------------------------------------
# Schemas
# --------------------------------------------------------------------------------------


def _schema_links(extraction, role: str) -> set[tuple[str, str]]:
    return {
        (item.source, item.target)
        for item in extraction.relationships
        if item.type == "USES_SCHEMA" and item.role == role
    }


def test_response_model_becomes_a_response_schema(extraction) -> None:
    endpoint = endpoint_for(extraction, "GET", "/health")

    assert (
        endpoint.id,
        "schema.ftgo.gateway.application.schemas.common.healthresponse",
    ) in _schema_links(extraction, "response")


def test_request_body_model_becomes_a_request_schema(extraction) -> None:
    endpoint = endpoint_for(extraction, "POST", f"{GATEWAY_ORDER_PREFIX}/")

    assert (
        endpoint.id,
        "schema.ftgo.gateway.application.schemas.order.createorderrequest",
    ) in _schema_links(extraction, "request")


def test_request_and_response_roles_stay_distinguishable(extraction) -> None:
    endpoint = endpoint_for(extraction, "PUT", f"{GATEWAY_ORDER_PREFIX}/{{order_id}}")
    request_targets = {
        target for source, target in _schema_links(extraction, "request") if source == endpoint.id
    }
    response_targets = {
        target for source, target in _schema_links(extraction, "response") if source == endpoint.id
    }

    assert request_targets == {"schema.ftgo.gateway.application.schemas.order.createorderrequest"}
    assert response_targets == {"schema.ftgo.gateway.application.schemas.order.ordersummary"}


def test_list_and_optional_response_models_are_unwrapped(extraction) -> None:
    listed = endpoint_for(extraction, "GET", f"{GATEWAY_ORDER_PREFIX}/list")
    optional = endpoint_for(extraction, "GET", f"{GATEWAY_ORDER_PREFIX}/search")
    summary = "schema.ftgo.gateway.application.schemas.order.ordersummary"

    assert (listed.id, summary) in _schema_links(extraction, "response")
    assert (optional.id, summary) in _schema_links(extraction, "response")
    assert listed.attributes["response_model"] == "list[OrderSummary]"
    assert optional.attributes["response_model"] == "Optional[OrderSummary]"


def test_primitive_and_dependency_parameters_are_not_request_schemas(extraction) -> None:
    listed = endpoint_for(extraction, "GET", f"{GATEWAY_ORDER_PREFIX}/list")
    searched = endpoint_for(extraction, "GET", f"{GATEWAY_ORDER_PREFIX}/search")
    bulk = endpoint_for(extraction, "POST", f"{GATEWAY_ORDER_PREFIX}/bulk")
    requests = _schema_links(extraction, "request")

    # limit: int = 10 is a query parameter, not a body.
    assert not any(source == listed.id for source, _ in requests)
    # Annotated[OrderFilters, Depends()] is a dependency, not a body.
    assert not any(source == searched.id for source, _ in requests)
    # actor: AccessManager = Depends(...) is a dependency; only payload is a body.
    assert {target for source, target in requests if source == bulk.id} == {
        "schema.ftgo.gateway.application.schemas.order.createorderrequest"
    }
    assert not any("accessmanager" in target for _, target in requests)


def test_path_parameters_are_not_request_schemas(extraction) -> None:
    endpoint = endpoint_for(extraction, "GET", f"{GATEWAY_ORDER_PREFIX}/{{order_id}}")

    assert not any(source == endpoint.id for source, _ in _schema_links(extraction, "request"))


def test_framework_request_object_is_never_a_schema(extraction) -> None:
    assert not any("request" == item.detail.get("parameter") for item in extraction.relationships)
    assert not any("starlette" in schema.qualified_name for schema in extraction.schemas)


def test_pydantic_base_is_confirmed_through_aliases_and_local_chains(extraction) -> None:
    schemas = {item.id: item for item in extraction.schemas}
    common = schemas["schema.ftgo.gateway.application.schemas.common.healthresponse"]
    ordered = schemas["schema.ftgo.gateway.application.schemas.order.ordersummary"]

    # BaseModel imported as PydanticBase.
    assert common.pydantic_confirmed is True
    assert common.base_resolution == "pydantic_basemodel"
    # ProjectBase(BaseModel) resolved through a local base class.
    assert ordered.pydantic_confirmed is True
    assert ordered.bases == ("ProjectBase",)


def test_schema_with_an_external_base_is_emitted_but_not_confirmed(extraction) -> None:
    profile = next(item for item in extraction.schemas if item.title == "UserProfile")

    assert profile.pydantic_confirmed is False
    assert profile.base_resolution == "external_base"
    assert profile.bases == ("ExternalBase",)


def test_external_schema_symbols_are_reported_and_never_invented(extraction) -> None:
    reported = {(item.role, item.expression) for item in extraction.unresolved_schemas}

    assert ("response", "ExternalSummary") in reported
    assert ("request", "ExternalPayload") in reported
    codes = {item.reason_code for item in extraction.unresolved_schemas}
    assert codes == {"external_schema_symbol"}
    # Nothing was fabricated for either symbol.
    titles = {item.title for item in extraction.schemas}
    assert "ExternalSummary" not in titles
    assert "ExternalPayload" not in titles


def test_declared_fields_and_annotations_are_captured_as_source_text(extraction) -> None:
    order_request = next(
        item for item in extraction.schemas if item.title == "CreateOrderRequest"
    )
    fields = {item.name: item for item in order_request.fields}

    assert fields["restaurant_id"].annotation == "str"
    assert fields["items"].annotation == "list[dict]"
    assert fields["note"].default == "plain-note"
    assert fields["quantity"].default == 3
    # A non-literal default is recorded as an expression, never evaluated.
    total = next(item for item in extraction.schemas if item.title == "OrderSummary")
    assert {item.name: item.default_expression for item in total.fields}["total"] == (
        "Field(..., gt=0)"
    )


def test_only_endpoint_referenced_schemas_become_entities(extraction) -> None:
    titles = {item.title for item in extraction.schemas}

    assert titles == {
        "HealthResponse",
        "SuccessResponse",
        "CreateOrderRequest",
        "OrderSummary",
        "UserProfile",
    }
    # Discovered but unreferenced models are reported, not promoted to entities.
    assert "OrderFilters" not in titles
    assert "OrderRecord" not in titles
    assert "order:models.order.OrderRecord" in extraction.discovered_models
    assert "gateway:application.schemas.order.OrderFilters" in extraction.discovered_models


def test_uses_schema_is_only_generated_when_a_class_definition_exists(extraction) -> None:
    known = {item.id for item in extraction.schemas}
    links = [item for item in extraction.relationships if item.type == "USES_SCHEMA"]

    assert links
    assert all(item.target in known for item in links)
    assert all(item.role in ("request", "response") for item in links)


# --------------------------------------------------------------------------------------
# Ontology conformance and relationship scope
# --------------------------------------------------------------------------------------


def test_only_ontology_approved_entity_kinds_are_emitted(extraction) -> None:
    allowed = set(
        yaml.safe_load((AIDE_ROOT / "ontology/entity-types.yaml").read_text(encoding="utf-8"))[
            "entity_types"
        ]
    )
    emitted = (
        {item.kind for item in extraction.apis}
        | {item.kind for item in extraction.endpoints}
        | {item.kind for item in extraction.schemas}
    )

    assert emitted <= allowed
    assert emitted == {"API", "Endpoint", "Schema"}


def test_only_ontology_approved_relationship_types_are_emitted(extraction) -> None:
    document = yaml.safe_load(
        (AIDE_ROOT / "ontology/relationship-types.yaml").read_text(encoding="utf-8")
    )
    allowed = {item["type"] for item in document["relationship_types"]}
    emitted = {item.type for item in extraction.relationships}

    assert emitted <= allowed
    assert emitted == {"EXPOSES", "CONTAINS", "USES_SCHEMA"}


def test_no_out_of_scope_relationship_is_created(extraction) -> None:
    emitted = {item.type for item in extraction.relationships}

    assert not emitted & {
        "CALLS",
        "CONSUMES",
        "PUBLISHES",
        "READS",
        "WRITES",
        "DEPENDS_ON",
        "PARTICIPATES_IN",
    }


# --------------------------------------------------------------------------------------
# Provenance
# --------------------------------------------------------------------------------------


def test_every_entity_carries_full_provenance(extraction) -> None:
    entities = list(extraction.apis) + list(extraction.endpoints) + list(extraction.schemas)

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
        assert provenance.line_end is not None
        assert provenance.line_end >= provenance.line_start


def test_every_relationship_carries_full_provenance(extraction) -> None:
    for relation in extraction.relationships:
        assert relation.provenance.repository == "ftgo"
        assert relation.provenance.commit == FROZEN_COMMIT
        assert relation.provenance.evidence_type == "implemented"
        assert relation.provenance.source_path.endswith(".py")


def test_endpoint_provenance_names_the_decorator_and_handler(extraction) -> None:
    endpoint = endpoint_for(extraction, "GET", f"{GATEWAY_ORDER_PREFIX}/list")

    assert endpoint.provenance.source_path == (
        "backend/gateway/src/application/routes/order/order.py"
    )
    assert endpoint.provenance.symbol == "application.routes.order.order.list_orders"
    assert (
        endpoint.attributes["decorator"]
        == 'router.get("/list", response_model=list[OrderSummary])'
    )
    assert endpoint.attributes["method"] == "GET"
    assert endpoint.attributes["effective_path"] == f"{GATEWAY_ORDER_PREFIX}/list"


def test_unresolved_items_carry_provenance(extraction) -> None:
    for item in list(extraction.unresolved_routes) + list(extraction.unresolved_schemas):
        assert item.provenance.commit == FROZEN_COMMIT
        assert item.provenance.source_path.endswith(".py")


# --------------------------------------------------------------------------------------
# Candidate rendering, secret safety, and report
# --------------------------------------------------------------------------------------


def test_candidates_are_never_approved(extraction) -> None:
    rendered, _ = render_bundle(extraction)

    expected = len(extraction.apis) + len(extraction.endpoints) + len(extraction.schemas)
    assert len(rendered) == expected
    for path, content in rendered.items():
        frontmatter = yaml.safe_load(content.split("---")[1])
        assert frontmatter["status"] == "candidate"
        assert frontmatter["review_status"] == "pending"
        assert frontmatter["kind"] == frontmatter["type"]
        assert "status: approved" not in content
        assert path.startswith(("apis/", "endpoints/", "schemas/"))


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
    # Field names stay visible and non-secret defaults are preserved.
    assert "[redacted]" in blob
    assert "api_token" in blob
    assert "plain-note" in blob


def test_report_contains_the_required_fields(extraction) -> None:
    _, report = render_bundle(extraction)

    for key in (
        "repository",
        "commit",
        "source_files",
        "services_scanned",
        "apis",
        "endpoints",
        "schemas",
        "relationships",
        "unresolved_routes",
        "unresolved_schemas",
        "warnings",
        "secret_values_emitted",
        "graph_mutations",
    ):
        assert key in report, f"missing report key {key!r}"
    assert report["graph_mutations"] == 0
    assert report["neo4j_mutations"] == 0
    assert report["graphiti"] == "disabled"
    assert report["modules_imported"] == 0
    assert report["modules_executed"] == 0
    assert report["analysis"] == "python-ast"
    assert report["counts"]["apis"] == 1


# --------------------------------------------------------------------------------------
# CLI behavior: dry-run, commit gate, determinism
# --------------------------------------------------------------------------------------


def test_dry_run_writes_nothing(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    repo_root = build_repository(tmp_path / "repo")
    manifest = write_manifest(tmp_path, repo_root)
    output_dir = tmp_path / "candidates"
    monkeypatch.setattr("knowledge_plane.extract.read_git_head", lambda path: FROZEN_COMMIT)

    summary = run("ftgo", "fastapi", manifest_path=manifest, output_dir=output_dir, dry_run=True)

    assert summary["status"] == "dry-run"
    assert summary["dry_run"] is True
    assert summary["commit"] == FROZEN_COMMIT
    assert summary["commit_verified"] is True
    assert summary["counts"]["apis"] == 1
    assert summary["secret_values_emitted"] == 0
    assert summary["graph_mutations"] == 0
    assert summary["wiki_writes"] == 0
    assert summary["neo4j_mutations"] == 0
    assert summary["graphiti"] == "disabled"
    # Zero filesystem candidate changes.
    assert not output_dir.exists()


def test_dry_run_still_reports_unresolved_constructs(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    manifest = write_manifest(tmp_path, build_repository(tmp_path / "repo"))
    monkeypatch.setattr("knowledge_plane.extract.read_git_head", lambda path: FROZEN_COMMIT)

    summary = run("ftgo", "fastapi", manifest_path=manifest, dry_run=True)

    codes = {item["reason_code"] for item in summary["unresolved_routes"]}
    assert codes == {"dynamic_route_path", "dynamic_router_prefix", "unresolved_include_target"}
    assert {item["expression"] for item in summary["unresolved_schemas"]} == {
        "ExternalSummary",
        "ExternalPayload",
    }


def test_real_run_requires_an_output_directory(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    manifest = write_manifest(tmp_path, build_repository(tmp_path / "repo"))
    monkeypatch.setattr("knowledge_plane.extract.read_git_head", lambda path: FROZEN_COMMIT)

    with pytest.raises(Exception, match="--output-dir is required"):
        run("ftgo", "fastapi", manifest_path=manifest, dry_run=False)


def test_commit_mismatch_aborts_before_writing_anything(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    manifest = write_manifest(tmp_path, build_repository(tmp_path / "repo"))
    output_dir = tmp_path / "candidates"
    monkeypatch.setattr("knowledge_plane.extract.read_git_head", lambda path: WRONG_COMMIT)

    with pytest.raises(CommitMismatchError) as excinfo:
        run("ftgo", "fastapi", manifest_path=manifest, output_dir=output_dir, dry_run=False)

    assert excinfo.value.expected == FROZEN_COMMIT
    assert excinfo.value.actual == WRONG_COMMIT
    assert not output_dir.exists()


def test_expected_output_structure_is_written(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    manifest = write_manifest(tmp_path, build_repository(tmp_path / "repo"))
    output_dir = tmp_path / "candidates"
    monkeypatch.setattr("knowledge_plane.extract.read_git_head", lambda path: FROZEN_COMMIT)

    summary = run("ftgo", "fastapi", manifest_path=manifest, output_dir=output_dir)

    assert summary["status"] == "ok"
    assert (output_dir / "extraction-report.json").is_file()
    assert len(list((output_dir / "apis").glob("*.md"))) == 1
    assert len(list((output_dir / "endpoints").glob("*.md"))) == summary["counts"]["endpoints"]
    assert len(list((output_dir / "schemas").glob("*.md"))) == 5

    report = json.loads((output_dir / "extraction-report.json").read_text(encoding="utf-8"))
    assert report["commit"] == FROZEN_COMMIT
    assert report["secret_values_emitted"] == 0
    assert report["graph_mutations"] == 0


def test_repeat_extraction_is_byte_identical(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    manifest = write_manifest(tmp_path, build_repository(tmp_path / "repo"))
    monkeypatch.setattr("knowledge_plane.extract.read_git_head", lambda path: FROZEN_COMMIT)
    first = tmp_path / "run-one"
    second = tmp_path / "run-two"

    run("ftgo", "fastapi", manifest_path=manifest, output_dir=first)
    run("ftgo", "fastapi", manifest_path=manifest, output_dir=second)

    first_files = sorted(path.relative_to(first) for path in first.rglob("*") if path.is_file())
    second_files = sorted(path.relative_to(second) for path in second.rglob("*") if path.is_file())
    assert first_files == second_files
    assert first_files, "extraction produced no files"
    for relative_path in first_files:
        assert (first / relative_path).read_bytes() == (second / relative_path).read_bytes(), (
            f"{relative_path} differs between runs"
        )


def test_rerun_into_the_same_directory_prunes_orphans(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    manifest = write_manifest(tmp_path, build_repository(tmp_path / "repo"))
    monkeypatch.setattr("knowledge_plane.extract.read_git_head", lambda path: FROZEN_COMMIT)
    output_dir = tmp_path / "candidates"

    run("ftgo", "fastapi", manifest_path=manifest, output_dir=output_dir)
    orphan = output_dir / "endpoints" / "endpoint.ftgo.gateway.get.retired.md"
    orphan.write_text("stale", encoding="utf-8")

    run("ftgo", "fastapi", manifest_path=manifest, output_dir=output_dir)

    assert not orphan.exists()


def test_compose_candidates_are_not_touched_by_the_fastapi_pass(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    # The fastapi pass owns apis/, endpoints/, schemas/ only; a sibling pass's output in the
    # same directory must survive pruning.
    manifest = write_manifest(tmp_path, build_repository(tmp_path / "repo"))
    monkeypatch.setattr("knowledge_plane.extract.read_git_head", lambda path: FROZEN_COMMIT)
    output_dir = tmp_path / "candidates"
    foreign = output_dir / "services" / "service.ftgo.gateway.md"
    foreign.parent.mkdir(parents=True, exist_ok=True)
    foreign.write_text("owned by the compose pass", encoding="utf-8")

    run("ftgo", "fastapi", manifest_path=manifest, output_dir=output_dir)

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
    return extract_fastapi(record, FROZEN_COMMIT)


def test_real_ftgo_exposes_only_the_gateway_http_surface(real_extraction) -> None:
    assert [api.id for api in real_extraction.apis] == ["api.ftgo.gateway"]
    assert real_extraction.apis[0].title == "Food Delivery Server"
    # All six Pass 1 services are scanned; only the gateway has a FastAPI surface.
    scanned = {scan.entity_id for scan in real_extraction.services_scanned}
    assert scanned == PASS_ONE_SERVICE_IDS
    for scan in real_extraction.services_scanned:
        if scan.slug != "gateway":
            assert scan.surfaces == 0
            assert scan.api is None


def test_real_ftgo_endpoints_are_all_gateway_owned(real_extraction) -> None:
    assert real_extraction.endpoints
    assert all(item.service == "gateway" for item in real_extraction.endpoints)
    assert all(item.api == "api.ftgo.gateway" for item in real_extraction.endpoints)
    assert all(item.id.startswith("endpoint.ftgo.gateway.") for item in real_extraction.endpoints)


def test_real_ftgo_dynamic_api_prefix_is_reported_not_guessed(real_extraction) -> None:
    reported = [
        item
        for item in real_extraction.unresolved_routes
        if item.reason_code == "dynamic_include_prefix"
    ]

    assert reported, "the env-driven api_prefix mount must be reported"
    assert any(item.expression == "service_config.api_prefix" for item in reported)
    # Because the mount prefix is configuration-driven, no endpoint may claim a complete path.
    assert all(item.path_resolution == "partial" for item in real_extraction.endpoints)
    assert not any("/api/v1" in item.effective_path for item in real_extraction.endpoints)


def test_real_ftgo_router_prefixes_are_resolved(real_extraction) -> None:
    paths = {item.effective_path for item in real_extraction.endpoints}

    # Statically declared APIRouter prefixes must appear in the effective paths.
    assert "/order/create" in paths
    assert "/profile/logout" in paths
    assert "/restaurant/register" in paths
    assert "/menu/add" in paths
    assert "/vehicle/register" in paths
    assert "/address/add" in paths
    assert "/status/online" in paths
    assert "/location/submit" in paths


def test_real_ftgo_relationships_are_in_scope_and_well_formed(real_extraction) -> None:
    known = (
        {item.id for item in real_extraction.apis}
        | {item.id for item in real_extraction.endpoints}
        | {item.id for item in real_extraction.schemas}
        | PASS_ONE_SERVICE_IDS
    )

    assert {item.type for item in real_extraction.relationships} == {
        "EXPOSES",
        "CONTAINS",
        "USES_SCHEMA",
    }
    for relation in real_extraction.relationships:
        assert relation.source in known
        assert relation.target in known


def test_real_ftgo_external_schema_symbols_are_reported(real_extraction) -> None:
    expressions = {item.expression for item in real_extraction.unresolved_schemas}

    # ftgo_utils is not vendored in the repository, so its schemas cannot be resolved.
    assert any("Mixin" in expression for expression in expressions)
    titles = {item.title for item in real_extraction.schemas}
    assert "UserInfoMixin" not in titles


def test_real_ftgo_emits_no_secret_values(real_extraction) -> None:
    _, report = render_bundle(real_extraction)

    assert report["secret_values_emitted"] == 0
    assert report["graph_mutations"] == 0


def test_real_ftgo_extraction_is_deterministic(real_extraction) -> None:
    record = _real_ftgo_record()
    assert record is not None
    repeated = extract_fastapi(record, FROZEN_COMMIT)

    first, _ = render_bundle(real_extraction)
    second, _ = render_bundle(repeated)
    assert first.keys() == second.keys()
    for key in first:
        assert first[key] == second[key], f"{key} differs between identical runs"
