---
id: step.ftgo.gateway.get.feedback.order.rating.customer.publish.ftgo.rabbitmq.order.rating.get-customer-ratings
kind: FlowStep
type: FlowStep
title: publish order.rating.get_customer_ratings
status: approved
review_status: approved
candidate_of: user-flow-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: user-flow
owner: aide-ftgo-cohort
role: event_publish
flow: flow.ftgo.gateway.get.feedback.order.rating.customer
service: service.ftgo.gateway
derived_from: event.ftgo.rabbitmq.order.rating.get-customer-ratings
derived_from_kind: Event
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/feedback.py
  symbol: services.feedback.FeedbackService.get_customer_order_ratings
  line_start: 45
  line_end: 45
  evidence_type: implemented
relations:
- type: DERIVED_FROM
  target: event.ftgo.rabbitmq.order.rating.get-customer-ratings
  anchor_kind: Event
  role: event_publish
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/feedback.py
  symbol: services.feedback.FeedbackService.get_customer_order_ratings
  line_start: 45
  line_end: 45
  evidence_type: implemented
- type: IMPLEMENTS
  target: service.ftgo.gateway
  role: event_publish
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/feedback.py
  symbol: services.feedback.FeedbackService.get_customer_order_ratings
  line_start: 45
  line_end: 45
  evidence_type: implemented
- type: PRECEDES
  target: step.ftgo.gateway.get.feedback.order.rating.customer.consume.feedback.order.rating.get-customer-ratings
  established_by: handler registration
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/feedback/src/events.py
  symbol: events.register_events
  line_start: 37
  line_end: 37
  evidence_type: implemented
inbound_relations:
- type: CONTAINS
  source: flow.ftgo.gateway.get.feedback.order.rating.customer
  role: event_publish
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/feedback.py
  symbol: services.feedback.FeedbackService.get_customer_order_ratings
  line_start: 45
  line_end: 45
  evidence_type: implemented
- type: PRECEDES
  source: step.ftgo.gateway.get.feedback.order.rating.customer.dispatch.services.feedback.feedbackservice.get-customer-order-ratings
  established_by: publisher call site
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/feedback.py
  symbol: services.feedback.FeedbackService.get_customer_order_ratings
  line_start: 45
  line_end: 45
  evidence_type: implemented
attributes:
  event_identity: order.rating.get_customer_ratings
  operation: call
  mechanism: rpc
  broker_library: rabbitmq_rpc
  via_wrapper: services.base.Microservice._call_rpc
  correlation: matched
---

# publish order.rating.get_customer_ratings

Canonical execution step extracted from call evidence in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Role: `event_publish`
- Flow: `flow.ftgo.gateway.get.feedback.order.rating.customer`
- Performed by: `service.ftgo.gateway`
- Anchored on: `event.ftgo.rabbitmq.order.rating.get-customer-ratings` (`Event`)
- Declared in: `backend/gateway/src/services/feedback.py` (lines 45-45)
- Evidence class: `implemented`

## Review notes

This approved canonical page records a source-backed execution step. The step exists because a concrete call site proves it, and its ordering edges carry that call site as evidence.

