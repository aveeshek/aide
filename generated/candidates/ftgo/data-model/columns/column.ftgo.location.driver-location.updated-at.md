---
id: column.ftgo.location.driver-location.updated-at
kind: Column
type: Column
title: updated_at
status: candidate
review_status: pending
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
primary_key: false
declared_type: DateTime(timezone=True)
annotation: Mapped[datetime]
has_default: false
has_server_default: true
constructor: mapped_column
line: 22
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/location/src/data_access/models/base.py
  symbol: data_access.models.base.Base.updated_at
  line_start: 22
  line_end: 24
  evidence_type: implemented
inbound_relations:
- type: CONTAINS
  source: table.ftgo.location.driver-location
  column_name: updated_at
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/location/src/data_access/models/base.py
  symbol: data_access.models.base.Base.updated_at
  line_start: 22
  line_end: 24
  evidence_type: implemented
---

# driver_location.updated_at

Candidate column extracted from an ORM mapping in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Table: `table.ftgo.location.driver-location`
- Declared by: `data_access.models.base.Base`
- Declared in: `backend/microservices/location/src/data_access/models/base.py` (lines 22-24)
- Evidence class: `implemented`

## Review notes

This page is a candidate awaiting review. Only the presence of a default is recorded, never its value.

