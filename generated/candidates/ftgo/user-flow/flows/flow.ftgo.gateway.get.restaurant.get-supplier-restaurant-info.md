---
id: flow.ftgo.gateway.get.restaurant.get-supplier-restaurant-info
kind: UserFlow
type: UserFlow
title: GET /restaurant/get_supplier_restaurant_info execution flow
status: candidate
review_status: pending
candidate_of: user-flow-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: user-flow
owner: aide-ftgo-cohort
entry_endpoint: endpoint.ftgo.gateway.get.restaurant.get-supplier-restaurant-info
http_method: GET
path: /restaurant/get_supplier_restaurant_info
path_resolution: partial
completeness: resolved
handler: application.routes.restaurant.restaurant.get_supplier_restaurant_info
participating_services:
- service.ftgo.gateway
- service.ftgo.restaurant
events:
- event.ftgo.rabbitmq.restaurant.supplier.get-supplier-restaurant-info
persistence_targets:
- table.ftgo.restaurant.supplier-profile
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/restaurant/restaurant.py
  symbol: application.routes.restaurant.restaurant.get_supplier_restaurant_info
  line_start: 46
  line_end: 71
  evidence_type: implemented
relations:
- type: CONTAINS
  target: step.ftgo.gateway.get.restaurant.get-supplier-restaurant-info.consume.restaurant.restaurant.supplier.get-supplier-restaurant-info
  role: event_consume
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/restaurant/src/events.py
  symbol: events.register_events
  line_start: 32
  line_end: 32
  evidence_type: implemented
- type: CONTAINS
  target: step.ftgo.gateway.get.restaurant.get-supplier-restaurant-info.dispatch.services.restaurant.restaurantservice.get-supplier-restaurant-info
  role: service_dispatch
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/restaurant/restaurant.py
  symbol: application.routes.restaurant.restaurant.get_supplier_restaurant_info
  line_start: 51
  line_end: 51
  evidence_type: implemented
- type: CONTAINS
  target: step.ftgo.gateway.get.restaurant.get-supplier-restaurant-info.http-ingress
  role: http_ingress
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/restaurant/restaurant.py
  symbol: application.routes.restaurant.restaurant.get_supplier_restaurant_info
  line_start: 46
  line_end: 71
  evidence_type: implemented
- type: CONTAINS
  target: step.ftgo.gateway.get.restaurant.get-supplier-restaurant-info.publish.ftgo.rabbitmq.restaurant.supplier.get-supplier-restaurant-info
  role: event_publish
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/restaurant.py
  symbol: services.restaurant.RestaurantService.get_supplier_restaurant_info
  line_start: 23
  line_end: 23
  evidence_type: implemented
- type: CONTAINS
  target: step.ftgo.gateway.get.restaurant.get-supplier-restaurant-info.read.ftgo.restaurant.supplier-profile
  role: persistence_read
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/restaurant/src/domain/restaurant.py
  symbol: domain.restaurant.RestaurantDomain.load
  line_start: 53
  line_end: 53
  evidence_type: implemented
inbound_relations:
- type: PARTICIPATES_IN
  source: service.ftgo.gateway
  completeness: resolved
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/restaurant/restaurant.py
  symbol: application.routes.restaurant.restaurant.get_supplier_restaurant_info
  line_start: 46
  line_end: 71
  evidence_type: implemented
- type: PARTICIPATES_IN
  source: service.ftgo.restaurant
  completeness: resolved
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/restaurant/restaurant.py
  symbol: application.routes.restaurant.restaurant.get_supplier_restaurant_info
  line_start: 46
  line_end: 71
  evidence_type: implemented
attributes:
  step_count: 5
  classification_reason: endpoint, publish, consume and persistence are all source-backed
  max_call_depth: 3
---

# GET /restaurant/get_supplier_restaurant_info execution flow

Candidate execution flow stitched from source-backed call evidence in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Entry endpoint: `endpoint.ftgo.gateway.get.restaurant.get-supplier-restaurant-info`
- Completeness: `resolved`
- Handler: `application.routes.restaurant.restaurant.get_supplier_restaurant_info`
- Declared in: `backend/gateway/src/application/routes/restaurant/restaurant.py` (lines 46-71)
- Evidence class: `implemented`

## Steps

- `http_ingress` `step.ftgo.gateway.get.restaurant.get-supplier-restaurant-info.http-ingress`
- `service_dispatch` `step.ftgo.gateway.get.restaurant.get-supplier-restaurant-info.dispatch.services.restaurant.restaurantservice.get-supplier-restaurant-info`
- `event_publish` `step.ftgo.gateway.get.restaurant.get-supplier-restaurant-info.publish.ftgo.rabbitmq.restaurant.supplier.get-supplier-restaurant-info`
- `event_consume` `step.ftgo.gateway.get.restaurant.get-supplier-restaurant-info.consume.restaurant.restaurant.supplier.get-supplier-restaurant-info`
- `persistence_read` `step.ftgo.gateway.get.restaurant.get-supplier-restaurant-info.read.ftgo.restaurant.supplier-profile`

## Review notes

This page is a candidate awaiting review. Every step is backed by a bounded call trace of at most 3 hops; no segment was inferred from the similarity between an endpoint path and an event name.

