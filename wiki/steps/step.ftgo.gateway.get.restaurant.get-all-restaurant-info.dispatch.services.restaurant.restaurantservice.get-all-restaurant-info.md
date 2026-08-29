---
id: step.ftgo.gateway.get.restaurant.get-all-restaurant-info.dispatch.services.restaurant.restaurantservice.get-all-restaurant-info
kind: FlowStep
type: FlowStep
title: services.restaurant.RestaurantService.get_all_restaurant_info dispatch
status: approved
review_status: approved
candidate_of: user-flow-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: user-flow
owner: aide-ftgo-cohort
role: service_dispatch
flow: flow.ftgo.gateway.get.restaurant.get-all-restaurant-info
service: service.ftgo.gateway
derived_from: endpoint.ftgo.gateway.get.restaurant.get-all-restaurant-info
derived_from_kind: Endpoint
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/restaurant/restaurant.py
  symbol: application.routes.restaurant.restaurant.get_all_restaurant_info
  line_start: 77
  line_end: 77
  evidence_type: implemented
traces:
- target: services.restaurant.RestaurantService.get_all_restaurant_info
  depth: 1
  hops:
  - caller: application.routes.restaurant.restaurant.get_all_restaurant_info
    callee: services.restaurant.RestaurantService.get_all_restaurant_info
    call: RestaurantService.get_all_restaurant_info
    repository: ftgo
    commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
    path: backend/gateway/src/application/routes/restaurant/restaurant.py
    symbol: application.routes.restaurant.restaurant.get_all_restaurant_info
    line_start: 77
    line_end: 77
    evidence_type: implemented
relations:
- type: DERIVED_FROM
  target: endpoint.ftgo.gateway.get.restaurant.get-all-restaurant-info
  anchor_kind: Endpoint
  role: service_dispatch
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/restaurant/restaurant.py
  symbol: application.routes.restaurant.restaurant.get_all_restaurant_info
  line_start: 77
  line_end: 77
  evidence_type: implemented
- type: IMPLEMENTS
  target: service.ftgo.gateway
  role: service_dispatch
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/restaurant/restaurant.py
  symbol: application.routes.restaurant.restaurant.get_all_restaurant_info
  line_start: 77
  line_end: 77
  evidence_type: implemented
- type: PRECEDES
  target: step.ftgo.gateway.get.restaurant.get-all-restaurant-info.publish.ftgo.rabbitmq.restaurant.supplier.get-all-restaurant-info
  established_by: publisher call site
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/restaurant.py
  symbol: services.restaurant.RestaurantService.get_all_restaurant_info
  line_start: 19
  line_end: 19
  evidence_type: implemented
inbound_relations:
- type: CONTAINS
  source: flow.ftgo.gateway.get.restaurant.get-all-restaurant-info
  role: service_dispatch
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/restaurant/restaurant.py
  symbol: application.routes.restaurant.restaurant.get_all_restaurant_info
  line_start: 77
  line_end: 77
  evidence_type: implemented
- type: PRECEDES
  source: step.ftgo.gateway.get.restaurant.get-all-restaurant-info.http-ingress
  established_by: handler call site
  call_depth: 1
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/restaurant/restaurant.py
  symbol: application.routes.restaurant.restaurant.get_all_restaurant_info
  line_start: 77
  line_end: 77
  evidence_type: implemented
attributes:
  gateway_symbol: services.restaurant.RestaurantService.get_all_restaurant_info
  call_depth: 1
---

# services.restaurant.RestaurantService.get_all_restaurant_info dispatch

Canonical execution step extracted from call evidence in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Role: `service_dispatch`
- Flow: `flow.ftgo.gateway.get.restaurant.get-all-restaurant-info`
- Performed by: `service.ftgo.gateway`
- Anchored on: `endpoint.ftgo.gateway.get.restaurant.get-all-restaurant-info` (`Endpoint`)
- Declared in: `backend/gateway/src/application/routes/restaurant/restaurant.py` (lines 77-77)
- Evidence class: `implemented`

## Call trace

- `application.routes.restaurant.restaurant.get_all_restaurant_info` -> `services.restaurant.RestaurantService.get_all_restaurant_info` (`backend/gateway/src/application/routes/restaurant/restaurant.py:77`)

## Review notes

This approved canonical page records a source-backed execution step. The step exists because a concrete call site proves it, and its ordering edges carry that call site as evidence.

