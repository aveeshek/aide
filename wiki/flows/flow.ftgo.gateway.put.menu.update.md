---
id: flow.ftgo.gateway.put.menu.update
kind: UserFlow
type: UserFlow
title: PUT /menu/update execution flow
status: approved
review_status: approved
candidate_of: user-flow-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: user-flow
owner: aide-ftgo-cohort
entry_endpoint: endpoint.ftgo.gateway.put.menu.update
http_method: PUT
path: /menu/update
path_resolution: partial
completeness: resolved
handler: application.routes.restaurant.menu.update_item
participating_services:
- service.ftgo.gateway
- service.ftgo.restaurant
events:
- event.ftgo.rabbitmq.restaurant.menu.update-item
persistence_targets:
- table.ftgo.restaurant.menu-item
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/restaurant/menu.py
  symbol: application.routes.restaurant.menu.update_item
  line_start: 66
  line_end: 85
  evidence_type: implemented
relations:
- type: CONTAINS
  target: step.ftgo.gateway.put.menu.update.consume.restaurant.restaurant.menu.update-item
  role: event_consume
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/restaurant/src/events.py
  symbol: events.register_events
  line_start: 32
  line_end: 32
  evidence_type: implemented
- type: CONTAINS
  target: step.ftgo.gateway.put.menu.update.dispatch.services.menu.menuservice.update-item
  role: service_dispatch
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/restaurant/menu.py
  symbol: application.routes.restaurant.menu.update_item
  line_start: 70
  line_end: 70
  evidence_type: implemented
- type: CONTAINS
  target: step.ftgo.gateway.put.menu.update.http-ingress
  role: http_ingress
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/restaurant/menu.py
  symbol: application.routes.restaurant.menu.update_item
  line_start: 66
  line_end: 85
  evidence_type: implemented
- type: CONTAINS
  target: step.ftgo.gateway.put.menu.update.publish.ftgo.rabbitmq.restaurant.menu.update-item
  role: event_publish
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/menu.py
  symbol: services.menu.MenuService.update_item
  line_start: 19
  line_end: 19
  evidence_type: implemented
- type: CONTAINS
  target: step.ftgo.gateway.put.menu.update.read.ftgo.restaurant.menu-item
  role: persistence_read
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/restaurant/src/domain/menu.py
  symbol: domain.menu.MenuDomain.update_item
  line_start: 95
  line_end: 99
  evidence_type: implemented
inbound_relations:
- type: PARTICIPATES_IN
  source: service.ftgo.gateway
  completeness: resolved
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/restaurant/menu.py
  symbol: application.routes.restaurant.menu.update_item
  line_start: 66
  line_end: 85
  evidence_type: implemented
- type: PARTICIPATES_IN
  source: service.ftgo.restaurant
  completeness: resolved
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/restaurant/menu.py
  symbol: application.routes.restaurant.menu.update_item
  line_start: 66
  line_end: 85
  evidence_type: implemented
attributes:
  step_count: 5
  classification_reason: endpoint, publish, consume and persistence are all source-backed
  max_call_depth: 3
---

# PUT /menu/update execution flow

Canonical execution flow stitched from source-backed call evidence in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Entry endpoint: `endpoint.ftgo.gateway.put.menu.update`
- Completeness: `resolved`
- Handler: `application.routes.restaurant.menu.update_item`
- Declared in: `backend/gateway/src/application/routes/restaurant/menu.py` (lines 66-85)
- Evidence class: `implemented`

## Steps

- `http_ingress` `step.ftgo.gateway.put.menu.update.http-ingress`
- `service_dispatch` `step.ftgo.gateway.put.menu.update.dispatch.services.menu.menuservice.update-item`
- `event_publish` `step.ftgo.gateway.put.menu.update.publish.ftgo.rabbitmq.restaurant.menu.update-item`
- `event_consume` `step.ftgo.gateway.put.menu.update.consume.restaurant.restaurant.menu.update-item`
- `persistence_read` `step.ftgo.gateway.put.menu.update.read.ftgo.restaurant.menu-item`

## Review notes

This approved canonical page records a source-backed execution flow. Every step is backed by a bounded call trace of at most 3 hops; no segment was inferred from similarity between an endpoint path and an event name.

