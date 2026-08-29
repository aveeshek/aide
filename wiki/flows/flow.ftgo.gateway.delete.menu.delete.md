---
id: flow.ftgo.gateway.delete.menu.delete
kind: UserFlow
type: UserFlow
title: DELETE /menu/delete execution flow
status: approved
review_status: approved
candidate_of: user-flow-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: user-flow
owner: aide-ftgo-cohort
entry_endpoint: endpoint.ftgo.gateway.delete.menu.delete
http_method: DELETE
path: /menu/delete
path_resolution: partial
completeness: resolved
handler: application.routes.restaurant.menu.delete_item
participating_services:
- service.ftgo.gateway
- service.ftgo.restaurant
events:
- event.ftgo.rabbitmq.restaurant.menu.delete-item
persistence_targets:
- table.ftgo.restaurant.menu-item
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/restaurant/menu.py
  symbol: application.routes.restaurant.menu.delete_item
  line_start: 88
  line_end: 107
  evidence_type: implemented
relations:
- type: CONTAINS
  target: step.ftgo.gateway.delete.menu.delete.consume.restaurant.restaurant.menu.delete-item
  role: event_consume
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/restaurant/src/events.py
  symbol: events.register_events
  line_start: 32
  line_end: 32
  evidence_type: implemented
- type: CONTAINS
  target: step.ftgo.gateway.delete.menu.delete.dispatch.services.menu.menuservice.delete-item
  role: service_dispatch
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/restaurant/menu.py
  symbol: application.routes.restaurant.menu.delete_item
  line_start: 92
  line_end: 92
  evidence_type: implemented
- type: CONTAINS
  target: step.ftgo.gateway.delete.menu.delete.http-ingress
  role: http_ingress
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/restaurant/menu.py
  symbol: application.routes.restaurant.menu.delete_item
  line_start: 88
  line_end: 107
  evidence_type: implemented
- type: CONTAINS
  target: step.ftgo.gateway.delete.menu.delete.publish.ftgo.rabbitmq.restaurant.menu.delete-item
  role: event_publish
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/menu.py
  symbol: services.menu.MenuService.delete_item
  line_start: 23
  line_end: 23
  evidence_type: implemented
- type: CONTAINS
  target: step.ftgo.gateway.delete.menu.delete.read.ftgo.restaurant.menu-item
  role: persistence_read
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/restaurant/src/domain/menu.py
  symbol: domain.menu.MenuDomain.delete_item
  line_start: 113
  line_end: 113
  evidence_type: implemented
inbound_relations:
- type: PARTICIPATES_IN
  source: service.ftgo.gateway
  completeness: resolved
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/restaurant/menu.py
  symbol: application.routes.restaurant.menu.delete_item
  line_start: 88
  line_end: 107
  evidence_type: implemented
- type: PARTICIPATES_IN
  source: service.ftgo.restaurant
  completeness: resolved
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/restaurant/menu.py
  symbol: application.routes.restaurant.menu.delete_item
  line_start: 88
  line_end: 107
  evidence_type: implemented
attributes:
  step_count: 5
  classification_reason: endpoint, publish, consume and persistence are all source-backed
  max_call_depth: 3
---

# DELETE /menu/delete execution flow

Canonical execution flow stitched from source-backed call evidence in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Entry endpoint: `endpoint.ftgo.gateway.delete.menu.delete`
- Completeness: `resolved`
- Handler: `application.routes.restaurant.menu.delete_item`
- Declared in: `backend/gateway/src/application/routes/restaurant/menu.py` (lines 88-107)
- Evidence class: `implemented`

## Steps

- `http_ingress` `step.ftgo.gateway.delete.menu.delete.http-ingress`
- `service_dispatch` `step.ftgo.gateway.delete.menu.delete.dispatch.services.menu.menuservice.delete-item`
- `event_publish` `step.ftgo.gateway.delete.menu.delete.publish.ftgo.rabbitmq.restaurant.menu.delete-item`
- `event_consume` `step.ftgo.gateway.delete.menu.delete.consume.restaurant.restaurant.menu.delete-item`
- `persistence_read` `step.ftgo.gateway.delete.menu.delete.read.ftgo.restaurant.menu-item`

## Review notes

This approved canonical page records a source-backed execution flow. Every step is backed by a bounded call trace of at most 3 hops; no segment was inferred from similarity between an endpoint path and an event name.

