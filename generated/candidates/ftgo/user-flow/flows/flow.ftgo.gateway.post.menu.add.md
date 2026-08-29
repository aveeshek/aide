---
id: flow.ftgo.gateway.post.menu.add
kind: UserFlow
type: UserFlow
title: POST /menu/add execution flow
status: candidate
review_status: pending
candidate_of: user-flow-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: user-flow
owner: aide-ftgo-cohort
entry_endpoint: endpoint.ftgo.gateway.post.menu.add
http_method: POST
path: /menu/add
path_resolution: partial
completeness: resolved
handler: application.routes.restaurant.menu.add_item
participating_services:
- service.ftgo.gateway
- service.ftgo.restaurant
events:
- event.ftgo.rabbitmq.restaurant.menu.add-item
persistence_targets:
- table.ftgo.restaurant.menu-item
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/restaurant/menu.py
  symbol: application.routes.restaurant.menu.add_item
  line_start: 21
  line_end: 40
  evidence_type: implemented
relations:
- type: CONTAINS
  target: step.ftgo.gateway.post.menu.add.consume.restaurant.restaurant.menu.add-item
  role: event_consume
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/restaurant/src/events.py
  symbol: events.register_events
  line_start: 32
  line_end: 32
  evidence_type: implemented
- type: CONTAINS
  target: step.ftgo.gateway.post.menu.add.dispatch.services.menu.menuservice.add-item
  role: service_dispatch
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/restaurant/menu.py
  symbol: application.routes.restaurant.menu.add_item
  line_start: 26
  line_end: 26
  evidence_type: implemented
- type: CONTAINS
  target: step.ftgo.gateway.post.menu.add.http-ingress
  role: http_ingress
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/restaurant/menu.py
  symbol: application.routes.restaurant.menu.add_item
  line_start: 21
  line_end: 40
  evidence_type: implemented
- type: CONTAINS
  target: step.ftgo.gateway.post.menu.add.publish.ftgo.rabbitmq.restaurant.menu.add-item
  role: event_publish
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/menu.py
  symbol: services.menu.MenuService.add_item
  line_start: 11
  line_end: 11
  evidence_type: implemented
- type: CONTAINS
  target: step.ftgo.gateway.post.menu.add.write.ftgo.restaurant.menu-item
  role: persistence_write
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/restaurant/src/domain/menu.py
  symbol: domain.menu.MenuDomain.add_item
  line_start: 50
  line_end: 50
  evidence_type: implemented
inbound_relations:
- type: PARTICIPATES_IN
  source: service.ftgo.gateway
  completeness: resolved
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/restaurant/menu.py
  symbol: application.routes.restaurant.menu.add_item
  line_start: 21
  line_end: 40
  evidence_type: implemented
- type: PARTICIPATES_IN
  source: service.ftgo.restaurant
  completeness: resolved
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/restaurant/menu.py
  symbol: application.routes.restaurant.menu.add_item
  line_start: 21
  line_end: 40
  evidence_type: implemented
attributes:
  step_count: 5
  classification_reason: endpoint, publish, consume and persistence are all source-backed
  max_call_depth: 3
---

# POST /menu/add execution flow

Candidate execution flow stitched from source-backed call evidence in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Entry endpoint: `endpoint.ftgo.gateway.post.menu.add`
- Completeness: `resolved`
- Handler: `application.routes.restaurant.menu.add_item`
- Declared in: `backend/gateway/src/application/routes/restaurant/menu.py` (lines 21-40)
- Evidence class: `implemented`

## Steps

- `http_ingress` `step.ftgo.gateway.post.menu.add.http-ingress`
- `service_dispatch` `step.ftgo.gateway.post.menu.add.dispatch.services.menu.menuservice.add-item`
- `event_publish` `step.ftgo.gateway.post.menu.add.publish.ftgo.rabbitmq.restaurant.menu.add-item`
- `event_consume` `step.ftgo.gateway.post.menu.add.consume.restaurant.restaurant.menu.add-item`
- `persistence_write` `step.ftgo.gateway.post.menu.add.write.ftgo.restaurant.menu-item`

## Review notes

This page is a candidate awaiting review. Every step is backed by a bounded call trace of at most 3 hops; no segment was inferred from the similarity between an endpoint path and an event name.

