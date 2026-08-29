---
id: step.ftgo.gateway.post.address.add.dispatch.services.user.userservice.add-address
kind: FlowStep
type: FlowStep
title: services.user.UserService.add_address dispatch
status: approved
review_status: approved
candidate_of: user-flow-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: user-flow
owner: aide-ftgo-cohort
role: service_dispatch
flow: flow.ftgo.gateway.post.address.add
service: service.ftgo.gateway
derived_from: endpoint.ftgo.gateway.post.address.add
derived_from_kind: Endpoint
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/customer/address.py
  symbol: application.routes.customer.address.add_address
  line_start: 48
  line_end: 48
  evidence_type: implemented
traces:
- target: services.user.UserService.add_address
  depth: 1
  hops:
  - caller: application.routes.customer.address.add_address
    callee: services.user.UserService.add_address
    call: UserService.add_address
    repository: ftgo
    commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
    path: backend/gateway/src/application/routes/customer/address.py
    symbol: application.routes.customer.address.add_address
    line_start: 48
    line_end: 48
    evidence_type: implemented
relations:
- type: DERIVED_FROM
  target: endpoint.ftgo.gateway.post.address.add
  anchor_kind: Endpoint
  role: service_dispatch
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/customer/address.py
  symbol: application.routes.customer.address.add_address
  line_start: 48
  line_end: 48
  evidence_type: implemented
- type: IMPLEMENTS
  target: service.ftgo.gateway
  role: service_dispatch
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/customer/address.py
  symbol: application.routes.customer.address.add_address
  line_start: 48
  line_end: 48
  evidence_type: implemented
- type: PRECEDES
  target: step.ftgo.gateway.post.address.add.publish.ftgo.rabbitmq.user.address.add-address
  established_by: publisher call site
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/user.py
  symbol: services.user.UserService.add_address
  line_start: 15
  line_end: 15
  evidence_type: implemented
inbound_relations:
- type: CONTAINS
  source: flow.ftgo.gateway.post.address.add
  role: service_dispatch
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/customer/address.py
  symbol: application.routes.customer.address.add_address
  line_start: 48
  line_end: 48
  evidence_type: implemented
- type: PRECEDES
  source: step.ftgo.gateway.post.address.add.http-ingress
  established_by: handler call site
  call_depth: 1
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/customer/address.py
  symbol: application.routes.customer.address.add_address
  line_start: 48
  line_end: 48
  evidence_type: implemented
attributes:
  gateway_symbol: services.user.UserService.add_address
  call_depth: 1
---

# services.user.UserService.add_address dispatch

Canonical execution step extracted from call evidence in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Role: `service_dispatch`
- Flow: `flow.ftgo.gateway.post.address.add`
- Performed by: `service.ftgo.gateway`
- Anchored on: `endpoint.ftgo.gateway.post.address.add` (`Endpoint`)
- Declared in: `backend/gateway/src/application/routes/customer/address.py` (lines 48-48)
- Evidence class: `implemented`

## Call trace

- `application.routes.customer.address.add_address` -> `services.user.UserService.add_address` (`backend/gateway/src/application/routes/customer/address.py:48`)

## Review notes

This approved canonical page records a source-backed execution step. The step exists because a concrete call site proves it, and its ordering edges carry that call site as evidence.

