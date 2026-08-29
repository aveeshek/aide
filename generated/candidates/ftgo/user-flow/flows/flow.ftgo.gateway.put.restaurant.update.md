---
id: flow.ftgo.gateway.put.restaurant.update
kind: UserFlow
type: UserFlow
title: PUT /restaurant/update execution flow
status: candidate
review_status: pending
candidate_of: user-flow-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: user-flow
owner: aide-ftgo-cohort
entry_endpoint: endpoint.ftgo.gateway.put.restaurant.update
http_method: PUT
path: /restaurant/update
path_resolution: partial
completeness: resolved
handler: application.routes.restaurant.restaurant.update_information
participating_services:
- service.ftgo.gateway
- service.ftgo.restaurant
events:
- event.ftgo.rabbitmq.restaurant.supplier.update-information
persistence_targets:
- table.ftgo.restaurant.supplier-profile
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/restaurant/restaurant.py
  symbol: application.routes.restaurant.restaurant.update_information
  line_start: 115
  line_end: 133
  evidence_type: implemented
relations:
- type: CONTAINS
  target: step.ftgo.gateway.put.restaurant.update.consume.restaurant.restaurant.supplier.update-information
  role: event_consume
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/restaurant/src/events.py
  symbol: events.register_events
  line_start: 32
  line_end: 32
  evidence_type: implemented
- type: CONTAINS
  target: step.ftgo.gateway.put.restaurant.update.dispatch.services.restaurant.restaurantservice.update-information
  role: service_dispatch
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/restaurant/restaurant.py
  symbol: application.routes.restaurant.restaurant.update_information
  line_start: 119
  line_end: 119
  evidence_type: implemented
- type: CONTAINS
  target: step.ftgo.gateway.put.restaurant.update.http-ingress
  role: http_ingress
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/restaurant/restaurant.py
  symbol: application.routes.restaurant.restaurant.update_information
  line_start: 115
  line_end: 133
  evidence_type: implemented
- type: CONTAINS
  target: step.ftgo.gateway.put.restaurant.update.publish.ftgo.rabbitmq.restaurant.supplier.update-information
  role: event_publish
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/restaurant.py
  symbol: services.restaurant.RestaurantService.update_information
  line_start: 27
  line_end: 27
  evidence_type: implemented
- type: CONTAINS
  target: step.ftgo.gateway.put.restaurant.update.read.ftgo.restaurant.supplier-profile
  role: persistence_read
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/restaurant/src/domain/restaurant.py
  symbol: domain.restaurant.RestaurantDomain.update_profile_information
  line_start: 139
  line_end: 143
  evidence_type: implemented
inbound_relations:
- type: PARTICIPATES_IN
  source: service.ftgo.gateway
  completeness: resolved
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/restaurant/restaurant.py
  symbol: application.routes.restaurant.restaurant.update_information
  line_start: 115
  line_end: 133
  evidence_type: implemented
- type: PARTICIPATES_IN
  source: service.ftgo.restaurant
  completeness: resolved
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/restaurant/restaurant.py
  symbol: application.routes.restaurant.restaurant.update_information
  line_start: 115
  line_end: 133
  evidence_type: implemented
attributes:
  step_count: 5
  classification_reason: endpoint, publish, consume and persistence are all source-backed
  max_call_depth: 3
---

# PUT /restaurant/update execution flow

Candidate execution flow stitched from source-backed call evidence in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Entry endpoint: `endpoint.ftgo.gateway.put.restaurant.update`
- Completeness: `resolved`
- Handler: `application.routes.restaurant.restaurant.update_information`
- Declared in: `backend/gateway/src/application/routes/restaurant/restaurant.py` (lines 115-133)
- Evidence class: `implemented`

## Steps

- `http_ingress` `step.ftgo.gateway.put.restaurant.update.http-ingress`
- `service_dispatch` `step.ftgo.gateway.put.restaurant.update.dispatch.services.restaurant.restaurantservice.update-information`
- `event_publish` `step.ftgo.gateway.put.restaurant.update.publish.ftgo.rabbitmq.restaurant.supplier.update-information`
- `event_consume` `step.ftgo.gateway.put.restaurant.update.consume.restaurant.restaurant.supplier.update-information`
- `persistence_read` `step.ftgo.gateway.put.restaurant.update.read.ftgo.restaurant.supplier-profile`

## Review notes

This page is a candidate awaiting review. Every step is backed by a bounded call trace of at most 3 hops; no segment was inferred from the similarity between an endpoint path and an event name.

