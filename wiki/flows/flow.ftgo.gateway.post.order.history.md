---
id: flow.ftgo.gateway.post.order.history
kind: UserFlow
type: UserFlow
title: POST /order/history execution flow
status: approved
review_status: approved
candidate_of: user-flow-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: user-flow
owner: aide-ftgo-cohort
entry_endpoint: endpoint.ftgo.gateway.post.order.history
http_method: POST
path: /order/history
path_resolution: partial
completeness: partial
handler: application.routes.order.order.get_order_history
participating_services:
- service.ftgo.gateway
events:
- event.ftgo.rabbitmq.order.history
persistence_targets: []
unresolved_segments:
- consume:order.history
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/order/order.py
  symbol: application.routes.order.order.get_order_history
  line_start: 19
  line_end: 40
  evidence_type: implemented
relations:
- type: CONTAINS
  target: step.ftgo.gateway.post.order.history.dispatch.services.order.orderservice.get-order-history
  role: service_dispatch
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/order/order.py
  symbol: application.routes.order.order.get_order_history
  line_start: 25
  line_end: 25
  evidence_type: implemented
- type: CONTAINS
  target: step.ftgo.gateway.post.order.history.http-ingress
  role: http_ingress
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/order/order.py
  symbol: application.routes.order.order.get_order_history
  line_start: 19
  line_end: 40
  evidence_type: implemented
- type: CONTAINS
  target: step.ftgo.gateway.post.order.history.publish.ftgo.rabbitmq.order.history
  role: event_publish
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/order.py
  symbol: services.order.OrderService.get_order_history
  line_start: 11
  line_end: 11
  evidence_type: implemented
inbound_relations:
- type: PARTICIPATES_IN
  source: service.ftgo.gateway
  completeness: partial
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/order/order.py
  symbol: application.routes.order.order.get_order_history
  line_start: 19
  line_end: 40
  evidence_type: implemented
attributes:
  step_count: 3
  classification_reason: publish is proven but no consumer binding exists for the identity
  max_call_depth: 3
---

# POST /order/history execution flow

Canonical execution flow stitched from source-backed call evidence in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Entry endpoint: `endpoint.ftgo.gateway.post.order.history`
- Completeness: `partial`
- Handler: `application.routes.order.order.get_order_history`
- Declared in: `backend/gateway/src/application/routes/order/order.py` (lines 19-40)
- Evidence class: `implemented`

## Steps

- `http_ingress` `step.ftgo.gateway.post.order.history.http-ingress`
- `service_dispatch` `step.ftgo.gateway.post.order.history.dispatch.services.order.orderservice.get-order-history`
- `event_publish` `step.ftgo.gateway.post.order.history.publish.ftgo.rabbitmq.order.history`

## Unresolved segments

This flow is not complete. The following segments could not be proven from source and are deliberately not invented:

- `consume:order.history`

## Review notes

This approved canonical page records a source-backed execution flow. Every step is backed by a bounded call trace of at most 3 hops; no segment was inferred from similarity between an endpoint path and an event name.

