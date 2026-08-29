---
id: step.ftgo.gateway.put.feedback.delivery.rating.update.consume.feedback.delivery.rating.update
kind: FlowStep
type: FlowStep
title: feedback consumes delivery.rating.update
status: candidate
review_status: pending
candidate_of: user-flow-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: user-flow
owner: aide-ftgo-cohort
role: event_consume
flow: flow.ftgo.gateway.put.feedback.delivery.rating.update
service: service.ftgo.feedback
derived_from: event.ftgo.rabbitmq.delivery.rating.update
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
  target: event.ftgo.rabbitmq.delivery.rating.update
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
  source: flow.ftgo.gateway.put.feedback.delivery.rating.update
  role: event_consume
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/feedback/src/events.py
  symbol: events.register_events
  line_start: 37
  line_end: 37
  evidence_type: implemented
- type: PRECEDES
  source: step.ftgo.gateway.put.feedback.delivery.rating.update.publish.ftgo.rabbitmq.delivery.rating.update
  established_by: handler registration
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/feedback/src/events.py
  symbol: events.register_events
  line_start: 37
  line_end: 37
  evidence_type: implemented
attributes:
  event_identity: delivery.rating.update
  handler_expression: DeliveryRatingService.update_delivery_rating
  handler_symbol: application.delivery.DeliveryRatingService.update_delivery_rating
  operation: register_event
---

# feedback consumes delivery.rating.update

Candidate execution step extracted from call evidence in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Role: `event_consume`
- Flow: `flow.ftgo.gateway.put.feedback.delivery.rating.update`
- Performed by: `service.ftgo.feedback`
- Anchored on: `event.ftgo.rabbitmq.delivery.rating.update` (`Event`)
- Declared in: `backend/microservices/feedback/src/events.py` (lines 37-37)
- Evidence class: `implemented`

## Review notes

This page is a candidate awaiting review. The step exists because a concrete call site proves it, and its ordering edges carry that call site as evidence.

