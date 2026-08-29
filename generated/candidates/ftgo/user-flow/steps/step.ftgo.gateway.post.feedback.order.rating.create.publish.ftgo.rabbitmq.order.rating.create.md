---
id: step.ftgo.gateway.post.feedback.order.rating.create.publish.ftgo.rabbitmq.order.rating.create
kind: FlowStep
type: FlowStep
title: publish order.rating.create
status: candidate
review_status: pending
candidate_of: user-flow-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: user-flow
owner: aide-ftgo-cohort
role: event_publish
flow: flow.ftgo.gateway.post.feedback.order.rating.create
service: service.ftgo.gateway
derived_from: event.ftgo.rabbitmq.order.rating.create
derived_from_kind: Event
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/feedback.py
  symbol: services.feedback.FeedbackService.create_order_rating
  line_start: 33
  line_end: 33
  evidence_type: implemented
relations:
- type: DERIVED_FROM
  target: event.ftgo.rabbitmq.order.rating.create
  anchor_kind: Event
  role: event_publish
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/feedback.py
  symbol: services.feedback.FeedbackService.create_order_rating
  line_start: 33
  line_end: 33
  evidence_type: implemented
- type: IMPLEMENTS
  target: service.ftgo.gateway
  role: event_publish
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/feedback.py
  symbol: services.feedback.FeedbackService.create_order_rating
  line_start: 33
  line_end: 33
  evidence_type: implemented
- type: PRECEDES
  target: step.ftgo.gateway.post.feedback.order.rating.create.consume.feedback.order.rating.create
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
  source: flow.ftgo.gateway.post.feedback.order.rating.create
  role: event_publish
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/feedback.py
  symbol: services.feedback.FeedbackService.create_order_rating
  line_start: 33
  line_end: 33
  evidence_type: implemented
- type: PRECEDES
  source: step.ftgo.gateway.post.feedback.order.rating.create.dispatch.services.feedback.feedbackservice.create-order-rating
  established_by: publisher call site
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/feedback.py
  symbol: services.feedback.FeedbackService.create_order_rating
  line_start: 33
  line_end: 33
  evidence_type: implemented
attributes:
  event_identity: order.rating.create
  operation: call
  mechanism: rpc
  broker_library: rabbitmq_rpc
  via_wrapper: services.base.Microservice._call_rpc
  correlation: matched
---

# publish order.rating.create

Candidate execution step extracted from call evidence in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Role: `event_publish`
- Flow: `flow.ftgo.gateway.post.feedback.order.rating.create`
- Performed by: `service.ftgo.gateway`
- Anchored on: `event.ftgo.rabbitmq.order.rating.create` (`Event`)
- Declared in: `backend/gateway/src/services/feedback.py` (lines 33-33)
- Evidence class: `implemented`

## Review notes

This page is a candidate awaiting review. The step exists because a concrete call site proves it, and its ordering edges carry that call site as evidence.

