---
id: step.ftgo.gateway.post.feedback.order.rating.create.consume.feedback.order.rating.create
kind: FlowStep
type: FlowStep
title: feedback consumes order.rating.create
status: candidate
review_status: pending
candidate_of: user-flow-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: user-flow
owner: aide-ftgo-cohort
role: event_consume
flow: flow.ftgo.gateway.post.feedback.order.rating.create
service: service.ftgo.feedback
derived_from: event.ftgo.rabbitmq.order.rating.create
derived_from_kind: Event
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/feedback/src/events.py
  symbol: events.register_events
  line_start: 37
  line_end: 37
  evidence_type: implemented
relations:
- type: DERIVED_FROM
  target: event.ftgo.rabbitmq.order.rating.create
  anchor_kind: Event
  role: event_consume
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/feedback/src/events.py
  symbol: events.register_events
  line_start: 37
  line_end: 37
  evidence_type: implemented
- type: IMPLEMENTS
  target: service.ftgo.feedback
  role: event_consume
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
  role: event_consume
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/feedback/src/events.py
  symbol: events.register_events
  line_start: 37
  line_end: 37
  evidence_type: implemented
- type: PRECEDES
  source: step.ftgo.gateway.post.feedback.order.rating.create.publish.ftgo.rabbitmq.order.rating.create
  established_by: handler registration
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/feedback/src/events.py
  symbol: events.register_events
  line_start: 37
  line_end: 37
  evidence_type: implemented
attributes:
  event_identity: order.rating.create
  handler_expression: OrderRatingService.create_order_rating
  handler_symbol: application.order.OrderRatingService.create_order_rating
  operation: register_event
---

# feedback consumes order.rating.create

Candidate execution step extracted from call evidence in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Role: `event_consume`
- Flow: `flow.ftgo.gateway.post.feedback.order.rating.create`
- Performed by: `service.ftgo.feedback`
- Anchored on: `event.ftgo.rabbitmq.order.rating.create` (`Event`)
- Declared in: `backend/microservices/feedback/src/events.py` (lines 37-37)
- Evidence class: `implemented`

## Review notes

This page is a candidate awaiting review. The step exists because a concrete call site proves it, and its ordering edges carry that call site as evidence.

