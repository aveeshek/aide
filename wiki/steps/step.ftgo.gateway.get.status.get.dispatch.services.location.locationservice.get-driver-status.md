---
id: step.ftgo.gateway.get.status.get.dispatch.services.location.locationservice.get-driver-status
kind: FlowStep
type: FlowStep
title: services.location.LocationService.get_driver_status dispatch
status: approved
review_status: approved
candidate_of: user-flow-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: user-flow
owner: aide-ftgo-cohort
role: service_dispatch
flow: flow.ftgo.gateway.get.status.get
service: service.ftgo.gateway
derived_from: endpoint.ftgo.gateway.get.status.get
derived_from_kind: Endpoint
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/driver/online_status.py
  symbol: application.routes.driver.online_status.get_status
  line_start: 54
  line_end: 54
  evidence_type: implemented
traces:
- target: services.location.LocationService.get_driver_status
  depth: 1
  hops:
  - caller: application.routes.driver.online_status.get_status
    callee: services.location.LocationService.get_driver_status
    call: LocationService.get_driver_status
    repository: ftgo
    commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
    path: backend/gateway/src/application/routes/driver/online_status.py
    symbol: application.routes.driver.online_status.get_status
    line_start: 54
    line_end: 54
    evidence_type: implemented
relations:
- type: DERIVED_FROM
  target: endpoint.ftgo.gateway.get.status.get
  anchor_kind: Endpoint
  role: service_dispatch
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/driver/online_status.py
  symbol: application.routes.driver.online_status.get_status
  line_start: 54
  line_end: 54
  evidence_type: implemented
- type: IMPLEMENTS
  target: service.ftgo.gateway
  role: service_dispatch
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/driver/online_status.py
  symbol: application.routes.driver.online_status.get_status
  line_start: 54
  line_end: 54
  evidence_type: implemented
- type: PRECEDES
  target: step.ftgo.gateway.get.status.get.publish.ftgo.rabbitmq.driver.status.get
  established_by: publisher call site
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/location.py
  symbol: services.location.LocationService.get_driver_status
  line_start: 31
  line_end: 31
  evidence_type: implemented
inbound_relations:
- type: CONTAINS
  source: flow.ftgo.gateway.get.status.get
  role: service_dispatch
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/driver/online_status.py
  symbol: application.routes.driver.online_status.get_status
  line_start: 54
  line_end: 54
  evidence_type: implemented
- type: PRECEDES
  source: step.ftgo.gateway.get.status.get.http-ingress
  established_by: handler call site
  call_depth: 1
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/driver/online_status.py
  symbol: application.routes.driver.online_status.get_status
  line_start: 54
  line_end: 54
  evidence_type: implemented
attributes:
  gateway_symbol: services.location.LocationService.get_driver_status
  call_depth: 1
---

# services.location.LocationService.get_driver_status dispatch

Canonical execution step extracted from call evidence in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Role: `service_dispatch`
- Flow: `flow.ftgo.gateway.get.status.get`
- Performed by: `service.ftgo.gateway`
- Anchored on: `endpoint.ftgo.gateway.get.status.get` (`Endpoint`)
- Declared in: `backend/gateway/src/application/routes/driver/online_status.py` (lines 54-54)
- Evidence class: `implemented`

## Call trace

- `application.routes.driver.online_status.get_status` -> `services.location.LocationService.get_driver_status` (`backend/gateway/src/application/routes/driver/online_status.py:54`)

## Review notes

This approved canonical page records a source-backed execution step. The step exists because a concrete call site proves it, and its ordering edges carry that call site as evidence.

