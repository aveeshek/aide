---
id: step.ftgo.gateway.get.location.get.dispatch.services.location.locationservice.get-last-location
kind: FlowStep
type: FlowStep
title: services.location.LocationService.get_last_location dispatch
status: candidate
review_status: pending
candidate_of: user-flow-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: user-flow
owner: aide-ftgo-cohort
role: service_dispatch
flow: flow.ftgo.gateway.get.location.get
service: service.ftgo.gateway
derived_from: endpoint.ftgo.gateway.get.location.get
derived_from_kind: Endpoint
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/driver/location.py
  symbol: application.routes.driver.location.get_location
  line_start: 45
  line_end: 45
  evidence_type: implemented
traces:
- target: services.location.LocationService.get_last_location
  depth: 1
  hops:
  - caller: application.routes.driver.location.get_location
    callee: services.location.LocationService.get_last_location
    call: LocationService.get_last_location
    repository: ftgo
    commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
    path: backend/gateway/src/application/routes/driver/location.py
    symbol: application.routes.driver.location.get_location
    line_start: 45
    line_end: 45
    evidence_type: implemented
relations:
- type: DERIVED_FROM
  target: endpoint.ftgo.gateway.get.location.get
  anchor_kind: Endpoint
  role: service_dispatch
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/driver/location.py
  symbol: application.routes.driver.location.get_location
  line_start: 45
  line_end: 45
  evidence_type: implemented
- type: IMPLEMENTS
  target: service.ftgo.gateway
  role: service_dispatch
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/driver/location.py
  symbol: application.routes.driver.location.get_location
  line_start: 45
  line_end: 45
  evidence_type: implemented
- type: PRECEDES
  target: step.ftgo.gateway.get.location.get.publish.ftgo.rabbitmq.driver.location.get
  established_by: publisher call site
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/location.py
  symbol: services.location.LocationService.get_last_location
  line_start: 27
  line_end: 27
  evidence_type: implemented
inbound_relations:
- type: CONTAINS
  source: flow.ftgo.gateway.get.location.get
  role: service_dispatch
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/driver/location.py
  symbol: application.routes.driver.location.get_location
  line_start: 45
  line_end: 45
  evidence_type: implemented
- type: PRECEDES
  source: step.ftgo.gateway.get.location.get.http-ingress
  established_by: handler call site
  call_depth: 1
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/driver/location.py
  symbol: application.routes.driver.location.get_location
  line_start: 45
  line_end: 45
  evidence_type: implemented
attributes:
  gateway_symbol: services.location.LocationService.get_last_location
  call_depth: 1
---

# services.location.LocationService.get_last_location dispatch

Candidate execution step extracted from call evidence in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Role: `service_dispatch`
- Flow: `flow.ftgo.gateway.get.location.get`
- Performed by: `service.ftgo.gateway`
- Anchored on: `endpoint.ftgo.gateway.get.location.get` (`Endpoint`)
- Declared in: `backend/gateway/src/application/routes/driver/location.py` (lines 45-45)
- Evidence class: `implemented`

## Call trace

- `application.routes.driver.location.get_location` -> `services.location.LocationService.get_last_location` (`backend/gateway/src/application/routes/driver/location.py:45`)

## Review notes

This page is a candidate awaiting review. The step exists because a concrete call site proves it, and its ordering edges carry that call site as evidence.

