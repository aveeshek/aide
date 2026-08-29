---
id: step.ftgo.gateway.get.feedback.delivery.rating.driver.consume.feedback.delivery.rating.get-driver-ratings
kind: FlowStep
type: FlowStep
title: feedback consumes delivery.rating.get_driver_ratings
status: candidate
review_status: pending
candidate_of: user-flow-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: user-flow
owner: aide-ftgo-cohort
role: event_consume
flow: flow.ftgo.gateway.get.feedback.delivery.rating.driver
service: service.ftgo.feedback
derived_from: event.ftgo.rabbitmq.delivery.rating.get-driver-ratings
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
  target: event.ftgo.rabbitmq.delivery.rating.get-driver-ratings
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
- type: PRECEDES
  target: step.ftgo.gateway.get.feedback.delivery.rating.driver.read.ftgo.feedback.delivery-ratings
  established_by: consumer call trace
  call_depth: 1
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/feedback/src/domain/delivery_rating.py
  symbol: domain.delivery_rating.DeliveryRatingHandler.get_driver_delivery_ratings
  line_start: 61
  line_end: 61
  evidence_type: implemented
inbound_relations:
- type: CONTAINS
  source: flow.ftgo.gateway.get.feedback.delivery.rating.driver
  role: event_consume
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/feedback/src/events.py
  symbol: events.register_events
  line_start: 37
  line_end: 37
  evidence_type: implemented
- type: PRECEDES
  source: step.ftgo.gateway.get.feedback.delivery.rating.driver.publish.ftgo.rabbitmq.delivery.rating.get-driver-ratings
  established_by: handler registration
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/feedback/src/events.py
  symbol: events.register_events
  line_start: 37
  line_end: 37
  evidence_type: implemented
attributes:
  event_identity: delivery.rating.get_driver_ratings
  handler_expression: DeliveryRatingService.get_driver_delivery_ratings
  handler_symbol: application.delivery.DeliveryRatingService.get_driver_delivery_ratings
  operation: register_event
---

# feedback consumes delivery.rating.get_driver_ratings

Candidate execution step extracted from call evidence in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Role: `event_consume`
- Flow: `flow.ftgo.gateway.get.feedback.delivery.rating.driver`
- Performed by: `service.ftgo.feedback`
- Anchored on: `event.ftgo.rabbitmq.delivery.rating.get-driver-ratings` (`Event`)
- Declared in: `backend/microservices/feedback/src/events.py` (lines 37-37)
- Evidence class: `implemented`

## Review notes

This page is a candidate awaiting review. The step exists because a concrete call site proves it, and its ordering edges carry that call site as evidence.

