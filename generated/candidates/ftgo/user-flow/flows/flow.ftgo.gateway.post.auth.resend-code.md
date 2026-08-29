---
id: flow.ftgo.gateway.post.auth.resend-code
kind: UserFlow
type: UserFlow
title: POST /auth/resend_code execution flow
status: candidate
review_status: pending
candidate_of: user-flow-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: user-flow
owner: aide-ftgo-cohort
entry_endpoint: endpoint.ftgo.gateway.post.auth.resend-code
http_method: POST
path: /auth/resend_code
path_resolution: partial
completeness: partial
handler: application.routes.auth.registration.resend_auth_code
participating_services:
- service.ftgo.gateway
- service.ftgo.user
events:
- event.ftgo.rabbitmq.user.profile.resend-auth-code
persistence_targets: []
unresolved_segments:
- persistence:user.profile.resend_auth_code
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/auth/registration.py
  symbol: application.routes.auth.registration.resend_auth_code
  line_start: 60
  line_end: 76
  evidence_type: implemented
relations:
- type: CONTAINS
  target: step.ftgo.gateway.post.auth.resend-code.consume.user.user.profile.resend-auth-code
  role: event_consume
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/user/src/events.py
  symbol: events.register_events
  line_start: 39
  line_end: 39
  evidence_type: implemented
- type: CONTAINS
  target: step.ftgo.gateway.post.auth.resend-code.dispatch.services.user.userservice.resend-auth-code
  role: service_dispatch
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/auth/registration.py
  symbol: application.routes.auth.registration.resend_auth_code
  line_start: 64
  line_end: 64
  evidence_type: implemented
- type: CONTAINS
  target: step.ftgo.gateway.post.auth.resend-code.http-ingress
  role: http_ingress
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/auth/registration.py
  symbol: application.routes.auth.registration.resend_auth_code
  line_start: 60
  line_end: 76
  evidence_type: implemented
- type: CONTAINS
  target: step.ftgo.gateway.post.auth.resend-code.publish.ftgo.rabbitmq.user.profile.resend-auth-code
  role: event_publish
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/user.py
  symbol: services.user.UserService.resend_auth_code
  line_start: 23
  line_end: 23
  evidence_type: implemented
inbound_relations:
- type: PARTICIPATES_IN
  source: service.ftgo.gateway
  completeness: partial
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/auth/registration.py
  symbol: application.routes.auth.registration.resend_auth_code
  line_start: 60
  line_end: 76
  evidence_type: implemented
- type: PARTICIPATES_IN
  source: service.ftgo.user
  completeness: partial
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/auth/registration.py
  symbol: application.routes.auth.registration.resend_auth_code
  line_start: 60
  line_end: 76
  evidence_type: implemented
attributes:
  step_count: 4
  classification_reason: publish and consume are proven but a later segment is unresolved
  max_call_depth: 3
---

# POST /auth/resend_code execution flow

Candidate execution flow stitched from source-backed call evidence in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Entry endpoint: `endpoint.ftgo.gateway.post.auth.resend-code`
- Completeness: `partial`
- Handler: `application.routes.auth.registration.resend_auth_code`
- Declared in: `backend/gateway/src/application/routes/auth/registration.py` (lines 60-76)
- Evidence class: `implemented`

## Steps

- `http_ingress` `step.ftgo.gateway.post.auth.resend-code.http-ingress`
- `service_dispatch` `step.ftgo.gateway.post.auth.resend-code.dispatch.services.user.userservice.resend-auth-code`
- `event_publish` `step.ftgo.gateway.post.auth.resend-code.publish.ftgo.rabbitmq.user.profile.resend-auth-code`
- `event_consume` `step.ftgo.gateway.post.auth.resend-code.consume.user.user.profile.resend-auth-code`

## Unresolved segments

This flow is not complete. The following segments could not be proven from source and are deliberately not invented:

- `persistence:user.profile.resend_auth_code`

## Review notes

This page is a candidate awaiting review. Every step is backed by a bounded call trace of at most 3 hops; no segment was inferred from the similarity between an endpoint path and an event name.

