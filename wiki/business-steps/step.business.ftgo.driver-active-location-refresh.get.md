---
id: step.business.ftgo.driver-active-location-refresh.get
kind: FlowStep
type: FlowStep
title: 'Driver active location refresh: GET /status/get'
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
position: 1
user_flow: flow.ftgo.gateway.get.status.get
http_method: GET
path: /status/get
trigger: automatic
evidence_mechanism:
- interval_loop
- helper_call
loop_interval_ms: 5000
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
  - interval_loop
  - helper_call
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: ui/src/components/DeliveryMainPage.vue
  symbol: DeliveryMainPage.fetchDriverOnlineStatus
  line_start: 132
  line_end: 136
  evidence_type: implemented
- type: PRECEDES
  target: step.business.ftgo.driver-active-location-refresh.submit
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
inbound_relations:
- type: CONTAINS
  source: business-flow.ftgo.ui.driver-active-location-refresh
  position: 1
  layer: business
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
  position: 1
  trigger: automatic
  http_method: GET
  path: /status/get
  evidence_mechanism:
  - interval_loop
  - helper_call
  actor: driver
  loop_interval_ms: 5000
---

# Driver active location refresh: GET /status/get

Canonical business step referencing an approved Pass-5 UserFlow, extracted from reachability evidence in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Layer: `business`
- Role: `user_flow_reference`
- Business flow: `business-flow.ftgo.ui.driver-active-location-refresh` (position 1)
- References user flow: `flow.ftgo.gateway.get.status.get`
- Trigger: `automatic`
- Evidence mechanism: `interval_loop`, `helper_call`
- Declared in: `ui/src/components/DeliveryMainPage.vue` (lines 132-136)
- Evidence class: `implemented`

## Repetition

This step runs on a timer every 5000 ms, so its position in the journey is a repeating stage rather than a one-off transition.

## Review notes

This approved canonical page records a source-backed business journey. It carries no endpoint, event or persistence detail of its own: that evidence already lives on the referenced UserFlow page and is not duplicated here.

