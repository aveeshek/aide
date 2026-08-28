---
id: table.ftgo.location.driver-location
kind: Table
type: Table
title: driver_location
status: candidate
review_status: pending
candidate_of: data-model-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: data-model
service: service.ftgo.location
owner: aide-ftgo-cohort
table_name: driver_location
storage_engine: postgresql
persistence_library: sqlalchemy
database: database.ftgo.location-postgres
model_class: data_access.models.driver_location.DriverLocation
primary_key:
- id
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/location/src/data_access/models/driver_location.py
  symbol: data_access.models.driver_location.DriverLocation
  line_start: 11
  line_end: 49
  evidence_type: implemented
inbound_relations:
- type: CONTAINS
  source: database.ftgo.location-postgres
  table_name: driver_location
  storage_engine: postgresql
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/location/src/data_access/models/driver_location.py
  symbol: data_access.models.driver_location.DriverLocation
  line_start: 11
  line_end: 49
  evidence_type: implemented
- type: READS
  source: service.ftgo.location
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
    path: backend/microservices/location/src/data_access/repository/db_repository.py
    symbol: data_access.repository.db_repository.DatabaseRepository.fetch
    line_start: 53
    line_end: 53
    evidence_type: implemented
  - operation: select
    resolution: model_map_enumeration
    call: select(model_class)
    repository: ftgo
    commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
    path: backend/microservices/location/src/data_access/repository/db_repository.py
    symbol: data_access.repository.db_repository.DatabaseRepository.update
    line_start: 95
    line_end: 95
    evidence_type: implemented
  - operation: select
    resolution: model_map_enumeration
    call: select(model_class)
    repository: ftgo
    commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
    path: backend/microservices/location/src/data_access/repository/db_repository.py
    symbol: data_access.repository.db_repository.DatabaseRepository.delete
    line_start: 119
    line_end: 119
    evidence_type: implemented
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/location/src/data_access/repository/db_repository.py
  symbol: data_access.repository.db_repository.DatabaseRepository.fetch
  line_start: 53
  line_end: 53
  evidence_type: implemented
- type: WRITES
  source: service.ftgo.location
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
    path: backend/microservices/location/src/data_access/repository/db_repository.py
    symbol: data_access.repository.db_repository.DatabaseRepository.insert
    line_start: 72
    line_end: 72
    evidence_type: implemented
  - operation: add
    resolution: model_map_enumeration
    call: session.add(record)
    repository: ftgo
    commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
    path: backend/microservices/location/src/data_access/repository/db_repository.py
    symbol: data_access.repository.db_repository.DatabaseRepository.update
    line_start: 103
    line_end: 103
    evidence_type: implemented
  - operation: delete
    resolution: model_map_enumeration
    call: session.delete(record)
    repository: ftgo
    commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
    path: backend/microservices/location/src/data_access/repository/db_repository.py
    symbol: data_access.repository.db_repository.DatabaseRepository.delete
    line_start: 125
    line_end: 125
    evidence_type: implemented
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/location/src/data_access/repository/db_repository.py
  symbol: data_access.repository.db_repository.DatabaseRepository.insert
  line_start: 72
  line_end: 72
  evidence_type: implemented
relations:
- type: CHANGED_BY
  target: migration.ftgo.location.9fafa9afc18d
  revision: 9fafa9afc18d
  operations:
  - create_table
  - drop_table
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/location/migrations/versions/9fafa9afc18d_initial.py
  symbol: migrations.versions.9fafa9afc18d_initial.revision
  line_start: 1
  line_end: 40
  evidence_type: implemented
- type: CONTAINS
  target: column.ftgo.location.driver-location.accuracy
  column_name: accuracy
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/location/src/data_access/models/driver_location.py
  symbol: data_access.models.driver_location.DriverLocation.accuracy
  line_start: 19
  line_end: 19
  evidence_type: implemented
- type: CONTAINS
  target: column.ftgo.location.driver-location.bearing
  column_name: bearing
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/location/src/data_access/models/driver_location.py
  symbol: data_access.models.driver_location.DriverLocation.bearing
  line_start: 21
  line_end: 21
  evidence_type: implemented
- type: CONTAINS
  target: column.ftgo.location.driver-location.created-at
  column_name: created_at
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/location/src/data_access/models/base.py
  symbol: data_access.models.base.Base.created_at
  line_start: 19
  line_end: 21
  evidence_type: implemented
- type: CONTAINS
  target: column.ftgo.location.driver-location.driver-id
  column_name: driver_id
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/location/src/data_access/models/driver_location.py
  symbol: data_access.models.driver_location.DriverLocation.driver_id
  line_start: 14
  line_end: 14
  evidence_type: implemented
- type: CONTAINS
  target: column.ftgo.location.driver-location.id
  column_name: id
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/location/src/data_access/models/base.py
  symbol: data_access.models.base.Base.id
  line_start: 16
  line_end: 18
  evidence_type: implemented
- type: CONTAINS
  target: column.ftgo.location.driver-location.latitude
  column_name: latitude
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/location/src/data_access/models/driver_location.py
  symbol: data_access.models.driver_location.DriverLocation.latitude
  line_start: 16
  line_end: 16
  evidence_type: implemented
- type: CONTAINS
  target: column.ftgo.location.driver-location.longitude
  column_name: longitude
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/location/src/data_access/models/driver_location.py
  symbol: data_access.models.driver_location.DriverLocation.longitude
  line_start: 17
  line_end: 17
  evidence_type: implemented
- type: CONTAINS
  target: column.ftgo.location.driver-location.speed
  column_name: speed
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/location/src/data_access/models/driver_location.py
  symbol: data_access.models.driver_location.DriverLocation.speed
  line_start: 20
  line_end: 20
  evidence_type: implemented
- type: CONTAINS
  target: column.ftgo.location.driver-location.timestamp
  column_name: timestamp
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/location/src/data_access/models/driver_location.py
  symbol: data_access.models.driver_location.DriverLocation.timestamp
  line_start: 23
  line_end: 23
  evidence_type: implemented
- type: CONTAINS
  target: column.ftgo.location.driver-location.updated-at
  column_name: updated_at
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/location/src/data_access/models/base.py
  symbol: data_access.models.base.Base.updated_at
  line_start: 22
  line_end: 24
  evidence_type: implemented
attributes:
  persistence_role: relational_table
  declarative_base: DeclarativeBase
  column_count: 10
---

# driver_location

Candidate relational table extracted from an ORM mapping in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Owning service: `service.ftgo.location`
- Database: `database.ftgo.location-postgres`
- Mapped class: `data_access.models.driver_location.DriverLocation`
- Persistence library: `sqlalchemy`
- Declared in: `backend/microservices/location/src/data_access/models/driver_location.py` (lines 11-49)
- Evidence class: `implemented`

## Review notes

This page is a candidate awaiting review. The physical table name comes from an explicit `__tablename__`; column metadata is read from the mapping and no default value is ever evaluated or emitted.

