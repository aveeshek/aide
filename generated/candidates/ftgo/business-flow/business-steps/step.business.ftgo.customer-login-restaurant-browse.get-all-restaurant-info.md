---
id: step.business.ftgo.customer-login-restaurant-browse.get-all-restaurant-info
kind: FlowStep
type: FlowStep
title: 'Customer login and restaurant browsing: GET /restaurant/get_all_restaurant_info'
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
business_flow: business-flow.ftgo.ui.customer-login-restaurant-browse
position: 2
user_flow: flow.ftgo.gateway.get.restaurant.get-all-restaurant-info
http_method: GET
path: /restaurant/get_all_restaurant_info
trigger: automatic
evidence_mechanism:
- route_navigation
- lifecycle_hook
- helper_call
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: ui/src/components/CustomerMainPage.vue
  symbol: CustomerMainPage.fetchRestaurants
  line_start: 86
  line_end: 91
  evidence_type: implemented
relations:
- type: DERIVED_FROM
  target: flow.ftgo.gateway.get.restaurant.get-all-restaurant-info
  evidence_mechanism:
  - route_navigation
  - lifecycle_hook
  - helper_call
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: ui/src/components/CustomerMainPage.vue
  symbol: CustomerMainPage.fetchRestaurants
  line_start: 86
  line_end: 91
  evidence_type: implemented
inbound_relations:
- type: CONTAINS
  source: business-flow.ftgo.ui.customer-login-restaurant-browse
  position: 2
  layer: business
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: ui/src/components/CustomerMainPage.vue
  symbol: CustomerMainPage.fetchRestaurants
  line_start: 86
  line_end: 91
  evidence_type: implemented
- type: PRECEDES
  source: step.business.ftgo.customer-login-restaurant-browse.login
  evidence_mechanism:
  - route_navigation
  - lifecycle_hook
  - helper_call
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: ui/src/components/CustomerMainPage.vue
  symbol: CustomerMainPage.fetchRestaurants
  line_start: 86
  line_end: 91
  evidence_type: implemented
attributes:
  layer: business
  role: user_flow_reference
  position: 2
  trigger: automatic
  http_method: GET
  path: /restaurant/get_all_restaurant_info
  evidence_mechanism:
  - route_navigation
  - lifecycle_hook
  - helper_call
  actor: customer
---

# Customer login and restaurant browsing: GET /restaurant/get_all_restaurant_info

Candidate business step referencing an approved Pass-5 UserFlow, extracted from reachability evidence in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Layer: `business`
- Role: `user_flow_reference`
- Business flow: `business-flow.ftgo.ui.customer-login-restaurant-browse` (position 2)
- References user flow: `flow.ftgo.gateway.get.restaurant.get-all-restaurant-info`
- Trigger: `automatic`
- Evidence mechanism: `route_navigation`, `lifecycle_hook`, `helper_call`
- Declared in: `ui/src/components/CustomerMainPage.vue` (lines 86-91)
- Evidence class: `implemented`

## Review notes

This page is a candidate awaiting review. It carries no endpoint, event or persistence detail of its own: that evidence already lives on the referenced UserFlow page and is not duplicated here.

