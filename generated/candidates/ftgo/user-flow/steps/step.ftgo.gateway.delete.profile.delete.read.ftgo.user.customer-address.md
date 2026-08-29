---
id: step.ftgo.gateway.delete.profile.delete.read.ftgo.user.customer-address
kind: FlowStep
type: FlowStep
title: read table.ftgo.user.customer-address
status: candidate
review_status: pending
candidate_of: user-flow-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: user-flow
owner: aide-ftgo-cohort
role: persistence_read
flow: flow.ftgo.gateway.delete.profile.delete
service: service.ftgo.user
derived_from: table.ftgo.user.customer-address
derived_from_kind: Table
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/user/src/data_access/repository/db_repository.py
  symbol: data_access.repository.db_repository.DatabaseRepository.delete
  line_start: 121
  line_end: 121
  evidence_type: implemented
traces:
- target: data_access.repository.db_repository.DatabaseRepository.delete
  depth: 2
  hops:
  - caller: application.profile.ProfileService.delete_account
    callee: domain.user.User.delete_account
    call: user.delete_account
    repository: ftgo
    commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
    path: backend/microservices/user/src/application/profile.py
    symbol: application.profile.ProfileService.delete_account
    line_start: 71
    line_end: 71
    evidence_type: implemented
  - caller: domain.user.User.delete_account
    callee: data_access.repository.db_repository.DatabaseRepository.delete
    call: DatabaseRepository.delete
    repository: ftgo
    commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
    path: backend/microservices/user/src/domain/user.py
    symbol: domain.user.User.delete_account
    line_start: 81
    line_end: 81
    evidence_type: implemented
- target: data_access.repository.db_repository.DatabaseRepository.fetch
  depth: 3
  hops:
  - caller: application.profile.ProfileService.delete_account
    callee: domain.manager.UserManager.load
    call: UserManager.load
    repository: ftgo
    commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
    path: backend/microservices/user/src/application/profile.py
    symbol: application.profile.ProfileService.delete_account
    line_start: 70
    line_end: 70
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
  symbol: data_access.repository.db_repository.DatabaseRepository.delete
  line_start: 121
  line_end: 121
  evidence_type: implemented
- type: IMPLEMENTS
  target: service.ftgo.user
  role: persistence_read
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/user/src/data_access/repository/db_repository.py
  symbol: data_access.repository.db_repository.DatabaseRepository.delete
  line_start: 121
  line_end: 121
  evidence_type: implemented
inbound_relations:
- type: CONTAINS
  source: flow.ftgo.gateway.delete.profile.delete
  role: persistence_read
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/user/src/data_access/repository/db_repository.py
  symbol: data_access.repository.db_repository.DatabaseRepository.delete
  line_start: 121
  line_end: 121
  evidence_type: implemented
- type: PRECEDES
  source: step.ftgo.gateway.delete.profile.delete.consume.user.user.profile.delete-account
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
  call_depth: 2
  event_identity: user.profile.delete_account
---

# read table.ftgo.user.customer-address

Candidate execution step extracted from call evidence in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Role: `persistence_read`
- Flow: `flow.ftgo.gateway.delete.profile.delete`
- Performed by: `service.ftgo.user`
- Anchored on: `table.ftgo.user.customer-address` (`Table`)
- Declared in: `backend/microservices/user/src/data_access/repository/db_repository.py` (lines 121-121)
- Evidence class: `implemented`

## Call trace

- `application.profile.ProfileService.delete_account` -> `domain.user.User.delete_account` (`backend/microservices/user/src/application/profile.py:71`)
- `domain.user.User.delete_account` -> `data_access.repository.db_repository.DatabaseRepository.delete` (`backend/microservices/user/src/domain/user.py:81`)
- `application.profile.ProfileService.delete_account` -> `domain.manager.UserManager.load` (`backend/microservices/user/src/application/profile.py:70`)
- `domain.manager.UserManager.load` -> `domain.user.User.load_profile` (`backend/microservices/user/src/domain/manager.py:28`)
- `domain.user.User.load_profile` -> `data_access.repository.db_repository.DatabaseRepository.fetch` (`backend/microservices/user/src/domain/user.py:60`)

## Review notes

This page is a candidate awaiting review. The step exists because a concrete call site proves it, and its ordering edges carry that call site as evidence.

