---
id: step.ftgo.gateway.post.auth.verify.consume.user.user.profile.verify-account
kind: FlowStep
type: FlowStep
title: user consumes user.profile.verify_account
status: candidate
review_status: pending
candidate_of: user-flow-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: user-flow
owner: aide-ftgo-cohort
role: event_consume
flow: flow.ftgo.gateway.post.auth.verify
service: service.ftgo.user
derived_from: event.ftgo.rabbitmq.user.profile.verify-account
derived_from_kind: Event
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/user/src/events.py
  symbol: events.register_events
  line_start: 39
  line_end: 39
  evidence_type: implemented
relations:
- type: DERIVED_FROM
  target: event.ftgo.rabbitmq.user.profile.verify-account
  anchor_kind: Event
  role: event_consume
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/user/src/events.py
  symbol: events.register_events
  line_start: 39
  line_end: 39
  evidence_type: implemented
- type: IMPLEMENTS
  target: service.ftgo.user
  role: event_consume
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/user/src/events.py
  symbol: events.register_events
  line_start: 39
  line_end: 39
  evidence_type: implemented
- type: PRECEDES
  target: step.ftgo.gateway.post.auth.verify.read.ftgo.user.customer-address
  established_by: consumer call trace
  call_depth: 2
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/user/src/data_access/repository/db_repository.py
  symbol: data_access.repository.db_repository.DatabaseRepository.update
  line_start: 97
  line_end: 97
  evidence_type: implemented
- type: PRECEDES
  target: step.ftgo.gateway.post.auth.verify.read.ftgo.user.user-profile
  established_by: consumer call trace
  call_depth: 2
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/user/src/data_access/repository/db_repository.py
  symbol: data_access.repository.db_repository.DatabaseRepository.update
  line_start: 97
  line_end: 97
  evidence_type: implemented
- type: PRECEDES
  target: step.ftgo.gateway.post.auth.verify.read.ftgo.user.vehicle-info
  established_by: consumer call trace
  call_depth: 2
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/user/src/data_access/repository/db_repository.py
  symbol: data_access.repository.db_repository.DatabaseRepository.update
  line_start: 97
  line_end: 97
  evidence_type: implemented
- type: PRECEDES
  target: step.ftgo.gateway.post.auth.verify.write.ftgo.user.customer-address
  established_by: consumer call trace
  call_depth: 2
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/user/src/data_access/repository/db_repository.py
  symbol: data_access.repository.db_repository.DatabaseRepository.update
  line_start: 105
  line_end: 105
  evidence_type: implemented
- type: PRECEDES
  target: step.ftgo.gateway.post.auth.verify.write.ftgo.user.user-profile
  established_by: consumer call trace
  call_depth: 2
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/user/src/data_access/repository/db_repository.py
  symbol: data_access.repository.db_repository.DatabaseRepository.update
  line_start: 105
  line_end: 105
  evidence_type: implemented
- type: PRECEDES
  target: step.ftgo.gateway.post.auth.verify.write.ftgo.user.vehicle-info
  established_by: consumer call trace
  call_depth: 2
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/user/src/data_access/repository/db_repository.py
  symbol: data_access.repository.db_repository.DatabaseRepository.update
  line_start: 105
  line_end: 105
  evidence_type: implemented
inbound_relations:
- type: CONTAINS
  source: flow.ftgo.gateway.post.auth.verify
  role: event_consume
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/user/src/events.py
  symbol: events.register_events
  line_start: 39
  line_end: 39
  evidence_type: implemented
- type: PRECEDES
  source: step.ftgo.gateway.post.auth.verify.publish.ftgo.rabbitmq.user.profile.verify-account
  established_by: handler registration
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/user/src/events.py
  symbol: events.register_events
  line_start: 39
  line_end: 39
  evidence_type: implemented
attributes:
  event_identity: user.profile.verify_account
  handler_expression: ProfileService.verify_account
  handler_symbol: application.profile.ProfileService.verify_account
  operation: register_event
---

# user consumes user.profile.verify_account

Candidate execution step extracted from call evidence in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Role: `event_consume`
- Flow: `flow.ftgo.gateway.post.auth.verify`
- Performed by: `service.ftgo.user`
- Anchored on: `event.ftgo.rabbitmq.user.profile.verify-account` (`Event`)
- Declared in: `backend/microservices/user/src/events.py` (lines 39-39)
- Evidence class: `implemented`

## Review notes

This page is a candidate awaiting review. The step exists because a concrete call site proves it, and its ordering edges carry that call site as evidence.

