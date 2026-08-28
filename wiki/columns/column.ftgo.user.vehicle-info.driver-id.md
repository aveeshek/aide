---
id: column.ftgo.user.vehicle-info.driver-id
kind: Column
type: Column
title: driver_id
status: approved
review_status: approved
candidate_of: data-model-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: data-model
service: service.ftgo.user
owner: aide-ftgo-cohort
table: table.ftgo.user.vehicle-info
table_name: vehicle_info
declaring_class: data_access.models.vehicle.VehicleInfo
primary_key: false
declared_type: String
annotation: Mapped[str]
nullable: false
foreign_key: user_profile.id
has_default: false
has_server_default: false
constructor: mapped_column
line: 10
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/user/src/data_access/models/vehicle.py
  symbol: data_access.models.vehicle.VehicleInfo.driver_id
  line_start: 10
  line_end: 10
  evidence_type: implemented
inbound_relations:
- type: CONTAINS
  source: table.ftgo.user.vehicle-info
  column_name: driver_id
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/user/src/data_access/models/vehicle.py
  symbol: data_access.models.vehicle.VehicleInfo.driver_id
  line_start: 10
  line_end: 10
  evidence_type: implemented
---

# vehicle_info.driver_id

Canonical column extracted from an ORM mapping in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Table: `table.ftgo.user.vehicle-info`
- Declared by: `data_access.models.vehicle.VehicleInfo`
- Declared in: `backend/microservices/user/src/data_access/models/vehicle.py` (lines 10-10)
- Evidence class: `implemented`

## Review notes

This page was promoted to canonical knowledge after review. Only the presence of a default is recorded, never its value.

