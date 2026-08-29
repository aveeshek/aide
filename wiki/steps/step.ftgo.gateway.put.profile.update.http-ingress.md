---
id: step.ftgo.gateway.put.profile.update.http-ingress
kind: FlowStep
type: FlowStep
title: PUT /profile/update ingress
status: approved
review_status: approved
candidate_of: user-flow-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: user-flow
owner: aide-ftgo-cohort
role: http_ingress
flow: flow.ftgo.gateway.put.profile.update
service: service.ftgo.gateway
derived_from: endpoint.ftgo.gateway.put.profile.update
derived_from_kind: Endpoint
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/account/profile.py
  symbol: application.routes.account.profile.update_profile
  line_start: 85
  line_end: 106
  evidence_type: implemented
relations:
- type: DERIVED_FROM
  target: endpoint.ftgo.gateway.put.profile.update
  anchor_kind: Endpoint
  role: http_ingress
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/account/profile.py
  symbol: application.routes.account.profile.update_profile
  line_start: 85
  line_end: 106
  evidence_type: implemented
- type: IMPLEMENTS
  target: service.ftgo.gateway
  role: http_ingress
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/account/profile.py
  symbol: application.routes.account.profile.update_profile
  line_start: 85
  line_end: 106
  evidence_type: implemented
- type: PRECEDES
  target: step.ftgo.gateway.put.profile.update.dispatch.services.user.userservice.update-profile
  established_by: handler call site
  call_depth: 1
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/account/profile.py
  symbol: application.routes.account.profile.update_profile
  line_start: 91
  line_end: 91
  evidence_type: implemented
inbound_relations:
- type: CONTAINS
  source: flow.ftgo.gateway.put.profile.update
  role: http_ingress
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/account/profile.py
  symbol: application.routes.account.profile.update_profile
  line_start: 85
  line_end: 106
  evidence_type: implemented
attributes:
  http_method: PUT
  path: /profile/update
  path_resolution: partial
  handler: application.routes.account.profile.update_profile
---

# PUT /profile/update ingress

Canonical execution step extracted from call evidence in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Role: `http_ingress`
- Flow: `flow.ftgo.gateway.put.profile.update`
- Performed by: `service.ftgo.gateway`
- Anchored on: `endpoint.ftgo.gateway.put.profile.update` (`Endpoint`)
- Declared in: `backend/gateway/src/application/routes/account/profile.py` (lines 85-106)
- Evidence class: `implemented`

## Review notes

This approved canonical page records a source-backed execution step. The step exists because a concrete call site proves it, and its ordering edges carry that call site as evidence.

