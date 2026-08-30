---
id: step.business.ftgo.driver-vehicle-onboarding.get
kind: FlowStep
type: FlowStep
title: 'Driver vehicle onboarding: GET /status/get'
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
business_flow: business-flow.ftgo.ui.driver-vehicle-onboarding
position: 3
user_flow: flow.ftgo.gateway.get.status.get
http_method: GET
path: /status/get
trigger: automatic
evidence_mechanism:
- route_navigation
- lifecycle_hook
- helper_call
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: ui/src/components/DeliveryMainPage.vue
  symbol: DeliveryMainPage.fetchDriverOnlineStatus
  line_start: 132
  line_end: 136
  evidence_type: implemented
relations:
- type: DERIVED_FROM
  target: flow.ftgo.gateway.get.status.get
  evidence_mechanism:
  - route_navigation
  - lifecycle_hook
  - helper_call
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: ui/src/components/DeliveryMainPage.vue
  symbol: DeliveryMainPage.fetchDriverOnlineStatus
  line_start: 132
  line_end: 136
  evidence_type: implemented
inbound_relations:
- type: CONTAINS
  source: business-flow.ftgo.ui.driver-vehicle-onboarding
  position: 3
  layer: business
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: ui/src/components/DeliveryMainPage.vue
  symbol: DeliveryMainPage.fetchDriverOnlineStatus
  line_start: 132
  line_end: 136
  evidence_type: implemented
- type: PRECEDES
  source: step.business.ftgo.driver-vehicle-onboarding.get-info
  evidence_mechanism:
  - route_navigation
  - lifecycle_hook
  - helper_call
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: ui/src/components/DeliveryMainPage.vue
  symbol: DeliveryMainPage.fetchDriverOnlineStatus
  line_start: 132
  line_end: 136
  evidence_type: implemented
attributes:
  layer: business
  role: user_flow_reference
  position: 3
  trigger: automatic
  http_method: GET
  path: /status/get
  evidence_mechanism:
  - route_navigation
  - lifecycle_hook
  - helper_call
  actor: driver
---

# Driver vehicle onboarding: GET /status/get

Canonical business step referencing an approved Pass-5 UserFlow, extracted from reachability evidence in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Layer: `business`
- Role: `user_flow_reference`
- Business flow: `business-flow.ftgo.ui.driver-vehicle-onboarding` (position 3)
- References user flow: `flow.ftgo.gateway.get.status.get`
- Trigger: `automatic`
- Evidence mechanism: `route_navigation`, `lifecycle_hook`, `helper_call`
- Declared in: `ui/src/components/DeliveryMainPage.vue` (lines 132-136)
- Evidence class: `implemented`

## Review notes

This approved canonical page records a source-backed business journey. It carries no endpoint, event or persistence detail of its own: that evidence already lives on the referenced UserFlow page and is not duplicated here.

