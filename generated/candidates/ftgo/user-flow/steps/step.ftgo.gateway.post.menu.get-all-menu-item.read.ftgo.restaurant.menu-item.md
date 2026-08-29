---
id: step.ftgo.gateway.post.menu.get-all-menu-item.read.ftgo.restaurant.menu-item
kind: FlowStep
type: FlowStep
title: read table.ftgo.restaurant.menu-item
status: candidate
review_status: pending
candidate_of: user-flow-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: user-flow
owner: aide-ftgo-cohort
role: persistence_read
flow: flow.ftgo.gateway.post.menu.get-all-menu-item
service: service.ftgo.restaurant
derived_from: table.ftgo.restaurant.menu-item
derived_from_kind: Table
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/restaurant/src/domain/restaurant.py
  symbol: domain.restaurant.RestaurantDomain.load_all_menu_item
  line_start: 205
  line_end: 205
  evidence_type: implemented
traces:
- target: domain.restaurant.RestaurantDomain.load_all_menu_item
  depth: 2
  hops:
  - caller: application.menu.MenuService.get_all_menu_item
    callee: domain.restaurant.RestaurantDomain.get_all_menu_item_info
    call: restaurant.get_all_menu_item_info
    repository: ftgo
    commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
    path: backend/microservices/restaurant/src/application/menu.py
    symbol: application.menu.MenuService.get_all_menu_item
    line_start: 94
    line_end: 94
    evidence_type: implemented
  - caller: domain.restaurant.RestaurantDomain.get_all_menu_item_info
    callee: domain.restaurant.RestaurantDomain.load_all_menu_item
    call: self.load_all_menu_item
    repository: ftgo
    commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
    path: backend/microservices/restaurant/src/domain/restaurant.py
    symbol: domain.restaurant.RestaurantDomain.get_all_menu_item_info
    line_start: 217
    line_end: 217
    evidence_type: implemented
relations:
- type: DERIVED_FROM
  target: table.ftgo.restaurant.menu-item
  anchor_kind: Table
  role: persistence_read
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/restaurant/src/domain/restaurant.py
  symbol: domain.restaurant.RestaurantDomain.load_all_menu_item
  line_start: 205
  line_end: 205
  evidence_type: implemented
- type: IMPLEMENTS
  target: service.ftgo.restaurant
  role: persistence_read
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/restaurant/src/domain/restaurant.py
  symbol: domain.restaurant.RestaurantDomain.load_all_menu_item
  line_start: 205
  line_end: 205
  evidence_type: implemented
inbound_relations:
- type: CONTAINS
  source: flow.ftgo.gateway.post.menu.get-all-menu-item
  role: persistence_read
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/restaurant/src/domain/restaurant.py
  symbol: domain.restaurant.RestaurantDomain.load_all_menu_item
  line_start: 205
  line_end: 205
  evidence_type: implemented
- type: PRECEDES
  source: step.ftgo.gateway.post.menu.get-all-menu-item.consume.restaurant.restaurant.menu.get-all-menu-item
  established_by: consumer call trace
  call_depth: 2
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/restaurant/src/domain/restaurant.py
  symbol: domain.restaurant.RestaurantDomain.load_all_menu_item
  line_start: 205
  line_end: 205
  evidence_type: implemented
attributes:
  operation: select
  persistence_library: sqlalchemy
  resolution: wrapper_argument
  call_depth: 2
  event_identity: restaurant.menu.get_all_menu_item
---

# read table.ftgo.restaurant.menu-item

Candidate execution step extracted from call evidence in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Role: `persistence_read`
- Flow: `flow.ftgo.gateway.post.menu.get-all-menu-item`
- Performed by: `service.ftgo.restaurant`
- Anchored on: `table.ftgo.restaurant.menu-item` (`Table`)
- Declared in: `backend/microservices/restaurant/src/domain/restaurant.py` (lines 205-205)
- Evidence class: `implemented`

## Call trace

- `application.menu.MenuService.get_all_menu_item` -> `domain.restaurant.RestaurantDomain.get_all_menu_item_info` (`backend/microservices/restaurant/src/application/menu.py:94`)
- `domain.restaurant.RestaurantDomain.get_all_menu_item_info` -> `domain.restaurant.RestaurantDomain.load_all_menu_item` (`backend/microservices/restaurant/src/domain/restaurant.py:217`)

## Review notes

This page is a candidate awaiting review. The step exists because a concrete call site proves it, and its ordering edges carry that call site as evidence.

