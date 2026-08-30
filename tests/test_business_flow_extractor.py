"""Deterministic tests for the user/business flow extractor (Graph Engineering Pass 6).

The synthetic fixture is a miniature Vue application shaped like the FTGO frontend: a router
table, a Vuex store, views that mount components, and one view that mounts nothing at all. It
deliberately contains every case that must *not* compose - two unawaited requests in one
handler, a navigation to a route that does not exist, a navigation to a view that renders
nothing, a request URL that is a conditional expression, a request that no approved UserFlow
declares, and a request path two UserFlows both claim. Opt-in tests at the end assert the ten
declared journeys against the real frozen FTGO checkout, including the ones the source must
refuse to support.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest
import yaml

from knowledge_plane.extractors import EXTRACTORS
from knowledge_plane.extractors import business_flow as bf
from knowledge_plane.extractors import user_flow as uf
from knowledge_plane.extractors.business_flow import (
    BUSINESS_FLOW_KIND,
    CANDIDATE_SUBDIRECTORIES,
    CONTAINS,
    DERIVED_FROM,
    FLOW_STEP_KIND,
    MECHANISM_AWAIT,
    MECHANISM_HELPER,
    MECHANISM_INTERVAL,
    MECHANISM_LIFECYCLE,
    MECHANISM_NAVIGATION,
    MECHANISM_VUEX,
    MIN_USER_FLOWS_PER_BUSINESS_FLOW,
    OUTCOME_REJECTED,
    OUTCOME_RESOLVED,
    PRECEDES,
    TRIGGER_AUTOMATIC,
    TRIGGER_CONDITIONAL,
    TRIGGER_LIFECYCLE,
    TRIGGER_USER_ACTION,
    ChainWalker,
    build_frontend_model,
    build_source_text,
    business_flow_id,
    business_step_id,
    collides_with_pass5,
    extract_business_flow,
    extract_script_blocks,
    load_canonical_user_flows,
    map_to_user_flow,
    parse_component,
    parse_router,
    parse_store,
    render_bundle,
    resolve_api_prefix,
    resolve_view,
)
from knowledge_plane.repository_manifest import (
    DEFAULT_MANIFEST_RELATIVE_PATH,
    RepositoryRecord,
    load_repository_manifest,
    read_git_head,
)

FROZEN_COMMIT = "52b1fd1b5d808e32b7925e890f560445a8460e7a"
AIDE_ROOT = Path(__file__).resolve().parents[1]

COMPONENTS = bf.COMPONENTS_DIR
VIEWS = bf.VIEWS_DIR

# --------------------------------------------------------------------------------------
# Fixture: gateway configuration that makes the route prefix a fact
# --------------------------------------------------------------------------------------

GATEWAY_CONFIG = '''\
from config.base import BaseConfig, env_var


class ServiceConfig(BaseConfig):
    def __init__(self, api_prefix: str = None):
        self.api_prefix = api_prefix or env_var('API_PREFIX', default='/api/v1')
'''

GATEWAY_MAIN = '''\
from fastapi import FastAPI

from application.app import init_router
from config import ServiceConfig

service_config = ServiceConfig()
app = FastAPI()
app.include_router(init_router(), prefix=service_config.api_prefix)
'''

# --------------------------------------------------------------------------------------
# Fixture: router, store, views
# --------------------------------------------------------------------------------------

ROUTER = '''\
import Vue from 'vue'
import VueRouter from 'vue-router'
import Landing from '../views/Landing.vue'
import Detail from '../views/Detail.vue'
import Empty from '../views/Empty.vue'
import Verify from '../views/Verify.vue'

Vue.use(VueRouter)

const routes = [{
        path: '/',
        name: 'Landing',
        component: Landing
    },
    {
        path: '/Detail',
        name: 'Detail',
        component: Detail
    },
    {
        path: '/Empty',
        name: 'Empty',
        component: Empty
    },
    {
        path: '/Verify',
        name: 'Verify',
        component: Verify
    },
]

const router = new VueRouter({ mode: 'history', routes })

export default router
'''

STORE = '''\
import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);

export default new Vuex.Store({
    state: { userId: null, token: null },
    mutations: {
        setUserId(state, userId) { state.userId = userId; },
        setToken(state, token) { state.token = token; },
    },
    actions: {
        updateUserId({ commit }, userId) { commit('setUserId', userId); },
        updateToken({ commit }, token) { commit('setToken', token); },
    },
    getters: {
        getUserId: state => state.userId,
        getToken: state => state.token,
    }
});
'''

VIEW_LANDING = '''\
<template>
  <div>
    <landing-comp />
  </div>
</template>
<script>
import LandingComp from '../components/Landing.vue'
export default {
  components: {
    LandingComp,
  }
}
</script>
'''

VIEW_DETAIL = '''\
<template>
  <div>
    <detail-comp />
  </div>
</template>
<script>
import DetailComp from '../components/Detail.vue'
export default {
  components: {
    DetailComp,
  }
}
</script>
'''

VIEW_VERIFY = '''\
<template>
  <div>
    <verify-comp />
  </div>
</template>
<script>
import VerifyComp from '../components/Verify.vue'
export default {
  components: {
    VerifyComp,
  }
}
</script>
'''

# The dead end. Mirrors ui/src/views/MenuPage.vue at the frozen FTGO commit.
VIEW_EMPTY = '''\
<script setup>
</script>
<template>
</template>
<style scoped>
</style>
'''

# --------------------------------------------------------------------------------------
# Fixture: components
# --------------------------------------------------------------------------------------

COMPONENT_LANDING = '''\
<template>
  <div>
    <b-button @click="submit()">login</b-button>
    <b-button @click="mutateAndRefresh">save</b-button>
    <b-button @click="confirmMutation">delete</b-button>
    <b-button @click="unordered">both</b-button>
    <b-button @click="ambiguous">twin</b-button>
    <b-button @click="missingFlow">online</b-button>
    <b-button @click="goMissing">missing</b-button>
    <b-button @click="goEmpty">empty</b-button>
    <b-button @click="goBack">back</b-button>
    <b-button @click="justNavigate">detail</b-button>
    <b-button @click="startTicker">tick</b-button>
    <b-button @click="toggle">toggle</b-button>
  </div>
</template>

<script>
import Vue from "vue";
import axios from "axios";
import {mapActions, mapGetters} from 'vuex';

export default {
  data() {
    return {
      role: 'driver',
      roles: [
        {value: 'driver', text: 'D'},
        {value: 'rider', text: 'R'}
      ],
      active: false,
    };
  },
  computed: {
    ...mapGetters(['getToken', 'getUserId']),
    token() {
      return this.getToken;
    }
  },
  methods: {
    ...mapActions(['updateUserId', 'updateToken']),
    async submit() {
      let api = "http://localhost:8000/api/v1/auth/login";
      const response = await Vue.axios.post(api, {});
      this.updateUserId(response.data.user_id);
      this.updateToken(response.data.token);

      if (this.role === 'driver') {
        await this.loadVehicle();
      }

      if (this.role === 'rider') {
        await this.loadRider();
      }

      switch (this.role) {
        case 'driver':
          this.$router.push('/Detail');
          break;
        case 'rider':
          this.$router.push({
            name: 'Verify'
          });
          break;
        default:
          this.$router.push('/');
      }
    },
    async loadVehicle() {
      await axios.get('http://localhost:8000/api/v1/vehicle/get_info');
    },
    async loadRider() {
      await axios.get('http://localhost:8000/api/v1/profile/user_info');
    },
    async unordered() {
      this.loadVehicle();
      this.loadRider();
    },
    async ambiguous() {
      await axios.get('http://localhost:8000/api/v1/ambiguous/twin');
    },
    async missingFlow() {
      await axios.post('http://localhost:8000/api/v1/status/online', {});
    },
    async toggle() {
      const url = this.active
        ? 'http://localhost:8000/api/v1/status/online'
        : 'http://localhost:8000/api/v1/status/offline';
      await axios.post(url, {});
      await this.tick();
    },
    goMissing() {
      this.$router.push({ name: 'NoSuchRoute' });
    },
    goEmpty() {
      this.$router.push('/Empty');
    },
    goBack() {
      this.$router.go(-1);
    },
    justNavigate() {
      this.$router.push('/Detail');
    },
    startTicker() {
      setInterval(() => {
        this.tick();
      }, 5000);
    },
    async tick() {
      await axios.get('http://localhost:8000/api/v1/status/get');
      if (this.active) {
        await axios.post('http://localhost:8000/api/v1/location/submit', {});
      }
    },
    async mutateAndRefresh() {
      await axios.post('http://localhost:8000/api/v1/menu/add', {});
      this.resetForm();
      this.refresh();
    },
    async confirmMutation() {
      if (confirm('continue?')) {
        await this.deleteAndRefresh();
      }
    },
    async deleteAndRefresh() {
      await axios.delete('http://localhost:8000/api/v1/menu/delete', {});
      await this.unconditionalRefresh();
    },
    async unconditionalRefresh() {
      await axios.post('http://localhost:8000/api/v1/menu/get_all_menu_item', {});
    },
    resetForm() {
      this.form = {};
    },
    async refresh() {
      if (this.token) {
        await axios.post('http://localhost:8000/api/v1/menu/get_all_menu_item', {});
      }
    },
    neverBound() {
      this.loadVehicle();
    },
  }
}
</script>
'''

COMPONENT_DETAIL = '''\
<template>
  <div>
    <b-button @click="load">reload</b-button>
  </div>
</template>

<script>
import axios from "axios";
import {mapGetters} from 'vuex';

export default {
  computed: {
    ...mapGetters(['getToken']),
    token() {
      return this.getToken;
    }
  },
  methods: {
    async load() {
      await axios.get('http://localhost:8000/api/v1/restaurant/get_all_restaurant_info');
    },
  },
  async created() {
    await this.load();
  }
};
</script>
'''

COMPONENT_VERIFY = '''\
<template>
  <div>
    <b-button @click="verify">confirm</b-button>
  </div>
</template>

<script>
import axios from "axios";
import {mapGetters} from 'vuex';

export default {
  computed: {
    ...mapGetters(['getUserId']),
    userId() {
      return this.getUserId;
    }
  },
  methods: {
    async verify() {
      await axios.post('http://localhost:8000/api/v1/auth/verify', { user_id: this.userId });
      this.$router.push('/');
    },
  }
};
</script>
'''

# Never mounted by a routed view: dead code behind the router.
COMPONENT_GHOST = '''\
<template>
  <div>
    <b-button @click="load">ghost</b-button>
  </div>
</template>

<script>
import axios from "axios";

export default {
  methods: {
    async load() {
      await axios.get('http://localhost:8000/api/v1/status/get');
    },
  }
};
</script>
'''

# --------------------------------------------------------------------------------------
# Fixture: approved Pass-5 UserFlow pages the fixture composes
# --------------------------------------------------------------------------------------

FIXTURE_USER_FLOWS: tuple[tuple[str, str, str], ...] = (
    ("flow.fx.gateway.post.auth.login", "POST", "/auth/login"),
    ("flow.fx.gateway.post.auth.verify", "POST", "/auth/verify"),
    ("flow.fx.gateway.get.vehicle.get-info", "GET", "/vehicle/get_info"),
    ("flow.fx.gateway.get.profile.user-info", "GET", "/profile/user_info"),
    ("flow.fx.gateway.get.status.get", "GET", "/status/get"),
    ("flow.fx.gateway.post.location.submit", "POST", "/location/submit"),
    ("flow.fx.gateway.post.menu.add", "POST", "/menu/add"),
    ("flow.fx.gateway.delete.menu.delete", "DELETE", "/menu/delete"),
    ("flow.fx.gateway.post.menu.get-all-menu-item", "POST", "/menu/get_all_menu_item"),
    (
        "flow.fx.gateway.get.restaurant.get-all-restaurant-info",
        "GET",
        "/restaurant/get_all_restaurant_info",
    ),
    # Two approved pages claim the same method and path, so the mapping is ambiguous.
    ("flow.fx.gateway.get.ambiguous.twin-a", "GET", "/ambiguous/twin"),
    ("flow.fx.gateway.get.ambiguous.twin-b", "GET", "/ambiguous/twin"),
)


def _write(root: Path, relative: str, content: str) -> None:
    target = root / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    with open(target, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(content)


@pytest.fixture(scope="module")
def fixture_repo(tmp_path_factory) -> Path:
    root = tmp_path_factory.mktemp("fx-repo")
    _write(root, bf.ROUTER_PATH, ROUTER)
    _write(root, bf.STORE_PATH, STORE)
    _write(root, f"{VIEWS}/Landing.vue", VIEW_LANDING)
    _write(root, f"{VIEWS}/Detail.vue", VIEW_DETAIL)
    _write(root, f"{VIEWS}/Verify.vue", VIEW_VERIFY)
    _write(root, f"{VIEWS}/Empty.vue", VIEW_EMPTY)
    _write(root, f"{COMPONENTS}/Landing.vue", COMPONENT_LANDING)
    _write(root, f"{COMPONENTS}/Detail.vue", COMPONENT_DETAIL)
    _write(root, f"{COMPONENTS}/Verify.vue", COMPONENT_VERIFY)
    _write(root, f"{COMPONENTS}/Ghost.vue", COMPONENT_GHOST)
    _write(root, bf.GATEWAY_SERVICE_CONFIG_PATH, GATEWAY_CONFIG)
    _write(root, bf.GATEWAY_MAIN_PATH, GATEWAY_MAIN)
    return root


@pytest.fixture(scope="module")
def fixture_knowledge_root(tmp_path_factory) -> Path:
    root = tmp_path_factory.mktemp("fx-knowledge")
    for identifier, method, path in FIXTURE_USER_FLOWS:
        front = {
            "id": identifier,
            "kind": "UserFlow",
            "type": "UserFlow",
            "title": f"{method} {path} execution flow",
            "status": "approved",
            "http_method": method,
            "path": path,
        }
        body = yaml.safe_dump(front, sort_keys=False)
        _write(
            root,
            f"{bf.CANONICAL_FLOWS_DIR}/{identifier}.md",
            f"---\n{body}---\n\n# {identifier}\n",
        )
    return root


@pytest.fixture(scope="module")
def fixture_record(fixture_repo: Path) -> RepositoryRecord:
    return RepositoryRecord(
        id="fx",
        path=fixture_repo,
        url=None,
        default_branch="main",
        expected_commit="0" * 40,
        owner="fx-cohort",
        sources={"frontend": ("ui/**/*",), "code": ("backend/**/*",)},
    )


@pytest.fixture(scope="module")
def fixture_model(fixture_record, fixture_knowledge_root):
    warnings: list[str] = []
    flows = load_canonical_user_flows(fixture_knowledge_root / bf.CANONICAL_FLOWS_DIR)
    model = build_frontend_model(
        fixture_record, "0" * 40, canonical_flows=flows, warnings=warnings
    )
    return model, warnings


def walk(model, handler: str, world: dict[str, str] | None = None):
    walker = ChainWalker(model, world or {})
    return walker, walker.run(f"{COMPONENTS}/Landing.vue", handler)


# --------------------------------------------------------------------------------------
# Ontology and namespace ownership
# --------------------------------------------------------------------------------------


def test_business_flow_is_an_accepted_entity_kind() -> None:
    document = yaml.safe_load(
        (AIDE_ROOT / "ontology/entity-types.yaml").read_text(encoding="utf-8")
    )

    assert BUSINESS_FLOW_KIND in document["entity_types"]
    # The step kind is reused, not shadowed by a second business-only kind.
    assert FLOW_STEP_KIND in document["entity_types"]
    assert "BusinessStep" not in document["entity_types"]


def test_pass_six_introduces_no_relationship_type() -> None:
    document = yaml.safe_load(
        (AIDE_ROOT / "ontology/relationship-types.yaml").read_text(encoding="utf-8")
    )
    declared = {str(entry["type"]).upper() for entry in document["relationship_types"]}

    assert {CONTAINS, DERIVED_FROM, PRECEDES} <= declared


def test_candidate_directories_are_disjoint_from_pass_five() -> None:
    assert CANDIDATE_SUBDIRECTORIES == ("business-flows", "business-steps")
    assert not set(CANDIDATE_SUBDIRECTORIES) & set(uf.CANDIDATE_SUBDIRECTORIES)


def test_business_identity_namespace_cannot_collide_with_pass_five() -> None:
    flow = business_flow_id("ftgo", "account-registration-verification")
    step = business_step_id("ftgo", "account-registration-verification", "register")

    assert flow == "business-flow.ftgo.ui.account-registration-verification"
    assert step == "step.business.ftgo.account-registration-verification.register"
    assert not collides_with_pass5(flow)
    assert not collides_with_pass5(step)
    assert collides_with_pass5("flow.ftgo.gateway.post.auth.register")
    assert collides_with_pass5("step.ftgo.gateway.post.auth.register.http-ingress")


def test_business_flow_kind_is_registered_with_the_cli() -> None:
    spec = EXTRACTORS["business-flow"]

    assert spec.candidate_subdirectories == CANDIDATE_SUBDIRECTORIES
    assert spec.sidecars is None


# --------------------------------------------------------------------------------------
# Vue single-file component parsing
# --------------------------------------------------------------------------------------


def test_script_blocks_are_located_without_evaluating_the_component() -> None:
    source = build_source_text("x.vue", COMPONENT_VERIFY)
    blocks = extract_script_blocks(source.text)

    assert len(blocks) == 1
    body = source.text[blocks[0].start : blocks[0].end]
    assert "export default" in body
    assert "<template>" not in body


def test_an_empty_setup_block_leaves_the_component_empty() -> None:
    component = parse_component(f"{VIEWS}/Empty.vue", VIEW_EMPTY)

    assert component.is_empty
    assert component.handlers == {}


def test_only_template_bound_and_lifecycle_handlers_are_reachable(fixture_model) -> None:
    model, _ = fixture_model
    reachable = set(model.reachable_handlers[f"{COMPONENTS}/Landing.vue"])

    assert "submit" in reachable
    # Reached only through a bound handler, never bound itself.
    assert "loadVehicle" in reachable
    assert "tick" in reachable
    # Declared but wired to nothing: dead code must not seed a journey.
    assert "neverBound" not in reachable


def test_store_getters_and_actions_resolve_to_state_keys() -> None:
    store = parse_store(build_source_text(bf.STORE_PATH, STORE))

    assert store.state_read_by("getUserId") == "userId"
    assert store.state_written_by("updateUserId") == "userId"
    assert store.state_written_by("updateToken") == "token"
    assert store.state_read_by("nope") is None


# --------------------------------------------------------------------------------------
# Routes and views
# --------------------------------------------------------------------------------------


def test_routes_resolve_exactly_to_scanned_view_modules() -> None:
    source = build_source_text(bf.ROUTER_PATH, ROUTER)
    views = frozenset(
        f"{VIEWS}/{name}.vue" for name in ("Landing", "Detail", "Empty", "Verify")
    )
    routes, warnings = parse_router(source, views)

    assert warnings == ()
    assert {route.name for route in routes} == {"Landing", "Detail", "Empty", "Verify"}
    assert {route.path for route in routes} == {"/", "/Detail", "/Empty", "/Verify"}


def test_a_view_that_mounts_a_component_resolves_to_it() -> None:
    view = parse_component(f"{VIEWS}/Detail.vue", VIEW_DETAIL)
    resolved = resolve_view(view, frozenset({f"{COMPONENTS}/Detail.vue"}))

    assert resolved.component_path == f"{COMPONENTS}/Detail.vue"
    assert not resolved.is_empty


def test_an_empty_view_mounts_nothing(fixture_model) -> None:
    model, _ = fixture_model
    resolved = model.view_resolution[f"{VIEWS}/Empty.vue"]

    assert resolved.is_empty
    assert resolved.component_path is None


def test_multi_line_router_push_resolves_like_a_single_line_one(fixture_model) -> None:
    model, _ = fixture_model
    component = model.components[f"{COMPONENTS}/Landing.vue"]
    navigations = [
        operation
        for operation in bf._all_operations(component.handlers["submit"].operations)
        if operation.kind == bf.OP_NAVIGATION
    ]

    # '/Detail', the multi-line { name: 'Verify' }, and the default '/'.
    assert [item.route_name or item.route_path for item in navigations] == [
        "/Detail",
        "Verify",
        "/",
    ]


def test_a_navigation_to_an_undeclared_route_is_reported_not_guessed(fixture_model) -> None:
    model, _ = fixture_model
    _, chain = walk(model, "goMissing")

    assert chain.steps == ()
    assert chain.unknown_routes == ("NoSuchRoute",)
    assert "not a declared route" in str(chain.stop_reason)


def test_a_non_static_navigation_is_reported_not_followed(fixture_model) -> None:
    model, _ = fixture_model
    _, chain = walk(model, "goBack")

    assert chain.steps == ()
    assert [item["reason"] for item in chain.route_failures] == [
        "this.$router.go has no statically resolvable destination"
    ]


def test_a_route_to_an_empty_view_stops_the_journey(fixture_model) -> None:
    model, _ = fixture_model
    _, chain = walk(model, "goEmpty")

    assert chain.steps == ()
    assert [item["view"] for item in chain.empty_views] == [f"{VIEWS}/Empty.vue"]
    assert "mounts nothing" in str(chain.stop_reason)


# --------------------------------------------------------------------------------------
# API prefix and UserFlow mapping
# --------------------------------------------------------------------------------------


def test_the_api_prefix_needs_both_a_default_and_a_mount_site() -> None:
    resolved = resolve_api_prefix("fx", "0" * 40, GATEWAY_CONFIG, GATEWAY_MAIN)

    assert resolved.resolved
    assert resolved.value == "/api/v1"
    assert resolved.config_provenance is not None
    assert resolved.mount_provenance is not None

    # The default alone does not prove every route is mounted behind it.
    without_mount = resolve_api_prefix("fx", "0" * 40, GATEWAY_CONFIG, "app = 1\n")
    assert not without_mount.resolved
    assert "include_router" in str(without_mount.reason)


def test_url_normalization_strips_origin_and_the_configured_prefix(fixture_model) -> None:
    model, _ = fixture_model
    mapping = map_to_user_flow(
        "post",
        "http://localhost:8000/api/v1/auth/register",
        model.prefix,
        {("POST", "/auth/register"): ("flow.fx.gateway.post.auth.register",)},
    )

    assert mapping.path == "/auth/register"
    assert mapping.user_flow_id == "flow.fx.gateway.post.auth.register"


def test_mapping_requires_one_exact_method_and_path_match(fixture_model) -> None:
    model, _ = fixture_model
    index = model.user_flow_index

    exact = map_to_user_flow("get", "http://h/api/v1/status/get", model.prefix, index)
    assert exact.user_flow_id == "flow.fx.gateway.get.status.get"
    # Same path, wrong method: no suffix or nearest-name fallback is attempted.
    wrong_method = map_to_user_flow("post", "http://h/api/v1/status/get", model.prefix, index)
    assert wrong_method.user_flow_id is None
    assert "no approved Pass-5 UserFlow declares POST /status/get" in str(wrong_method.reason)


def test_an_ambiguous_mapping_is_refused(fixture_model) -> None:
    model, _ = fixture_model
    mapping = map_to_user_flow(
        "get", "http://h/api/v1/ambiguous/twin", model.prefix, model.user_flow_index
    )

    assert mapping.user_flow_id is None
    assert len(mapping.matches) == 2
    assert "2 approved Pass-5 UserFlows" in str(mapping.reason)


def test_a_zero_match_request_becomes_an_unresolved_segment(fixture_model) -> None:
    model, _ = fixture_model
    _, chain = walk(model, "missingFlow")

    assert chain.steps == ()
    assert [item["normalized_path"] for item in chain.unresolved_segments] == ["/status/online"]


def test_a_conditional_request_url_yields_every_literal_outcome(fixture_model) -> None:
    model, _ = fixture_model
    _, chain = walk(model, "toggle")

    assert sorted(item["normalized_path"] for item in chain.unresolved_segments) == [
        "/status/offline",
        "/status/online",
    ]
    # The awaited unresolved request still orders the status read that follows it.
    assert [step.path for step in chain.steps] == ["/status/get", "/location/submit"]


# --------------------------------------------------------------------------------------
# Ordering evidence
# --------------------------------------------------------------------------------------


def test_an_awaited_mutation_orders_an_unawaited_refresh(fixture_model) -> None:
    model, _ = fixture_model
    _, chain = walk(model, "mutateAndRefresh")

    assert [step.path for step in chain.steps] == ["/menu/add", "/menu/get_all_menu_item"]
    assert chain.steps[1].ordered_from_previous
    assert MECHANISM_AWAIT in chain.steps[1].order_mechanisms
    assert MECHANISM_HELPER in chain.steps[1].mechanisms


def test_two_unawaited_calls_in_one_handler_prove_no_order(fixture_model) -> None:
    model, _ = fixture_model
    _, chain = walk(model, "unordered")

    assert [step.path for step in chain.steps] == ["/vehicle/get_info"]
    assert "no ordering evidence" in str(chain.stop_reason)


def test_a_synchronous_helper_does_not_destroy_ordering_evidence(fixture_model) -> None:
    """``resetForm()`` issues no request, so it cannot invalidate the awaited mutation."""
    model, _ = fixture_model
    _, chain = walk(model, "mutateAndRefresh")

    assert len(chain.steps) == MIN_USER_FLOWS_PER_BUSINESS_FLOW


def test_a_lifecycle_hook_continues_the_journey_after_navigation(fixture_model) -> None:
    model, _ = fixture_model
    _, chain = walk(model, "submit", {"this.role": "driver"})

    assert [step.path for step in chain.steps] == [
        "/auth/login",
        "/vehicle/get_info",
        "/restaurant/get_all_restaurant_info",
    ]
    last = chain.steps[-1]
    assert last.trigger == TRIGGER_AUTOMATIC
    assert MECHANISM_NAVIGATION in last.mechanisms
    assert MECHANISM_LIFECYCLE in last.mechanisms


def test_navigation_alone_does_not_imply_a_later_request(fixture_model) -> None:
    model, _ = fixture_model
    _, chain = walk(model, "justNavigate")

    # The destination does have a lifecycle request, but nothing preceded the navigation, so
    # there is no journey: a page visit on its own is not a business flow.
    assert [step.path for step in chain.steps] == ["/restaurant/get_all_restaurant_info"]
    assert len(chain.steps) < MIN_USER_FLOWS_PER_BUSINESS_FLOW


def test_a_user_action_destination_composes_only_on_a_vuex_dependency(fixture_model) -> None:
    model, _ = fixture_model
    _, chain = walk(model, "submit", {"this.role": "rider"})

    assert [step.path for step in chain.steps] == [
        "/auth/login",
        "/profile/user_info",
        "/auth/verify",
    ]
    verify = chain.steps[-1]
    assert verify.trigger == TRIGGER_USER_ACTION
    assert MECHANISM_VUEX in verify.mechanisms
    # The verify page navigates on to the landing page, which offers several request-issuing
    # buttons, so the walk stops rather than picking one.
    assert "the next stage is ambiguous" in str(chain.stop_reason)


def test_a_role_branch_selects_only_its_own_world(fixture_model) -> None:
    model, _ = fixture_model
    _, driver = walk(model, "submit", {"this.role": "driver"})
    _, rider = walk(model, "submit", {"this.role": "rider"})

    assert "/vehicle/get_info" in [step.path for step in driver.steps]
    assert "/vehicle/get_info" not in [step.path for step in rider.steps]
    assert "/profile/user_info" in [step.path for step in rider.steps]
    assert "/profile/user_info" not in [step.path for step in driver.steps]


def test_a_conditional_request_keeps_its_guard(fixture_model) -> None:
    model, _ = fixture_model
    _, chain = walk(model, "mutateAndRefresh")
    refresh = chain.steps[-1]

    assert refresh.trigger == TRIGGER_CONDITIONAL
    assert [item.text for item in refresh.conditions] == ["this.token"]


def test_a_confirmation_gate_triggers_only_the_mutation_not_an_unconditional_refresh(
    fixture_model,
) -> None:
    model, _ = fixture_model
    _, chain = walk(model, "confirmMutation")
    mutation, refresh = chain.steps

    assert [step.path for step in chain.steps] == [
        "/menu/delete",
        "/menu/get_all_menu_item",
    ]
    assert mutation.trigger == TRIGGER_CONDITIONAL
    assert [item.text for item in mutation.conditions] == ["confirm('continue?')"]
    assert refresh.trigger == TRIGGER_AUTOMATIC
    assert refresh.conditions == ()
    assert [item.text for item in refresh.inherited_conditions] == ["confirm('continue?')"]


def test_an_interval_callback_carries_its_period_and_breaks_ordering(fixture_model) -> None:
    model, _ = fixture_model
    _, chain = walk(model, "startTicker")

    assert [step.path for step in chain.steps] == ["/status/get", "/location/submit"]
    assert [step.loop_interval_ms for step in chain.steps] == [5000, 5000]
    assert MECHANISM_INTERVAL in chain.steps[0].mechanisms
    assert chain.steps[1].trigger == TRIGGER_CONDITIONAL
    assert [item.text for item in chain.steps[1].conditions] == ["this.active"]


def test_a_timer_callback_is_not_a_continuation_of_its_scheduler(fixture_model) -> None:
    """A request awaited before ``setInterval`` cannot order one made inside the callback."""
    model, _ = fixture_model
    walker = ChainWalker(model, {})
    chain = walker.run(f"{COMPONENTS}/Landing.vue", "startTicker")

    assert not chain.steps[0].ordered_from_previous


def test_an_unmounted_component_is_reported_as_unreachable(fixture_model) -> None:
    _, warnings = fixture_model

    assert any(f"{COMPONENTS}/Ghost.vue" in warning for warning in warnings)


def test_the_minimum_is_two_distinct_user_flows(fixture_model) -> None:
    model, _ = fixture_model
    _, single = walk(model, "justNavigate")
    _, pair = walk(model, "mutateAndRefresh")

    assert bf._outcome(single, ()) == OUTCOME_REJECTED
    assert bf._outcome(pair, ()) == OUTCOME_RESOLVED


def test_step_slugs_qualify_only_when_they_collide() -> None:
    assert bf._assign_step_slugs(
        ("flow.x.gateway.post.auth.login", "flow.x.gateway.get.status.get")
    ) == ("login", "get")
    assert bf._assign_step_slugs(
        ("flow.x.gateway.post.menu.add", "flow.x.gateway.post.address.add")
    ) == ("menu.add", "address.add")


def test_the_fixture_repository_yields_no_declared_ftgo_journey(
    fixture_record, fixture_knowledge_root
) -> None:
    """The catalog names FTGO components; a different frontend must reject every one."""
    extraction = extract_business_flow(
        fixture_record, "0" * 40, knowledge_root=fixture_knowledge_root
    )

    assert extraction.flows == ()
    assert extraction.steps == ()
    assert len(extraction.rejected) == len(bf.HYPOTHESES) + len(bf.REJECTION_PROBES)
    # Something is still provable there; it is reported rather than silently dropped.
    assert extraction.deferred


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
    return extract_business_flow(record, FROZEN_COMMIT, knowledge_root=AIDE_ROOT)


def journeys(extraction) -> dict[str, tuple[str, ...]]:
    return {flow.id: flow.user_flow_ids for flow in extraction.flows}


def rendered_frontmatter(real_extraction) -> dict[str, dict]:
    rendered, _ = render_bundle(real_extraction)
    return {
        relative_path: yaml.safe_load(content.split("---")[1])
        for relative_path, content in rendered.items()
    }


def test_real_ftgo_cross_file_flow_uses_separate_concrete_source_refs(real_extraction) -> None:
    fronts = rendered_frontmatter(real_extraction)
    page = fronts[
        "business-flows/business-flow.ftgo.ui.account-registration-verification.md"
    ]

    assert [
        (ref["path"], ref["symbol"], ref["line_start"], ref["line_end"])
        for ref in page["source_refs"]
    ] == [
        ("ui/src/components/SignUpComp.vue", "SignUpComp.signup", 113, 113),
        (
            "ui/src/components/VerifyAccountPage.vue",
            "VerifyAccountPage.verify",
            75,
            75,
        ),
    ]


def test_real_ftgo_every_candidate_and_relation_has_coherent_provenance(
    real_extraction,
) -> None:
    record = _real_ftgo_record()
    assert record is not None
    fronts = rendered_frontmatter(real_extraction)

    assert len(fronts) == 34
    for front in fronts.values():
        refs = [*front.get("source_refs", []), *front.get("relations", [])]
        for ref in refs:
            assert ("line_start" in ref) == ("line_end" in ref)
            if "line_start" in ref:
                assert ref["line_start"] <= ref["line_end"]
            assert (record.path / ref["path"]).is_file()
            assert ref["commit"] == FROZEN_COMMIT
            if symbol := ref.get("symbol"):
                assert symbol.startswith(f"{Path(ref['path']).stem}.")

    step_fronts = {
        front["id"]: front for front in fronts.values() if front["kind"] == FLOW_STEP_KIND
    }
    for flow_front in (front for front in fronts.values() if front["kind"] == BUSINESS_FLOW_KIND):
        contains = sorted(
            (item for item in flow_front["relations"] if item["type"] == CONTAINS),
            key=lambda item: item["position"],
        )
        expected: list[dict] = []
        for relation in contains:
            for ref in step_fronts[relation["target"]]["source_refs"]:
                if ref not in expected:
                    expected.append(ref)
        assert flow_front["source_refs"] == expected


def test_real_ftgo_same_file_multi_handler_flow_keeps_separate_ranges(
    real_extraction,
) -> None:
    fronts = rendered_frontmatter(real_extraction)
    page = fronts[
        "business-flows/business-flow.ftgo.ui.restaurant-menu-delete-refresh.md"
    ]

    assert [
        (ref["symbol"], ref["line_start"], ref["line_end"]) for ref in page["source_refs"]
    ] == [
        ("SupplierMainPage.deleteItem", 189, 192),
        ("SupplierMainPage.fetchMenu", 131, 137),
    ]


def test_real_ftgo_lifecycle_invocation_sets_the_flow_entry_trigger(
    real_extraction,
) -> None:
    flow = next(
        item
        for item in real_extraction.flows
        if item.id == "business-flow.ftgo.ui.driver-active-location-refresh"
    )
    fronts = rendered_frontmatter(real_extraction)
    page = fronts[
        "business-flows/business-flow.ftgo.ui.driver-active-location-refresh.md"
    ]

    assert flow.entry_trigger == TRIGGER_LIFECYCLE
    assert flow.attributes["entry_trigger"] == TRIGGER_LIFECYCLE
    assert page["attributes"]["entry_trigger"] == TRIGGER_LIFECYCLE


def test_real_ftgo_registration_is_followed_by_verification(real_extraction) -> None:
    flow = next(
        item
        for item in real_extraction.flows
        if item.id == "business-flow.ftgo.ui.account-registration-verification"
    )

    assert flow.user_flow_ids == (
        "flow.ftgo.gateway.post.auth.register",
        "flow.ftgo.gateway.post.auth.verify",
    )
    assert flow.outcome == OUTCOME_RESOLVED
    # The role is a form field, so the journey belongs to every declared role, not one.
    assert flow.actor is None
    assert flow.actors == ("customer", "driver", "restaurant_admin")
    verify = real_extraction.steps_of(flow.id)[1]
    assert MECHANISM_VUEX in verify.evidence_mechanisms
    assert verify.trigger == TRIGGER_USER_ACTION


def test_real_ftgo_does_not_append_login_to_verification(real_extraction) -> None:
    """Verification navigates to the sign-in page; submitting the form is a separate choice."""
    for identifier, chain in journeys(real_extraction).items():
        if identifier == "business-flow.ftgo.ui.account-registration-verification":
            assert "flow.ftgo.gateway.post.auth.login" not in chain


def test_real_ftgo_customer_login_lands_on_the_restaurant_list(real_extraction) -> None:
    flow = next(
        item
        for item in real_extraction.flows
        if item.id == "business-flow.ftgo.ui.customer-login-restaurant-browse"
    )

    assert flow.user_flow_ids == (
        "flow.ftgo.gateway.post.auth.login",
        "flow.ftgo.gateway.get.restaurant.get-all-restaurant-info",
    )
    assert flow.actor == "customer"


def test_real_ftgo_driver_login_bootstraps_vehicle_then_status(real_extraction) -> None:
    flow = next(
        item
        for item in real_extraction.flows
        if item.id == "business-flow.ftgo.ui.driver-login-bootstrap"
    )

    assert flow.user_flow_ids == (
        "flow.ftgo.gateway.post.auth.login",
        "flow.ftgo.gateway.get.vehicle.get-info",
        "flow.ftgo.gateway.get.status.get",
    )
    assert flow.actor == "driver"


def test_real_ftgo_restaurant_admin_login_bootstraps_restaurant_then_menu(
    real_extraction,
) -> None:
    flow = next(
        item
        for item in real_extraction.flows
        if item.id == "business-flow.ftgo.ui.restaurant-admin-login-bootstrap"
    )

    assert flow.user_flow_ids == (
        "flow.ftgo.gateway.post.auth.login",
        "flow.ftgo.gateway.get.restaurant.get-supplier-restaurant-info",
        "flow.ftgo.gateway.post.menu.get-all-menu-item",
    )
    assert flow.actor == "restaurant_admin"
    # The menu read is guarded by the restaurant the previous step stored.
    menu = real_extraction.steps_of(flow.id)[2]
    assert [item.text for item in menu.conditions] == ["this.restaurant"]


def test_real_ftgo_vehicle_onboarding_and_restaurant_onboarding(real_extraction) -> None:
    mapping = journeys(real_extraction)

    assert mapping["business-flow.ftgo.ui.driver-vehicle-onboarding"] == (
        "flow.ftgo.gateway.post.vehicle.register",
        "flow.ftgo.gateway.get.vehicle.get-info",
        "flow.ftgo.gateway.get.status.get",
    )
    assert mapping["business-flow.ftgo.ui.restaurant-onboarding"] == (
        "flow.ftgo.gateway.post.restaurant.register",
        "flow.ftgo.gateway.get.restaurant.get-supplier-restaurant-info",
        "flow.ftgo.gateway.post.menu.get-all-menu-item",
    )


def test_real_ftgo_driver_location_refresh_is_conditional_and_periodic(real_extraction) -> None:
    flow = next(
        item
        for item in real_extraction.flows
        if item.id == "business-flow.ftgo.ui.driver-active-location-refresh"
    )
    steps = real_extraction.steps_of(flow.id)

    assert flow.user_flow_ids == (
        "flow.ftgo.gateway.get.status.get",
        "flow.ftgo.gateway.post.location.submit",
    )
    assert [step.loop_interval_ms for step in steps] == [5000, 5000]
    assert steps[1].trigger == TRIGGER_CONDITIONAL
    assert [item.text for item in steps[1].conditions] == ["this.isActive"]


def test_real_ftgo_has_three_menu_mutation_refresh_journeys(real_extraction) -> None:
    mapping = journeys(real_extraction)

    assert mapping["business-flow.ftgo.ui.restaurant-menu-add-refresh"] == (
        "flow.ftgo.gateway.post.menu.add",
        "flow.ftgo.gateway.post.menu.get-all-menu-item",
    )
    assert mapping["business-flow.ftgo.ui.restaurant-menu-update-refresh"] == (
        "flow.ftgo.gateway.put.menu.update",
        "flow.ftgo.gateway.post.menu.get-all-menu-item",
    )
    assert mapping["business-flow.ftgo.ui.restaurant-menu-delete-refresh"] == (
        "flow.ftgo.gateway.delete.menu.delete",
        "flow.ftgo.gateway.post.menu.get-all-menu-item",
    )


def test_real_ftgo_menu_delete_keeps_its_confirmation_guard(real_extraction) -> None:
    steps = real_extraction.steps_of("business-flow.ftgo.ui.restaurant-menu-delete-refresh")
    mutation, refresh = steps
    guards = [item.kind for item in mutation.conditions]

    assert bf.CONDITION_CONFIRM in guards
    assert mutation.trigger == TRIGGER_CONDITIONAL
    assert [item.text for item in refresh.conditions] == ["this.restaurant"]
    assert [item.kind for item in refresh.inherited_conditions] == [bf.CONDITION_CONFIRM]


def test_real_ftgo_emits_exactly_the_declared_journeys(real_extraction) -> None:
    declared = {
        business_flow_id("ftgo", hypothesis.journey_slug) for hypothesis in bf.HYPOTHESES
    }

    assert set(journeys(real_extraction)) == declared
    assert all(flow.outcome == OUTCOME_RESOLVED for flow in real_extraction.flows)


def test_real_ftgo_every_step_is_a_business_layer_user_flow_reference(real_extraction) -> None:
    assert {step.kind for step in real_extraction.steps} == {FLOW_STEP_KIND}
    assert {flow.kind for flow in real_extraction.flows} == {BUSINESS_FLOW_KIND}
    for step in real_extraction.steps:
        assert step.attributes["layer"] == bf.BUSINESS_LAYER
        assert step.attributes["role"] == bf.BUSINESS_STEP_ROLE
        assert step.id.startswith(bf.BUSINESS_STEP_PREFIX)
        assert step.user_flow_id.startswith("flow.ftgo.gateway.")


def test_real_ftgo_relationships_are_only_the_three_reused_types(real_extraction) -> None:
    counts: dict[str, int] = {}
    for relation in real_extraction.relationships:
        counts[relation.type] = counts.get(relation.type, 0) + 1

    assert set(counts) == {CONTAINS, DERIVED_FROM, PRECEDES}
    assert counts[CONTAINS] == len(real_extraction.steps)
    assert counts[DERIVED_FROM] == len(real_extraction.steps)
    assert counts[PRECEDES] == len(real_extraction.steps) - len(real_extraction.flows)


def test_real_ftgo_derived_from_targets_are_approved_user_flow_pages(real_extraction) -> None:
    approved = {
        ref.id for ref in load_canonical_user_flows(AIDE_ROOT / bf.CANONICAL_FLOWS_DIR)
    }

    for relation in real_extraction.relationships:
        if relation.type == DERIVED_FROM:
            assert relation.target in approved


def test_real_ftgo_stops_at_the_empty_menu_page(real_extraction) -> None:
    rejected = {item["id"]: item for item in real_extraction.rejected}
    entry = rejected["business-flow.ftgo.ui.customer-browse-menu-order-placement"]

    assert entry["verified"]
    assert entry["probe"] == bf.PROBE_EMPTY_VIEW
    assert [item["view"] for item in real_extraction.empty_views] == [
        "ui/src/views/MenuPage.vue"
    ]
    for chain in journeys(real_extraction).values():
        assert "flow.ftgo.gateway.post.order.create" not in chain
        assert "flow.ftgo.gateway.get.menu.get-info" not in chain


def test_real_ftgo_fabricates_no_order_lifecycle_or_feedback_journey(real_extraction) -> None:
    rejected = {item["id"]: item for item in real_extraction.rejected}

    for slug in ("order-lifecycle-create-confirm-delivery", "feedback-rating-journey"):
        entry = rejected[business_flow_id("ftgo", slug)]
        assert entry["verified"]
        assert entry["probe"] == bf.PROBE_ABSENT_CALL_SITES

    referenced = {flow for chain in journeys(real_extraction).values() for flow in chain}
    assert not any("order" in identifier for identifier in referenced)
    assert not any("feedback" in identifier for identifier in referenced)


def test_real_ftgo_leaves_online_and_offline_as_unresolved_segments(real_extraction) -> None:
    paths = {item["normalized_path"] for item in real_extraction.unresolved_segments}

    assert {"/status/online", "/status/offline"} <= paths
    for chain in journeys(real_extraction).values():
        assert not any("status.online" in flow or "status.offline" in flow for flow in chain)


def test_real_ftgo_does_not_canonicalize_logout_or_teardown(real_extraction) -> None:
    rejected = {item["id"]: item for item in real_extraction.rejected}

    for slug in (
        "customer-logout-login",
        "customer-profile-address-management",
        "restaurant-vehicle-teardown",
        "driver-online-status-toggle",
    ):
        assert rejected[business_flow_id("ftgo", slug)]["verified"]

    referenced = {flow for chain in journeys(real_extraction).values() for flow in chain}
    assert "flow.ftgo.gateway.post.profile.logout" not in referenced
    assert "flow.ftgo.gateway.delete.profile.delete" not in referenced


def test_real_ftgo_has_no_collisions_or_cycles(real_extraction) -> None:
    assert real_extraction.identity_collisions == ()
    assert real_extraction.cycles_detected == ()


def test_real_ftgo_report_records_no_mutation_and_no_graphiti(real_extraction) -> None:
    _, report = render_bundle(real_extraction)

    assert report["graph_mutations"] == 0
    assert report["wiki_writes"] == 0
    assert report["neo4j_mutations"] == 0
    assert report["graphiti"] == "disabled"
    assert report["modules_imported"] == 0
    assert report["modules_executed"] == 0
    assert report["runtime_connections_opened"] == 0
    assert report["relationship_types_introduced"] == []
    assert report["ontology_kinds_introduced"] == [BUSINESS_FLOW_KIND]


def test_real_ftgo_extraction_leaves_canonical_knowledge_untouched() -> None:
    record = _real_ftgo_record()
    if record is None:
        pytest.skip("FTGO checkout at the frozen commit is not available")

    def digest() -> str:
        hasher = hashlib.sha256()
        for page in sorted((AIDE_ROOT / "wiki").rglob("*.md")):
            hasher.update(page.relative_to(AIDE_ROOT).as_posix().encode("utf-8"))
            hasher.update(page.read_bytes())
        return hasher.hexdigest()

    before = digest()
    extraction = extract_business_flow(record, FROZEN_COMMIT, knowledge_root=AIDE_ROOT)
    render_bundle(extraction)

    assert digest() == before


def test_real_ftgo_output_is_byte_identical_across_runs(real_extraction) -> None:
    record = _real_ftgo_record()
    assert record is not None
    repeated = extract_business_flow(record, FROZEN_COMMIT, knowledge_root=AIDE_ROOT)

    first, first_report = render_bundle(real_extraction)
    second, second_report = render_bundle(repeated)

    assert first.keys() == second.keys()
    for relative_path in first:
        assert first[relative_path] == second[relative_path], relative_path
    assert json.dumps(first_report, indent=2, sort_keys=True) == json.dumps(
        second_report, indent=2, sort_keys=True
    )


def test_real_ftgo_renders_one_page_per_candidate(real_extraction) -> None:
    rendered, _ = render_bundle(real_extraction)
    flow_pages = [name for name in rendered if name.startswith("business-flows/")]
    step_pages = [name for name in rendered if name.startswith("business-steps/")]

    assert len(flow_pages) == len(real_extraction.flows)
    assert len(step_pages) == len(real_extraction.steps)
    assert set(rendered) == set(flow_pages) | set(step_pages)
    for content in rendered.values():
        front = yaml.safe_load(content.split("---")[1])
        assert front["status"] == "candidate"
        assert front["review_status"] == "pending"
        assert front["commit"] == FROZEN_COMMIT
