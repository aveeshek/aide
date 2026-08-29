---
id: step.ftgo.gateway.post.restaurant.register.dispatch.services.restaurant.restaurantservice.register
kind: FlowStep
type: FlowStep
title: services.restaurant.RestaurantService.register dispatch
status: approved
review_status: approved
candidate_of: user-flow-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: user-flow
owner: aide-ftgo-cohort
role: service_dispatch
flow: flow.ftgo.gateway.post.restaurant.register
service: service.ftgo.gateway
derived_from: endpoint.ftgo.gateway.post.restaurant.register
derived_from_kind: Endpoint
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/restaurant/restaurant.py
  symbol: application.routes.restaurant.restaurant.register
  line_start: 29
  line_end: 29
  evidence_type: implemented
traces:
- target: services.restaurant.RestaurantService.register
  depth: 1
  hops:
  - caller: application.routes.restaurant.restaurant.register
    callee: services.restaurant.RestaurantService.register
    call: RestaurantService.register
    repository: ftgo
    commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
    path: backend/gateway/src/application/routes/restaurant/restaurant.py
    symbol: application.routes.restaurant.restaurant.register
    line_start: 29
    line_end: 29
    evidence_type: implemented
relations:
- type: DERIVED_FROM
  target: endpoint.ftgo.gateway.post.restaurant.register
  anchor_kind: Endpoint
  role: service_dispatch
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/restaurant/restaurant.py
  symbol: application.routes.restaurant.restaurant.register
  line_start: 29
  line_end: 29
  evidence_type: implemented
- type: IMPLEMENTS
  target: service.ftgo.gateway
  role: service_dispatch
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/restaurant/restaurant.py
  symbol: application.routes.restaurant.restaurant.register
  line_start: 29
  line_end: 29
  evidence_type: implemented
- type: PRECEDES
  target: step.ftgo.gateway.post.restaurant.register.publish.ftgo.rabbitmq.restaurant.supplier.register
  established_by: publisher call site
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/restaurant.py
  symbol: services.restaurant.RestaurantService.register
  line_start: 11
  line_end: 11
  evidence_type: implemented
inbound_relations:
- type: CONTAINS
  source: flow.ftgo.gateway.post.restaurant.register
  role: service_dispatch
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/restaurant/restaurant.py
  symbol: application.routes.restaurant.restaurant.register
  line_start: 29
  line_end: 29
  evidence_type: implemented
- type: PRECEDES
  source: step.ftgo.gateway.post.restaurant.register.http-ingress
  established_by: handler call site
  call_depth: 1
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/restaurant/restaurant.py
  symbol: application.routes.restaurant.restaurant.register
  line_start: 29
  line_end: 29
  evidence_type: implemented
attributes:
  gateway_symbol: services.restaurant.RestaurantService.register
  call_depth: 1
---

# services.restaurant.RestaurantService.register dispatch

Canonical execution step extracted from call evidence in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Role: `service_dispatch`
- Flow: `flow.ftgo.gateway.post.restaurant.register`
- Performed by: `service.ftgo.gateway`
- Anchored on: `endpoint.ftgo.gateway.post.restaurant.register` (`Endpoint`)
- Declared in: `backend/gateway/src/application/routes/restaurant/restaurant.py` (lines 29-29)
- Evidence class: `implemented`

## Call trace

- `application.routes.restaurant.restaurant.register` -> `services.restaurant.RestaurantService.register` (`backend/gateway/src/application/routes/restaurant/restaurant.py:29`)

## Review notes

This approved canonical page records a source-backed execution step. The step exists because a concrete call site proves it, and its ordering edges carry that call site as evidence.

