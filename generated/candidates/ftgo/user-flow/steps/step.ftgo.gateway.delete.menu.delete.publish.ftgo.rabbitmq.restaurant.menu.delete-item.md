---
id: step.ftgo.gateway.delete.menu.delete.publish.ftgo.rabbitmq.restaurant.menu.delete-item
kind: FlowStep
type: FlowStep
title: publish restaurant.menu.delete_item
status: candidate
review_status: pending
candidate_of: user-flow-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: user-flow
owner: aide-ftgo-cohort
role: event_publish
flow: flow.ftgo.gateway.delete.menu.delete
service: service.ftgo.gateway
derived_from: event.ftgo.rabbitmq.restaurant.menu.delete-item
derived_from_kind: Event
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/menu.py
  symbol: services.menu.MenuService.delete_item
  line_start: 23
  line_end: 23
  evidence_type: implemented
relations:
- type: DERIVED_FROM
  target: event.ftgo.rabbitmq.restaurant.menu.delete-item
  anchor_kind: Event
  role: event_publish
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/menu.py
  symbol: services.menu.MenuService.delete_item
  line_start: 23
  line_end: 23
  evidence_type: implemented
- type: IMPLEMENTS
  target: service.ftgo.gateway
  role: event_publish
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/menu.py
  symbol: services.menu.MenuService.delete_item
  line_start: 23
  line_end: 23
  evidence_type: implemented
- type: PRECEDES
  target: step.ftgo.gateway.delete.menu.delete.consume.restaurant.restaurant.menu.delete-item
  established_by: handler registration
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/restaurant/src/events.py
  symbol: events.register_events
  line_start: 32
  line_end: 32
  evidence_type: implemented
inbound_relations:
- type: CONTAINS
  source: flow.ftgo.gateway.delete.menu.delete
  role: event_publish
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/menu.py
  symbol: services.menu.MenuService.delete_item
  line_start: 23
  line_end: 23
  evidence_type: implemented
- type: PRECEDES
  source: step.ftgo.gateway.delete.menu.delete.dispatch.services.menu.menuservice.delete-item
  established_by: publisher call site
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/menu.py
  symbol: services.menu.MenuService.delete_item
  line_start: 23
  line_end: 23
  evidence_type: implemented
attributes:
  event_identity: restaurant.menu.delete_item
  operation: call
  mechanism: rpc
  broker_library: rabbitmq_rpc
  via_wrapper: services.base.Microservice._call_rpc
  correlation: matched
---

# publish restaurant.menu.delete_item

Candidate execution step extracted from call evidence in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Role: `event_publish`
- Flow: `flow.ftgo.gateway.delete.menu.delete`
- Performed by: `service.ftgo.gateway`
- Anchored on: `event.ftgo.rabbitmq.restaurant.menu.delete-item` (`Event`)
- Declared in: `backend/gateway/src/services/menu.py` (lines 23-23)
- Evidence class: `implemented`

## Review notes

This page is a candidate awaiting review. The step exists because a concrete call site proves it, and its ordering edges carry that call site as evidence.

