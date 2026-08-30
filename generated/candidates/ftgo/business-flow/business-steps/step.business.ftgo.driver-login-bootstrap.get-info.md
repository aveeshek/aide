---
id: step.business.ftgo.driver-login-bootstrap.get-info
kind: FlowStep
type: FlowStep
title: 'Driver login bootstrap: GET /vehicle/get_info'
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
business_flow: business-flow.ftgo.ui.driver-login-bootstrap
position: 2
user_flow: flow.ftgo.gateway.get.vehicle.get-info
http_method: GET
path: /vehicle/get_info
trigger: automatic
evidence_mechanism:
- await_sequence
- helper_call
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: ui/src/components/SignInComp.vue
  symbol: SignInComp.fetchAndStoreVehicleInfo
  line_start: 157
  line_end: 161
  evidence_type: implemented
relations:
- type: DERIVED_FROM
  target: flow.ftgo.gateway.get.vehicle.get-info
  evidence_mechanism:
  - await_sequence
  - helper_call
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: ui/src/components/SignInComp.vue
  symbol: SignInComp.fetchAndStoreVehicleInfo
  line_start: 157
  line_end: 161
  evidence_type: implemented
- type: PRECEDES
  target: step.business.ftgo.driver-login-bootstrap.get
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
  source: business-flow.ftgo.ui.driver-login-bootstrap
  position: 2
  layer: business
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: ui/src/components/SignInComp.vue
  symbol: SignInComp.fetchAndStoreVehicleInfo
  line_start: 157
  line_end: 161
  evidence_type: implemented
- type: PRECEDES
  source: step.business.ftgo.driver-login-bootstrap.login
  evidence_mechanism:
  - await_sequence
  - helper_call
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: ui/src/components/SignInComp.vue
  symbol: SignInComp.fetchAndStoreVehicleInfo
  line_start: 157
  line_end: 161
  evidence_type: implemented
attributes:
  layer: business
  role: user_flow_reference
  position: 2
  trigger: automatic
  http_method: GET
  path: /vehicle/get_info
  evidence_mechanism:
  - await_sequence
  - helper_call
  actor: driver
---

# Driver login bootstrap: GET /vehicle/get_info

Candidate business step referencing an approved Pass-5 UserFlow, extracted from reachability evidence in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Layer: `business`
- Role: `user_flow_reference`
- Business flow: `business-flow.ftgo.ui.driver-login-bootstrap` (position 2)
- References user flow: `flow.ftgo.gateway.get.vehicle.get-info`
- Trigger: `automatic`
- Evidence mechanism: `await_sequence`, `helper_call`
- Declared in: `ui/src/components/SignInComp.vue` (lines 157-161)
- Evidence class: `implemented`

## Review notes

This page is a candidate awaiting review. It carries no endpoint, event or persistence detail of its own: that evidence already lives on the referenced UserFlow page and is not duplicated here.

