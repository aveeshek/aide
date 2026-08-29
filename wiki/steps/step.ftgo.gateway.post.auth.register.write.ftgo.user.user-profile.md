---
id: step.ftgo.gateway.post.auth.register.write.ftgo.user.user-profile
kind: FlowStep
type: FlowStep
title: write table.ftgo.user.user-profile
status: approved
review_status: approved
candidate_of: user-flow-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: user-flow
owner: aide-ftgo-cohort
role: persistence_write
flow: flow.ftgo.gateway.post.auth.register
service: service.ftgo.user
derived_from: table.ftgo.user.user-profile
derived_from_kind: Table
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/user/src/data_access/repository/db_repository.py
  symbol: data_access.repository.db_repository.DatabaseRepository.insert
  line_start: 74
  line_end: 74
  evidence_type: implemented
traces:
- target: data_access.repository.db_repository.DatabaseRepository.insert
  depth: 2
  hops:
  - caller: application.profile.ProfileService.register
    callee: domain.manager.UserManager.register
    call: UserManager.register
    repository: ftgo
    commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
    path: backend/microservices/user/src/application/profile.py
    symbol: application.profile.ProfileService.register
    line_start: 19
    line_end: 28
    evidence_type: implemented
  - caller: domain.manager.UserManager.register
    callee: data_access.repository.db_repository.DatabaseRepository.insert
    call: DatabaseRepository.insert
    repository: ftgo
    commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
    path: backend/microservices/user/src/domain/manager.py
    symbol: domain.manager.UserManager.register
    line_start: 78
    line_end: 78
    evidence_type: implemented
relations:
- type: DERIVED_FROM
  target: table.ftgo.user.user-profile
  anchor_kind: Table
  role: persistence_write
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/user/src/data_access/repository/db_repository.py
  symbol: data_access.repository.db_repository.DatabaseRepository.insert
  line_start: 74
  line_end: 74
  evidence_type: implemented
- type: IMPLEMENTS
  target: service.ftgo.user
  role: persistence_write
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/user/src/data_access/repository/db_repository.py
  symbol: data_access.repository.db_repository.DatabaseRepository.insert
  line_start: 74
  line_end: 74
  evidence_type: implemented
inbound_relations:
- type: CONTAINS
  source: flow.ftgo.gateway.post.auth.register
  role: persistence_write
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/user/src/data_access/repository/db_repository.py
  symbol: data_access.repository.db_repository.DatabaseRepository.insert
  line_start: 74
  line_end: 74
  evidence_type: implemented
- type: PRECEDES
  source: step.ftgo.gateway.post.auth.register.consume.user.user.profile.create
  established_by: consumer call trace
  call_depth: 2
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/user/src/data_access/repository/db_repository.py
  symbol: data_access.repository.db_repository.DatabaseRepository.insert
  line_start: 74
  line_end: 74
  evidence_type: implemented
attributes:
  operation: add_all
  persistence_library: asyncpg_client
  resolution: model_map_enumeration
  call_depth: 2
  event_identity: user.profile.create
---

# write table.ftgo.user.user-profile

Canonical execution step extracted from call evidence in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Role: `persistence_write`
- Flow: `flow.ftgo.gateway.post.auth.register`
- Performed by: `service.ftgo.user`
- Anchored on: `table.ftgo.user.user-profile` (`Table`)
- Declared in: `backend/microservices/user/src/data_access/repository/db_repository.py` (lines 74-74)
- Evidence class: `implemented`

## Call trace

- `application.profile.ProfileService.register` -> `domain.manager.UserManager.register` (`backend/microservices/user/src/application/profile.py:19`)
- `domain.manager.UserManager.register` -> `data_access.repository.db_repository.DatabaseRepository.insert` (`backend/microservices/user/src/domain/manager.py:78`)

## Review notes

This approved canonical page records a source-backed execution step. The step exists because a concrete call site proves it, and its ordering edges carry that call site as evidence.

