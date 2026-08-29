---
id: flow.ftgo.gateway.post.menu.get-all-menu-item
kind: UserFlow
type: UserFlow
title: POST /menu/get_all_menu_item execution flow
status: approved
review_status: approved
candidate_of: user-flow-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: user-flow
owner: aide-ftgo-cohort
entry_endpoint: endpoint.ftgo.gateway.post.menu.get-all-menu-item
http_method: POST
path: /menu/get_all_menu_item
path_resolution: partial
completeness: resolved
handler: application.routes.restaurant.menu.get_all_menu_item
participating_services:
- service.ftgo.gateway
- service.ftgo.restaurant
events:
- event.ftgo.rabbitmq.restaurant.menu.get-all-menu-item
persistence_targets:
- table.ftgo.restaurant.menu-item
- table.ftgo.restaurant.supplier-profile
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/restaurant/menu.py
  symbol: application.routes.restaurant.menu.get_all_menu_item
  line_start: 109
  line_end: 128
  evidence_type: implemented
relations:
- type: CONTAINS
  target: step.ftgo.gateway.post.menu.get-all-menu-item.consume.restaurant.restaurant.menu.get-all-menu-item
  role: event_consume
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/restaurant/src/events.py
  symbol: events.register_events
  line_start: 32
  line_end: 32
  evidence_type: implemented
- type: CONTAINS
  target: step.ftgo.gateway.post.menu.get-all-menu-item.dispatch.services.menu.menuservice.get-all-menu-item
  role: service_dispatch
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/restaurant/menu.py
  symbol: application.routes.restaurant.menu.get_all_menu_item
  line_start: 113
  line_end: 113
  evidence_type: implemented
- type: CONTAINS
  target: step.ftgo.gateway.post.menu.get-all-menu-item.http-ingress
  role: http_ingress
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/restaurant/menu.py
  symbol: application.routes.restaurant.menu.get_all_menu_item
  line_start: 109
  line_end: 128
  evidence_type: implemented
- type: CONTAINS
  target: step.ftgo.gateway.post.menu.get-all-menu-item.publish.ftgo.rabbitmq.restaurant.menu.get-all-menu-item
  role: event_publish
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/menu.py
  symbol: services.menu.MenuService.get_all_menu_item
  line_start: 27
  line_end: 27
  evidence_type: implemented
- type: CONTAINS
  target: step.ftgo.gateway.post.menu.get-all-menu-item.read.ftgo.restaurant.menu-item
  role: persistence_read
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/restaurant/src/domain/restaurant.py
  symbol: domain.restaurant.RestaurantDomain.load_all_menu_item
  line_start: 205
  line_end: 205
  evidence_type: implemented
- type: CONTAINS
  target: step.ftgo.gateway.post.menu.get-all-menu-item.read.ftgo.restaurant.supplier-profile
  role: persistence_read
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/restaurant/src/domain/restaurant.py
  symbol: domain.restaurant.RestaurantDomain.load
  line_start: 53
  line_end: 53
  evidence_type: implemented
inbound_relations:
- type: PARTICIPATES_IN
  source: service.ftgo.gateway
  completeness: resolved
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/restaurant/menu.py
  symbol: application.routes.restaurant.menu.get_all_menu_item
  line_start: 109
  line_end: 128
  evidence_type: implemented
- type: PARTICIPATES_IN
  source: service.ftgo.restaurant
  completeness: resolved
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/restaurant/menu.py
  symbol: application.routes.restaurant.menu.get_all_menu_item
  line_start: 109
  line_end: 128
  evidence_type: implemented
attributes:
  step_count: 6
  classification_reason: endpoint, publish, consume and persistence are all source-backed
  max_call_depth: 3
---

# POST /menu/get_all_menu_item execution flow

Canonical execution flow stitched from source-backed call evidence in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Entry endpoint: `endpoint.ftgo.gateway.post.menu.get-all-menu-item`
- Completeness: `resolved`
- Handler: `application.routes.restaurant.menu.get_all_menu_item`
- Declared in: `backend/gateway/src/application/routes/restaurant/menu.py` (lines 109-128)
- Evidence class: `implemented`

## Steps

- `http_ingress` `step.ftgo.gateway.post.menu.get-all-menu-item.http-ingress`
- `service_dispatch` `step.ftgo.gateway.post.menu.get-all-menu-item.dispatch.services.menu.menuservice.get-all-menu-item`
- `event_publish` `step.ftgo.gateway.post.menu.get-all-menu-item.publish.ftgo.rabbitmq.restaurant.menu.get-all-menu-item`
- `event_consume` `step.ftgo.gateway.post.menu.get-all-menu-item.consume.restaurant.restaurant.menu.get-all-menu-item`
- `persistence_read` `step.ftgo.gateway.post.menu.get-all-menu-item.read.ftgo.restaurant.menu-item`
- `persistence_read` `step.ftgo.gateway.post.menu.get-all-menu-item.read.ftgo.restaurant.supplier-profile`

## Review notes

This approved canonical page records a source-backed execution flow. Every step is backed by a bounded call trace of at most 3 hops; no segment was inferred from similarity between an endpoint path and an event name.

