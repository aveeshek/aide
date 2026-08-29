---
id: step.ftgo.gateway.post.location.submit.dispatch.services.location.locationservice.submit-location
kind: FlowStep
type: FlowStep
title: services.location.LocationService.submit_location dispatch
status: candidate
review_status: pending
candidate_of: user-flow-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: user-flow
owner: aide-ftgo-cohort
role: service_dispatch
flow: flow.ftgo.gateway.post.location.submit
service: service.ftgo.gateway
derived_from: endpoint.ftgo.gateway.post.location.submit
derived_from_kind: Endpoint
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/driver/location.py
  symbol: application.routes.driver.location.submit_location
  line_start: 23
  line_end: 23
  evidence_type: implemented
traces:
- target: services.location.LocationService.submit_location
  depth: 1
  hops:
  - caller: application.routes.driver.location.submit_location
    callee: services.location.LocationService.submit_location
    call: LocationService.submit_location
    repository: ftgo
    commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
    path: backend/gateway/src/application/routes/driver/location.py
    symbol: application.routes.driver.location.submit_location
    line_start: 23
    line_end: 23
    evidence_type: implemented
relations:
- type: DERIVED_FROM
  target: endpoint.ftgo.gateway.post.location.submit
  anchor_kind: Endpoint
  role: service_dispatch
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/driver/location.py
  symbol: application.routes.driver.location.submit_location
  line_start: 23
  line_end: 23
  evidence_type: implemented
- type: IMPLEMENTS
  target: service.ftgo.gateway
  role: service_dispatch
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/driver/location.py
  symbol: application.routes.driver.location.submit_location
  line_start: 23
  line_end: 23
  evidence_type: implemented
- type: PRECEDES
  target: step.ftgo.gateway.post.location.submit.publish.ftgo.rabbitmq.driver.location.submit
  established_by: publisher call site
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/location.py
  symbol: services.location.LocationService.submit_location
  line_start: 11
  line_end: 11
  evidence_type: implemented
inbound_relations:
- type: CONTAINS
  source: flow.ftgo.gateway.post.location.submit
  role: service_dispatch
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/driver/location.py
  symbol: application.routes.driver.location.submit_location
  line_start: 23
  line_end: 23
  evidence_type: implemented
- type: PRECEDES
  source: step.ftgo.gateway.post.location.submit.http-ingress
  established_by: handler call site
  call_depth: 1
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/driver/location.py
  symbol: application.routes.driver.location.submit_location
  line_start: 23
  line_end: 23
  evidence_type: implemented
attributes:
  gateway_symbol: services.location.LocationService.submit_location
  call_depth: 1
---

# services.location.LocationService.submit_location dispatch

Candidate execution step extracted from call evidence in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Role: `service_dispatch`
- Flow: `flow.ftgo.gateway.post.location.submit`
- Performed by: `service.ftgo.gateway`
- Anchored on: `endpoint.ftgo.gateway.post.location.submit` (`Endpoint`)
- Declared in: `backend/gateway/src/application/routes/driver/location.py` (lines 23-23)
- Evidence class: `implemented`

## Call trace

- `application.routes.driver.location.submit_location` -> `services.location.LocationService.submit_location` (`backend/gateway/src/application/routes/driver/location.py:23`)

## Review notes

This page is a candidate awaiting review. The step exists because a concrete call site proves it, and its ordering edges carry that call site as evidence.

