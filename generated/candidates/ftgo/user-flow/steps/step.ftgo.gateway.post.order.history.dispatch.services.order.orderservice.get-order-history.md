---
id: step.ftgo.gateway.post.order.history.dispatch.services.order.orderservice.get-order-history
kind: FlowStep
type: FlowStep
title: services.order.OrderService.get_order_history dispatch
status: candidate
review_status: pending
candidate_of: user-flow-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: user-flow
owner: aide-ftgo-cohort
role: service_dispatch
flow: flow.ftgo.gateway.post.order.history
service: service.ftgo.gateway
derived_from: endpoint.ftgo.gateway.post.order.history
derived_from_kind: Endpoint
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/order/order.py
  symbol: application.routes.order.order.get_order_history
  line_start: 25
  line_end: 25
  evidence_type: implemented
traces:
- target: services.order.OrderService.get_order_history
  depth: 1
  hops:
  - caller: application.routes.order.order.get_order_history
    callee: services.order.OrderService.get_order_history
    call: OrderService.get_order_history
    repository: ftgo
    commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
    path: backend/gateway/src/application/routes/order/order.py
    symbol: application.routes.order.order.get_order_history
    line_start: 25
    line_end: 25
    evidence_type: implemented
relations:
- type: DERIVED_FROM
  target: endpoint.ftgo.gateway.post.order.history
  anchor_kind: Endpoint
  role: service_dispatch
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/order/order.py
  symbol: application.routes.order.order.get_order_history
  line_start: 25
  line_end: 25
  evidence_type: implemented
- type: IMPLEMENTS
  target: service.ftgo.gateway
  role: service_dispatch
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/order/order.py
  symbol: application.routes.order.order.get_order_history
  line_start: 25
  line_end: 25
  evidence_type: implemented
- type: PRECEDES
  target: step.ftgo.gateway.post.order.history.publish.ftgo.rabbitmq.order.history
  established_by: publisher call site
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/order.py
  symbol: services.order.OrderService.get_order_history
  line_start: 11
  line_end: 11
  evidence_type: implemented
inbound_relations:
- type: CONTAINS
  source: flow.ftgo.gateway.post.order.history
  role: service_dispatch
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/order/order.py
  symbol: application.routes.order.order.get_order_history
  line_start: 25
  line_end: 25
  evidence_type: implemented
- type: PRECEDES
  source: step.ftgo.gateway.post.order.history.http-ingress
  established_by: handler call site
  call_depth: 1
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/order/order.py
  symbol: application.routes.order.order.get_order_history
  line_start: 25
  line_end: 25
  evidence_type: implemented
attributes:
  gateway_symbol: services.order.OrderService.get_order_history
  call_depth: 1
---

# services.order.OrderService.get_order_history dispatch

Candidate execution step extracted from call evidence in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Role: `service_dispatch`
- Flow: `flow.ftgo.gateway.post.order.history`
- Performed by: `service.ftgo.gateway`
- Anchored on: `endpoint.ftgo.gateway.post.order.history` (`Endpoint`)
- Declared in: `backend/gateway/src/application/routes/order/order.py` (lines 25-25)
- Evidence class: `implemented`

## Call trace

- `application.routes.order.order.get_order_history` -> `services.order.OrderService.get_order_history` (`backend/gateway/src/application/routes/order/order.py:25`)

## Review notes

This page is a candidate awaiting review. The step exists because a concrete call site proves it, and its ordering edges carry that call site as evidence.

