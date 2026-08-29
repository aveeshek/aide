---
id: step.ftgo.gateway.put.menu.update.read.ftgo.restaurant.menu-item
kind: FlowStep
type: FlowStep
title: read table.ftgo.restaurant.menu-item
status: approved
review_status: approved
candidate_of: user-flow-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: user-flow
owner: aide-ftgo-cohort
role: persistence_read
flow: flow.ftgo.gateway.put.menu.update
service: service.ftgo.restaurant
derived_from: table.ftgo.restaurant.menu-item
derived_from_kind: Table
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/restaurant/src/domain/menu.py
  symbol: domain.menu.MenuDomain.update_item
  line_start: 95
  line_end: 99
  evidence_type: implemented
traces:
- target: domain.menu.MenuDomain.update_item
  depth: 1
  hops:
  - caller: application.menu.MenuService.update_item
    callee: domain.menu.MenuDomain.update_item
    call: MenuDomain.update_item
    repository: ftgo
    commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
    path: backend/microservices/restaurant/src/application/menu.py
    symbol: application.menu.MenuService.update_item
    line_start: 54
    line_end: 55
    evidence_type: implemented
relations:
- type: DERIVED_FROM
  target: table.ftgo.restaurant.menu-item
  anchor_kind: Table
  role: persistence_read
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/restaurant/src/domain/menu.py
  symbol: domain.menu.MenuDomain.update_item
  line_start: 95
  line_end: 99
  evidence_type: implemented
- type: IMPLEMENTS
  target: service.ftgo.restaurant
  role: persistence_read
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/restaurant/src/domain/menu.py
  symbol: domain.menu.MenuDomain.update_item
  line_start: 95
  line_end: 99
  evidence_type: implemented
inbound_relations:
- type: CONTAINS
  source: flow.ftgo.gateway.put.menu.update
  role: persistence_read
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/restaurant/src/domain/menu.py
  symbol: domain.menu.MenuDomain.update_item
  line_start: 95
  line_end: 99
  evidence_type: implemented
- type: PRECEDES
  source: step.ftgo.gateway.put.menu.update.consume.restaurant.restaurant.menu.update-item
  established_by: consumer call trace
  call_depth: 1
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/restaurant/src/domain/menu.py
  symbol: domain.menu.MenuDomain.update_item
  line_start: 95
  line_end: 99
  evidence_type: implemented
attributes:
  operation: select
  persistence_library: sqlalchemy
  resolution: wrapper_argument
  call_depth: 1
  event_identity: restaurant.menu.update_item
---

# read table.ftgo.restaurant.menu-item

Canonical execution step extracted from call evidence in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Role: `persistence_read`
- Flow: `flow.ftgo.gateway.put.menu.update`
- Performed by: `service.ftgo.restaurant`
- Anchored on: `table.ftgo.restaurant.menu-item` (`Table`)
- Declared in: `backend/microservices/restaurant/src/domain/menu.py` (lines 95-99)
- Evidence class: `implemented`

## Call trace

- `application.menu.MenuService.update_item` -> `domain.menu.MenuDomain.update_item` (`backend/microservices/restaurant/src/application/menu.py:54`)

## Review notes

This approved canonical page records a source-backed execution step. The step exists because a concrete call site proves it, and its ordering edges carry that call site as evidence.

