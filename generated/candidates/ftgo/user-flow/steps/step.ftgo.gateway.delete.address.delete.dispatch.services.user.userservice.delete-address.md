---
id: step.ftgo.gateway.delete.address.delete.dispatch.services.user.userservice.delete-address
kind: FlowStep
type: FlowStep
title: services.user.UserService.delete_address dispatch
status: candidate
review_status: pending
candidate_of: user-flow-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: user-flow
owner: aide-ftgo-cohort
role: service_dispatch
flow: flow.ftgo.gateway.delete.address.delete
service: service.ftgo.gateway
derived_from: endpoint.ftgo.gateway.delete.address.delete
derived_from_kind: Endpoint
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/customer/address.py
  symbol: application.routes.customer.address.delete_address
  line_start: 72
  line_end: 72
  evidence_type: implemented
traces:
- target: services.user.UserService.delete_address
  depth: 1
  hops:
  - caller: application.routes.customer.address.delete_address
    callee: services.user.UserService.delete_address
    call: UserService.delete_address
    repository: ftgo
    commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
    path: backend/gateway/src/application/routes/customer/address.py
    symbol: application.routes.customer.address.delete_address
    line_start: 72
    line_end: 72
    evidence_type: implemented
relations:
- type: DERIVED_FROM
  target: endpoint.ftgo.gateway.delete.address.delete
  anchor_kind: Endpoint
  role: service_dispatch
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/customer/address.py
  symbol: application.routes.customer.address.delete_address
  line_start: 72
  line_end: 72
  evidence_type: implemented
- type: IMPLEMENTS
  target: service.ftgo.gateway
  role: service_dispatch
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/customer/address.py
  symbol: application.routes.customer.address.delete_address
  line_start: 72
  line_end: 72
  evidence_type: implemented
- type: PRECEDES
  target: step.ftgo.gateway.delete.address.delete.publish.ftgo.rabbitmq.user.address.delete
  established_by: publisher call site
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/user.py
  symbol: services.user.UserService.delete_address
  line_start: 55
  line_end: 55
  evidence_type: implemented
inbound_relations:
- type: CONTAINS
  source: flow.ftgo.gateway.delete.address.delete
  role: service_dispatch
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/customer/address.py
  symbol: application.routes.customer.address.delete_address
  line_start: 72
  line_end: 72
  evidence_type: implemented
- type: PRECEDES
  source: step.ftgo.gateway.delete.address.delete.http-ingress
  established_by: handler call site
  call_depth: 1
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/customer/address.py
  symbol: application.routes.customer.address.delete_address
  line_start: 72
  line_end: 72
  evidence_type: implemented
attributes:
  gateway_symbol: services.user.UserService.delete_address
  call_depth: 1
---

# services.user.UserService.delete_address dispatch

Candidate execution step extracted from call evidence in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Role: `service_dispatch`
- Flow: `flow.ftgo.gateway.delete.address.delete`
- Performed by: `service.ftgo.gateway`
- Anchored on: `endpoint.ftgo.gateway.delete.address.delete` (`Endpoint`)
- Declared in: `backend/gateway/src/application/routes/customer/address.py` (lines 72-72)
- Evidence class: `implemented`

## Call trace

- `application.routes.customer.address.delete_address` -> `services.user.UserService.delete_address` (`backend/gateway/src/application/routes/customer/address.py:72`)

## Review notes

This page is a candidate awaiting review. The step exists because a concrete call site proves it, and its ordering edges carry that call site as evidence.

