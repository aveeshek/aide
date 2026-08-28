---
id: column.ftgo.user.customer-address.created-at
kind: Column
type: Column
title: created_at
status: candidate
review_status: pending
candidate_of: data-model-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: data-model
service: service.ftgo.user
owner: aide-ftgo-cohort
table: table.ftgo.user.customer-address
table_name: customer_address
declaring_class: data_access.models.base.Base
primary_key: false
declared_type: DateTime(timezone=True)
annotation: Mapped[datetime]
has_default: false
has_server_default: true
constructor: mapped_column
line: 19
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/user/src/data_access/models/base.py
  symbol: data_access.models.base.Base.created_at
  line_start: 19
  line_end: 21
  evidence_type: implemented
inbound_relations:
- type: CONTAINS
  source: table.ftgo.user.customer-address
  column_name: created_at
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/user/src/data_access/models/base.py
  symbol: data_access.models.base.Base.created_at
  line_start: 19
  line_end: 21
  evidence_type: implemented
---

# customer_address.created_at

Candidate column extracted from an ORM mapping in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Table: `table.ftgo.user.customer-address`
- Declared by: `data_access.models.base.Base`
- Declared in: `backend/microservices/user/src/data_access/models/base.py` (lines 19-21)
- Evidence class: `implemented`

## Review notes

This page is a candidate awaiting review. Only the presence of a default is recorded, never its value.

