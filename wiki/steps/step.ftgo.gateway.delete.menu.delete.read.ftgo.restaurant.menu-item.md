---
id: step.ftgo.gateway.delete.menu.delete.read.ftgo.restaurant.menu-item
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
flow: flow.ftgo.gateway.delete.menu.delete
service: service.ftgo.restaurant
derived_from: table.ftgo.restaurant.menu-item
derived_from_kind: Table
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/restaurant/src/domain/menu.py
  symbol: domain.menu.MenuDomain.delete_item
  line_start: 113
  line_end: 113
  evidence_type: implemented
traces:
- target: domain.menu.MenuDomain.delete_item
  depth: 1
  hops:
  - caller: application.menu.MenuService.delete_item
    callee: domain.menu.MenuDomain.delete_item
    call: MenuDomain.delete_item
    repository: ftgo
    commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
    path: backend/microservices/restaurant/src/application/menu.py
    symbol: application.menu.MenuService.delete_item
    line_start: 65
    line_end: 65
    evidence_type: implemented
relations:
- type: DERIVED_FROM
  target: table.ftgo.restaurant.menu-item
  anchor_kind: Table
  role: persistence_read
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/restaurant/src/domain/menu.py
  symbol: domain.menu.MenuDomain.delete_item
  line_start: 113
  line_end: 113
  evidence_type: implemented
- type: IMPLEMENTS
  target: service.ftgo.restaurant
  role: persistence_read
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/restaurant/src/domain/menu.py
  symbol: domain.menu.MenuDomain.delete_item
  line_start: 113
  line_end: 113
  evidence_type: implemented
inbound_relations:
- type: CONTAINS
  source: flow.ftgo.gateway.delete.menu.delete
  role: persistence_read
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/restaurant/src/domain/menu.py
  symbol: domain.menu.MenuDomain.delete_item
  line_start: 113
  line_end: 113
  evidence_type: implemented
- type: PRECEDES
  source: step.ftgo.gateway.delete.menu.delete.consume.restaurant.restaurant.menu.delete-item
  established_by: consumer call trace
  call_depth: 1
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/restaurant/src/domain/menu.py
  symbol: domain.menu.MenuDomain.delete_item
  line_start: 113
  line_end: 113
  evidence_type: implemented
attributes:
  operation: select
  persistence_library: sqlalchemy
  resolution: wrapper_argument
  call_depth: 1
  event_identity: restaurant.menu.delete_item
---

# read table.ftgo.restaurant.menu-item

Canonical execution step extracted from call evidence in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Role: `persistence_read`
- Flow: `flow.ftgo.gateway.delete.menu.delete`
- Performed by: `service.ftgo.restaurant`
- Anchored on: `table.ftgo.restaurant.menu-item` (`Table`)
- Declared in: `backend/microservices/restaurant/src/domain/menu.py` (lines 113-113)
- Evidence class: `implemented`

## Call trace

- `application.menu.MenuService.delete_item` -> `domain.menu.MenuDomain.delete_item` (`backend/microservices/restaurant/src/application/menu.py:65`)

## Review notes

This approved canonical page records a source-backed execution step. The step exists because a concrete call site proves it, and its ordering edges carry that call site as evidence.

