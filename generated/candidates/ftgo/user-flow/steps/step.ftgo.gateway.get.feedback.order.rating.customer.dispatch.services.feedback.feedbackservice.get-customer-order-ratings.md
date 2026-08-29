---
id: step.ftgo.gateway.get.feedback.order.rating.customer.dispatch.services.feedback.feedbackservice.get-customer-order-ratings
kind: FlowStep
type: FlowStep
title: services.feedback.FeedbackService.get_customer_order_ratings dispatch
status: candidate
review_status: pending
candidate_of: user-flow-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: user-flow
owner: aide-ftgo-cohort
role: service_dispatch
flow: flow.ftgo.gateway.get.feedback.order.rating.customer
service: service.ftgo.gateway
derived_from: endpoint.ftgo.gateway.get.feedback.order.rating.customer
derived_from_kind: Endpoint
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/order/feedback.py
  symbol: application.routes.order.feedback.get_customer_order_ratings
  line_start: 197
  line_end: 197
  evidence_type: implemented
traces:
- target: services.feedback.FeedbackService.get_customer_order_ratings
  depth: 1
  hops:
  - caller: application.routes.order.feedback.get_customer_order_ratings
    callee: services.feedback.FeedbackService.get_customer_order_ratings
    call: FeedbackService.get_customer_order_ratings
    repository: ftgo
    commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
    path: backend/gateway/src/application/routes/order/feedback.py
    symbol: application.routes.order.feedback.get_customer_order_ratings
    line_start: 197
    line_end: 197
    evidence_type: implemented
relations:
- type: DERIVED_FROM
  target: endpoint.ftgo.gateway.get.feedback.order.rating.customer
  anchor_kind: Endpoint
  role: service_dispatch
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/order/feedback.py
  symbol: application.routes.order.feedback.get_customer_order_ratings
  line_start: 197
  line_end: 197
  evidence_type: implemented
- type: IMPLEMENTS
  target: service.ftgo.gateway
  role: service_dispatch
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/order/feedback.py
  symbol: application.routes.order.feedback.get_customer_order_ratings
  line_start: 197
  line_end: 197
  evidence_type: implemented
- type: PRECEDES
  target: step.ftgo.gateway.get.feedback.order.rating.customer.publish.ftgo.rabbitmq.order.rating.get-customer-ratings
  established_by: publisher call site
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/feedback.py
  symbol: services.feedback.FeedbackService.get_customer_order_ratings
  line_start: 45
  line_end: 45
  evidence_type: implemented
inbound_relations:
- type: CONTAINS
  source: flow.ftgo.gateway.get.feedback.order.rating.customer
  role: service_dispatch
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/order/feedback.py
  symbol: application.routes.order.feedback.get_customer_order_ratings
  line_start: 197
  line_end: 197
  evidence_type: implemented
- type: PRECEDES
  source: step.ftgo.gateway.get.feedback.order.rating.customer.http-ingress
  established_by: handler call site
  call_depth: 1
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/order/feedback.py
  symbol: application.routes.order.feedback.get_customer_order_ratings
  line_start: 197
  line_end: 197
  evidence_type: implemented
attributes:
  gateway_symbol: services.feedback.FeedbackService.get_customer_order_ratings
  call_depth: 1
---

# services.feedback.FeedbackService.get_customer_order_ratings dispatch

Candidate execution step extracted from call evidence in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Role: `service_dispatch`
- Flow: `flow.ftgo.gateway.get.feedback.order.rating.customer`
- Performed by: `service.ftgo.gateway`
- Anchored on: `endpoint.ftgo.gateway.get.feedback.order.rating.customer` (`Endpoint`)
- Declared in: `backend/gateway/src/application/routes/order/feedback.py` (lines 197-197)
- Evidence class: `implemented`

## Call trace

- `application.routes.order.feedback.get_customer_order_ratings` -> `services.feedback.FeedbackService.get_customer_order_ratings` (`backend/gateway/src/application/routes/order/feedback.py:197`)

## Review notes

This page is a candidate awaiting review. The step exists because a concrete call site proves it, and its ordering edges carry that call site as evidence.

