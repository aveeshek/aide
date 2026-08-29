---
id: step.ftgo.gateway.post.auth.verify.publish.ftgo.rabbitmq.user.profile.verify-account
kind: FlowStep
type: FlowStep
title: publish user.profile.verify_account
status: candidate
review_status: pending
candidate_of: user-flow-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: user-flow
owner: aide-ftgo-cohort
role: event_publish
flow: flow.ftgo.gateway.post.auth.verify
service: service.ftgo.gateway
derived_from: event.ftgo.rabbitmq.user.profile.verify-account
derived_from_kind: Event
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/user.py
  symbol: services.user.UserService.verify_account
  line_start: 27
  line_end: 27
  evidence_type: implemented
relations:
- type: DERIVED_FROM
  target: event.ftgo.rabbitmq.user.profile.verify-account
  anchor_kind: Event
  role: event_publish
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/user.py
  symbol: services.user.UserService.verify_account
  line_start: 27
  line_end: 27
  evidence_type: implemented
- type: IMPLEMENTS
  target: service.ftgo.gateway
  role: event_publish
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/user.py
  symbol: services.user.UserService.verify_account
  line_start: 27
  line_end: 27
  evidence_type: implemented
- type: PRECEDES
  target: step.ftgo.gateway.post.auth.verify.consume.user.user.profile.verify-account
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
  source: flow.ftgo.gateway.post.auth.verify
  role: event_publish
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/user.py
  symbol: services.user.UserService.verify_account
  line_start: 27
  line_end: 27
  evidence_type: implemented
- type: PRECEDES
  source: step.ftgo.gateway.post.auth.verify.dispatch.services.user.userservice.verify-account
  established_by: publisher call site
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/user.py
  symbol: services.user.UserService.verify_account
  line_start: 27
  line_end: 27
  evidence_type: implemented
attributes:
  event_identity: user.profile.verify_account
  operation: call
  mechanism: rpc
  broker_library: rabbitmq_rpc
  via_wrapper: services.base.Microservice._call_rpc
  correlation: matched
---

# publish user.profile.verify_account

Candidate execution step extracted from call evidence in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Role: `event_publish`
- Flow: `flow.ftgo.gateway.post.auth.verify`
- Performed by: `service.ftgo.gateway`
- Anchored on: `event.ftgo.rabbitmq.user.profile.verify-account` (`Event`)
- Declared in: `backend/gateway/src/services/user.py` (lines 27-27)
- Evidence class: `implemented`

## Review notes

This page is a candidate awaiting review. The step exists because a concrete call site proves it, and its ordering edges carry that call site as evidence.

