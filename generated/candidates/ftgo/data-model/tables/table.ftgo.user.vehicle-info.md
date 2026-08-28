---
id: table.ftgo.user.vehicle-info
kind: Table
type: Table
title: vehicle_info
status: candidate
review_status: pending
candidate_of: data-model-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: data-model
service: service.ftgo.user
owner: aide-ftgo-cohort
table_name: vehicle_info
storage_engine: postgresql
persistence_library: sqlalchemy
database: database.ftgo.user-postgres
model_class: data_access.models.vehicle.VehicleInfo
primary_key:
- id
foreign_keys:
- column: driver_id
  references: user_profile.id
orm_relationships:
- attribute: driver
  line: 14
  target: '"Profile"'
  back_populates: vehicle_info
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/user/src/data_access/models/vehicle.py
  symbol: data_access.models.vehicle.VehicleInfo
  line_start: 7
  line_end: 32
  evidence_type: implemented
inbound_relations:
- type: CONTAINS
  source: database.ftgo.user-postgres
  table_name: vehicle_info
  storage_engine: postgresql
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/user/src/data_access/models/vehicle.py
  symbol: data_access.models.vehicle.VehicleInfo
  line_start: 7
  line_end: 32
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
relations:
- type: CONTAINS
  target: column.ftgo.user.vehicle-info.created-at
  column_name: created_at
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/user/src/data_access/models/base.py
  symbol: data_access.models.base.Base.created_at
  line_start: 19
  line_end: 21
  evidence_type: implemented
- type: CONTAINS
  target: column.ftgo.user.vehicle-info.driver-id
  column_name: driver_id
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/user/src/data_access/models/vehicle.py
  symbol: data_access.models.vehicle.VehicleInfo.driver_id
  line_start: 10
  line_end: 10
  evidence_type: implemented
- type: CONTAINS
  target: column.ftgo.user.vehicle-info.id
  column_name: id
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/user/src/data_access/models/base.py
  symbol: data_access.models.base.Base.id
  line_start: 16
  line_end: 18
  evidence_type: implemented
- type: CONTAINS
  target: column.ftgo.user.vehicle-info.license-number
  column_name: license_number
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/user/src/data_access/models/vehicle.py
  symbol: data_access.models.vehicle.VehicleInfo.license_number
  line_start: 12
  line_end: 12
  evidence_type: implemented
- type: CONTAINS
  target: column.ftgo.user.vehicle-info.plate-number
  column_name: plate_number
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/user/src/data_access/models/vehicle.py
  symbol: data_access.models.vehicle.VehicleInfo.plate_number
  line_start: 11
  line_end: 11
  evidence_type: implemented
- type: CONTAINS
  target: column.ftgo.user.vehicle-info.updated-at
  column_name: updated_at
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/user/src/data_access/models/base.py
  symbol: data_access.models.base.Base.updated_at
  line_start: 22
  line_end: 24
  evidence_type: implemented
- type: DEPENDS_ON
  target: table.ftgo.user.user-profile
  foreign_key_column: driver_id
  references: user_profile.id
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/user/src/data_access/models/vehicle.py
  symbol: data_access.models.vehicle.VehicleInfo
  line_start: 7
  line_end: 32
  evidence_type: implemented
attributes:
  persistence_role: relational_table
  declarative_base: DeclarativeBase
  column_count: 6
---

# vehicle_info

Candidate relational table extracted from an ORM mapping in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Owning service: `service.ftgo.user`
- Database: `database.ftgo.user-postgres`
- Mapped class: `data_access.models.vehicle.VehicleInfo`
- Persistence library: `sqlalchemy`
- Declared in: `backend/microservices/user/src/data_access/models/vehicle.py` (lines 7-32)
- Evidence class: `implemented`

## Review notes

This page is a candidate awaiting review. The physical table name comes from an explicit `__tablename__`; column metadata is read from the mapping and no default value is ever evaluated or emitted.

