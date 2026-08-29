---
id: flow.ftgo.gateway.get.vehicle.get-info
kind: UserFlow
type: UserFlow
title: GET /vehicle/get_info execution flow
status: candidate
review_status: pending
candidate_of: user-flow-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: user-flow
owner: aide-ftgo-cohort
entry_endpoint: endpoint.ftgo.gateway.get.vehicle.get-info
http_method: GET
path: /vehicle/get_info
path_resolution: partial
completeness: resolved
handler: application.routes.driver.vehicle.get_info
participating_services:
- service.ftgo.gateway
- service.ftgo.user
events:
- event.ftgo.rabbitmq.driver.vehicle.get-info
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
  path: backend/gateway/src/application/routes/driver/vehicle.py
  symbol: application.routes.driver.vehicle.get_info
  line_start: 42
  line_end: 60
  evidence_type: implemented
relations:
- type: CONTAINS
  target: step.ftgo.gateway.get.vehicle.get-info.consume.user.driver.vehicle.get-info
  role: event_consume
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/user/src/events.py
  symbol: events.register_events
  line_start: 39
  line_end: 39
  evidence_type: implemented
- type: CONTAINS
  target: step.ftgo.gateway.get.vehicle.get-info.dispatch.services.vehicle.vehicleservice.get-info
  role: service_dispatch
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/driver/vehicle.py
  symbol: application.routes.driver.vehicle.get_info
  line_start: 47
  line_end: 47
  evidence_type: implemented
- type: CONTAINS
  target: step.ftgo.gateway.get.vehicle.get-info.http-ingress
  role: http_ingress
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/driver/vehicle.py
  symbol: application.routes.driver.vehicle.get_info
  line_start: 42
  line_end: 60
  evidence_type: implemented
- type: CONTAINS
  target: step.ftgo.gateway.get.vehicle.get-info.publish.ftgo.rabbitmq.driver.vehicle.get-info
  role: event_publish
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/vehicle.py
  symbol: services.vehicle.VehicleService.get_info
  line_start: 15
  line_end: 15
  evidence_type: implemented
- type: CONTAINS
  target: step.ftgo.gateway.get.vehicle.get-info.read.ftgo.user.customer-address
  role: persistence_read
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/user/src/data_access/repository/db_repository.py
  symbol: data_access.repository.db_repository.DatabaseRepository.fetch
  line_start: 55
  line_end: 55
  evidence_type: implemented
- type: CONTAINS
  target: step.ftgo.gateway.get.vehicle.get-info.read.ftgo.user.user-profile
  role: persistence_read
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/user/src/data_access/repository/db_repository.py
  symbol: data_access.repository.db_repository.DatabaseRepository.fetch
  line_start: 55
  line_end: 55
  evidence_type: implemented
- type: CONTAINS
  target: step.ftgo.gateway.get.vehicle.get-info.read.ftgo.user.vehicle-info
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
  path: backend/gateway/src/application/routes/driver/vehicle.py
  symbol: application.routes.driver.vehicle.get_info
  line_start: 42
  line_end: 60
  evidence_type: implemented
- type: PARTICIPATES_IN
  source: service.ftgo.user
  completeness: resolved
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/driver/vehicle.py
  symbol: application.routes.driver.vehicle.get_info
  line_start: 42
  line_end: 60
  evidence_type: implemented
attributes:
  step_count: 7
  classification_reason: endpoint, publish, consume and persistence are all source-backed
  max_call_depth: 3
---

# GET /vehicle/get_info execution flow

Candidate execution flow stitched from source-backed call evidence in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Entry endpoint: `endpoint.ftgo.gateway.get.vehicle.get-info`
- Completeness: `resolved`
- Handler: `application.routes.driver.vehicle.get_info`
- Declared in: `backend/gateway/src/application/routes/driver/vehicle.py` (lines 42-60)
- Evidence class: `implemented`

## Steps

- `http_ingress` `step.ftgo.gateway.get.vehicle.get-info.http-ingress`
- `service_dispatch` `step.ftgo.gateway.get.vehicle.get-info.dispatch.services.vehicle.vehicleservice.get-info`
- `event_publish` `step.ftgo.gateway.get.vehicle.get-info.publish.ftgo.rabbitmq.driver.vehicle.get-info`
- `event_consume` `step.ftgo.gateway.get.vehicle.get-info.consume.user.driver.vehicle.get-info`
- `persistence_read` `step.ftgo.gateway.get.vehicle.get-info.read.ftgo.user.customer-address`
- `persistence_read` `step.ftgo.gateway.get.vehicle.get-info.read.ftgo.user.user-profile`
- `persistence_read` `step.ftgo.gateway.get.vehicle.get-info.read.ftgo.user.vehicle-info`

## Persistence targets that are not pinned by the call site

The call path to these targets is proven, but the target itself comes from a generic repository that takes the model as an argument, so every mapped model is a possible target. Treat the specific target as a candidate, not a fact:

- `table.ftgo.user.customer-address`
- `table.ftgo.user.user-profile`
- `table.ftgo.user.vehicle-info`

## Review notes

This page is a candidate awaiting review. Every step is backed by a bounded call trace of at most 3 hops; no segment was inferred from the similarity between an endpoint path and an event name.

