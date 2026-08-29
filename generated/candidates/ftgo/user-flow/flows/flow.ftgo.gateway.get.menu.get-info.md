---
id: flow.ftgo.gateway.get.menu.get-info
kind: UserFlow
type: UserFlow
title: GET /menu/get_info execution flow
status: candidate
review_status: pending
candidate_of: user-flow-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: user-flow
owner: aide-ftgo-cohort
entry_endpoint: endpoint.ftgo.gateway.get.menu.get-info
http_method: GET
path: /menu/get_info
path_resolution: partial
completeness: resolved
handler: application.routes.restaurant.menu.get_info
participating_services:
- service.ftgo.gateway
- service.ftgo.restaurant
events:
- event.ftgo.rabbitmq.restaurant.menu.get-item-info
persistence_targets:
- table.ftgo.restaurant.menu-item
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/restaurant/menu.py
  symbol: application.routes.restaurant.menu.get_info
  line_start: 43
  line_end: 63
  evidence_type: implemented
relations:
- type: CONTAINS
  target: step.ftgo.gateway.get.menu.get-info.consume.restaurant.restaurant.menu.get-item-info
  role: event_consume
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/restaurant/src/events.py
  symbol: events.register_events
  line_start: 32
  line_end: 32
  evidence_type: implemented
- type: CONTAINS
  target: step.ftgo.gateway.get.menu.get-info.dispatch.services.menu.menuservice.get-item-info
  role: service_dispatch
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/restaurant/menu.py
  symbol: application.routes.restaurant.menu.get_info
  line_start: 48
  line_end: 48
  evidence_type: implemented
- type: CONTAINS
  target: step.ftgo.gateway.get.menu.get-info.http-ingress
  role: http_ingress
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/restaurant/menu.py
  symbol: application.routes.restaurant.menu.get_info
  line_start: 43
  line_end: 63
  evidence_type: implemented
- type: CONTAINS
  target: step.ftgo.gateway.get.menu.get-info.publish.ftgo.rabbitmq.restaurant.menu.get-item-info
  role: event_publish
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/menu.py
  symbol: services.menu.MenuService.get_item_info
  line_start: 15
  line_end: 15
  evidence_type: implemented
- type: CONTAINS
  target: step.ftgo.gateway.get.menu.get-info.read.ftgo.restaurant.menu-item
  role: persistence_read
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/restaurant/src/domain/menu.py
  symbol: domain.menu.MenuDomain.load
  line_start: 67
  line_end: 67
  evidence_type: implemented
inbound_relations:
- type: PARTICIPATES_IN
  source: service.ftgo.gateway
  completeness: resolved
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/restaurant/menu.py
  symbol: application.routes.restaurant.menu.get_info
  line_start: 43
  line_end: 63
  evidence_type: implemented
- type: PARTICIPATES_IN
  source: service.ftgo.restaurant
  completeness: resolved
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/restaurant/menu.py
  symbol: application.routes.restaurant.menu.get_info
  line_start: 43
  line_end: 63
  evidence_type: implemented
attributes:
  step_count: 5
  classification_reason: endpoint, publish, consume and persistence are all source-backed
  max_call_depth: 3
---

# GET /menu/get_info execution flow

Candidate execution flow stitched from source-backed call evidence in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Entry endpoint: `endpoint.ftgo.gateway.get.menu.get-info`
- Completeness: `resolved`
- Handler: `application.routes.restaurant.menu.get_info`
- Declared in: `backend/gateway/src/application/routes/restaurant/menu.py` (lines 43-63)
- Evidence class: `implemented`

## Steps

- `http_ingress` `step.ftgo.gateway.get.menu.get-info.http-ingress`
- `service_dispatch` `step.ftgo.gateway.get.menu.get-info.dispatch.services.menu.menuservice.get-item-info`
- `event_publish` `step.ftgo.gateway.get.menu.get-info.publish.ftgo.rabbitmq.restaurant.menu.get-item-info`
- `event_consume` `step.ftgo.gateway.get.menu.get-info.consume.restaurant.restaurant.menu.get-item-info`
- `persistence_read` `step.ftgo.gateway.get.menu.get-info.read.ftgo.restaurant.menu-item`

## Review notes

This page is a candidate awaiting review. Every step is backed by a bounded call trace of at most 3 hops; no segment was inferred from the similarity between an endpoint path and an event name.

