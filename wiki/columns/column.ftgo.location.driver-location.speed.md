---
id: column.ftgo.location.driver-location.speed
kind: Column
type: Column
title: speed
status: approved
review_status: approved
candidate_of: data-model-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: data-model
service: service.ftgo.location
owner: aide-ftgo-cohort
table: table.ftgo.location.driver-location
table_name: driver_location
declaring_class: data_access.models.driver_location.DriverLocation
primary_key: false
declared_type: Float(precision=32)
annotation: Mapped[Optional[float]]
nullable: true
has_default: false
has_server_default: false
constructor: mapped_column
line: 20
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/location/src/data_access/models/driver_location.py
  symbol: data_access.models.driver_location.DriverLocation.speed
  line_start: 20
  line_end: 20
  evidence_type: implemented
inbound_relations:
- type: CONTAINS
  source: table.ftgo.location.driver-location
  column_name: speed
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/location/src/data_access/models/driver_location.py
  symbol: data_access.models.driver_location.DriverLocation.speed
  line_start: 20
  line_end: 20
  evidence_type: implemented
---

# driver_location.speed

Canonical column extracted from an ORM mapping in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Table: `table.ftgo.location.driver-location`
- Declared by: `data_access.models.driver_location.DriverLocation`
- Declared in: `backend/microservices/location/src/data_access/models/driver_location.py` (lines 20-20)
- Evidence class: `implemented`

## Review notes

This page was promoted to canonical knowledge after review. Only the presence of a default is recorded, never its value.

