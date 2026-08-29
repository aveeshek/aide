---
id: step.ftgo.gateway.delete.profile.delete.dispatch.services.user.userservice.delete-account
kind: FlowStep
type: FlowStep
title: services.user.UserService.delete_account dispatch
status: candidate
review_status: pending
candidate_of: user-flow-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: user-flow
owner: aide-ftgo-cohort
role: service_dispatch
flow: flow.ftgo.gateway.delete.profile.delete
service: service.ftgo.gateway
derived_from: endpoint.ftgo.gateway.delete.profile.delete
derived_from_kind: Endpoint
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/account/profile.py
  symbol: application.routes.account.profile.delete_account
  line_start: 69
  line_end: 69
  evidence_type: implemented
traces:
- target: services.user.UserService.delete_account
  depth: 1
  hops:
  - caller: application.routes.account.profile.delete_account
    callee: services.user.UserService.delete_account
    call: UserService.delete_account
    repository: ftgo
    commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
    path: backend/gateway/src/application/routes/account/profile.py
    symbol: application.routes.account.profile.delete_account
    line_start: 69
    line_end: 69
    evidence_type: implemented
relations:
- type: DERIVED_FROM
  target: endpoint.ftgo.gateway.delete.profile.delete
  anchor_kind: Endpoint
  role: service_dispatch
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/account/profile.py
  symbol: application.routes.account.profile.delete_account
  line_start: 69
  line_end: 69
  evidence_type: implemented
- type: IMPLEMENTS
  target: service.ftgo.gateway
  role: service_dispatch
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/account/profile.py
  symbol: application.routes.account.profile.delete_account
  line_start: 69
  line_end: 69
  evidence_type: implemented
- type: PRECEDES
  target: step.ftgo.gateway.delete.profile.delete.publish.ftgo.rabbitmq.user.profile.delete-account
  established_by: publisher call site
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/user.py
  symbol: services.user.UserService.delete_account
  line_start: 39
  line_end: 39
  evidence_type: implemented
inbound_relations:
- type: CONTAINS
  source: flow.ftgo.gateway.delete.profile.delete
  role: service_dispatch
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/account/profile.py
  symbol: application.routes.account.profile.delete_account
  line_start: 69
  line_end: 69
  evidence_type: implemented
- type: PRECEDES
  source: step.ftgo.gateway.delete.profile.delete.http-ingress
  established_by: handler call site
  call_depth: 1
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/account/profile.py
  symbol: application.routes.account.profile.delete_account
  line_start: 69
  line_end: 69
  evidence_type: implemented
attributes:
  gateway_symbol: services.user.UserService.delete_account
  call_depth: 1
---

# services.user.UserService.delete_account dispatch

Candidate execution step extracted from call evidence in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Role: `service_dispatch`
- Flow: `flow.ftgo.gateway.delete.profile.delete`
- Performed by: `service.ftgo.gateway`
- Anchored on: `endpoint.ftgo.gateway.delete.profile.delete` (`Endpoint`)
- Declared in: `backend/gateway/src/application/routes/account/profile.py` (lines 69-69)
- Evidence class: `implemented`

## Call trace

- `application.routes.account.profile.delete_account` -> `services.user.UserService.delete_account` (`backend/gateway/src/application/routes/account/profile.py:69`)

## Review notes

This page is a candidate awaiting review. The step exists because a concrete call site proves it, and its ordering edges carry that call site as evidence.

