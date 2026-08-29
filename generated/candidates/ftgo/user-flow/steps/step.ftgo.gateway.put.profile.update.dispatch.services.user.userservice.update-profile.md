---
id: step.ftgo.gateway.put.profile.update.dispatch.services.user.userservice.update-profile
kind: FlowStep
type: FlowStep
title: services.user.UserService.update_profile dispatch
status: candidate
review_status: pending
candidate_of: user-flow-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: user-flow
owner: aide-ftgo-cohort
role: service_dispatch
flow: flow.ftgo.gateway.put.profile.update
service: service.ftgo.gateway
derived_from: endpoint.ftgo.gateway.put.profile.update
derived_from_kind: Endpoint
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/account/profile.py
  symbol: application.routes.account.profile.update_profile
  line_start: 91
  line_end: 91
  evidence_type: implemented
traces:
- target: services.user.UserService.update_profile
  depth: 1
  hops:
  - caller: application.routes.account.profile.update_profile
    callee: services.user.UserService.update_profile
    call: UserService.update_profile
    repository: ftgo
    commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
    path: backend/gateway/src/application/routes/account/profile.py
    symbol: application.routes.account.profile.update_profile
    line_start: 91
    line_end: 91
    evidence_type: implemented
relations:
- type: DERIVED_FROM
  target: endpoint.ftgo.gateway.put.profile.update
  anchor_kind: Endpoint
  role: service_dispatch
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/account/profile.py
  symbol: application.routes.account.profile.update_profile
  line_start: 91
  line_end: 91
  evidence_type: implemented
- type: IMPLEMENTS
  target: service.ftgo.gateway
  role: service_dispatch
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/account/profile.py
  symbol: application.routes.account.profile.update_profile
  line_start: 91
  line_end: 91
  evidence_type: implemented
- type: PRECEDES
  target: step.ftgo.gateway.put.profile.update.publish.ftgo.rabbitmq.user.profile.update-profile
  established_by: publisher call site
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/user.py
  symbol: services.user.UserService.update_profile
  line_start: 47
  line_end: 47
  evidence_type: implemented
inbound_relations:
- type: CONTAINS
  source: flow.ftgo.gateway.put.profile.update
  role: service_dispatch
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/account/profile.py
  symbol: application.routes.account.profile.update_profile
  line_start: 91
  line_end: 91
  evidence_type: implemented
- type: PRECEDES
  source: step.ftgo.gateway.put.profile.update.http-ingress
  established_by: handler call site
  call_depth: 1
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/account/profile.py
  symbol: application.routes.account.profile.update_profile
  line_start: 91
  line_end: 91
  evidence_type: implemented
attributes:
  gateway_symbol: services.user.UserService.update_profile
  call_depth: 1
---

# services.user.UserService.update_profile dispatch

Candidate execution step extracted from call evidence in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Role: `service_dispatch`
- Flow: `flow.ftgo.gateway.put.profile.update`
- Performed by: `service.ftgo.gateway`
- Anchored on: `endpoint.ftgo.gateway.put.profile.update` (`Endpoint`)
- Declared in: `backend/gateway/src/application/routes/account/profile.py` (lines 91-91)
- Evidence class: `implemented`

## Call trace

- `application.routes.account.profile.update_profile` -> `services.user.UserService.update_profile` (`backend/gateway/src/application/routes/account/profile.py:91`)

## Review notes

This page is a candidate awaiting review. The step exists because a concrete call site proves it, and its ordering edges carry that call site as evidence.

