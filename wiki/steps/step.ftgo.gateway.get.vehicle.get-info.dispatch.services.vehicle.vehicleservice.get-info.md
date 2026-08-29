---
id: step.ftgo.gateway.get.vehicle.get-info.dispatch.services.vehicle.vehicleservice.get-info
kind: FlowStep
type: FlowStep
title: services.vehicle.VehicleService.get_info dispatch
status: approved
review_status: approved
candidate_of: user-flow-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: user-flow
owner: aide-ftgo-cohort
role: service_dispatch
flow: flow.ftgo.gateway.get.vehicle.get-info
service: service.ftgo.gateway
derived_from: endpoint.ftgo.gateway.get.vehicle.get-info
derived_from_kind: Endpoint
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/driver/vehicle.py
  symbol: application.routes.driver.vehicle.get_info
  line_start: 47
  line_end: 47
  evidence_type: implemented
traces:
- target: services.vehicle.VehicleService.get_info
  depth: 1
  hops:
  - caller: application.routes.driver.vehicle.get_info
    callee: services.vehicle.VehicleService.get_info
    call: VehicleService.get_info
    repository: ftgo
    commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
    path: backend/gateway/src/application/routes/driver/vehicle.py
    symbol: application.routes.driver.vehicle.get_info
    line_start: 47
    line_end: 47
    evidence_type: implemented
relations:
- type: DERIVED_FROM
  target: endpoint.ftgo.gateway.get.vehicle.get-info
  anchor_kind: Endpoint
  role: service_dispatch
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/driver/vehicle.py
  symbol: application.routes.driver.vehicle.get_info
  line_start: 47
  line_end: 47
  evidence_type: implemented
- type: IMPLEMENTS
  target: service.ftgo.gateway
  role: service_dispatch
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/driver/vehicle.py
  symbol: application.routes.driver.vehicle.get_info
  line_start: 47
  line_end: 47
  evidence_type: implemented
- type: PRECEDES
  target: step.ftgo.gateway.get.vehicle.get-info.publish.ftgo.rabbitmq.driver.vehicle.get-info
  established_by: publisher call site
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/vehicle.py
  symbol: services.vehicle.VehicleService.get_info
  line_start: 15
  line_end: 15
  evidence_type: implemented
inbound_relations:
- type: CONTAINS
  source: flow.ftgo.gateway.get.vehicle.get-info
  role: service_dispatch
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/driver/vehicle.py
  symbol: application.routes.driver.vehicle.get_info
  line_start: 47
  line_end: 47
  evidence_type: implemented
- type: PRECEDES
  source: step.ftgo.gateway.get.vehicle.get-info.http-ingress
  established_by: handler call site
  call_depth: 1
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/driver/vehicle.py
  symbol: application.routes.driver.vehicle.get_info
  line_start: 47
  line_end: 47
  evidence_type: implemented
attributes:
  gateway_symbol: services.vehicle.VehicleService.get_info
  call_depth: 1
---

# services.vehicle.VehicleService.get_info dispatch

Canonical execution step extracted from call evidence in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Role: `service_dispatch`
- Flow: `flow.ftgo.gateway.get.vehicle.get-info`
- Performed by: `service.ftgo.gateway`
- Anchored on: `endpoint.ftgo.gateway.get.vehicle.get-info` (`Endpoint`)
- Declared in: `backend/gateway/src/application/routes/driver/vehicle.py` (lines 47-47)
- Evidence class: `implemented`

## Call trace

- `application.routes.driver.vehicle.get_info` -> `services.vehicle.VehicleService.get_info` (`backend/gateway/src/application/routes/driver/vehicle.py:47`)

## Review notes

This approved canonical page records a source-backed execution step. The step exists because a concrete call site proves it, and its ordering edges carry that call site as evidence.

