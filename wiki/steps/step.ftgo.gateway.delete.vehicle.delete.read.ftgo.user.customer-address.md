---
id: step.ftgo.gateway.delete.vehicle.delete.read.ftgo.user.customer-address
kind: FlowStep
type: FlowStep
title: read table.ftgo.user.customer-address
status: approved
review_status: approved
candidate_of: user-flow-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: user-flow
owner: aide-ftgo-cohort
role: persistence_read
flow: flow.ftgo.gateway.delete.vehicle.delete
service: service.ftgo.user
derived_from: table.ftgo.user.customer-address
derived_from_kind: Table
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/user/src/data_access/repository/db_repository.py
  symbol: data_access.repository.db_repository.DatabaseRepository.fetch
  line_start: 55
  line_end: 55
  evidence_type: implemented
traces:
- target: data_access.repository.db_repository.DatabaseRepository.fetch
  depth: 3
  hops:
  - caller: application.vehicle.VehicleService.delete_vehicle
    callee: domain.manager.UserManager.load
    call: UserManager.load
    repository: ftgo
    commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
    path: backend/microservices/user/src/application/vehicle.py
    symbol: application.vehicle.VehicleService.delete_vehicle
    line_start: 23
    line_end: 23
    evidence_type: implemented
  - caller: domain.manager.UserManager.load
    callee: domain.user.User.load_profile
    call: User.load_profile
    repository: ftgo
    commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
    path: backend/microservices/user/src/domain/manager.py
    symbol: domain.manager.UserManager.load
    line_start: 28
    line_end: 28
    evidence_type: implemented
  - caller: domain.user.User.load_profile
    callee: data_access.repository.db_repository.DatabaseRepository.fetch
    call: DatabaseRepository.fetch
    repository: ftgo
    commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
    path: backend/microservices/user/src/domain/user.py
    symbol: domain.user.User.load_profile
    line_start: 60
    line_end: 60
    evidence_type: implemented
relations:
- type: DERIVED_FROM
  target: table.ftgo.user.customer-address
  anchor_kind: Table
  role: persistence_read
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/user/src/data_access/repository/db_repository.py
  symbol: data_access.repository.db_repository.DatabaseRepository.fetch
  line_start: 55
  line_end: 55
  evidence_type: implemented
- type: IMPLEMENTS
  target: service.ftgo.user
  role: persistence_read
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/user/src/data_access/repository/db_repository.py
  symbol: data_access.repository.db_repository.DatabaseRepository.fetch
  line_start: 55
  line_end: 55
  evidence_type: implemented
inbound_relations:
- type: CONTAINS
  source: flow.ftgo.gateway.delete.vehicle.delete
  role: persistence_read
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/user/src/data_access/repository/db_repository.py
  symbol: data_access.repository.db_repository.DatabaseRepository.fetch
  line_start: 55
  line_end: 55
  evidence_type: implemented
- type: PRECEDES
  source: step.ftgo.gateway.delete.vehicle.delete.consume.user.driver.vehicle.delete
  established_by: consumer call trace
  call_depth: 3
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/user/src/data_access/repository/db_repository.py
  symbol: data_access.repository.db_repository.DatabaseRepository.fetch
  line_start: 55
  line_end: 55
  evidence_type: implemented
attributes:
  operation: select
  persistence_library: sqlalchemy
  resolution: model_map_enumeration
  call_depth: 3
  event_identity: driver.vehicle.delete
---

# read table.ftgo.user.customer-address

Canonical execution step extracted from call evidence in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Role: `persistence_read`
- Flow: `flow.ftgo.gateway.delete.vehicle.delete`
- Performed by: `service.ftgo.user`
- Anchored on: `table.ftgo.user.customer-address` (`Table`)
- Declared in: `backend/microservices/user/src/data_access/repository/db_repository.py` (lines 55-55)
- Evidence class: `implemented`

## Call trace

- `application.vehicle.VehicleService.delete_vehicle` -> `domain.manager.UserManager.load` (`backend/microservices/user/src/application/vehicle.py:23`)
- `domain.manager.UserManager.load` -> `domain.user.User.load_profile` (`backend/microservices/user/src/domain/manager.py:28`)
- `domain.user.User.load_profile` -> `data_access.repository.db_repository.DatabaseRepository.fetch` (`backend/microservices/user/src/domain/user.py:60`)

## Review notes

This approved canonical page records a source-backed execution step. The step exists because a concrete call site proves it, and its ordering edges carry that call site as evidence.

