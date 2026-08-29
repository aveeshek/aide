---
id: flow.ftgo.gateway.post.address.set-preferred
kind: UserFlow
type: UserFlow
title: POST /address/set-preferred execution flow
status: candidate
review_status: pending
candidate_of: user-flow-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: user-flow
owner: aide-ftgo-cohort
entry_endpoint: endpoint.ftgo.gateway.post.address.set-preferred
http_method: POST
path: /address/set-preferred
path_resolution: partial
completeness: resolved
handler: application.routes.customer.address.set_address_preferency
participating_services:
- service.ftgo.gateway
- service.ftgo.user
events:
- event.ftgo.rabbitmq.user.address.set-preferred-address
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
  path: backend/gateway/src/application/routes/customer/address.py
  symbol: application.routes.customer.address.set_address_preferency
  line_start: 88
  line_end: 110
  evidence_type: implemented
relations:
- type: CONTAINS
  target: step.ftgo.gateway.post.address.set-preferred.consume.user.user.address.set-preferred-address
  role: event_consume
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/user/src/events.py
  symbol: events.register_events
  line_start: 39
  line_end: 39
  evidence_type: implemented
- type: CONTAINS
  target: step.ftgo.gateway.post.address.set-preferred.dispatch.services.user.userservice.set-preferred-address
  role: service_dispatch
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/customer/address.py
  symbol: application.routes.customer.address.set_address_preferency
  line_start: 94
  line_end: 94
  evidence_type: implemented
- type: CONTAINS
  target: step.ftgo.gateway.post.address.set-preferred.http-ingress
  role: http_ingress
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/customer/address.py
  symbol: application.routes.customer.address.set_address_preferency
  line_start: 88
  line_end: 110
  evidence_type: implemented
- type: CONTAINS
  target: step.ftgo.gateway.post.address.set-preferred.publish.ftgo.rabbitmq.user.address.set-preferred-address
  role: event_publish
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/user.py
  symbol: services.user.UserService.set_preferred_address
  line_start: 59
  line_end: 59
  evidence_type: implemented
- type: CONTAINS
  target: step.ftgo.gateway.post.address.set-preferred.read.ftgo.user.customer-address
  role: persistence_read
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/user/src/data_access/repository/db_repository.py
  symbol: data_access.repository.db_repository.DatabaseRepository.fetch
  line_start: 55
  line_end: 55
  evidence_type: implemented
- type: CONTAINS
  target: step.ftgo.gateway.post.address.set-preferred.read.ftgo.user.user-profile
  role: persistence_read
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/user/src/data_access/repository/db_repository.py
  symbol: data_access.repository.db_repository.DatabaseRepository.fetch
  line_start: 55
  line_end: 55
  evidence_type: implemented
- type: CONTAINS
  target: step.ftgo.gateway.post.address.set-preferred.read.ftgo.user.vehicle-info
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
  path: backend/gateway/src/application/routes/customer/address.py
  symbol: application.routes.customer.address.set_address_preferency
  line_start: 88
  line_end: 110
  evidence_type: implemented
- type: PARTICIPATES_IN
  source: service.ftgo.user
  completeness: resolved
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/customer/address.py
  symbol: application.routes.customer.address.set_address_preferency
  line_start: 88
  line_end: 110
  evidence_type: implemented
attributes:
  step_count: 7
  classification_reason: endpoint, publish, consume and persistence are all source-backed
  max_call_depth: 3
---

# POST /address/set-preferred execution flow

Candidate execution flow stitched from source-backed call evidence in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Entry endpoint: `endpoint.ftgo.gateway.post.address.set-preferred`
- Completeness: `resolved`
- Handler: `application.routes.customer.address.set_address_preferency`
- Declared in: `backend/gateway/src/application/routes/customer/address.py` (lines 88-110)
- Evidence class: `implemented`

## Steps

- `http_ingress` `step.ftgo.gateway.post.address.set-preferred.http-ingress`
- `service_dispatch` `step.ftgo.gateway.post.address.set-preferred.dispatch.services.user.userservice.set-preferred-address`
- `event_publish` `step.ftgo.gateway.post.address.set-preferred.publish.ftgo.rabbitmq.user.address.set-preferred-address`
- `event_consume` `step.ftgo.gateway.post.address.set-preferred.consume.user.user.address.set-preferred-address`
- `persistence_read` `step.ftgo.gateway.post.address.set-preferred.read.ftgo.user.customer-address`
- `persistence_read` `step.ftgo.gateway.post.address.set-preferred.read.ftgo.user.user-profile`
- `persistence_read` `step.ftgo.gateway.post.address.set-preferred.read.ftgo.user.vehicle-info`

## Persistence targets that are not pinned by the call site

The call path to these targets is proven, but the target itself comes from a generic repository that takes the model as an argument, so every mapped model is a possible target. Treat the specific target as a candidate, not a fact:

- `table.ftgo.user.customer-address`
- `table.ftgo.user.user-profile`
- `table.ftgo.user.vehicle-info`

## Review notes

This page is a candidate awaiting review. Every step is backed by a bounded call trace of at most 3 hops; no segment was inferred from the similarity between an endpoint path and an event name.

