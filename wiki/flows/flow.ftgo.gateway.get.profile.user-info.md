---
id: flow.ftgo.gateway.get.profile.user-info
kind: UserFlow
type: UserFlow
title: GET /profile/user_info execution flow
status: approved
review_status: approved
candidate_of: user-flow-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: user-flow
owner: aide-ftgo-cohort
entry_endpoint: endpoint.ftgo.gateway.get.profile.user-info
http_method: GET
path: /profile/user_info
path_resolution: partial
completeness: resolved
handler: application.routes.account.profile.get_info
participating_services:
- service.ftgo.gateway
- service.ftgo.user
events:
- event.ftgo.rabbitmq.user.profile.get-info
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
  symbol: application.routes.account.profile.get_info
  line_start: 39
  line_end: 63
  evidence_type: implemented
relations:
- type: CONTAINS
  target: step.ftgo.gateway.get.profile.user-info.consume.user.user.profile.get-info
  role: event_consume
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/user/src/events.py
  symbol: events.register_events
  line_start: 39
  line_end: 39
  evidence_type: implemented
- type: CONTAINS
  target: step.ftgo.gateway.get.profile.user-info.dispatch.services.user.userservice.get-profile-info
  role: service_dispatch
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/account/profile.py
  symbol: application.routes.account.profile.get_info
  line_start: 44
  line_end: 44
  evidence_type: implemented
- type: CONTAINS
  target: step.ftgo.gateway.get.profile.user-info.http-ingress
  role: http_ingress
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/account/profile.py
  symbol: application.routes.account.profile.get_info
  line_start: 39
  line_end: 63
  evidence_type: implemented
- type: CONTAINS
  target: step.ftgo.gateway.get.profile.user-info.publish.ftgo.rabbitmq.user.profile.get-info
  role: event_publish
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/user.py
  symbol: services.user.UserService.get_profile_info
  line_start: 35
  line_end: 35
  evidence_type: implemented
- type: CONTAINS
  target: step.ftgo.gateway.get.profile.user-info.read.ftgo.user.customer-address
  role: persistence_read
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/user/src/data_access/repository/db_repository.py
  symbol: data_access.repository.db_repository.DatabaseRepository.fetch
  line_start: 55
  line_end: 55
  evidence_type: implemented
- type: CONTAINS
  target: step.ftgo.gateway.get.profile.user-info.read.ftgo.user.user-profile
  role: persistence_read
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/user/src/data_access/repository/db_repository.py
  symbol: data_access.repository.db_repository.DatabaseRepository.fetch
  line_start: 55
  line_end: 55
  evidence_type: implemented
- type: CONTAINS
  target: step.ftgo.gateway.get.profile.user-info.read.ftgo.user.vehicle-info
  role: persistence_read
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/user/src/data_access/repository/db_repository.py
  symbol: data_access.repository.db_repository.DatabaseRepository.fetch
  line_start: 55
  line_end: 55
  evidence_type: implemented
inbound_relations:
- type: PARTICIPATES_IN
  source: service.ftgo.gateway
  completeness: resolved
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/account/profile.py
  symbol: application.routes.account.profile.get_info
  line_start: 39
  line_end: 63
  evidence_type: implemented
- type: PARTICIPATES_IN
  source: service.ftgo.user
  completeness: resolved
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/account/profile.py
  symbol: application.routes.account.profile.get_info
  line_start: 39
  line_end: 63
  evidence_type: implemented
attributes:
  step_count: 7
  classification_reason: endpoint, publish, consume and persistence are all source-backed
  max_call_depth: 3
---

# GET /profile/user_info execution flow

Canonical execution flow stitched from source-backed call evidence in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Entry endpoint: `endpoint.ftgo.gateway.get.profile.user-info`
- Completeness: `resolved`
- Handler: `application.routes.account.profile.get_info`
- Declared in: `backend/gateway/src/application/routes/account/profile.py` (lines 39-63)
- Evidence class: `implemented`

## Steps

- `http_ingress` `step.ftgo.gateway.get.profile.user-info.http-ingress`
- `service_dispatch` `step.ftgo.gateway.get.profile.user-info.dispatch.services.user.userservice.get-profile-info`
- `event_publish` `step.ftgo.gateway.get.profile.user-info.publish.ftgo.rabbitmq.user.profile.get-info`
- `event_consume` `step.ftgo.gateway.get.profile.user-info.consume.user.user.profile.get-info`
- `persistence_read` `step.ftgo.gateway.get.profile.user-info.read.ftgo.user.customer-address`
- `persistence_read` `step.ftgo.gateway.get.profile.user-info.read.ftgo.user.user-profile`
- `persistence_read` `step.ftgo.gateway.get.profile.user-info.read.ftgo.user.vehicle-info`

## Persistence targets that are not pinned by the call site

The call path to these targets is proven, but the target itself comes from a generic repository that takes the model as an argument, so every mapped model is a possible target. Treat the specific target as a candidate, not a fact:

- `table.ftgo.user.customer-address`
- `table.ftgo.user.user-profile`
- `table.ftgo.user.vehicle-info`

## Review notes

This approved canonical page records a source-backed execution flow. Every step is backed by a bounded call trace of at most 3 hops; no segment was inferred from similarity between an endpoint path and an event name.

