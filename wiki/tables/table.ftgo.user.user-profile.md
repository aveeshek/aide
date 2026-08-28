---
id: table.ftgo.user.user-profile
kind: Table
type: Table
title: user_profile
status: approved
review_status: approved
candidate_of: data-model-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: data-model
service: service.ftgo.user
owner: aide-ftgo-cohort
table_name: user_profile
storage_engine: postgresql
persistence_library: sqlalchemy
database: database.ftgo.user-postgres
model_class: data_access.models.profile.Profile
primary_key:
- id
orm_relationships:
- attribute: addresses
  line: 24
  target: '"Address"'
  back_populates: profile
- attribute: vehicle_info
  line: 27
  target: '"VehicleInfo"'
  back_populates: driver
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/user/src/data_access/models/profile.py
  symbol: data_access.models.profile.Profile
  line_start: 10
  line_end: 61
  evidence_type: implemented
inbound_relations:
- type: CONTAINS
  source: database.ftgo.user-postgres
  table_name: user_profile
  storage_engine: postgresql
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/user/src/data_access/models/profile.py
  symbol: data_access.models.profile.Profile
  line_start: 10
  line_end: 61
  evidence_type: implemented
- type: READS
  source: service.ftgo.user
  role: read
  target_kind: Table
  persistence_library: sqlalchemy
  call_site_count: 3
  call_sites:
  - operation: select
    resolution: model_map_enumeration
    call: select(model_class)
    repository: ftgo
    commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
    path: backend/microservices/user/src/data_access/repository/db_repository.py
    symbol: data_access.repository.db_repository.DatabaseRepository.fetch
    line_start: 55
    line_end: 55
    evidence_type: implemented
  - operation: select
    resolution: model_map_enumeration
    call: select(model_class)
    repository: ftgo
    commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
    path: backend/microservices/user/src/data_access/repository/db_repository.py
    symbol: data_access.repository.db_repository.DatabaseRepository.update
    line_start: 97
    line_end: 97
    evidence_type: implemented
  - operation: select
    resolution: model_map_enumeration
    call: select(model_class)
    repository: ftgo
    commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
    path: backend/microservices/user/src/data_access/repository/db_repository.py
    symbol: data_access.repository.db_repository.DatabaseRepository.delete
    line_start: 121
    line_end: 121
    evidence_type: implemented
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/user/src/data_access/repository/db_repository.py
  symbol: data_access.repository.db_repository.DatabaseRepository.fetch
  line_start: 55
  line_end: 55
  evidence_type: implemented
- type: WRITES
  source: service.ftgo.user
  role: write
  target_kind: Table
  persistence_library: asyncpg_client
  call_site_count: 3
  call_sites:
  - operation: add_all
    resolution: model_map_enumeration
    call: session.add_all(model_instances)
    repository: ftgo
    commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
    path: backend/microservices/user/src/data_access/repository/db_repository.py
    symbol: data_access.repository.db_repository.DatabaseRepository.insert
    line_start: 74
    line_end: 74
    evidence_type: implemented
  - operation: add
    resolution: model_map_enumeration
    call: session.add(record)
    repository: ftgo
    commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
    path: backend/microservices/user/src/data_access/repository/db_repository.py
    symbol: data_access.repository.db_repository.DatabaseRepository.update
    line_start: 105
    line_end: 105
    evidence_type: implemented
  - operation: delete
    resolution: model_map_enumeration
    call: session.delete(record)
    repository: ftgo
    commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
    path: backend/microservices/user/src/data_access/repository/db_repository.py
    symbol: data_access.repository.db_repository.DatabaseRepository.delete
    line_start: 127
    line_end: 127
    evidence_type: implemented
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/user/src/data_access/repository/db_repository.py
  symbol: data_access.repository.db_repository.DatabaseRepository.insert
  line_start: 74
  line_end: 74
  evidence_type: implemented
- type: DEPENDS_ON
  source: table.ftgo.user.customer-address
  foreign_key_column: user_id
  references: user_profile.id
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/user/src/data_access/models/address.py
  symbol: data_access.models.address.Address
  line_start: 8
  line_end: 51
  evidence_type: implemented
- type: DEPENDS_ON
  source: table.ftgo.user.vehicle-info
  foreign_key_column: driver_id
  references: user_profile.id
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/user/src/data_access/models/vehicle.py
  symbol: data_access.models.vehicle.VehicleInfo
  line_start: 7
  line_end: 32
  evidence_type: implemented
relations:
- type: CONTAINS
  target: column.ftgo.user.user-profile.created-at
  column_name: created_at
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/user/src/data_access/models/base.py
  symbol: data_access.models.base.Base.created_at
  line_start: 19
  line_end: 21
  evidence_type: implemented
- type: CONTAINS
  target: column.ftgo.user.user-profile.email
  column_name: email
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/user/src/data_access/models/profile.py
  symbol: data_access.models.profile.Profile.email
  line_start: 19
  line_end: 19
  evidence_type: implemented
- type: CONTAINS
  target: column.ftgo.user.user-profile.first-name
  column_name: first_name
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/user/src/data_access/models/profile.py
  symbol: data_access.models.profile.Profile.first_name
  line_start: 16
  line_end: 16
  evidence_type: implemented
- type: CONTAINS
  target: column.ftgo.user.user-profile.gender
  column_name: gender
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/user/src/data_access/models/profile.py
  symbol: data_access.models.profile.Profile.gender
  line_start: 18
  line_end: 18
  evidence_type: implemented
- type: CONTAINS
  target: column.ftgo.user.user-profile.hashed-password
  column_name: hashed_password
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/user/src/data_access/models/profile.py
  symbol: data_access.models.profile.Profile.hashed_password
  line_start: 14
  line_end: 14
  evidence_type: implemented
- type: CONTAINS
  target: column.ftgo.user.user-profile.id
  column_name: id
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/user/src/data_access/models/base.py
  symbol: data_access.models.base.Base.id
  line_start: 16
  line_end: 18
  evidence_type: implemented
- type: CONTAINS
  target: column.ftgo.user.user-profile.last-login-time
  column_name: last_login_time
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/user/src/data_access/models/profile.py
  symbol: data_access.models.profile.Profile.last_login_time
  line_start: 22
  line_end: 22
  evidence_type: implemented
- type: CONTAINS
  target: column.ftgo.user.user-profile.last-name
  column_name: last_name
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/user/src/data_access/models/profile.py
  symbol: data_access.models.profile.Profile.last_name
  line_start: 17
  line_end: 17
  evidence_type: implemented
- type: CONTAINS
  target: column.ftgo.user.user-profile.national-id
  column_name: national_id
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/user/src/data_access/models/profile.py
  symbol: data_access.models.profile.Profile.national_id
  line_start: 15
  line_end: 15
  evidence_type: implemented
- type: CONTAINS
  target: column.ftgo.user.user-profile.phone-number
  column_name: phone_number
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/user/src/data_access/models/profile.py
  symbol: data_access.models.profile.Profile.phone_number
  line_start: 13
  line_end: 13
  evidence_type: implemented
- type: CONTAINS
  target: column.ftgo.user.user-profile.role
  column_name: role
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/user/src/data_access/models/profile.py
  symbol: data_access.models.profile.Profile.role
  line_start: 20
  line_end: 20
  evidence_type: implemented
- type: CONTAINS
  target: column.ftgo.user.user-profile.updated-at
  column_name: updated_at
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/user/src/data_access/models/base.py
  symbol: data_access.models.base.Base.updated_at
  line_start: 22
  line_end: 24
  evidence_type: implemented
- type: CONTAINS
  target: column.ftgo.user.user-profile.verified-at
  column_name: verified_at
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/user/src/data_access/models/profile.py
  symbol: data_access.models.profile.Profile.verified_at
  line_start: 21
  line_end: 21
  evidence_type: implemented
attributes:
  persistence_role: relational_table
  declarative_base: DeclarativeBase
  column_count: 13
---

# user_profile

Canonical relational table extracted from an ORM mapping in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Owning service: `service.ftgo.user`
- Database: `database.ftgo.user-postgres`
- Mapped class: `data_access.models.profile.Profile`
- Persistence library: `sqlalchemy`
- Declared in: `backend/microservices/user/src/data_access/models/profile.py` (lines 10-61)
- Evidence class: `implemented`

## Review notes

This page was promoted to canonical knowledge after review. The physical table name comes from an explicit `__tablename__`; column metadata is read from the mapping and no default value is ever evaluated or emitted.

