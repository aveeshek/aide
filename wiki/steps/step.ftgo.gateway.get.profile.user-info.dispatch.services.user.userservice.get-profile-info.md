---
id: step.ftgo.gateway.get.profile.user-info.dispatch.services.user.userservice.get-profile-info
kind: FlowStep
type: FlowStep
title: services.user.UserService.get_profile_info dispatch
status: approved
review_status: approved
candidate_of: user-flow-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: user-flow
owner: aide-ftgo-cohort
role: service_dispatch
flow: flow.ftgo.gateway.get.profile.user-info
service: service.ftgo.gateway
derived_from: endpoint.ftgo.gateway.get.profile.user-info
derived_from_kind: Endpoint
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/account/profile.py
  symbol: application.routes.account.profile.get_info
  line_start: 44
  line_end: 44
  evidence_type: implemented
traces:
- target: services.user.UserService.get_profile_info
  depth: 1
  hops:
  - caller: application.routes.account.profile.get_info
    callee: services.user.UserService.get_profile_info
    call: UserService.get_profile_info
    repository: ftgo
    commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
    path: backend/gateway/src/application/routes/account/profile.py
    symbol: application.routes.account.profile.get_info
    line_start: 44
    line_end: 44
    evidence_type: implemented
relations:
- type: DERIVED_FROM
  target: endpoint.ftgo.gateway.get.profile.user-info
  anchor_kind: Endpoint
  role: service_dispatch
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/account/profile.py
  symbol: application.routes.account.profile.get_info
  line_start: 44
  line_end: 44
  evidence_type: implemented
- type: IMPLEMENTS
  target: service.ftgo.gateway
  role: service_dispatch
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/account/profile.py
  symbol: application.routes.account.profile.get_info
  line_start: 44
  line_end: 44
  evidence_type: implemented
- type: PRECEDES
  target: step.ftgo.gateway.get.profile.user-info.publish.ftgo.rabbitmq.user.profile.get-info
  established_by: publisher call site
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/user.py
  symbol: services.user.UserService.get_profile_info
  line_start: 35
  line_end: 35
  evidence_type: implemented
inbound_relations:
- type: CONTAINS
  source: flow.ftgo.gateway.get.profile.user-info
  role: service_dispatch
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/account/profile.py
  symbol: application.routes.account.profile.get_info
  line_start: 44
  line_end: 44
  evidence_type: implemented
- type: PRECEDES
  source: step.ftgo.gateway.get.profile.user-info.http-ingress
  established_by: handler call site
  call_depth: 1
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/account/profile.py
  symbol: application.routes.account.profile.get_info
  line_start: 44
  line_end: 44
  evidence_type: implemented
attributes:
  gateway_symbol: services.user.UserService.get_profile_info
  call_depth: 1
---

# services.user.UserService.get_profile_info dispatch

Canonical execution step extracted from call evidence in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Role: `service_dispatch`
- Flow: `flow.ftgo.gateway.get.profile.user-info`
- Performed by: `service.ftgo.gateway`
- Anchored on: `endpoint.ftgo.gateway.get.profile.user-info` (`Endpoint`)
- Declared in: `backend/gateway/src/application/routes/account/profile.py` (lines 44-44)
- Evidence class: `implemented`

## Call trace

- `application.routes.account.profile.get_info` -> `services.user.UserService.get_profile_info` (`backend/gateway/src/application/routes/account/profile.py:44`)

## Review notes

This approved canonical page records a source-backed execution step. The step exists because a concrete call site proves it, and its ordering edges carry that call site as evidence.

