---
id: step.ftgo.gateway.post.auth.login.read.ftgo.user.user-profile
kind: FlowStep
type: FlowStep
title: read table.ftgo.user.user-profile
status: approved
review_status: approved
candidate_of: user-flow-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: user-flow
owner: aide-ftgo-cohort
role: persistence_read
flow: flow.ftgo.gateway.post.auth.login
service: service.ftgo.user
derived_from: table.ftgo.user.user-profile
derived_from_kind: Table
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/user/src/data_access/repository/db_repository.py
  symbol: data_access.repository.db_repository.DatabaseRepository.update
  line_start: 97
  line_end: 97
  evidence_type: implemented
traces:
- target: data_access.repository.db_repository.DatabaseRepository.update
  depth: 2
  hops:
  - caller: application.profile.ProfileService.login
    callee: domain.manager.UserManager.login
    call: UserManager.login
    repository: ftgo
    commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
    path: backend/microservices/user/src/application/profile.py
    symbol: application.profile.ProfileService.login
    line_start: 55
    line_end: 60
    evidence_type: implemented
  - caller: domain.manager.UserManager.login
    callee: data_access.repository.db_repository.DatabaseRepository.update
    call: DatabaseRepository.update
    repository: ftgo
    commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
    path: backend/microservices/user/src/domain/manager.py
    symbol: domain.manager.UserManager.login
    line_start: 151
    line_end: 151
    evidence_type: implemented
relations:
- type: DERIVED_FROM
  target: table.ftgo.user.user-profile
  anchor_kind: Table
  role: persistence_read
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/user/src/data_access/repository/db_repository.py
  symbol: data_access.repository.db_repository.DatabaseRepository.update
  line_start: 97
  line_end: 97
  evidence_type: implemented
- type: IMPLEMENTS
  target: service.ftgo.user
  role: persistence_read
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/user/src/data_access/repository/db_repository.py
  symbol: data_access.repository.db_repository.DatabaseRepository.update
  line_start: 97
  line_end: 97
  evidence_type: implemented
inbound_relations:
- type: CONTAINS
  source: flow.ftgo.gateway.post.auth.login
  role: persistence_read
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/user/src/data_access/repository/db_repository.py
  symbol: data_access.repository.db_repository.DatabaseRepository.update
  line_start: 97
  line_end: 97
  evidence_type: implemented
- type: PRECEDES
  source: step.ftgo.gateway.post.auth.login.consume.user.user.profile.login
  established_by: consumer call trace
  call_depth: 2
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/user/src/data_access/repository/db_repository.py
  symbol: data_access.repository.db_repository.DatabaseRepository.update
  line_start: 97
  line_end: 97
  evidence_type: implemented
attributes:
  operation: select
  persistence_library: sqlalchemy
  resolution: model_map_enumeration
  call_depth: 2
  event_identity: user.profile.login
---

# read table.ftgo.user.user-profile

Canonical execution step extracted from call evidence in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Role: `persistence_read`
- Flow: `flow.ftgo.gateway.post.auth.login`
- Performed by: `service.ftgo.user`
- Anchored on: `table.ftgo.user.user-profile` (`Table`)
- Declared in: `backend/microservices/user/src/data_access/repository/db_repository.py` (lines 97-97)
- Evidence class: `implemented`

## Call trace

- `application.profile.ProfileService.login` -> `domain.manager.UserManager.login` (`backend/microservices/user/src/application/profile.py:55`)
- `domain.manager.UserManager.login` -> `data_access.repository.db_repository.DatabaseRepository.update` (`backend/microservices/user/src/domain/manager.py:151`)

## Review notes

This approved canonical page records a source-backed execution step. The step exists because a concrete call site proves it, and its ordering edges carry that call site as evidence.

