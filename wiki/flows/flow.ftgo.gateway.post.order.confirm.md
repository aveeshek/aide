---
id: flow.ftgo.gateway.post.order.confirm
kind: UserFlow
type: UserFlow
title: POST /order/confirm execution flow
status: approved
review_status: approved
candidate_of: user-flow-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: user-flow
owner: aide-ftgo-cohort
entry_endpoint: endpoint.ftgo.gateway.post.order.confirm
http_method: POST
path: /order/confirm
path_resolution: partial
completeness: resolved
handler: application.routes.order.order.restaurant_confirm
participating_services:
- service.ftgo.gateway
- service.ftgo.order
events:
- event.ftgo.rabbitmq.order.create
persistence_targets:
- collection.ftgo.order.orders
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/order/order.py
  symbol: application.routes.order.order.restaurant_confirm
  line_start: 96
  line_end: 118
  evidence_type: implemented
relations:
- type: CONTAINS
  target: step.ftgo.gateway.post.order.confirm.consume.order.order.create
  role: event_consume
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/order/src/events.py
  symbol: events.register_events
  line_start: 45
  line_end: 45
  evidence_type: implemented
- type: CONTAINS
  target: step.ftgo.gateway.post.order.confirm.dispatch.services.order.orderservice.create-order
  role: service_dispatch
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/order/order.py
  symbol: application.routes.order.order.restaurant_confirm
  line_start: 103
  line_end: 103
  evidence_type: implemented
- type: CONTAINS
  target: step.ftgo.gateway.post.order.confirm.http-ingress
  role: http_ingress
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/order/order.py
  symbol: application.routes.order.order.restaurant_confirm
  line_start: 96
  line_end: 118
  evidence_type: implemented
- type: CONTAINS
  target: step.ftgo.gateway.post.order.confirm.publish.ftgo.rabbitmq.order.create
  role: event_publish
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/order.py
  symbol: services.order.OrderService.create_order
  line_start: 15
  line_end: 15
  evidence_type: implemented
- type: CONTAINS
  target: step.ftgo.gateway.post.order.confirm.write.ftgo.order.orders
  role: persistence_write
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/order/src/domain/entities/order.py
  symbol: domain.entities.order.Order.save
  line_start: 46
  line_end: 46
  evidence_type: implemented
inbound_relations:
- type: PARTICIPATES_IN
  source: service.ftgo.gateway
  completeness: resolved
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/order/order.py
  symbol: application.routes.order.order.restaurant_confirm
  line_start: 96
  line_end: 118
  evidence_type: implemented
- type: PARTICIPATES_IN
  source: service.ftgo.order
  completeness: resolved
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/order/order.py
  symbol: application.routes.order.order.restaurant_confirm
  line_start: 96
  line_end: 118
  evidence_type: implemented
attributes:
  step_count: 5
  classification_reason: endpoint, publish, consume and persistence are all source-backed
  max_call_depth: 3
---

# POST /order/confirm execution flow

Canonical execution flow stitched from source-backed call evidence in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Entry endpoint: `endpoint.ftgo.gateway.post.order.confirm`
- Completeness: `resolved`
- Handler: `application.routes.order.order.restaurant_confirm`
- Declared in: `backend/gateway/src/application/routes/order/order.py` (lines 96-118)
- Evidence class: `implemented`

## Steps

- `http_ingress` `step.ftgo.gateway.post.order.confirm.http-ingress`
- `service_dispatch` `step.ftgo.gateway.post.order.confirm.dispatch.services.order.orderservice.create-order`
- `event_publish` `step.ftgo.gateway.post.order.confirm.publish.ftgo.rabbitmq.order.create`
- `event_consume` `step.ftgo.gateway.post.order.confirm.consume.order.order.create`
- `persistence_write` `step.ftgo.gateway.post.order.confirm.write.ftgo.order.orders`

## Review notes

This approved canonical page records a source-backed execution flow. Every step is backed by a bounded call trace of at most 3 hops; no segment was inferred from similarity between an endpoint path and an event name.



### Source-code observation

At the frozen FTGO commit, this Gateway handler calls `OrderService.create_order(...)`, which publishes `order.create`. Although `OrderService` also defines dedicated update/confirm/reject methods, this endpoint does not invoke them. The Knowledge Plane records the implemented call path without substituting behavior based on endpoint naming.
