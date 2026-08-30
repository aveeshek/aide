---
id: step.business.ftgo.restaurant-admin-login-bootstrap.get-supplier-restaurant-info
kind: FlowStep
type: FlowStep
title: 'Restaurant admin login bootstrap: GET /restaurant/get_supplier_restaurant_info'
status: candidate
review_status: pending
candidate_of: business-flow-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: business-flow
owner: aide-ftgo-cohort
layer: business
role: user_flow_reference
business_flow: business-flow.ftgo.ui.restaurant-admin-login-bootstrap
position: 2
user_flow: flow.ftgo.gateway.get.restaurant.get-supplier-restaurant-info
http_method: GET
path: /restaurant/get_supplier_restaurant_info
trigger: automatic
evidence_mechanism:
- await_sequence
- helper_call
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: ui/src/components/SignInComp.vue
  symbol: SignInComp.fetchAndStoreRestaurantInfo
  line_start: 140
  line_end: 144
  evidence_type: implemented
relations:
- type: DERIVED_FROM
  target: flow.ftgo.gateway.get.restaurant.get-supplier-restaurant-info
  evidence_mechanism:
  - await_sequence
  - helper_call
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: ui/src/components/SignInComp.vue
  symbol: SignInComp.fetchAndStoreRestaurantInfo
  line_start: 140
  line_end: 144
  evidence_type: implemented
- type: PRECEDES
  target: step.business.ftgo.restaurant-admin-login-bootstrap.get-all-menu-item
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
inbound_relations:
- type: CONTAINS
  source: business-flow.ftgo.ui.restaurant-admin-login-bootstrap
  position: 2
  layer: business
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: ui/src/components/SignInComp.vue
  symbol: SignInComp.fetchAndStoreRestaurantInfo
  line_start: 140
  line_end: 144
  evidence_type: implemented
- type: PRECEDES
  source: step.business.ftgo.restaurant-admin-login-bootstrap.login
  evidence_mechanism:
  - await_sequence
  - helper_call
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: ui/src/components/SignInComp.vue
  symbol: SignInComp.fetchAndStoreRestaurantInfo
  line_start: 140
  line_end: 144
  evidence_type: implemented
attributes:
  layer: business
  role: user_flow_reference
  position: 2
  trigger: automatic
  http_method: GET
  path: /restaurant/get_supplier_restaurant_info
  evidence_mechanism:
  - await_sequence
  - helper_call
  actor: restaurant_admin
---

# Restaurant admin login bootstrap: GET /restaurant/get_supplier_restaurant_info

Candidate business step referencing an approved Pass-5 UserFlow, extracted from reachability evidence in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Layer: `business`
- Role: `user_flow_reference`
- Business flow: `business-flow.ftgo.ui.restaurant-admin-login-bootstrap` (position 2)
- References user flow: `flow.ftgo.gateway.get.restaurant.get-supplier-restaurant-info`
- Trigger: `automatic`
- Evidence mechanism: `await_sequence`, `helper_call`
- Declared in: `ui/src/components/SignInComp.vue` (lines 140-144)
- Evidence class: `implemented`

## Review notes

This page is a candidate awaiting review. It carries no endpoint, event or persistence detail of its own: that evidence already lives on the referenced UserFlow page and is not duplicated here.

