---
id: flow.ftgo.gateway.delete.profile.delete
kind: UserFlow
type: UserFlow
title: DELETE /profile/delete execution flow
status: candidate
review_status: pending
candidate_of: user-flow-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: user-flow
owner: aide-ftgo-cohort
entry_endpoint: endpoint.ftgo.gateway.delete.profile.delete
http_method: DELETE
path: /profile/delete
path_resolution: partial
completeness: resolved
handler: application.routes.account.profile.delete_account
participating_services:
- service.ftgo.gateway
- service.ftgo.user
events:
- event.ftgo.rabbitmq.user.profile.delete-account
persistence_targets:
- table.ftgo.user.customer-address
- table.ftgo.user.user-profile
- table.ftgo.user.vehicle-info
enumerated_persistence_targets:
- table.ftgo.user.customer-address
- table.ftgo.user.user-profile
- table.ftgo.user.vehicle-info
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/account/profile.py
  symbol: application.routes.account.profile.delete_account
  line_start: 65
  line_end: 81
  evidence_type: implemented
relations:
- type: CONTAINS
  target: step.ftgo.gateway.delete.profile.delete.consume.user.user.profile.delete-account
  role: event_consume
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/user/src/events.py
  symbol: events.register_events
  line_start: 39
  line_end: 39
  evidence_type: implemented
- type: CONTAINS
  target: step.ftgo.gateway.delete.profile.delete.dispatch.services.user.userservice.delete-account
  role: service_dispatch
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/account/profile.py
  symbol: application.routes.account.profile.delete_account
  line_start: 69
  line_end: 69
  evidence_type: implemented
- type: CONTAINS
  target: step.ftgo.gateway.delete.profile.delete.http-ingress
  role: http_ingress
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/account/profile.py
  symbol: application.routes.account.profile.delete_account
  line_start: 65
  line_end: 81
  evidence_type: implemented
- type: CONTAINS
  target: step.ftgo.gateway.delete.profile.delete.publish.ftgo.rabbitmq.user.profile.delete-account
  role: event_publish
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/user.py
  symbol: services.user.UserService.delete_account
  line_start: 39
  line_end: 39
  evidence_type: implemented
- type: CONTAINS
  target: step.ftgo.gateway.delete.profile.delete.read.ftgo.user.customer-address
  role: persistence_read
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/user/src/data_access/repository/db_repository.py
  symbol: data_access.repository.db_repository.DatabaseRepository.delete
  line_start: 121
  line_end: 121
  evidence_type: implemented
- type: CONTAINS
  target: step.ftgo.gateway.delete.profile.delete.read.ftgo.user.user-profile
  role: persistence_read
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/user/src/data_access/repository/db_repository.py
  symbol: data_access.repository.db_repository.DatabaseRepository.delete
  line_start: 121
  line_end: 121
  evidence_type: implemented
- type: CONTAINS
  target: step.ftgo.gateway.delete.profile.delete.read.ftgo.user.vehicle-info
  role: persistence_read
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/user/src/data_access/repository/db_repository.py
  symbol: data_access.repository.db_repository.DatabaseRepository.delete
  line_start: 121
  line_end: 121
  evidence_type: implemented
- type: CONTAINS
  target: step.ftgo.gateway.delete.profile.delete.write.ftgo.user.customer-address
  role: persistence_write
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/user/src/data_access/repository/db_repository.py
  symbol: data_access.repository.db_repository.DatabaseRepository.delete
  line_start: 127
  line_end: 127
  evidence_type: implemented
- type: CONTAINS
  target: step.ftgo.gateway.delete.profile.delete.write.ftgo.user.user-profile
  role: persistence_write
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/user/src/data_access/repository/db_repository.py
  symbol: data_access.repository.db_repository.DatabaseRepository.delete
  line_start: 127
  line_end: 127
  evidence_type: implemented
- type: CONTAINS
  target: step.ftgo.gateway.delete.profile.delete.write.ftgo.user.vehicle-info
  role: persistence_write
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/user/src/data_access/repository/db_repository.py
  symbol: data_access.repository.db_repository.DatabaseRepository.delete
  line_start: 127
  line_end: 127
  evidence_type: implemented
inbound_relations:
- type: PARTICIPATES_IN
  source: service.ftgo.gateway
  completeness: resolved
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/account/profile.py
  symbol: application.routes.account.profile.delete_account
  line_start: 65
  line_end: 81
  evidence_type: implemented
- type: PARTICIPATES_IN
  source: service.ftgo.user
  completeness: resolved
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/account/profile.py
  symbol: application.routes.account.profile.delete_account
  line_start: 65
  line_end: 81
  evidence_type: implemented
attributes:
  step_count: 10
  classification_reason: endpoint, publish, consume and persistence are all source-backed
  max_call_depth: 3
---

# DELETE /profile/delete execution flow

Candidate execution flow stitched from source-backed call evidence in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Entry endpoint: `endpoint.ftgo.gateway.delete.profile.delete`
- Completeness: `resolved`
- Handler: `application.routes.account.profile.delete_account`
- Declared in: `backend/gateway/src/application/routes/account/profile.py` (lines 65-81)
- Evidence class: `implemented`

## Steps

- `http_ingress` `step.ftgo.gateway.delete.profile.delete.http-ingress`
- `service_dispatch` `step.ftgo.gateway.delete.profile.delete.dispatch.services.user.userservice.delete-account`
- `event_publish` `step.ftgo.gateway.delete.profile.delete.publish.ftgo.rabbitmq.user.profile.delete-account`
- `event_consume` `step.ftgo.gateway.delete.profile.delete.consume.user.user.profile.delete-account`
- `persistence_read` `step.ftgo.gateway.delete.profile.delete.read.ftgo.user.customer-address`
- `persistence_read` `step.ftgo.gateway.delete.profile.delete.read.ftgo.user.user-profile`
- `persistence_read` `step.ftgo.gateway.delete.profile.delete.read.ftgo.user.vehicle-info`
- `persistence_write` `step.ftgo.gateway.delete.profile.delete.write.ftgo.user.customer-address`
- `persistence_write` `step.ftgo.gateway.delete.profile.delete.write.ftgo.user.user-profile`
- `persistence_write` `step.ftgo.gateway.delete.profile.delete.write.ftgo.user.vehicle-info`

## Persistence targets that are not pinned by the call site

The call path to these targets is proven, but the target itself comes from a generic repository that takes the model as an argument, so every mapped model is a possible target. Treat the specific target as a candidate, not a fact:

- `table.ftgo.user.customer-address`
- `table.ftgo.user.user-profile`
- `table.ftgo.user.vehicle-info`

## Review notes

This page is a candidate awaiting review. Every step is backed by a bounded call trace of at most 3 hops; no segment was inferred from the similarity between an endpoint path and an event name.

