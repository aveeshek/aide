---
id: column.ftgo.restaurant.supplier-profile.updated-at
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
service: service.ftgo.restaurant
owner: aide-ftgo-cohort
table: table.ftgo.restaurant.supplier-profile
table_name: supplier_profile
declaring_class: models.supplier.Supplier
primary_key: false
declared_type: DateTime(timezone=True)
has_default: false
has_server_default: true
constructor: Column
line: 23
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/restaurant/src/models/supplier.py
  symbol: models.supplier.Supplier.updated_at
  line_start: 23
  line_end: 23
  evidence_type: implemented
inbound_relations:
- type: CONTAINS
  source: table.ftgo.restaurant.supplier-profile
  column_name: updated_at
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/restaurant/src/models/supplier.py
  symbol: models.supplier.Supplier.updated_at
  line_start: 23
  line_end: 23
  evidence_type: implemented
---

# supplier_profile.updated_at

Candidate column extracted from an ORM mapping in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Table: `table.ftgo.restaurant.supplier-profile`
- Declared by: `models.supplier.Supplier`
- Declared in: `backend/microservices/restaurant/src/models/supplier.py` (lines 23-23)
- Evidence class: `implemented`

## Review notes

This page is a candidate awaiting review. Only the presence of a default is recorded, never its value.

