---
id: step.business.ftgo.restaurant-onboarding.register
kind: FlowStep
type: FlowStep
title: 'Restaurant onboarding: POST /restaurant/register'
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
position: 1
user_flow: flow.ftgo.gateway.post.restaurant.register
http_method: POST
path: /restaurant/register
trigger: user_action
evidence_mechanism:
- template_binding
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: ui/src/components/RegisterRestaurantPage.vue
  symbol: RegisterRestaurantPage.registerRestaurant
  line_start: 135
  line_end: 139
  evidence_type: implemented
relations:
- type: DERIVED_FROM
  target: flow.ftgo.gateway.post.restaurant.register
  evidence_mechanism:
  - template_binding
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: ui/src/components/RegisterRestaurantPage.vue
  symbol: RegisterRestaurantPage.registerRestaurant
  line_start: 135
  line_end: 139
  evidence_type: implemented
- type: PRECEDES
  target: step.business.ftgo.restaurant-onboarding.get-supplier-restaurant-info
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
inbound_relations:
- type: CONTAINS
  source: business-flow.ftgo.ui.restaurant-onboarding
  position: 1
  layer: business
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: ui/src/components/RegisterRestaurantPage.vue
  symbol: RegisterRestaurantPage.registerRestaurant
  line_start: 135
  line_end: 139
  evidence_type: implemented
attributes:
  layer: business
  role: user_flow_reference
  position: 1
  trigger: user_action
  http_method: POST
  path: /restaurant/register
  evidence_mechanism:
  - template_binding
  actor: restaurant_admin
---

# Restaurant onboarding: POST /restaurant/register

Canonical business step referencing an approved Pass-5 UserFlow, extracted from reachability evidence in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Layer: `business`
- Role: `user_flow_reference`
- Business flow: `business-flow.ftgo.ui.restaurant-onboarding` (position 1)
- References user flow: `flow.ftgo.gateway.post.restaurant.register`
- Trigger: `user_action`
- Evidence mechanism: `template_binding`
- Declared in: `ui/src/components/RegisterRestaurantPage.vue` (lines 135-139)
- Evidence class: `implemented`

## Review notes

This approved canonical page records a source-backed business journey. It carries no endpoint, event or persistence detail of its own: that evidence already lives on the referenced UserFlow page and is not duplicated here.

