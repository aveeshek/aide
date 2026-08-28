---
id: column.ftgo.user.vehicle-info.plate-number
kind: Column
type: Column
title: plate_number
status: candidate
review_status: pending
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
has_default: false
has_server_default: false
constructor: mapped_column
line: 11
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/user/src/data_access/models/vehicle.py
  symbol: data_access.models.vehicle.VehicleInfo.plate_number
  line_start: 11
  line_end: 11
  evidence_type: implemented
inbound_relations:
- type: CONTAINS
  source: table.ftgo.user.vehicle-info
  column_name: plate_number
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/user/src/data_access/models/vehicle.py
  symbol: data_access.models.vehicle.VehicleInfo.plate_number
  line_start: 11
  line_end: 11
  evidence_type: implemented
---

# vehicle_info.plate_number

Candidate column extracted from an ORM mapping in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Table: `table.ftgo.user.vehicle-info`
- Declared by: `data_access.models.vehicle.VehicleInfo`
- Declared in: `backend/microservices/user/src/data_access/models/vehicle.py` (lines 11-11)
- Evidence class: `implemented`

## Review notes

This page is a candidate awaiting review. Only the presence of a default is recorded, never its value.

