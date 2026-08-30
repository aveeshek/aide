---
id: step.business.ftgo.restaurant-onboarding.get-supplier-restaurant-info
kind: FlowStep
type: FlowStep
title: 'Restaurant onboarding: GET /restaurant/get_supplier_restaurant_info'
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
business_flow: business-flow.ftgo.ui.restaurant-onboarding
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
  path: ui/src/components/RegisterRestaurantPage.vue
  symbol: RegisterRestaurantPage.fetchAndStoreRestaurantInfo
  line_start: 163
  line_end: 167
  evidence_type: implemented
relations:
- type: DERIVED_FROM
  target: flow.ftgo.gateway.get.restaurant.get-supplier-restaurant-info
  evidence_mechanism:
  - await_sequence
  - helper_call
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: ui/src/components/RegisterRestaurantPage.vue
  symbol: RegisterRestaurantPage.fetchAndStoreRestaurantInfo
  line_start: 163
  line_end: 167
  evidence_type: implemented
- type: PRECEDES
  target: step.business.ftgo.restaurant-onboarding.get-all-menu-item
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
  source: business-flow.ftgo.ui.restaurant-onboarding
  position: 2
  layer: business
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: ui/src/components/RegisterRestaurantPage.vue
  symbol: RegisterRestaurantPage.fetchAndStoreRestaurantInfo
  line_start: 163
  line_end: 167
  evidence_type: implemented
- type: PRECEDES
  source: step.business.ftgo.restaurant-onboarding.register
  evidence_mechanism:
  - await_sequence
  - helper_call
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: ui/src/components/RegisterRestaurantPage.vue
  symbol: RegisterRestaurantPage.fetchAndStoreRestaurantInfo
  line_start: 163
  line_end: 167
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

# Restaurant onboarding: GET /restaurant/get_supplier_restaurant_info

Canonical business step referencing an approved Pass-5 UserFlow, extracted from reachability evidence in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Layer: `business`
- Role: `user_flow_reference`
- Business flow: `business-flow.ftgo.ui.restaurant-onboarding` (position 2)
- References user flow: `flow.ftgo.gateway.get.restaurant.get-supplier-restaurant-info`
- Trigger: `automatic`
- Evidence mechanism: `await_sequence`, `helper_call`
- Declared in: `ui/src/components/RegisterRestaurantPage.vue` (lines 163-167)
- Evidence class: `implemented`

## Review notes

This approved canonical page records a source-backed business journey. It carries no endpoint, event or persistence detail of its own: that evidence already lives on the referenced UserFlow page and is not duplicated here.

