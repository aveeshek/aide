---
id: step.ftgo.gateway.delete.profile.delete.write.ftgo.user.vehicle-info
kind: FlowStep
type: FlowStep
title: write table.ftgo.user.vehicle-info
status: candidate
review_status: pending
candidate_of: user-flow-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: user-flow
owner: aide-ftgo-cohort
role: persistence_write
flow: flow.ftgo.gateway.delete.profile.delete
service: service.ftgo.user
derived_from: table.ftgo.user.vehicle-info
derived_from_kind: Table
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/user/src/data_access/repository/db_repository.py
  symbol: data_access.repository.db_repository.DatabaseRepository.delete
  line_start: 127
  line_end: 127
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
relations:
- type: DERIVED_FROM
  target: table.ftgo.user.vehicle-info
  anchor_kind: Table
  role: persistence_write
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/user/src/data_access/repository/db_repository.py
  symbol: data_access.repository.db_repository.DatabaseRepository.delete
  line_start: 127
  line_end: 127
  evidence_type: implemented
- type: IMPLEMENTS
  target: service.ftgo.user
  role: persistence_write
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/user/src/data_access/repository/db_repository.py
  symbol: data_access.repository.db_repository.DatabaseRepository.delete
  line_start: 127
  line_end: 127
  evidence_type: implemented
inbound_relations:
- type: CONTAINS
  source: flow.ftgo.gateway.delete.profile.delete
  role: persistence_write
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/user/src/data_access/repository/db_repository.py
  symbol: data_access.repository.db_repository.DatabaseRepository.delete
  line_start: 127
  line_end: 127
  evidence_type: implemented
- type: PRECEDES
  source: step.ftgo.gateway.delete.profile.delete.consume.user.user.profile.delete-account
  established_by: consumer call trace
  call_depth: 2
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/user/src/data_access/repository/db_repository.py
  symbol: data_access.repository.db_repository.DatabaseRepository.delete
  line_start: 127
  line_end: 127
  evidence_type: implemented
attributes:
  operation: delete
  persistence_library: asyncpg_client
  resolution: model_map_enumeration
  call_depth: 2
  event_identity: user.profile.delete_account
---

# write table.ftgo.user.vehicle-info

Candidate execution step extracted from call evidence in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Role: `persistence_write`
- Flow: `flow.ftgo.gateway.delete.profile.delete`
- Performed by: `service.ftgo.user`
- Anchored on: `table.ftgo.user.vehicle-info` (`Table`)
- Declared in: `backend/microservices/user/src/data_access/repository/db_repository.py` (lines 127-127)
- Evidence class: `implemented`

## Call trace

- `application.profile.ProfileService.delete_account` -> `domain.user.User.delete_account` (`backend/microservices/user/src/application/profile.py:71`)
- `domain.user.User.delete_account` -> `data_access.repository.db_repository.DatabaseRepository.delete` (`backend/microservices/user/src/domain/user.py:81`)

## Review notes

This page is a candidate awaiting review. The step exists because a concrete call site proves it, and its ordering edges carry that call site as evidence.

