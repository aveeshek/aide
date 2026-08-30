---
id: step.business.ftgo.driver-vehicle-onboarding.register
kind: FlowStep
type: FlowStep
title: 'Driver vehicle onboarding: POST /vehicle/register'
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
business_flow: business-flow.ftgo.ui.driver-vehicle-onboarding
position: 1
user_flow: flow.ftgo.gateway.post.vehicle.register
http_method: POST
path: /vehicle/register
trigger: user_action
evidence_mechanism:
- template_binding
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: ui/src/components/RegisterVehiclePage.vue
  symbol: RegisterVehiclePage.registerVehicle
  line_start: 84
  line_end: 88
  evidence_type: implemented
relations:
- type: DERIVED_FROM
  target: flow.ftgo.gateway.post.vehicle.register
  evidence_mechanism:
  - template_binding
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: ui/src/components/RegisterVehiclePage.vue
  symbol: RegisterVehiclePage.registerVehicle
  line_start: 84
  line_end: 88
  evidence_type: implemented
- type: PRECEDES
  target: step.business.ftgo.driver-vehicle-onboarding.get-info
  evidence_mechanism:
  - await_sequence
  - helper_call
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: ui/src/components/RegisterVehiclePage.vue
  symbol: RegisterVehiclePage.fetchAndStoreVehicleInfo
  line_start: 111
  line_end: 115
  evidence_type: implemented
inbound_relations:
- type: CONTAINS
  source: business-flow.ftgo.ui.driver-vehicle-onboarding
  position: 1
  layer: business
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: ui/src/components/RegisterVehiclePage.vue
  symbol: RegisterVehiclePage.registerVehicle
  line_start: 84
  line_end: 88
  evidence_type: implemented
attributes:
  layer: business
  role: user_flow_reference
  position: 1
  trigger: user_action
  http_method: POST
  path: /vehicle/register
  evidence_mechanism:
  - template_binding
  actor: driver
---

# Driver vehicle onboarding: POST /vehicle/register

Candidate business step referencing an approved Pass-5 UserFlow, extracted from reachability evidence in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Layer: `business`
- Role: `user_flow_reference`
- Business flow: `business-flow.ftgo.ui.driver-vehicle-onboarding` (position 1)
- References user flow: `flow.ftgo.gateway.post.vehicle.register`
- Trigger: `user_action`
- Evidence mechanism: `template_binding`
- Declared in: `ui/src/components/RegisterVehiclePage.vue` (lines 84-88)
- Evidence class: `implemented`

## Review notes

This page is a candidate awaiting review. It carries no endpoint, event or persistence detail of its own: that evidence already lives on the referenced UserFlow page and is not duplicated here.

