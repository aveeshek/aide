---
id: flow.ftgo.gateway.delete.restaurant.delete
kind: UserFlow
type: UserFlow
title: DELETE /restaurant/delete execution flow
status: approved
review_status: approved
candidate_of: user-flow-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: user-flow
owner: aide-ftgo-cohort
entry_endpoint: endpoint.ftgo.gateway.delete.restaurant.delete
http_method: DELETE
path: /restaurant/delete
path_resolution: partial
completeness: resolved
handler: application.routes.restaurant.restaurant.delete_restaurant
participating_services:
- service.ftgo.gateway
- service.ftgo.restaurant
events:
- event.ftgo.rabbitmq.restaurant.supplier.delete-restaurant
persistence_targets:
- table.ftgo.restaurant.supplier-profile
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/restaurant/restaurant.py
  symbol: application.routes.restaurant.restaurant.delete_restaurant
  line_start: 93
  line_end: 112
  evidence_type: implemented
relations:
- type: CONTAINS
  target: step.ftgo.gateway.delete.restaurant.delete.consume.restaurant.restaurant.supplier.delete-restaurant
  role: event_consume
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/restaurant/src/events.py
  symbol: events.register_events
  line_start: 32
  line_end: 32
  evidence_type: implemented
- type: CONTAINS
  target: step.ftgo.gateway.delete.restaurant.delete.dispatch.services.restaurant.restaurantservice.delete-restaurant
  role: service_dispatch
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/restaurant/restaurant.py
  symbol: application.routes.restaurant.restaurant.delete_restaurant
  line_start: 97
  line_end: 97
  evidence_type: implemented
- type: CONTAINS
  target: step.ftgo.gateway.delete.restaurant.delete.http-ingress
  role: http_ingress
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/restaurant/restaurant.py
  symbol: application.routes.restaurant.restaurant.delete_restaurant
  line_start: 93
  line_end: 112
  evidence_type: implemented
- type: CONTAINS
  target: step.ftgo.gateway.delete.restaurant.delete.publish.ftgo.rabbitmq.restaurant.supplier.delete-restaurant
  role: event_publish
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/restaurant.py
  symbol: services.restaurant.RestaurantService.delete_restaurant
  line_start: 31
  line_end: 31
  evidence_type: implemented
- type: CONTAINS
  target: step.ftgo.gateway.delete.restaurant.delete.read.ftgo.restaurant.supplier-profile
  role: persistence_read
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/restaurant/src/domain/restaurant.py
  symbol: domain.restaurant.RestaurantDomain.delete_restaurant
  line_start: 153
  line_end: 153
  evidence_type: implemented
inbound_relations:
- type: PARTICIPATES_IN
  source: service.ftgo.gateway
  completeness: resolved
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/restaurant/restaurant.py
  symbol: application.routes.restaurant.restaurant.delete_restaurant
  line_start: 93
  line_end: 112
  evidence_type: implemented
- type: PARTICIPATES_IN
  source: service.ftgo.restaurant
  completeness: resolved
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/restaurant/restaurant.py
  symbol: application.routes.restaurant.restaurant.delete_restaurant
  line_start: 93
  line_end: 112
  evidence_type: implemented
attributes:
  step_count: 5
  classification_reason: endpoint, publish, consume and persistence are all source-backed
  max_call_depth: 3
---

# DELETE /restaurant/delete execution flow

Canonical execution flow stitched from source-backed call evidence in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Entry endpoint: `endpoint.ftgo.gateway.delete.restaurant.delete`
- Completeness: `resolved`
- Handler: `application.routes.restaurant.restaurant.delete_restaurant`
- Declared in: `backend/gateway/src/application/routes/restaurant/restaurant.py` (lines 93-112)
- Evidence class: `implemented`

## Steps

- `http_ingress` `step.ftgo.gateway.delete.restaurant.delete.http-ingress`
- `service_dispatch` `step.ftgo.gateway.delete.restaurant.delete.dispatch.services.restaurant.restaurantservice.delete-restaurant`
- `event_publish` `step.ftgo.gateway.delete.restaurant.delete.publish.ftgo.rabbitmq.restaurant.supplier.delete-restaurant`
- `event_consume` `step.ftgo.gateway.delete.restaurant.delete.consume.restaurant.restaurant.supplier.delete-restaurant`
- `persistence_read` `step.ftgo.gateway.delete.restaurant.delete.read.ftgo.restaurant.supplier-profile`

## Review notes

This approved canonical page records a source-backed execution flow. Every step is backed by a bounded call trace of at most 3 hops; no segment was inferred from similarity between an endpoint path and an event name.

