---
id: step.ftgo.gateway.post.restaurant.register.consume.restaurant.restaurant.supplier.register
kind: FlowStep
type: FlowStep
title: restaurant consumes restaurant.supplier.register
status: candidate
review_status: pending
candidate_of: user-flow-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: user-flow
owner: aide-ftgo-cohort
role: event_consume
flow: flow.ftgo.gateway.post.restaurant.register
service: service.ftgo.restaurant
derived_from: event.ftgo.rabbitmq.restaurant.supplier.register
derived_from_kind: Event
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/restaurant/src/events.py
  symbol: events.register_events
  line_start: 32
  line_end: 32
  evidence_type: implemented
relations:
- type: DERIVED_FROM
  target: event.ftgo.rabbitmq.restaurant.supplier.register
  anchor_kind: Event
  role: event_consume
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/restaurant/src/events.py
  symbol: events.register_events
  line_start: 32
  line_end: 32
  evidence_type: implemented
- type: IMPLEMENTS
  target: service.ftgo.restaurant
  role: event_consume
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/restaurant/src/events.py
  symbol: events.register_events
  line_start: 32
  line_end: 32
  evidence_type: implemented
- type: PRECEDES
  target: step.ftgo.gateway.post.restaurant.register.read.ftgo.restaurant.supplier-profile
  established_by: consumer call trace
  call_depth: 1
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/restaurant/src/domain/restaurant.py
  symbol: domain.restaurant.RestaurantDomain.register
  line_start: 88
  line_end: 88
  evidence_type: implemented
- type: PRECEDES
  target: step.ftgo.gateway.post.restaurant.register.write.ftgo.restaurant.supplier-profile
  established_by: consumer call trace
  call_depth: 1
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/restaurant/src/domain/restaurant.py
  symbol: domain.restaurant.RestaurantDomain.register
  line_start: 105
  line_end: 105
  evidence_type: implemented
inbound_relations:
- type: CONTAINS
  source: flow.ftgo.gateway.post.restaurant.register
  role: event_consume
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/restaurant/src/events.py
  symbol: events.register_events
  line_start: 32
  line_end: 32
  evidence_type: implemented
- type: PRECEDES
  source: step.ftgo.gateway.post.restaurant.register.publish.ftgo.rabbitmq.restaurant.supplier.register
  established_by: handler registration
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/restaurant/src/events.py
  symbol: events.register_events
  line_start: 32
  line_end: 32
  evidence_type: implemented
attributes:
  event_identity: restaurant.supplier.register
  handler_expression: RestaurantService.register
  handler_symbol: application.supplier.RestaurantService.register
  operation: register_event
---

# restaurant consumes restaurant.supplier.register

Candidate execution step extracted from call evidence in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Role: `event_consume`
- Flow: `flow.ftgo.gateway.post.restaurant.register`
- Performed by: `service.ftgo.restaurant`
- Anchored on: `event.ftgo.rabbitmq.restaurant.supplier.register` (`Event`)
- Declared in: `backend/microservices/restaurant/src/events.py` (lines 32-32)
- Evidence class: `implemented`

## Review notes

This page is a candidate awaiting review. The step exists because a concrete call site proves it, and its ordering edges carry that call site as evidence.

