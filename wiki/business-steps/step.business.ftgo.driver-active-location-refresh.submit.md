---
id: step.business.ftgo.driver-active-location-refresh.submit
kind: FlowStep
type: FlowStep
title: 'Driver active location refresh: POST /location/submit'
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
business_flow: business-flow.ftgo.ui.driver-active-location-refresh
position: 2
user_flow: flow.ftgo.gateway.post.location.submit
http_method: POST
path: /location/submit
trigger: conditional
evidence_mechanism:
- await_sequence
- helper_call
- conditional_branch
- interval_loop
condition:
- this.isActive
loop_interval_ms: 5000
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: ui/src/components/DeliveryMainPage.vue
  symbol: DeliveryMainPage.submitLocation
  line_start: 177
  line_end: 181
  evidence_type: implemented
relations:
- type: DERIVED_FROM
  target: flow.ftgo.gateway.post.location.submit
  evidence_mechanism:
  - await_sequence
  - helper_call
  - conditional_branch
  - interval_loop
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: ui/src/components/DeliveryMainPage.vue
  symbol: DeliveryMainPage.submitLocation
  line_start: 177
  line_end: 181
  evidence_type: implemented
inbound_relations:
- type: CONTAINS
  source: business-flow.ftgo.ui.driver-active-location-refresh
  position: 2
  layer: business
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: ui/src/components/DeliveryMainPage.vue
  symbol: DeliveryMainPage.submitLocation
  line_start: 177
  line_end: 181
  evidence_type: implemented
- type: PRECEDES
  source: step.business.ftgo.driver-active-location-refresh.get
  evidence_mechanism:
  - await_sequence
  - helper_call
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: ui/src/components/DeliveryMainPage.vue
  symbol: DeliveryMainPage.submitLocation
  line_start: 177
  line_end: 181
  evidence_type: implemented
attributes:
  layer: business
  role: user_flow_reference
  position: 2
  trigger: conditional
  http_method: POST
  path: /location/submit
  evidence_mechanism:
  - await_sequence
  - helper_call
  - conditional_branch
  - interval_loop
  actor: driver
  condition:
  - this.isActive
  condition_evidence:
  - condition: this.isActive
    kind: if
  loop_interval_ms: 5000
---

# Driver active location refresh: POST /location/submit

Canonical business step referencing an approved Pass-5 UserFlow, extracted from reachability evidence in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Layer: `business`
- Role: `user_flow_reference`
- Business flow: `business-flow.ftgo.ui.driver-active-location-refresh` (position 2)
- References user flow: `flow.ftgo.gateway.post.location.submit`
- Trigger: `conditional`
- Evidence mechanism: `await_sequence`, `helper_call`, `conditional_branch`, `interval_loop`
- Declared in: `ui/src/components/DeliveryMainPage.vue` (lines 177-181)
- Evidence class: `implemented`

## Guards

- `this.isActive` (`if`)

## Repetition

This step runs on a timer every 5000 ms, so its position in the journey is a repeating stage rather than a one-off transition.

## Review notes

This approved canonical page records a source-backed business journey. It carries no endpoint, event or persistence detail of its own: that evidence already lives on the referenced UserFlow page and is not duplicated here.

