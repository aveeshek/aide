---
id: step.ftgo.gateway.post.auth.register.dispatch.services.user.userservice.create-profile
kind: FlowStep
type: FlowStep
title: services.user.UserService.create_profile dispatch
status: approved
review_status: approved
candidate_of: user-flow-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: user-flow
owner: aide-ftgo-cohort
role: service_dispatch
flow: flow.ftgo.gateway.post.auth.register
service: service.ftgo.gateway
derived_from: endpoint.ftgo.gateway.post.auth.register
derived_from_kind: Endpoint
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/auth/registration.py
  symbol: application.routes.auth.registration.register
  line_start: 25
  line_end: 25
  evidence_type: implemented
traces:
- target: services.user.UserService.create_profile
  depth: 1
  hops:
  - caller: application.routes.auth.registration.register
    callee: services.user.UserService.create_profile
    call: UserService.create_profile
    repository: ftgo
    commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
    path: backend/gateway/src/application/routes/auth/registration.py
    symbol: application.routes.auth.registration.register
    line_start: 25
    line_end: 25
    evidence_type: implemented
relations:
- type: DERIVED_FROM
  target: endpoint.ftgo.gateway.post.auth.register
  anchor_kind: Endpoint
  role: service_dispatch
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/auth/registration.py
  symbol: application.routes.auth.registration.register
  line_start: 25
  line_end: 25
  evidence_type: implemented
- type: IMPLEMENTS
  target: service.ftgo.gateway
  role: service_dispatch
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/auth/registration.py
  symbol: application.routes.auth.registration.register
  line_start: 25
  line_end: 25
  evidence_type: implemented
- type: PRECEDES
  target: step.ftgo.gateway.post.auth.register.publish.ftgo.rabbitmq.user.profile.create
  established_by: publisher call site
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/user.py
  symbol: services.user.UserService.create_profile
  line_start: 11
  line_end: 11
  evidence_type: implemented
inbound_relations:
- type: CONTAINS
  source: flow.ftgo.gateway.post.auth.register
  role: service_dispatch
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/auth/registration.py
  symbol: application.routes.auth.registration.register
  line_start: 25
  line_end: 25
  evidence_type: implemented
- type: PRECEDES
  source: step.ftgo.gateway.post.auth.register.http-ingress
  established_by: handler call site
  call_depth: 1
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/auth/registration.py
  symbol: application.routes.auth.registration.register
  line_start: 25
  line_end: 25
  evidence_type: implemented
attributes:
  gateway_symbol: services.user.UserService.create_profile
  call_depth: 1
---

# services.user.UserService.create_profile dispatch

Canonical execution step extracted from call evidence in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Role: `service_dispatch`
- Flow: `flow.ftgo.gateway.post.auth.register`
- Performed by: `service.ftgo.gateway`
- Anchored on: `endpoint.ftgo.gateway.post.auth.register` (`Endpoint`)
- Declared in: `backend/gateway/src/application/routes/auth/registration.py` (lines 25-25)
- Evidence class: `implemented`

## Call trace

- `application.routes.auth.registration.register` -> `services.user.UserService.create_profile` (`backend/gateway/src/application/routes/auth/registration.py:25`)

## Review notes

This approved canonical page records a source-backed execution step. The step exists because a concrete call site proves it, and its ordering edges carry that call site as evidence.

