---
id: step.ftgo.gateway.get.menu.get-info.read.ftgo.restaurant.menu-item
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
flow: flow.ftgo.gateway.get.menu.get-info
service: service.ftgo.restaurant
derived_from: table.ftgo.restaurant.menu-item
derived_from_kind: Table
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/restaurant/src/domain/menu.py
  symbol: domain.menu.MenuDomain.load
  line_start: 67
  line_end: 67
  evidence_type: implemented
traces:
- target: domain.menu.MenuDomain.load
  depth: 1
  hops:
  - caller: application.menu.MenuService.get_item_info
    callee: domain.menu.MenuDomain.load
    call: MenuDomain.load
    repository: ftgo
    commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
    path: backend/microservices/restaurant/src/application/menu.py
    symbol: application.menu.MenuService.get_item_info
    line_start: 79
    line_end: 79
    evidence_type: implemented
relations:
- type: DERIVED_FROM
  target: table.ftgo.restaurant.menu-item
  anchor_kind: Table
  role: persistence_read
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/restaurant/src/domain/menu.py
  symbol: domain.menu.MenuDomain.load
  line_start: 67
  line_end: 67
  evidence_type: implemented
- type: IMPLEMENTS
  target: service.ftgo.restaurant
  role: persistence_read
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
  role: persistence_read
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/restaurant/src/domain/menu.py
  symbol: domain.menu.MenuDomain.load
  line_start: 67
  line_end: 67
  evidence_type: implemented
- type: PRECEDES
  source: step.ftgo.gateway.get.menu.get-info.consume.restaurant.restaurant.menu.get-item-info
  established_by: consumer call trace
  call_depth: 1
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/restaurant/src/domain/menu.py
  symbol: domain.menu.MenuDomain.load
  line_start: 67
  line_end: 67
  evidence_type: implemented
attributes:
  operation: select
  persistence_library: sqlalchemy
  resolution: wrapper_argument
  call_depth: 1
  event_identity: restaurant.menu.get_item_info
---

# read table.ftgo.restaurant.menu-item

Candidate execution step extracted from call evidence in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Role: `persistence_read`
- Flow: `flow.ftgo.gateway.get.menu.get-info`
- Performed by: `service.ftgo.restaurant`
- Anchored on: `table.ftgo.restaurant.menu-item` (`Table`)
- Declared in: `backend/microservices/restaurant/src/domain/menu.py` (lines 67-67)
- Evidence class: `implemented`

## Call trace

- `application.menu.MenuService.get_item_info` -> `domain.menu.MenuDomain.load` (`backend/microservices/restaurant/src/application/menu.py:79`)

## Review notes

This page is a candidate awaiting review. The step exists because a concrete call site proves it, and its ordering edges carry that call site as evidence.

