---
id: step.ftgo.gateway.put.profile.update.write.ftgo.user.customer-address
kind: FlowStep
type: FlowStep
title: write table.ftgo.user.customer-address
status: candidate
review_status: pending
candidate_of: user-flow-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: user-flow
owner: aide-ftgo-cohort
role: persistence_write
flow: flow.ftgo.gateway.put.profile.update
service: service.ftgo.user
derived_from: table.ftgo.user.customer-address
derived_from_kind: Table
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/user/src/data_access/repository/db_repository.py
  symbol: data_access.repository.db_repository.DatabaseRepository.update
  line_start: 105
  line_end: 105
  evidence_type: implemented
traces:
- target: data_access.repository.db_repository.DatabaseRepository.update
  depth: 2
  hops:
  - caller: application.profile.ProfileService.update_profile
    callee: domain.user.User.update_profile_information
    call: user.update_profile_information
    repository: ftgo
    commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
    path: backend/microservices/user/src/application/profile.py
    symbol: application.profile.ProfileService.update_profile
    line_start: 86
    line_end: 89
    evidence_type: implemented
  - caller: domain.user.User.update_profile_information
    callee: data_access.repository.db_repository.DatabaseRepository.update
    call: DatabaseRepository.update
    repository: ftgo
    commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
    path: backend/microservices/user/src/domain/user.py
    symbol: domain.user.User.update_profile_information
    line_start: 107
    line_end: 111
    evidence_type: implemented
relations:
- type: DERIVED_FROM
  target: table.ftgo.user.customer-address
  anchor_kind: Table
  role: persistence_write
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/user/src/data_access/repository/db_repository.py
  symbol: data_access.repository.db_repository.DatabaseRepository.update
  line_start: 105
  line_end: 105
  evidence_type: implemented
- type: IMPLEMENTS
  target: service.ftgo.user
  role: persistence_write
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/user/src/data_access/repository/db_repository.py
  symbol: data_access.repository.db_repository.DatabaseRepository.update
  line_start: 105
  line_end: 105
  evidence_type: implemented
inbound_relations:
- type: CONTAINS
  source: flow.ftgo.gateway.put.profile.update
  role: persistence_write
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/user/src/data_access/repository/db_repository.py
  symbol: data_access.repository.db_repository.DatabaseRepository.update
  line_start: 105
  line_end: 105
  evidence_type: implemented
- type: PRECEDES
  source: step.ftgo.gateway.put.profile.update.consume.user.user.profile.update-profile
  established_by: consumer call trace
  call_depth: 2
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/user/src/data_access/repository/db_repository.py
  symbol: data_access.repository.db_repository.DatabaseRepository.update
  line_start: 105
  line_end: 105
  evidence_type: implemented
attributes:
  operation: add
  persistence_library: asyncpg_client
  resolution: model_map_enumeration
  call_depth: 2
  event_identity: user.profile.update_profile
---

# write table.ftgo.user.customer-address

Candidate execution step extracted from call evidence in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Role: `persistence_write`
- Flow: `flow.ftgo.gateway.put.profile.update`
- Performed by: `service.ftgo.user`
- Anchored on: `table.ftgo.user.customer-address` (`Table`)
- Declared in: `backend/microservices/user/src/data_access/repository/db_repository.py` (lines 105-105)
- Evidence class: `implemented`

## Call trace

- `application.profile.ProfileService.update_profile` -> `domain.user.User.update_profile_information` (`backend/microservices/user/src/application/profile.py:86`)
- `domain.user.User.update_profile_information` -> `data_access.repository.db_repository.DatabaseRepository.update` (`backend/microservices/user/src/domain/user.py:107`)

## Review notes

This page is a candidate awaiting review. The step exists because a concrete call site proves it, and its ordering edges carry that call site as evidence.

