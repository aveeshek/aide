---
id: step.ftgo.gateway.post.auth.resend-code.http-ingress
kind: FlowStep
type: FlowStep
title: POST /auth/resend_code ingress
status: approved
review_status: approved
candidate_of: user-flow-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: user-flow
owner: aide-ftgo-cohort
role: http_ingress
flow: flow.ftgo.gateway.post.auth.resend-code
service: service.ftgo.gateway
derived_from: endpoint.ftgo.gateway.post.auth.resend-code
derived_from_kind: Endpoint
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/auth/registration.py
  symbol: application.routes.auth.registration.resend_auth_code
  line_start: 60
  line_end: 76
  evidence_type: implemented
relations:
- type: DERIVED_FROM
  target: endpoint.ftgo.gateway.post.auth.resend-code
  anchor_kind: Endpoint
  role: http_ingress
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/auth/registration.py
  symbol: application.routes.auth.registration.resend_auth_code
  line_start: 60
  line_end: 76
  evidence_type: implemented
- type: IMPLEMENTS
  target: service.ftgo.gateway
  role: http_ingress
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/auth/registration.py
  symbol: application.routes.auth.registration.resend_auth_code
  line_start: 60
  line_end: 76
  evidence_type: implemented
- type: PRECEDES
  target: step.ftgo.gateway.post.auth.resend-code.dispatch.services.user.userservice.resend-auth-code
  established_by: handler call site
  call_depth: 1
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/auth/registration.py
  symbol: application.routes.auth.registration.resend_auth_code
  line_start: 64
  line_end: 64
  evidence_type: implemented
inbound_relations:
- type: CONTAINS
  source: flow.ftgo.gateway.post.auth.resend-code
  role: http_ingress
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/auth/registration.py
  symbol: application.routes.auth.registration.resend_auth_code
  line_start: 60
  line_end: 76
  evidence_type: implemented
attributes:
  http_method: POST
  path: /auth/resend_code
  path_resolution: partial
  handler: application.routes.auth.registration.resend_auth_code
---

# POST /auth/resend_code ingress

Canonical execution step extracted from call evidence in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Role: `http_ingress`
- Flow: `flow.ftgo.gateway.post.auth.resend-code`
- Performed by: `service.ftgo.gateway`
- Anchored on: `endpoint.ftgo.gateway.post.auth.resend-code` (`Endpoint`)
- Declared in: `backend/gateway/src/application/routes/auth/registration.py` (lines 60-76)
- Evidence class: `implemented`

## Review notes

This approved canonical page records a source-backed execution step. The step exists because a concrete call site proves it, and its ordering edges carry that call site as evidence.

