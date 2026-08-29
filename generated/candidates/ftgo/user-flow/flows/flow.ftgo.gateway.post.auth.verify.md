---
id: flow.ftgo.gateway.post.auth.verify
kind: UserFlow
type: UserFlow
title: POST /auth/verify execution flow
status: candidate
review_status: pending
candidate_of: user-flow-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: user-flow
owner: aide-ftgo-cohort
entry_endpoint: endpoint.ftgo.gateway.post.auth.verify
http_method: POST
path: /auth/verify
path_resolution: partial
completeness: resolved
handler: application.routes.auth.registration.verify_account
participating_services:
- service.ftgo.gateway
- service.ftgo.user
events:
- event.ftgo.rabbitmq.user.profile.verify-account
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
  path: backend/gateway/src/application/routes/auth/registration.py
  symbol: application.routes.auth.registration.verify_account
  line_start: 42
  line_end: 58
  evidence_type: implemented
relations:
- type: CONTAINS
  target: step.ftgo.gateway.post.auth.verify.consume.user.user.profile.verify-account
  role: event_consume
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/user/src/events.py
  symbol: events.register_events
  line_start: 39
  line_end: 39
  evidence_type: implemented
- type: CONTAINS
  target: step.ftgo.gateway.post.auth.verify.dispatch.services.user.userservice.verify-account
  role: service_dispatch
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/auth/registration.py
  symbol: application.routes.auth.registration.verify_account
  line_start: 46
  line_end: 46
  evidence_type: implemented
- type: CONTAINS
  target: step.ftgo.gateway.post.auth.verify.http-ingress
  role: http_ingress
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/auth/registration.py
  symbol: application.routes.auth.registration.verify_account
  line_start: 42
  line_end: 58
  evidence_type: implemented
- type: CONTAINS
  target: step.ftgo.gateway.post.auth.verify.publish.ftgo.rabbitmq.user.profile.verify-account
  role: event_publish
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/user.py
  symbol: services.user.UserService.verify_account
  line_start: 27
  line_end: 27
  evidence_type: implemented
- type: CONTAINS
  target: step.ftgo.gateway.post.auth.verify.read.ftgo.user.customer-address
  role: persistence_read
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/user/src/data_access/repository/db_repository.py
  symbol: data_access.repository.db_repository.DatabaseRepository.update
  line_start: 97
  line_end: 97
  evidence_type: implemented
- type: CONTAINS
  target: step.ftgo.gateway.post.auth.verify.read.ftgo.user.user-profile
  role: persistence_read
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/user/src/data_access/repository/db_repository.py
  symbol: data_access.repository.db_repository.DatabaseRepository.update
  line_start: 97
  line_end: 97
  evidence_type: implemented
- type: CONTAINS
  target: step.ftgo.gateway.post.auth.verify.read.ftgo.user.vehicle-info
  role: persistence_read
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/user/src/data_access/repository/db_repository.py
  symbol: data_access.repository.db_repository.DatabaseRepository.update
  line_start: 97
  line_end: 97
  evidence_type: implemented
- type: CONTAINS
  target: step.ftgo.gateway.post.auth.verify.write.ftgo.user.customer-address
  role: persistence_write
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/user/src/data_access/repository/db_repository.py
  symbol: data_access.repository.db_repository.DatabaseRepository.update
  line_start: 105
  line_end: 105
  evidence_type: implemented
- type: CONTAINS
  target: step.ftgo.gateway.post.auth.verify.write.ftgo.user.user-profile
  role: persistence_write
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/user/src/data_access/repository/db_repository.py
  symbol: data_access.repository.db_repository.DatabaseRepository.update
  line_start: 105
  line_end: 105
  evidence_type: implemented
- type: CONTAINS
  target: step.ftgo.gateway.post.auth.verify.write.ftgo.user.vehicle-info
  role: persistence_write
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/user/src/data_access/repository/db_repository.py
  symbol: data_access.repository.db_repository.DatabaseRepository.update
  line_start: 105
  line_end: 105
  evidence_type: implemented
inbound_relations:
- type: PARTICIPATES_IN
  source: service.ftgo.gateway
  completeness: resolved
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/auth/registration.py
  symbol: application.routes.auth.registration.verify_account
  line_start: 42
  line_end: 58
  evidence_type: implemented
- type: PARTICIPATES_IN
  source: service.ftgo.user
  completeness: resolved
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/auth/registration.py
  symbol: application.routes.auth.registration.verify_account
  line_start: 42
  line_end: 58
  evidence_type: implemented
attributes:
  step_count: 10
  classification_reason: endpoint, publish, consume and persistence are all source-backed
  max_call_depth: 3
---

# POST /auth/verify execution flow

Candidate execution flow stitched from source-backed call evidence in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Entry endpoint: `endpoint.ftgo.gateway.post.auth.verify`
- Completeness: `resolved`
- Handler: `application.routes.auth.registration.verify_account`
- Declared in: `backend/gateway/src/application/routes/auth/registration.py` (lines 42-58)
- Evidence class: `implemented`

## Steps

- `http_ingress` `step.ftgo.gateway.post.auth.verify.http-ingress`
- `service_dispatch` `step.ftgo.gateway.post.auth.verify.dispatch.services.user.userservice.verify-account`
- `event_publish` `step.ftgo.gateway.post.auth.verify.publish.ftgo.rabbitmq.user.profile.verify-account`
- `event_consume` `step.ftgo.gateway.post.auth.verify.consume.user.user.profile.verify-account`
- `persistence_read` `step.ftgo.gateway.post.auth.verify.read.ftgo.user.customer-address`
- `persistence_read` `step.ftgo.gateway.post.auth.verify.read.ftgo.user.user-profile`
- `persistence_read` `step.ftgo.gateway.post.auth.verify.read.ftgo.user.vehicle-info`
- `persistence_write` `step.ftgo.gateway.post.auth.verify.write.ftgo.user.customer-address`
- `persistence_write` `step.ftgo.gateway.post.auth.verify.write.ftgo.user.user-profile`
- `persistence_write` `step.ftgo.gateway.post.auth.verify.write.ftgo.user.vehicle-info`

## Persistence targets that are not pinned by the call site

The call path to these targets is proven, but the target itself comes from a generic repository that takes the model as an argument, so every mapped model is a possible target. Treat the specific target as a candidate, not a fact:

- `table.ftgo.user.customer-address`
- `table.ftgo.user.user-profile`
- `table.ftgo.user.vehicle-info`

## Review notes

This page is a candidate awaiting review. Every step is backed by a bounded call trace of at most 3 hops; no segment was inferred from the similarity between an endpoint path and an event name.

