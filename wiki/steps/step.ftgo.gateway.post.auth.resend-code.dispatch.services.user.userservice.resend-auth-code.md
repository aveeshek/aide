---
id: step.ftgo.gateway.post.auth.resend-code.dispatch.services.user.userservice.resend-auth-code
kind: FlowStep
type: FlowStep
title: services.user.UserService.resend_auth_code dispatch
status: approved
review_status: approved
candidate_of: user-flow-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: user-flow
owner: aide-ftgo-cohort
role: service_dispatch
flow: flow.ftgo.gateway.post.auth.resend-code
service: service.ftgo.gateway
derived_from: endpoint.ftgo.gateway.post.auth.resend-code
derived_from_kind: Endpoint
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/auth/registration.py
  symbol: application.routes.auth.registration.resend_auth_code
  line_start: 64
  line_end: 64
  evidence_type: implemented
traces:
- target: services.user.UserService.resend_auth_code
  depth: 1
  hops:
  - caller: application.routes.auth.registration.resend_auth_code
    callee: services.user.UserService.resend_auth_code
    call: UserService.resend_auth_code
    repository: ftgo
    commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
    path: backend/gateway/src/application/routes/auth/registration.py
    symbol: application.routes.auth.registration.resend_auth_code
    line_start: 64
    line_end: 64
    evidence_type: implemented
relations:
- type: DERIVED_FROM
  target: endpoint.ftgo.gateway.post.auth.resend-code
  anchor_kind: Endpoint
  role: service_dispatch
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/auth/registration.py
  symbol: application.routes.auth.registration.resend_auth_code
  line_start: 64
  line_end: 64
  evidence_type: implemented
- type: IMPLEMENTS
  target: service.ftgo.gateway
  role: service_dispatch
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/auth/registration.py
  symbol: application.routes.auth.registration.resend_auth_code
  line_start: 64
  line_end: 64
  evidence_type: implemented
- type: PRECEDES
  target: step.ftgo.gateway.post.auth.resend-code.publish.ftgo.rabbitmq.user.profile.resend-auth-code
  established_by: publisher call site
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/user.py
  symbol: services.user.UserService.resend_auth_code
  line_start: 23
  line_end: 23
  evidence_type: implemented
inbound_relations:
- type: CONTAINS
  source: flow.ftgo.gateway.post.auth.resend-code
  role: service_dispatch
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/auth/registration.py
  symbol: application.routes.auth.registration.resend_auth_code
  line_start: 64
  line_end: 64
  evidence_type: implemented
- type: PRECEDES
  source: step.ftgo.gateway.post.auth.resend-code.http-ingress
  established_by: handler call site
  call_depth: 1
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/auth/registration.py
  symbol: application.routes.auth.registration.resend_auth_code
  line_start: 64
  line_end: 64
  evidence_type: implemented
attributes:
  gateway_symbol: services.user.UserService.resend_auth_code
  call_depth: 1
---

# services.user.UserService.resend_auth_code dispatch

Canonical execution step extracted from call evidence in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Role: `service_dispatch`
- Flow: `flow.ftgo.gateway.post.auth.resend-code`
- Performed by: `service.ftgo.gateway`
- Anchored on: `endpoint.ftgo.gateway.post.auth.resend-code` (`Endpoint`)
- Declared in: `backend/gateway/src/application/routes/auth/registration.py` (lines 64-64)
- Evidence class: `implemented`

## Call trace

- `application.routes.auth.registration.resend_auth_code` -> `services.user.UserService.resend_auth_code` (`backend/gateway/src/application/routes/auth/registration.py:64`)

## Review notes

This approved canonical page records a source-backed execution step. The step exists because a concrete call site proves it, and its ordering edges carry that call site as evidence.

