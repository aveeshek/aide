---
id: flow.ftgo.gateway.post.restaurant.register
kind: UserFlow
type: UserFlow
title: POST /restaurant/register execution flow
status: approved
review_status: approved
candidate_of: user-flow-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: user-flow
owner: aide-ftgo-cohort
entry_endpoint: endpoint.ftgo.gateway.post.restaurant.register
http_method: POST
path: /restaurant/register
path_resolution: partial
completeness: resolved
handler: application.routes.restaurant.restaurant.register
participating_services:
- service.ftgo.gateway
- service.ftgo.restaurant
events:
- event.ftgo.rabbitmq.restaurant.supplier.register
persistence_targets:
- table.ftgo.restaurant.supplier-profile
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/restaurant/restaurant.py
  symbol: application.routes.restaurant.restaurant.register
  line_start: 22
  line_end: 44
  evidence_type: implemented
relations:
- type: CONTAINS
  target: step.ftgo.gateway.post.restaurant.register.consume.restaurant.restaurant.supplier.register
  role: event_consume
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/restaurant/src/events.py
  symbol: events.register_events
  line_start: 32
  line_end: 32
  evidence_type: implemented
- type: CONTAINS
  target: step.ftgo.gateway.post.restaurant.register.dispatch.services.restaurant.restaurantservice.register
  role: service_dispatch
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/restaurant/restaurant.py
  symbol: application.routes.restaurant.restaurant.register
  line_start: 29
  line_end: 29
  evidence_type: implemented
- type: CONTAINS
  target: step.ftgo.gateway.post.restaurant.register.http-ingress
  role: http_ingress
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/restaurant/restaurant.py
  symbol: application.routes.restaurant.restaurant.register
  line_start: 22
  line_end: 44
  evidence_type: implemented
- type: CONTAINS
  target: step.ftgo.gateway.post.restaurant.register.publish.ftgo.rabbitmq.restaurant.supplier.register
  role: event_publish
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/restaurant.py
  symbol: services.restaurant.RestaurantService.register
  line_start: 11
  line_end: 11
  evidence_type: implemented
- type: CONTAINS
  target: step.ftgo.gateway.post.restaurant.register.read.ftgo.restaurant.supplier-profile
  role: persistence_read
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/restaurant/src/domain/restaurant.py
  symbol: domain.restaurant.RestaurantDomain.register
  line_start: 88
  line_end: 88
  evidence_type: implemented
- type: CONTAINS
  target: step.ftgo.gateway.post.restaurant.register.write.ftgo.restaurant.supplier-profile
  role: persistence_write
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/restaurant/src/domain/restaurant.py
  symbol: domain.restaurant.RestaurantDomain.register
  line_start: 105
  line_end: 105
  evidence_type: implemented
inbound_relations:
- type: PARTICIPATES_IN
  source: service.ftgo.gateway
  completeness: resolved
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/restaurant/restaurant.py
  symbol: application.routes.restaurant.restaurant.register
  line_start: 22
  line_end: 44
  evidence_type: implemented
- type: PARTICIPATES_IN
  source: service.ftgo.restaurant
  completeness: resolved
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/restaurant/restaurant.py
  symbol: application.routes.restaurant.restaurant.register
  line_start: 22
  line_end: 44
  evidence_type: implemented
attributes:
  step_count: 6
  classification_reason: endpoint, publish, consume and persistence are all source-backed
  max_call_depth: 3
---

# POST /restaurant/register execution flow

Canonical execution flow stitched from source-backed call evidence in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Entry endpoint: `endpoint.ftgo.gateway.post.restaurant.register`
- Completeness: `resolved`
- Handler: `application.routes.restaurant.restaurant.register`
- Declared in: `backend/gateway/src/application/routes/restaurant/restaurant.py` (lines 22-44)
- Evidence class: `implemented`

## Steps

- `http_ingress` `step.ftgo.gateway.post.restaurant.register.http-ingress`
- `service_dispatch` `step.ftgo.gateway.post.restaurant.register.dispatch.services.restaurant.restaurantservice.register`
- `event_publish` `step.ftgo.gateway.post.restaurant.register.publish.ftgo.rabbitmq.restaurant.supplier.register`
- `event_consume` `step.ftgo.gateway.post.restaurant.register.consume.restaurant.restaurant.supplier.register`
- `persistence_read` `step.ftgo.gateway.post.restaurant.register.read.ftgo.restaurant.supplier-profile`
- `persistence_write` `step.ftgo.gateway.post.restaurant.register.write.ftgo.restaurant.supplier-profile`

## Review notes

This approved canonical page records a source-backed execution flow. Every step is backed by a bounded call trace of at most 3 hops; no segment was inferred from similarity between an endpoint path and an event name.

