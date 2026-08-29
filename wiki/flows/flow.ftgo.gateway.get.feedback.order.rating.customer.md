---
id: flow.ftgo.gateway.get.feedback.order.rating.customer
kind: UserFlow
type: UserFlow
title: GET /feedback/order/rating/customer execution flow
status: approved
review_status: approved
candidate_of: user-flow-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: user-flow
owner: aide-ftgo-cohort
entry_endpoint: endpoint.ftgo.gateway.get.feedback.order.rating.customer
http_method: GET
path: /feedback/order/rating/customer
path_resolution: partial
completeness: resolved
handler: application.routes.order.feedback.get_customer_order_ratings
participating_services:
- service.ftgo.feedback
- service.ftgo.gateway
events:
- event.ftgo.rabbitmq.order.rating.get-customer-ratings
persistence_targets:
- collection.ftgo.feedback.order-ratings
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/order/feedback.py
  symbol: application.routes.order.feedback.get_customer_order_ratings
  line_start: 191
  line_end: 209
  evidence_type: implemented
relations:
- type: CONTAINS
  target: step.ftgo.gateway.get.feedback.order.rating.customer.consume.feedback.order.rating.get-customer-ratings
  role: event_consume
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/feedback/src/events.py
  symbol: events.register_events
  line_start: 37
  line_end: 37
  evidence_type: implemented
- type: CONTAINS
  target: step.ftgo.gateway.get.feedback.order.rating.customer.dispatch.services.feedback.feedbackservice.get-customer-order-ratings
  role: service_dispatch
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/order/feedback.py
  symbol: application.routes.order.feedback.get_customer_order_ratings
  line_start: 197
  line_end: 197
  evidence_type: implemented
- type: CONTAINS
  target: step.ftgo.gateway.get.feedback.order.rating.customer.http-ingress
  role: http_ingress
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/order/feedback.py
  symbol: application.routes.order.feedback.get_customer_order_ratings
  line_start: 191
  line_end: 209
  evidence_type: implemented
- type: CONTAINS
  target: step.ftgo.gateway.get.feedback.order.rating.customer.publish.ftgo.rabbitmq.order.rating.get-customer-ratings
  role: event_publish
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/feedback.py
  symbol: services.feedback.FeedbackService.get_customer_order_ratings
  line_start: 45
  line_end: 45
  evidence_type: implemented
- type: CONTAINS
  target: step.ftgo.gateway.get.feedback.order.rating.customer.read.ftgo.feedback.order-ratings
  role: persistence_read
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/feedback/src/domain/order_rating.py
  symbol: domain.order_rating.OrderRatingHandler.get_customer_order_ratings
  line_start: 57
  line_end: 57
  evidence_type: implemented
inbound_relations:
- type: PARTICIPATES_IN
  source: service.ftgo.feedback
  completeness: resolved
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/order/feedback.py
  symbol: application.routes.order.feedback.get_customer_order_ratings
  line_start: 191
  line_end: 209
  evidence_type: implemented
- type: PARTICIPATES_IN
  source: service.ftgo.gateway
  completeness: resolved
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/order/feedback.py
  symbol: application.routes.order.feedback.get_customer_order_ratings
  line_start: 191
  line_end: 209
  evidence_type: implemented
attributes:
  step_count: 5
  classification_reason: endpoint, publish, consume and persistence are all source-backed
  max_call_depth: 3
---

# GET /feedback/order/rating/customer execution flow

Canonical execution flow stitched from source-backed call evidence in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Entry endpoint: `endpoint.ftgo.gateway.get.feedback.order.rating.customer`
- Completeness: `resolved`
- Handler: `application.routes.order.feedback.get_customer_order_ratings`
- Declared in: `backend/gateway/src/application/routes/order/feedback.py` (lines 191-209)
- Evidence class: `implemented`

## Steps

- `http_ingress` `step.ftgo.gateway.get.feedback.order.rating.customer.http-ingress`
- `service_dispatch` `step.ftgo.gateway.get.feedback.order.rating.customer.dispatch.services.feedback.feedbackservice.get-customer-order-ratings`
- `event_publish` `step.ftgo.gateway.get.feedback.order.rating.customer.publish.ftgo.rabbitmq.order.rating.get-customer-ratings`
- `event_consume` `step.ftgo.gateway.get.feedback.order.rating.customer.consume.feedback.order.rating.get-customer-ratings`
- `persistence_read` `step.ftgo.gateway.get.feedback.order.rating.customer.read.ftgo.feedback.order-ratings`

## Review notes

This approved canonical page records a source-backed execution flow. Every step is backed by a bounded call trace of at most 3 hops; no segment was inferred from similarity between an endpoint path and an event name.

