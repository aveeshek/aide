---
id: step.ftgo.gateway.post.auth.login.dispatch.services.user.userservice.login
kind: FlowStep
type: FlowStep
title: services.user.UserService.login dispatch
status: approved
review_status: approved
candidate_of: user-flow-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: user-flow
owner: aide-ftgo-cohort
role: service_dispatch
flow: flow.ftgo.gateway.post.auth.login
service: service.ftgo.gateway
derived_from: endpoint.ftgo.gateway.post.auth.login
derived_from_kind: Endpoint
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/auth/registration.py
  symbol: application.routes.auth.registration.login
  line_start: 82
  line_end: 82
  evidence_type: implemented
traces:
- target: services.user.UserService.login
  depth: 1
  hops:
  - caller: application.routes.auth.registration.login
    callee: services.user.UserService.login
    call: UserService.login
    repository: ftgo
    commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
    path: backend/gateway/src/application/routes/auth/registration.py
    symbol: application.routes.auth.registration.login
    line_start: 82
    line_end: 82
    evidence_type: implemented
relations:
- type: DERIVED_FROM
  target: endpoint.ftgo.gateway.post.auth.login
  anchor_kind: Endpoint
  role: service_dispatch
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/auth/registration.py
  symbol: application.routes.auth.registration.login
  line_start: 82
  line_end: 82
  evidence_type: implemented
- type: IMPLEMENTS
  target: service.ftgo.gateway
  role: service_dispatch
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/auth/registration.py
  symbol: application.routes.auth.registration.login
  line_start: 82
  line_end: 82
  evidence_type: implemented
- type: PRECEDES
  target: step.ftgo.gateway.post.auth.login.publish.ftgo.rabbitmq.user.profile.login
  established_by: publisher call site
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/user.py
  symbol: services.user.UserService.login
  line_start: 31
  line_end: 31
  evidence_type: implemented
inbound_relations:
- type: CONTAINS
  source: flow.ftgo.gateway.post.auth.login
  role: service_dispatch
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/auth/registration.py
  symbol: application.routes.auth.registration.login
  line_start: 82
  line_end: 82
  evidence_type: implemented
- type: PRECEDES
  source: step.ftgo.gateway.post.auth.login.http-ingress
  established_by: handler call site
  call_depth: 1
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/auth/registration.py
  symbol: application.routes.auth.registration.login
  line_start: 82
  line_end: 82
  evidence_type: implemented
attributes:
  gateway_symbol: services.user.UserService.login
  call_depth: 1
---

# services.user.UserService.login dispatch

Canonical execution step extracted from call evidence in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Role: `service_dispatch`
- Flow: `flow.ftgo.gateway.post.auth.login`
- Performed by: `service.ftgo.gateway`
- Anchored on: `endpoint.ftgo.gateway.post.auth.login` (`Endpoint`)
- Declared in: `backend/gateway/src/application/routes/auth/registration.py` (lines 82-82)
- Evidence class: `implemented`

## Call trace

- `application.routes.auth.registration.login` -> `services.user.UserService.login` (`backend/gateway/src/application/routes/auth/registration.py:82`)

## Review notes

This approved canonical page records a source-backed execution step. The step exists because a concrete call site proves it, and its ordering edges carry that call site as evidence.

