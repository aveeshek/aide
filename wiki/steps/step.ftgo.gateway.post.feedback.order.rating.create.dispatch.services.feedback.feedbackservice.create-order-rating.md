---
id: step.ftgo.gateway.post.feedback.order.rating.create.dispatch.services.feedback.feedbackservice.create-order-rating
kind: FlowStep
type: FlowStep
title: services.feedback.FeedbackService.create_order_rating dispatch
status: approved
review_status: approved
candidate_of: user-flow-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: user-flow
owner: aide-ftgo-cohort
role: service_dispatch
flow: flow.ftgo.gateway.post.feedback.order.rating.create
service: service.ftgo.gateway
derived_from: endpoint.ftgo.gateway.post.feedback.order.rating.create
derived_from_kind: Endpoint
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/order/feedback.py
  symbol: application.routes.order.feedback.create_order_rating
  line_start: 137
  line_end: 137
  evidence_type: implemented
traces:
- target: services.feedback.FeedbackService.create_order_rating
  depth: 1
  hops:
  - caller: application.routes.order.feedback.create_order_rating
    callee: services.feedback.FeedbackService.create_order_rating
    call: FeedbackService.create_order_rating
    repository: ftgo
    commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
    path: backend/gateway/src/application/routes/order/feedback.py
    symbol: application.routes.order.feedback.create_order_rating
    line_start: 137
    line_end: 137
    evidence_type: implemented
relations:
- type: DERIVED_FROM
  target: endpoint.ftgo.gateway.post.feedback.order.rating.create
  anchor_kind: Endpoint
  role: service_dispatch
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/order/feedback.py
  symbol: application.routes.order.feedback.create_order_rating
  line_start: 137
  line_end: 137
  evidence_type: implemented
- type: IMPLEMENTS
  target: service.ftgo.gateway
  role: service_dispatch
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/order/feedback.py
  symbol: application.routes.order.feedback.create_order_rating
  line_start: 137
  line_end: 137
  evidence_type: implemented
- type: PRECEDES
  target: step.ftgo.gateway.post.feedback.order.rating.create.publish.ftgo.rabbitmq.order.rating.create
  established_by: publisher call site
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/feedback.py
  symbol: services.feedback.FeedbackService.create_order_rating
  line_start: 33
  line_end: 33
  evidence_type: implemented
inbound_relations:
- type: CONTAINS
  source: flow.ftgo.gateway.post.feedback.order.rating.create
  role: service_dispatch
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/order/feedback.py
  symbol: application.routes.order.feedback.create_order_rating
  line_start: 137
  line_end: 137
  evidence_type: implemented
- type: PRECEDES
  source: step.ftgo.gateway.post.feedback.order.rating.create.http-ingress
  established_by: handler call site
  call_depth: 1
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/order/feedback.py
  symbol: application.routes.order.feedback.create_order_rating
  line_start: 137
  line_end: 137
  evidence_type: implemented
attributes:
  gateway_symbol: services.feedback.FeedbackService.create_order_rating
  call_depth: 1
---

# services.feedback.FeedbackService.create_order_rating dispatch

Canonical execution step extracted from call evidence in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Role: `service_dispatch`
- Flow: `flow.ftgo.gateway.post.feedback.order.rating.create`
- Performed by: `service.ftgo.gateway`
- Anchored on: `endpoint.ftgo.gateway.post.feedback.order.rating.create` (`Endpoint`)
- Declared in: `backend/gateway/src/application/routes/order/feedback.py` (lines 137-137)
- Evidence class: `implemented`

## Call trace

- `application.routes.order.feedback.create_order_rating` -> `services.feedback.FeedbackService.create_order_rating` (`backend/gateway/src/application/routes/order/feedback.py:137`)

## Review notes

This approved canonical page records a source-backed execution step. The step exists because a concrete call site proves it, and its ordering edges carry that call site as evidence.

