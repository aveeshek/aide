---
id: step.ftgo.gateway.post.menu.add.write.ftgo.restaurant.menu-item
kind: FlowStep
type: FlowStep
title: write table.ftgo.restaurant.menu-item
status: candidate
review_status: pending
candidate_of: user-flow-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: user-flow
owner: aide-ftgo-cohort
role: persistence_write
flow: flow.ftgo.gateway.post.menu.add
service: service.ftgo.restaurant
derived_from: table.ftgo.restaurant.menu-item
derived_from_kind: Table
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/restaurant/src/domain/menu.py
  symbol: domain.menu.MenuDomain.add_item
  line_start: 50
  line_end: 50
  evidence_type: implemented
traces:
- target: domain.menu.MenuDomain.add_item
  depth: 1
  hops:
  - caller: application.menu.MenuService.add_item
    callee: domain.menu.MenuDomain.add_item
    call: MenuDomain.add_item
    repository: ftgo
    commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
    path: backend/microservices/restaurant/src/application/menu.py
    symbol: application.menu.MenuService.add_item
    line_start: 29
    line_end: 30
    evidence_type: implemented
relations:
- type: DERIVED_FROM
  target: table.ftgo.restaurant.menu-item
  anchor_kind: Table
  role: persistence_write
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/restaurant/src/domain/menu.py
  symbol: domain.menu.MenuDomain.add_item
  line_start: 50
  line_end: 50
  evidence_type: implemented
- type: IMPLEMENTS
  target: service.ftgo.restaurant
  role: persistence_write
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/restaurant/src/domain/menu.py
  symbol: domain.menu.MenuDomain.add_item
  line_start: 50
  line_end: 50
  evidence_type: implemented
inbound_relations:
- type: CONTAINS
  source: flow.ftgo.gateway.post.menu.add
  role: persistence_write
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/restaurant/src/domain/menu.py
  symbol: domain.menu.MenuDomain.add_item
  line_start: 50
  line_end: 50
  evidence_type: implemented
- type: PRECEDES
  source: step.ftgo.gateway.post.menu.add.consume.restaurant.restaurant.menu.add-item
  established_by: consumer call trace
  call_depth: 1
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/restaurant/src/domain/menu.py
  symbol: domain.menu.MenuDomain.add_item
  line_start: 50
  line_end: 50
  evidence_type: implemented
attributes:
  operation: add
  persistence_library: asyncpg_client
  resolution: wrapper_argument
  call_depth: 1
  event_identity: restaurant.menu.add_item
---

# write table.ftgo.restaurant.menu-item

Candidate execution step extracted from call evidence in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Role: `persistence_write`
- Flow: `flow.ftgo.gateway.post.menu.add`
- Performed by: `service.ftgo.restaurant`
- Anchored on: `table.ftgo.restaurant.menu-item` (`Table`)
- Declared in: `backend/microservices/restaurant/src/domain/menu.py` (lines 50-50)
- Evidence class: `implemented`

## Call trace

- `application.menu.MenuService.add_item` -> `domain.menu.MenuDomain.add_item` (`backend/microservices/restaurant/src/application/menu.py:29`)

## Review notes

This page is a candidate awaiting review. The step exists because a concrete call site proves it, and its ordering edges carry that call site as evidence.

