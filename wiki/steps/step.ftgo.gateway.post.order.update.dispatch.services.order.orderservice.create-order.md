---
id: step.ftgo.gateway.post.order.update.dispatch.services.order.orderservice.create-order
kind: FlowStep
type: FlowStep
title: services.order.OrderService.create_order dispatch
status: approved
review_status: approved
candidate_of: user-flow-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: user-flow
owner: aide-ftgo-cohort
role: service_dispatch
flow: flow.ftgo.gateway.post.order.update
service: service.ftgo.gateway
derived_from: endpoint.ftgo.gateway.post.order.update
derived_from_kind: Endpoint
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/order/order.py
  symbol: application.routes.order.order.update_order
  line_start: 78
  line_end: 78
  evidence_type: implemented
traces:
- target: services.order.OrderService.create_order
  depth: 1
  hops:
  - caller: application.routes.order.order.update_order
    callee: services.order.OrderService.create_order
    call: OrderService.create_order
    repository: ftgo
    commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
    path: backend/gateway/src/application/routes/order/order.py
    symbol: application.routes.order.order.update_order
    line_start: 78
    line_end: 78
    evidence_type: implemented
relations:
- type: DERIVED_FROM
  target: endpoint.ftgo.gateway.post.order.update
  anchor_kind: Endpoint
  role: service_dispatch
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/order/order.py
  symbol: application.routes.order.order.update_order
  line_start: 78
  line_end: 78
  evidence_type: implemented
- type: IMPLEMENTS
  target: service.ftgo.gateway
  role: service_dispatch
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/order/order.py
  symbol: application.routes.order.order.update_order
  line_start: 78
  line_end: 78
  evidence_type: implemented
- type: PRECEDES
  target: step.ftgo.gateway.post.order.update.publish.ftgo.rabbitmq.order.create
  established_by: publisher call site
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/order.py
  symbol: services.order.OrderService.create_order
  line_start: 15
  line_end: 15
  evidence_type: implemented
inbound_relations:
- type: CONTAINS
  source: flow.ftgo.gateway.post.order.update
  role: service_dispatch
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/order/order.py
  symbol: application.routes.order.order.update_order
  line_start: 78
  line_end: 78
  evidence_type: implemented
- type: PRECEDES
  source: step.ftgo.gateway.post.order.update.http-ingress
  established_by: handler call site
  call_depth: 1
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/order/order.py
  symbol: application.routes.order.order.update_order
  line_start: 78
  line_end: 78
  evidence_type: implemented
attributes:
  gateway_symbol: services.order.OrderService.create_order
  call_depth: 1
---

# services.order.OrderService.create_order dispatch

Canonical execution step extracted from call evidence in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Role: `service_dispatch`
- Flow: `flow.ftgo.gateway.post.order.update`
- Performed by: `service.ftgo.gateway`
- Anchored on: `endpoint.ftgo.gateway.post.order.update` (`Endpoint`)
- Declared in: `backend/gateway/src/application/routes/order/order.py` (lines 78-78)
- Evidence class: `implemented`

## Call trace

- `application.routes.order.order.update_order` -> `services.order.OrderService.create_order` (`backend/gateway/src/application/routes/order/order.py:78`)

## Review notes

This approved canonical page records a source-backed execution step. The step exists because a concrete call site proves it, and its ordering edges carry that call site as evidence.

