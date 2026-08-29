---
id: step.ftgo.gateway.put.restaurant.update.dispatch.services.restaurant.restaurantservice.update-information
kind: FlowStep
type: FlowStep
title: services.restaurant.RestaurantService.update_information dispatch
status: approved
review_status: approved
candidate_of: user-flow-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: user-flow
owner: aide-ftgo-cohort
role: service_dispatch
flow: flow.ftgo.gateway.put.restaurant.update
service: service.ftgo.gateway
derived_from: endpoint.ftgo.gateway.put.restaurant.update
derived_from_kind: Endpoint
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/restaurant/restaurant.py
  symbol: application.routes.restaurant.restaurant.update_information
  line_start: 119
  line_end: 119
  evidence_type: implemented
traces:
- target: services.restaurant.RestaurantService.update_information
  depth: 1
  hops:
  - caller: application.routes.restaurant.restaurant.update_information
    callee: services.restaurant.RestaurantService.update_information
    call: RestaurantService.update_information
    repository: ftgo
    commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
    path: backend/gateway/src/application/routes/restaurant/restaurant.py
    symbol: application.routes.restaurant.restaurant.update_information
    line_start: 119
    line_end: 119
    evidence_type: implemented
relations:
- type: DERIVED_FROM
  target: endpoint.ftgo.gateway.put.restaurant.update
  anchor_kind: Endpoint
  role: service_dispatch
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/restaurant/restaurant.py
  symbol: application.routes.restaurant.restaurant.update_information
  line_start: 119
  line_end: 119
  evidence_type: implemented
- type: IMPLEMENTS
  target: service.ftgo.gateway
  role: service_dispatch
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/restaurant/restaurant.py
  symbol: application.routes.restaurant.restaurant.update_information
  line_start: 119
  line_end: 119
  evidence_type: implemented
- type: PRECEDES
  target: step.ftgo.gateway.put.restaurant.update.publish.ftgo.rabbitmq.restaurant.supplier.update-information
  established_by: publisher call site
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/restaurant.py
  symbol: services.restaurant.RestaurantService.update_information
  line_start: 27
  line_end: 27
  evidence_type: implemented
inbound_relations:
- type: CONTAINS
  source: flow.ftgo.gateway.put.restaurant.update
  role: service_dispatch
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/restaurant/restaurant.py
  symbol: application.routes.restaurant.restaurant.update_information
  line_start: 119
  line_end: 119
  evidence_type: implemented
- type: PRECEDES
  source: step.ftgo.gateway.put.restaurant.update.http-ingress
  established_by: handler call site
  call_depth: 1
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/restaurant/restaurant.py
  symbol: application.routes.restaurant.restaurant.update_information
  line_start: 119
  line_end: 119
  evidence_type: implemented
attributes:
  gateway_symbol: services.restaurant.RestaurantService.update_information
  call_depth: 1
---

# services.restaurant.RestaurantService.update_information dispatch

Canonical execution step extracted from call evidence in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Role: `service_dispatch`
- Flow: `flow.ftgo.gateway.put.restaurant.update`
- Performed by: `service.ftgo.gateway`
- Anchored on: `endpoint.ftgo.gateway.put.restaurant.update` (`Endpoint`)
- Declared in: `backend/gateway/src/application/routes/restaurant/restaurant.py` (lines 119-119)
- Evidence class: `implemented`

## Call trace

- `application.routes.restaurant.restaurant.update_information` -> `services.restaurant.RestaurantService.update_information` (`backend/gateway/src/application/routes/restaurant/restaurant.py:119`)

## Review notes

This approved canonical page records a source-backed execution step. The step exists because a concrete call site proves it, and its ordering edges carry that call site as evidence.

