---
id: step.ftgo.gateway.delete.restaurant.delete.read.ftgo.restaurant.supplier-profile
kind: FlowStep
type: FlowStep
title: read table.ftgo.restaurant.supplier-profile
status: approved
review_status: approved
candidate_of: user-flow-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: user-flow
owner: aide-ftgo-cohort
role: persistence_read
flow: flow.ftgo.gateway.delete.restaurant.delete
service: service.ftgo.restaurant
derived_from: table.ftgo.restaurant.supplier-profile
derived_from_kind: Table
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/restaurant/src/domain/restaurant.py
  symbol: domain.restaurant.RestaurantDomain.delete_restaurant
  line_start: 153
  line_end: 153
  evidence_type: implemented
traces:
- target: domain.restaurant.RestaurantDomain.delete_restaurant
  depth: 1
  hops:
  - caller: application.supplier.RestaurantService.delete_restaurant
    callee: domain.restaurant.RestaurantDomain.delete_restaurant
    call: restaurant.delete_restaurant
    repository: ftgo
    commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
    path: backend/microservices/restaurant/src/application/supplier.py
    symbol: application.supplier.RestaurantService.delete_restaurant
    line_start: 116
    line_end: 116
    evidence_type: implemented
- target: domain.restaurant.RestaurantDomain.load
  depth: 1
  hops:
  - caller: application.supplier.RestaurantService.delete_restaurant
    callee: domain.restaurant.RestaurantDomain.load
    call: RestaurantDomain.load
    repository: ftgo
    commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
    path: backend/microservices/restaurant/src/application/supplier.py
    symbol: application.supplier.RestaurantService.delete_restaurant
    line_start: 115
    line_end: 115
    evidence_type: implemented
relations:
- type: DERIVED_FROM
  target: table.ftgo.restaurant.supplier-profile
  anchor_kind: Table
  role: persistence_read
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/restaurant/src/domain/restaurant.py
  symbol: domain.restaurant.RestaurantDomain.delete_restaurant
  line_start: 153
  line_end: 153
  evidence_type: implemented
- type: IMPLEMENTS
  target: service.ftgo.restaurant
  role: persistence_read
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/restaurant/src/domain/restaurant.py
  symbol: domain.restaurant.RestaurantDomain.delete_restaurant
  line_start: 153
  line_end: 153
  evidence_type: implemented
inbound_relations:
- type: CONTAINS
  source: flow.ftgo.gateway.delete.restaurant.delete
  role: persistence_read
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/restaurant/src/domain/restaurant.py
  symbol: domain.restaurant.RestaurantDomain.delete_restaurant
  line_start: 153
  line_end: 153
  evidence_type: implemented
- type: PRECEDES
  source: step.ftgo.gateway.delete.restaurant.delete.consume.restaurant.restaurant.supplier.delete-restaurant
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
  event_identity: restaurant.supplier.delete_restaurant
---

# read table.ftgo.restaurant.supplier-profile

Canonical execution step extracted from call evidence in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Role: `persistence_read`
- Flow: `flow.ftgo.gateway.delete.restaurant.delete`
- Performed by: `service.ftgo.restaurant`
- Anchored on: `table.ftgo.restaurant.supplier-profile` (`Table`)
- Declared in: `backend/microservices/restaurant/src/domain/restaurant.py` (lines 153-153)
- Evidence class: `implemented`

## Call trace

- `application.supplier.RestaurantService.delete_restaurant` -> `domain.restaurant.RestaurantDomain.delete_restaurant` (`backend/microservices/restaurant/src/application/supplier.py:116`)
- `application.supplier.RestaurantService.delete_restaurant` -> `domain.restaurant.RestaurantDomain.load` (`backend/microservices/restaurant/src/application/supplier.py:115`)

## Review notes

This approved canonical page records a source-backed execution step. The step exists because a concrete call site proves it, and its ordering edges carry that call site as evidence.

