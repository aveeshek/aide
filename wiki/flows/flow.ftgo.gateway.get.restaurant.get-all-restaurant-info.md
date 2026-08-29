---
id: flow.ftgo.gateway.get.restaurant.get-all-restaurant-info
kind: UserFlow
type: UserFlow
title: GET /restaurant/get_all_restaurant_info execution flow
status: approved
review_status: approved
candidate_of: user-flow-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: user-flow
owner: aide-ftgo-cohort
entry_endpoint: endpoint.ftgo.gateway.get.restaurant.get-all-restaurant-info
http_method: GET
path: /restaurant/get_all_restaurant_info
path_resolution: partial
completeness: resolved
handler: application.routes.restaurant.restaurant.get_all_restaurant_info
participating_services:
- service.ftgo.gateway
- service.ftgo.restaurant
events:
- event.ftgo.rabbitmq.restaurant.supplier.get-all-restaurant-info
persistence_targets:
- table.ftgo.restaurant.supplier-profile
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/restaurant/restaurant.py
  symbol: application.routes.restaurant.restaurant.get_all_restaurant_info
  line_start: 74
  line_end: 91
  evidence_type: implemented
relations:
- type: CONTAINS
  target: step.ftgo.gateway.get.restaurant.get-all-restaurant-info.consume.restaurant.restaurant.supplier.get-all-restaurant-info
  role: event_consume
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/restaurant/src/events.py
  symbol: events.register_events
  line_start: 32
  line_end: 32
  evidence_type: implemented
- type: CONTAINS
  target: step.ftgo.gateway.get.restaurant.get-all-restaurant-info.dispatch.services.restaurant.restaurantservice.get-all-restaurant-info
  role: service_dispatch
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/restaurant/restaurant.py
  symbol: application.routes.restaurant.restaurant.get_all_restaurant_info
  line_start: 77
  line_end: 77
  evidence_type: implemented
- type: CONTAINS
  target: step.ftgo.gateway.get.restaurant.get-all-restaurant-info.http-ingress
  role: http_ingress
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/restaurant/restaurant.py
  symbol: application.routes.restaurant.restaurant.get_all_restaurant_info
  line_start: 74
  line_end: 91
  evidence_type: implemented
- type: CONTAINS
  target: step.ftgo.gateway.get.restaurant.get-all-restaurant-info.publish.ftgo.rabbitmq.restaurant.supplier.get-all-restaurant-info
  role: event_publish
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/restaurant.py
  symbol: services.restaurant.RestaurantService.get_all_restaurant_info
  line_start: 19
  line_end: 19
  evidence_type: implemented
- type: CONTAINS
  target: step.ftgo.gateway.get.restaurant.get-all-restaurant-info.read.ftgo.restaurant.supplier-profile
  role: persistence_read
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/restaurant/src/domain/restaurant.py
  symbol: domain.restaurant.RestaurantDomain.load_all
  line_start: 69
  line_end: 69
  evidence_type: implemented
inbound_relations:
- type: PARTICIPATES_IN
  source: service.ftgo.gateway
  completeness: resolved
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/restaurant/restaurant.py
  symbol: application.routes.restaurant.restaurant.get_all_restaurant_info
  line_start: 74
  line_end: 91
  evidence_type: implemented
- type: PARTICIPATES_IN
  source: service.ftgo.restaurant
  completeness: resolved
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/restaurant/restaurant.py
  symbol: application.routes.restaurant.restaurant.get_all_restaurant_info
  line_start: 74
  line_end: 91
  evidence_type: implemented
attributes:
  step_count: 5
  classification_reason: endpoint, publish, consume and persistence are all source-backed
  max_call_depth: 3
---

# GET /restaurant/get_all_restaurant_info execution flow

Canonical execution flow stitched from source-backed call evidence in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Entry endpoint: `endpoint.ftgo.gateway.get.restaurant.get-all-restaurant-info`
- Completeness: `resolved`
- Handler: `application.routes.restaurant.restaurant.get_all_restaurant_info`
- Declared in: `backend/gateway/src/application/routes/restaurant/restaurant.py` (lines 74-91)
- Evidence class: `implemented`

## Steps

- `http_ingress` `step.ftgo.gateway.get.restaurant.get-all-restaurant-info.http-ingress`
- `service_dispatch` `step.ftgo.gateway.get.restaurant.get-all-restaurant-info.dispatch.services.restaurant.restaurantservice.get-all-restaurant-info`
- `event_publish` `step.ftgo.gateway.get.restaurant.get-all-restaurant-info.publish.ftgo.rabbitmq.restaurant.supplier.get-all-restaurant-info`
- `event_consume` `step.ftgo.gateway.get.restaurant.get-all-restaurant-info.consume.restaurant.restaurant.supplier.get-all-restaurant-info`
- `persistence_read` `step.ftgo.gateway.get.restaurant.get-all-restaurant-info.read.ftgo.restaurant.supplier-profile`

## Review notes

This approved canonical page records a source-backed execution flow. Every step is backed by a bounded call trace of at most 3 hops; no segment was inferred from similarity between an endpoint path and an event name.

