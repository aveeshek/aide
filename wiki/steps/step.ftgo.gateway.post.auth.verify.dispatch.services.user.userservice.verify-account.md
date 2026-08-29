---
id: step.ftgo.gateway.post.auth.verify.dispatch.services.user.userservice.verify-account
kind: FlowStep
type: FlowStep
title: services.user.UserService.verify_account dispatch
status: approved
review_status: approved
candidate_of: user-flow-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: user-flow
owner: aide-ftgo-cohort
role: service_dispatch
flow: flow.ftgo.gateway.post.auth.verify
service: service.ftgo.gateway
derived_from: endpoint.ftgo.gateway.post.auth.verify
derived_from_kind: Endpoint
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/auth/registration.py
  symbol: application.routes.auth.registration.verify_account
  line_start: 46
  line_end: 46
  evidence_type: implemented
traces:
- target: services.user.UserService.verify_account
  depth: 1
  hops:
  - caller: application.routes.auth.registration.verify_account
    callee: services.user.UserService.verify_account
    call: UserService.verify_account
    repository: ftgo
    commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
    path: backend/gateway/src/application/routes/auth/registration.py
    symbol: application.routes.auth.registration.verify_account
    line_start: 46
    line_end: 46
    evidence_type: implemented
relations:
- type: DERIVED_FROM
  target: endpoint.ftgo.gateway.post.auth.verify
  anchor_kind: Endpoint
  role: service_dispatch
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/auth/registration.py
  symbol: application.routes.auth.registration.verify_account
  line_start: 46
  line_end: 46
  evidence_type: implemented
- type: IMPLEMENTS
  target: service.ftgo.gateway
  role: service_dispatch
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/auth/registration.py
  symbol: application.routes.auth.registration.verify_account
  line_start: 46
  line_end: 46
  evidence_type: implemented
- type: PRECEDES
  target: step.ftgo.gateway.post.auth.verify.publish.ftgo.rabbitmq.user.profile.verify-account
  established_by: publisher call site
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/user.py
  symbol: services.user.UserService.verify_account
  line_start: 27
  line_end: 27
  evidence_type: implemented
inbound_relations:
- type: CONTAINS
  source: flow.ftgo.gateway.post.auth.verify
  role: service_dispatch
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/auth/registration.py
  symbol: application.routes.auth.registration.verify_account
  line_start: 46
  line_end: 46
  evidence_type: implemented
- type: PRECEDES
  source: step.ftgo.gateway.post.auth.verify.http-ingress
  established_by: handler call site
  call_depth: 1
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/auth/registration.py
  symbol: application.routes.auth.registration.verify_account
  line_start: 46
  line_end: 46
  evidence_type: implemented
attributes:
  gateway_symbol: services.user.UserService.verify_account
  call_depth: 1
---

# services.user.UserService.verify_account dispatch

Canonical execution step extracted from call evidence in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Role: `service_dispatch`
- Flow: `flow.ftgo.gateway.post.auth.verify`
- Performed by: `service.ftgo.gateway`
- Anchored on: `endpoint.ftgo.gateway.post.auth.verify` (`Endpoint`)
- Declared in: `backend/gateway/src/application/routes/auth/registration.py` (lines 46-46)
- Evidence class: `implemented`

## Call trace

- `application.routes.auth.registration.verify_account` -> `services.user.UserService.verify_account` (`backend/gateway/src/application/routes/auth/registration.py:46`)

## Review notes

This approved canonical page records a source-backed execution step. The step exists because a concrete call site proves it, and its ordering edges carry that call site as evidence.

