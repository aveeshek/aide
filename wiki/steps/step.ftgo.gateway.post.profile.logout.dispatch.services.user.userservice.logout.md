---
id: step.ftgo.gateway.post.profile.logout.dispatch.services.user.userservice.logout
kind: FlowStep
type: FlowStep
title: services.user.UserService.logout dispatch
status: approved
review_status: approved
candidate_of: user-flow-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: user-flow
owner: aide-ftgo-cohort
role: service_dispatch
flow: flow.ftgo.gateway.post.profile.logout
service: service.ftgo.gateway
derived_from: endpoint.ftgo.gateway.post.profile.logout
derived_from_kind: Endpoint
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/account/profile.py
  symbol: application.routes.account.profile.logout
  line_start: 25
  line_end: 25
  evidence_type: implemented
traces:
- target: services.user.UserService.logout
  depth: 1
  hops:
  - caller: application.routes.account.profile.logout
    callee: services.user.UserService.logout
    call: UserService.logout
    repository: ftgo
    commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
    path: backend/gateway/src/application/routes/account/profile.py
    symbol: application.routes.account.profile.logout
    line_start: 25
    line_end: 25
    evidence_type: implemented
relations:
- type: DERIVED_FROM
  target: endpoint.ftgo.gateway.post.profile.logout
  anchor_kind: Endpoint
  role: service_dispatch
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/account/profile.py
  symbol: application.routes.account.profile.logout
  line_start: 25
  line_end: 25
  evidence_type: implemented
- type: IMPLEMENTS
  target: service.ftgo.gateway
  role: service_dispatch
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/account/profile.py
  symbol: application.routes.account.profile.logout
  line_start: 25
  line_end: 25
  evidence_type: implemented
- type: PRECEDES
  target: step.ftgo.gateway.post.profile.logout.publish.ftgo.rabbitmq.user.profile.logout
  established_by: publisher call site
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/user.py
  symbol: services.user.UserService.logout
  line_start: 43
  line_end: 43
  evidence_type: implemented
inbound_relations:
- type: CONTAINS
  source: flow.ftgo.gateway.post.profile.logout
  role: service_dispatch
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/account/profile.py
  symbol: application.routes.account.profile.logout
  line_start: 25
  line_end: 25
  evidence_type: implemented
- type: PRECEDES
  source: step.ftgo.gateway.post.profile.logout.http-ingress
  established_by: handler call site
  call_depth: 1
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/account/profile.py
  symbol: application.routes.account.profile.logout
  line_start: 25
  line_end: 25
  evidence_type: implemented
attributes:
  gateway_symbol: services.user.UserService.logout
  call_depth: 1
---

# services.user.UserService.logout dispatch

Canonical execution step extracted from call evidence in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Role: `service_dispatch`
- Flow: `flow.ftgo.gateway.post.profile.logout`
- Performed by: `service.ftgo.gateway`
- Anchored on: `endpoint.ftgo.gateway.post.profile.logout` (`Endpoint`)
- Declared in: `backend/gateway/src/application/routes/account/profile.py` (lines 25-25)
- Evidence class: `implemented`

## Call trace

- `application.routes.account.profile.logout` -> `services.user.UserService.logout` (`backend/gateway/src/application/routes/account/profile.py:25`)

## Review notes

This approved canonical page records a source-backed execution step. The step exists because a concrete call site proves it, and its ordering edges carry that call site as evidence.

