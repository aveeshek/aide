---
id: step.business.ftgo.restaurant-admin-login-bootstrap.get-all-menu-item
kind: FlowStep
type: FlowStep
title: 'Restaurant admin login bootstrap: POST /menu/get_all_menu_item'
status: approved
review_status: approved
candidate_of: business-flow-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: business-flow
owner: aide-ftgo-cohort
layer: business
role: user_flow_reference
business_flow: business-flow.ftgo.ui.restaurant-admin-login-bootstrap
position: 3
user_flow: flow.ftgo.gateway.post.menu.get-all-menu-item
http_method: POST
path: /menu/get_all_menu_item
trigger: conditional
evidence_mechanism:
- route_navigation
- lifecycle_hook
- helper_call
- conditional_branch
condition:
- this.restaurant
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: ui/src/components/SupplierMainPage.vue
  symbol: SupplierMainPage.fetchMenu
  line_start: 131
  line_end: 137
  evidence_type: implemented
relations:
- type: DERIVED_FROM
  target: flow.ftgo.gateway.post.menu.get-all-menu-item
  evidence_mechanism:
  - route_navigation
  - lifecycle_hook
  - helper_call
  - conditional_branch
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: ui/src/components/SupplierMainPage.vue
  symbol: SupplierMainPage.fetchMenu
  line_start: 131
  line_end: 137
  evidence_type: implemented
inbound_relations:
- type: CONTAINS
  source: business-flow.ftgo.ui.restaurant-admin-login-bootstrap
  position: 3
  layer: business
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: ui/src/components/SupplierMainPage.vue
  symbol: SupplierMainPage.fetchMenu
  line_start: 131
  line_end: 137
  evidence_type: implemented
- type: PRECEDES
  source: step.business.ftgo.restaurant-admin-login-bootstrap.get-supplier-restaurant-info
  evidence_mechanism:
  - route_navigation
  - lifecycle_hook
  - helper_call
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: ui/src/components/SupplierMainPage.vue
  symbol: SupplierMainPage.fetchMenu
  line_start: 131
  line_end: 137
  evidence_type: implemented
attributes:
  layer: business
  role: user_flow_reference
  position: 3
  trigger: conditional
  http_method: POST
  path: /menu/get_all_menu_item
  evidence_mechanism:
  - route_navigation
  - lifecycle_hook
  - helper_call
  - conditional_branch
  actor: restaurant_admin
  condition:
  - this.restaurant
  condition_evidence:
  - condition: this.restaurant
    kind: if
---

# Restaurant admin login bootstrap: POST /menu/get_all_menu_item

Canonical business step referencing an approved Pass-5 UserFlow, extracted from reachability evidence in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Layer: `business`
- Role: `user_flow_reference`
- Business flow: `business-flow.ftgo.ui.restaurant-admin-login-bootstrap` (position 3)
- References user flow: `flow.ftgo.gateway.post.menu.get-all-menu-item`
- Trigger: `conditional`
- Evidence mechanism: `route_navigation`, `lifecycle_hook`, `helper_call`, `conditional_branch`
- Declared in: `ui/src/components/SupplierMainPage.vue` (lines 131-137)
- Evidence class: `implemented`

## Guards

- `this.restaurant` (`if`)

## Review notes

This approved canonical page records a source-backed business journey. It carries no endpoint, event or persistence detail of its own: that evidence already lives on the referenced UserFlow page and is not duplicated here.

