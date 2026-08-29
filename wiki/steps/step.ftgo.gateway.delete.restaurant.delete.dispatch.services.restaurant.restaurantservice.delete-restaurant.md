---
id: step.ftgo.gateway.delete.restaurant.delete.dispatch.services.restaurant.restaurantservice.delete-restaurant
kind: FlowStep
type: FlowStep
title: services.restaurant.RestaurantService.delete_restaurant dispatch
status: approved
review_status: approved
candidate_of: user-flow-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: user-flow
owner: aide-ftgo-cohort
role: service_dispatch
flow: flow.ftgo.gateway.delete.restaurant.delete
service: service.ftgo.gateway
derived_from: endpoint.ftgo.gateway.delete.restaurant.delete
derived_from_kind: Endpoint
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/restaurant/restaurant.py
  symbol: application.routes.restaurant.restaurant.delete_restaurant
  line_start: 97
  line_end: 97
  evidence_type: implemented
traces:
- target: services.restaurant.RestaurantService.delete_restaurant
  depth: 1
  hops:
  - caller: application.routes.restaurant.restaurant.delete_restaurant
    callee: services.restaurant.RestaurantService.delete_restaurant
    call: RestaurantService.delete_restaurant
    repository: ftgo
    commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
    path: backend/gateway/src/application/routes/restaurant/restaurant.py
    symbol: application.routes.restaurant.restaurant.delete_restaurant
    line_start: 97
    line_end: 97
    evidence_type: implemented
relations:
- type: DERIVED_FROM
  target: endpoint.ftgo.gateway.delete.restaurant.delete
  anchor_kind: Endpoint
  role: service_dispatch
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/restaurant/restaurant.py
  symbol: application.routes.restaurant.restaurant.delete_restaurant
  line_start: 97
  line_end: 97
  evidence_type: implemented
- type: IMPLEMENTS
  target: service.ftgo.gateway
  role: service_dispatch
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/restaurant/restaurant.py
  symbol: application.routes.restaurant.restaurant.delete_restaurant
  line_start: 97
  line_end: 97
  evidence_type: implemented
- type: PRECEDES
  target: step.ftgo.gateway.delete.restaurant.delete.publish.ftgo.rabbitmq.restaurant.supplier.delete-restaurant
  established_by: publisher call site
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/restaurant.py
  symbol: services.restaurant.RestaurantService.delete_restaurant
  line_start: 31
  line_end: 31
  evidence_type: implemented
inbound_relations:
- type: CONTAINS
  source: flow.ftgo.gateway.delete.restaurant.delete
  role: service_dispatch
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/restaurant/restaurant.py
  symbol: application.routes.restaurant.restaurant.delete_restaurant
  line_start: 97
  line_end: 97
  evidence_type: implemented
- type: PRECEDES
  source: step.ftgo.gateway.delete.restaurant.delete.http-ingress
  established_by: handler call site
  call_depth: 1
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/restaurant/restaurant.py
  symbol: application.routes.restaurant.restaurant.delete_restaurant
  line_start: 97
  line_end: 97
  evidence_type: implemented
attributes:
  gateway_symbol: services.restaurant.RestaurantService.delete_restaurant
  call_depth: 1
---

# services.restaurant.RestaurantService.delete_restaurant dispatch

Canonical execution step extracted from call evidence in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Role: `service_dispatch`
- Flow: `flow.ftgo.gateway.delete.restaurant.delete`
- Performed by: `service.ftgo.gateway`
- Anchored on: `endpoint.ftgo.gateway.delete.restaurant.delete` (`Endpoint`)
- Declared in: `backend/gateway/src/application/routes/restaurant/restaurant.py` (lines 97-97)
- Evidence class: `implemented`

## Call trace

- `application.routes.restaurant.restaurant.delete_restaurant` -> `services.restaurant.RestaurantService.delete_restaurant` (`backend/gateway/src/application/routes/restaurant/restaurant.py:97`)

## Review notes

This approved canonical page records a source-backed execution step. The step exists because a concrete call site proves it, and its ordering edges carry that call site as evidence.

