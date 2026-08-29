---
id: step.ftgo.gateway.delete.vehicle.delete.http-ingress
kind: FlowStep
type: FlowStep
title: DELETE /vehicle/delete ingress
status: candidate
review_status: pending
candidate_of: user-flow-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: user-flow
owner: aide-ftgo-cohort
role: http_ingress
flow: flow.ftgo.gateway.delete.vehicle.delete
service: service.ftgo.gateway
derived_from: endpoint.ftgo.gateway.delete.vehicle.delete
derived_from_kind: Endpoint
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/driver/vehicle.py
  symbol: application.routes.driver.vehicle.delete
  line_start: 63
  line_end: 83
  evidence_type: implemented
relations:
- type: DERIVED_FROM
  target: endpoint.ftgo.gateway.delete.vehicle.delete
  anchor_kind: Endpoint
  role: http_ingress
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/driver/vehicle.py
  symbol: application.routes.driver.vehicle.delete
  line_start: 63
  line_end: 83
  evidence_type: implemented
- type: IMPLEMENTS
  target: service.ftgo.gateway
  role: http_ingress
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/driver/vehicle.py
  symbol: application.routes.driver.vehicle.delete
  line_start: 63
  line_end: 83
  evidence_type: implemented
- type: PRECEDES
  target: step.ftgo.gateway.delete.vehicle.delete.dispatch.services.vehicle.vehicleservice.delete
  established_by: handler call site
  call_depth: 1
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/driver/vehicle.py
  symbol: application.routes.driver.vehicle.delete
  line_start: 68
  line_end: 68
  evidence_type: implemented
inbound_relations:
- type: CONTAINS
  source: flow.ftgo.gateway.delete.vehicle.delete
  role: http_ingress
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/driver/vehicle.py
  symbol: application.routes.driver.vehicle.delete
  line_start: 63
  line_end: 83
  evidence_type: implemented
attributes:
  http_method: DELETE
  path: /vehicle/delete
  path_resolution: partial
  handler: application.routes.driver.vehicle.delete
---

# DELETE /vehicle/delete ingress

Candidate execution step extracted from call evidence in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Role: `http_ingress`
- Flow: `flow.ftgo.gateway.delete.vehicle.delete`
- Performed by: `service.ftgo.gateway`
- Anchored on: `endpoint.ftgo.gateway.delete.vehicle.delete` (`Endpoint`)
- Declared in: `backend/gateway/src/application/routes/driver/vehicle.py` (lines 63-83)
- Evidence class: `implemented`

## Review notes

This page is a candidate awaiting review. The step exists because a concrete call site proves it, and its ordering edges carry that call site as evidence.

