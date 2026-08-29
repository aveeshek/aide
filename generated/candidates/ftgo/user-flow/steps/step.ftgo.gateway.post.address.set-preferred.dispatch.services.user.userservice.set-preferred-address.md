---
id: step.ftgo.gateway.post.address.set-preferred.dispatch.services.user.userservice.set-preferred-address
kind: FlowStep
type: FlowStep
title: services.user.UserService.set_preferred_address dispatch
status: candidate
review_status: pending
candidate_of: user-flow-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: user-flow
owner: aide-ftgo-cohort
role: service_dispatch
flow: flow.ftgo.gateway.post.address.set-preferred
service: service.ftgo.gateway
derived_from: endpoint.ftgo.gateway.post.address.set-preferred
derived_from_kind: Endpoint
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/customer/address.py
  symbol: application.routes.customer.address.set_address_preferency
  line_start: 94
  line_end: 94
  evidence_type: implemented
traces:
- target: services.user.UserService.set_preferred_address
  depth: 1
  hops:
  - caller: application.routes.customer.address.set_address_preferency
    callee: services.user.UserService.set_preferred_address
    call: UserService.set_preferred_address
    repository: ftgo
    commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
    path: backend/gateway/src/application/routes/customer/address.py
    symbol: application.routes.customer.address.set_address_preferency
    line_start: 94
    line_end: 94
    evidence_type: implemented
relations:
- type: DERIVED_FROM
  target: endpoint.ftgo.gateway.post.address.set-preferred
  anchor_kind: Endpoint
  role: service_dispatch
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/customer/address.py
  symbol: application.routes.customer.address.set_address_preferency
  line_start: 94
  line_end: 94
  evidence_type: implemented
- type: IMPLEMENTS
  target: service.ftgo.gateway
  role: service_dispatch
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/customer/address.py
  symbol: application.routes.customer.address.set_address_preferency
  line_start: 94
  line_end: 94
  evidence_type: implemented
- type: PRECEDES
  target: step.ftgo.gateway.post.address.set-preferred.publish.ftgo.rabbitmq.user.address.set-preferred-address
  established_by: publisher call site
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/user.py
  symbol: services.user.UserService.set_preferred_address
  line_start: 59
  line_end: 59
  evidence_type: implemented
inbound_relations:
- type: CONTAINS
  source: flow.ftgo.gateway.post.address.set-preferred
  role: service_dispatch
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/customer/address.py
  symbol: application.routes.customer.address.set_address_preferency
  line_start: 94
  line_end: 94
  evidence_type: implemented
- type: PRECEDES
  source: step.ftgo.gateway.post.address.set-preferred.http-ingress
  established_by: handler call site
  call_depth: 1
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/customer/address.py
  symbol: application.routes.customer.address.set_address_preferency
  line_start: 94
  line_end: 94
  evidence_type: implemented
attributes:
  gateway_symbol: services.user.UserService.set_preferred_address
  call_depth: 1
---

# services.user.UserService.set_preferred_address dispatch

Candidate execution step extracted from call evidence in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Role: `service_dispatch`
- Flow: `flow.ftgo.gateway.post.address.set-preferred`
- Performed by: `service.ftgo.gateway`
- Anchored on: `endpoint.ftgo.gateway.post.address.set-preferred` (`Endpoint`)
- Declared in: `backend/gateway/src/application/routes/customer/address.py` (lines 94-94)
- Evidence class: `implemented`

## Call trace

- `application.routes.customer.address.set_address_preferency` -> `services.user.UserService.set_preferred_address` (`backend/gateway/src/application/routes/customer/address.py:94`)

## Review notes

This page is a candidate awaiting review. The step exists because a concrete call site proves it, and its ordering edges carry that call site as evidence.

