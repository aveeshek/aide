---
id: step.ftgo.gateway.post.auth.resend-code.publish.ftgo.rabbitmq.user.profile.resend-auth-code
kind: FlowStep
type: FlowStep
title: publish user.profile.resend_auth_code
status: approved
review_status: approved
candidate_of: user-flow-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: user-flow
owner: aide-ftgo-cohort
role: event_publish
flow: flow.ftgo.gateway.post.auth.resend-code
service: service.ftgo.gateway
derived_from: event.ftgo.rabbitmq.user.profile.resend-auth-code
derived_from_kind: Event
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/user.py
  symbol: services.user.UserService.resend_auth_code
  line_start: 23
  line_end: 23
  evidence_type: implemented
relations:
- type: DERIVED_FROM
  target: event.ftgo.rabbitmq.user.profile.resend-auth-code
  anchor_kind: Event
  role: event_publish
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/user.py
  symbol: services.user.UserService.resend_auth_code
  line_start: 23
  line_end: 23
  evidence_type: implemented
- type: IMPLEMENTS
  target: service.ftgo.gateway
  role: event_publish
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/user.py
  symbol: services.user.UserService.resend_auth_code
  line_start: 23
  line_end: 23
  evidence_type: implemented
- type: PRECEDES
  target: step.ftgo.gateway.post.auth.resend-code.consume.user.user.profile.resend-auth-code
  established_by: handler registration
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/user/src/events.py
  symbol: events.register_events
  line_start: 39
  line_end: 39
  evidence_type: implemented
inbound_relations:
- type: CONTAINS
  source: flow.ftgo.gateway.post.auth.resend-code
  role: event_publish
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/user.py
  symbol: services.user.UserService.resend_auth_code
  line_start: 23
  line_end: 23
  evidence_type: implemented
- type: PRECEDES
  source: step.ftgo.gateway.post.auth.resend-code.dispatch.services.user.userservice.resend-auth-code
  established_by: publisher call site
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/user.py
  symbol: services.user.UserService.resend_auth_code
  line_start: 23
  line_end: 23
  evidence_type: implemented
attributes:
  event_identity: user.profile.resend_auth_code
  operation: call
  mechanism: rpc
  broker_library: rabbitmq_rpc
  via_wrapper: services.base.Microservice._call_rpc
  correlation: matched
---

# publish user.profile.resend_auth_code

Canonical execution step extracted from call evidence in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Role: `event_publish`
- Flow: `flow.ftgo.gateway.post.auth.resend-code`
- Performed by: `service.ftgo.gateway`
- Anchored on: `event.ftgo.rabbitmq.user.profile.resend-auth-code` (`Event`)
- Declared in: `backend/gateway/src/services/user.py` (lines 23-23)
- Evidence class: `implemented`

## Review notes

This approved canonical page records a source-backed execution step. The step exists because a concrete call site proves it, and its ordering edges carry that call site as evidence.

