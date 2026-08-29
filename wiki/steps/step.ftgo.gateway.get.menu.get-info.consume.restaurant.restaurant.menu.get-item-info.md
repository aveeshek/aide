---
id: step.ftgo.gateway.get.menu.get-info.consume.restaurant.restaurant.menu.get-item-info
kind: FlowStep
type: FlowStep
title: restaurant consumes restaurant.menu.get_item_info
status: approved
review_status: approved
candidate_of: user-flow-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: user-flow
owner: aide-ftgo-cohort
role: event_consume
flow: flow.ftgo.gateway.get.menu.get-info
service: service.ftgo.restaurant
derived_from: event.ftgo.rabbitmq.restaurant.menu.get-item-info
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
  target: event.ftgo.rabbitmq.restaurant.menu.get-item-info
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
  target: step.ftgo.gateway.get.menu.get-info.read.ftgo.restaurant.menu-item
  established_by: consumer call trace
  call_depth: 1
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/restaurant/src/domain/menu.py
  symbol: domain.menu.MenuDomain.load
  line_start: 67
  line_end: 67
  evidence_type: implemented
inbound_relations:
- type: CONTAINS
  source: flow.ftgo.gateway.get.menu.get-info
  role: event_consume
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/restaurant/src/events.py
  symbol: events.register_events
  line_start: 32
  line_end: 32
  evidence_type: implemented
- type: PRECEDES
  source: step.ftgo.gateway.get.menu.get-info.publish.ftgo.rabbitmq.restaurant.menu.get-item-info
  established_by: handler registration
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/restaurant/src/events.py
  symbol: events.register_events
  line_start: 32
  line_end: 32
  evidence_type: implemented
attributes:
  event_identity: restaurant.menu.get_item_info
  handler_expression: MenuService.get_item_info
  handler_symbol: application.menu.MenuService.get_item_info
  operation: register_event
---

# restaurant consumes restaurant.menu.get_item_info

Canonical execution step extracted from call evidence in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Role: `event_consume`
- Flow: `flow.ftgo.gateway.get.menu.get-info`
- Performed by: `service.ftgo.restaurant`
- Anchored on: `event.ftgo.rabbitmq.restaurant.menu.get-item-info` (`Event`)
- Declared in: `backend/microservices/restaurant/src/events.py` (lines 32-32)
- Evidence class: `implemented`

## Review notes

This approved canonical page records a source-backed execution step. The step exists because a concrete call site proves it, and its ordering edges carry that call site as evidence.

