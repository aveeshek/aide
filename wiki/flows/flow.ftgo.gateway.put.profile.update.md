---
id: flow.ftgo.gateway.put.profile.update
kind: UserFlow
type: UserFlow
title: PUT /profile/update execution flow
status: approved
review_status: approved
candidate_of: user-flow-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: user-flow
owner: aide-ftgo-cohort
entry_endpoint: endpoint.ftgo.gateway.put.profile.update
http_method: PUT
path: /profile/update
path_resolution: partial
completeness: resolved
handler: application.routes.account.profile.update_profile
participating_services:
- service.ftgo.gateway
- service.ftgo.user
events:
- event.ftgo.rabbitmq.user.profile.update-profile
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
  symbol: application.routes.account.profile.update_profile
  line_start: 85
  line_end: 106
  evidence_type: implemented
relations:
- type: CONTAINS
  target: step.ftgo.gateway.put.profile.update.consume.user.user.profile.update-profile
  role: event_consume
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/user/src/events.py
  symbol: events.register_events
  line_start: 39
  line_end: 39
  evidence_type: implemented
- type: CONTAINS
  target: step.ftgo.gateway.put.profile.update.dispatch.services.user.userservice.update-profile
  role: service_dispatch
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/account/profile.py
  symbol: application.routes.account.profile.update_profile
  line_start: 91
  line_end: 91
  evidence_type: implemented
- type: CONTAINS
  target: step.ftgo.gateway.put.profile.update.http-ingress
  role: http_ingress
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/account/profile.py
  symbol: application.routes.account.profile.update_profile
  line_start: 85
  line_end: 106
  evidence_type: implemented
- type: CONTAINS
  target: step.ftgo.gateway.put.profile.update.publish.ftgo.rabbitmq.user.profile.update-profile
  role: event_publish
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/user.py
  symbol: services.user.UserService.update_profile
  line_start: 47
  line_end: 47
  evidence_type: implemented
- type: CONTAINS
  target: step.ftgo.gateway.put.profile.update.read.ftgo.user.customer-address
  role: persistence_read
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/user/src/data_access/repository/db_repository.py
  symbol: data_access.repository.db_repository.DatabaseRepository.update
  line_start: 97
  line_end: 97
  evidence_type: implemented
- type: CONTAINS
  target: step.ftgo.gateway.put.profile.update.read.ftgo.user.user-profile
  role: persistence_read
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/user/src/data_access/repository/db_repository.py
  symbol: data_access.repository.db_repository.DatabaseRepository.update
  line_start: 97
  line_end: 97
  evidence_type: implemented
- type: CONTAINS
  target: step.ftgo.gateway.put.profile.update.read.ftgo.user.vehicle-info
  role: persistence_read
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/user/src/data_access/repository/db_repository.py
  symbol: data_access.repository.db_repository.DatabaseRepository.update
  line_start: 97
  line_end: 97
  evidence_type: implemented
- type: CONTAINS
  target: step.ftgo.gateway.put.profile.update.write.ftgo.user.customer-address
  role: persistence_write
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/user/src/data_access/repository/db_repository.py
  symbol: data_access.repository.db_repository.DatabaseRepository.update
  line_start: 105
  line_end: 105
  evidence_type: implemented
- type: CONTAINS
  target: step.ftgo.gateway.put.profile.update.write.ftgo.user.user-profile
  role: persistence_write
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/user/src/data_access/repository/db_repository.py
  symbol: data_access.repository.db_repository.DatabaseRepository.update
  line_start: 105
  line_end: 105
  evidence_type: implemented
- type: CONTAINS
  target: step.ftgo.gateway.put.profile.update.write.ftgo.user.vehicle-info
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
  path: backend/gateway/src/application/routes/account/profile.py
  symbol: application.routes.account.profile.update_profile
  line_start: 85
  line_end: 106
  evidence_type: implemented
- type: PARTICIPATES_IN
  source: service.ftgo.user
  completeness: resolved
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/account/profile.py
  symbol: application.routes.account.profile.update_profile
  line_start: 85
  line_end: 106
  evidence_type: implemented
attributes:
  step_count: 10
  classification_reason: endpoint, publish, consume and persistence are all source-backed
  max_call_depth: 3
---

# PUT /profile/update execution flow

Canonical execution flow stitched from source-backed call evidence in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Entry endpoint: `endpoint.ftgo.gateway.put.profile.update`
- Completeness: `resolved`
- Handler: `application.routes.account.profile.update_profile`
- Declared in: `backend/gateway/src/application/routes/account/profile.py` (lines 85-106)
- Evidence class: `implemented`

## Steps

- `http_ingress` `step.ftgo.gateway.put.profile.update.http-ingress`
- `service_dispatch` `step.ftgo.gateway.put.profile.update.dispatch.services.user.userservice.update-profile`
- `event_publish` `step.ftgo.gateway.put.profile.update.publish.ftgo.rabbitmq.user.profile.update-profile`
- `event_consume` `step.ftgo.gateway.put.profile.update.consume.user.user.profile.update-profile`
- `persistence_read` `step.ftgo.gateway.put.profile.update.read.ftgo.user.customer-address`
- `persistence_read` `step.ftgo.gateway.put.profile.update.read.ftgo.user.user-profile`
- `persistence_read` `step.ftgo.gateway.put.profile.update.read.ftgo.user.vehicle-info`
- `persistence_write` `step.ftgo.gateway.put.profile.update.write.ftgo.user.customer-address`
- `persistence_write` `step.ftgo.gateway.put.profile.update.write.ftgo.user.user-profile`
- `persistence_write` `step.ftgo.gateway.put.profile.update.write.ftgo.user.vehicle-info`

## Persistence targets that are not pinned by the call site

The call path to these targets is proven, but the target itself comes from a generic repository that takes the model as an argument, so every mapped model is a possible target. Treat the specific target as a candidate, not a fact:

- `table.ftgo.user.customer-address`
- `table.ftgo.user.user-profile`
- `table.ftgo.user.vehicle-info`

## Review notes

This approved canonical page records a source-backed execution flow. Every step is backed by a bounded call trace of at most 3 hops; no segment was inferred from similarity between an endpoint path and an event name.

