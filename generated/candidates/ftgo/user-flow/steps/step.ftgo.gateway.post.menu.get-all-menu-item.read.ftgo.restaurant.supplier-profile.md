---
id: step.ftgo.gateway.post.menu.get-all-menu-item.read.ftgo.restaurant.supplier-profile
kind: FlowStep
type: FlowStep
title: read table.ftgo.restaurant.supplier-profile
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
derived_from: table.ftgo.restaurant.supplier-profile
derived_from_kind: Table
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/restaurant/src/domain/restaurant.py
  symbol: domain.restaurant.RestaurantDomain.load
  line_start: 53
  line_end: 53
  evidence_type: implemented
traces:
- target: domain.restaurant.RestaurantDomain.load
  depth: 1
  hops:
  - caller: application.menu.MenuService.get_all_menu_item
    callee: domain.restaurant.RestaurantDomain.load
    call: RestaurantDomain.load
    repository: ftgo
    commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
    path: backend/microservices/restaurant/src/application/menu.py
    symbol: application.menu.MenuService.get_all_menu_item
    line_start: 93
    line_end: 93
    evidence_type: implemented
relations:
- type: DERIVED_FROM
  target: table.ftgo.restaurant.supplier-profile
  anchor_kind: Table
  role: persistence_read
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/restaurant/src/domain/restaurant.py
  symbol: domain.restaurant.RestaurantDomain.load
  line_start: 53
  line_end: 53
  evidence_type: implemented
- type: IMPLEMENTS
  target: service.ftgo.restaurant
  role: persistence_read
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/restaurant/src/domain/restaurant.py
  symbol: domain.restaurant.RestaurantDomain.load
  line_start: 53
  line_end: 53
  evidence_type: implemented
inbound_relations:
- type: CONTAINS
  source: flow.ftgo.gateway.post.menu.get-all-menu-item
  role: persistence_read
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/restaurant/src/domain/restaurant.py
  symbol: domain.restaurant.RestaurantDomain.load
  line_start: 53
  line_end: 53
  evidence_type: implemented
- type: PRECEDES
  source: step.ftgo.gateway.post.menu.get-all-menu-item.consume.restaurant.restaurant.menu.get-all-menu-item
  established_by: consumer call trace
  call_depth: 1
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/restaurant/src/domain/restaurant.py
  symbol: domain.restaurant.RestaurantDomain.load
  line_start: 53
  line_end: 53
  evidence_type: implemented
attributes:
  operation: select
  persistence_library: sqlalchemy
  resolution: wrapper_argument
  call_depth: 1
  event_identity: restaurant.menu.get_all_menu_item
---

# read table.ftgo.restaurant.supplier-profile

Candidate execution step extracted from call evidence in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Role: `persistence_read`
- Flow: `flow.ftgo.gateway.post.menu.get-all-menu-item`
- Performed by: `service.ftgo.restaurant`
- Anchored on: `table.ftgo.restaurant.supplier-profile` (`Table`)
- Declared in: `backend/microservices/restaurant/src/domain/restaurant.py` (lines 53-53)
- Evidence class: `implemented`

## Call trace

- `application.menu.MenuService.get_all_menu_item` -> `domain.restaurant.RestaurantDomain.load` (`backend/microservices/restaurant/src/application/menu.py:93`)

## Review notes

This page is a candidate awaiting review. The step exists because a concrete call site proves it, and its ordering edges carry that call site as evidence.

