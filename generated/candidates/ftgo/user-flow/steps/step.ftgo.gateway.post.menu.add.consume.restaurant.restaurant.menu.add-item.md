---
id: step.ftgo.gateway.post.menu.add.consume.restaurant.restaurant.menu.add-item
kind: FlowStep
type: FlowStep
title: restaurant consumes restaurant.menu.add_item
status: candidate
review_status: pending
candidate_of: user-flow-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: user-flow
owner: aide-ftgo-cohort
role: event_consume
flow: flow.ftgo.gateway.post.menu.add
service: service.ftgo.restaurant
derived_from: event.ftgo.rabbitmq.restaurant.menu.add-item
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
  target: event.ftgo.rabbitmq.restaurant.menu.add-item
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
  target: step.ftgo.gateway.post.menu.add.write.ftgo.restaurant.menu-item
  established_by: consumer call trace
  call_depth: 1
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/restaurant/src/domain/menu.py
  symbol: domain.menu.MenuDomain.add_item
  line_start: 50
  line_end: 50
  evidence_type: implemented
inbound_relations:
- type: CONTAINS
  source: flow.ftgo.gateway.post.menu.add
  role: event_consume
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/restaurant/src/events.py
  symbol: events.register_events
  line_start: 32
  line_end: 32
  evidence_type: implemented
- type: PRECEDES
  source: step.ftgo.gateway.post.menu.add.publish.ftgo.rabbitmq.restaurant.menu.add-item
  established_by: handler registration
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/restaurant/src/events.py
  symbol: events.register_events
  line_start: 32
  line_end: 32
  evidence_type: implemented
attributes:
  event_identity: restaurant.menu.add_item
  handler_expression: MenuService.add_item
  handler_symbol: application.menu.MenuService.add_item
  operation: register_event
---

# restaurant consumes restaurant.menu.add_item

Candidate execution step extracted from call evidence in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Role: `event_consume`
- Flow: `flow.ftgo.gateway.post.menu.add`
- Performed by: `service.ftgo.restaurant`
- Anchored on: `event.ftgo.rabbitmq.restaurant.menu.add-item` (`Event`)
- Declared in: `backend/microservices/restaurant/src/events.py` (lines 32-32)
- Evidence class: `implemented`

## Review notes

This page is a candidate awaiting review. The step exists because a concrete call site proves it, and its ordering edges carry that call site as evidence.

