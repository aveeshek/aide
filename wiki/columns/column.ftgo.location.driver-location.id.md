---
id: column.ftgo.location.driver-location.id
kind: Column
type: Column
title: id
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
declaring_class: data_access.models.base.Base
primary_key: true
declared_type: sqlalchemy.String
annotation: Mapped[str]
has_default: true
has_server_default: false
constructor: mapped_column
line: 16
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/location/src/data_access/models/base.py
  symbol: data_access.models.base.Base.id
  line_start: 16
  line_end: 18
  evidence_type: implemented
inbound_relations:
- type: CONTAINS
  source: table.ftgo.location.driver-location
  column_name: id
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/location/src/data_access/models/base.py
  symbol: data_access.models.base.Base.id
  line_start: 16
  line_end: 18
  evidence_type: implemented
---

# driver_location.id

Canonical column extracted from an ORM mapping in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Table: `table.ftgo.location.driver-location`
- Declared by: `data_access.models.base.Base`
- Declared in: `backend/microservices/location/src/data_access/models/base.py` (lines 16-18)
- Evidence class: `implemented`

## Review notes

This page was promoted to canonical knowledge after review. Only the presence of a default is recorded, never its value.

