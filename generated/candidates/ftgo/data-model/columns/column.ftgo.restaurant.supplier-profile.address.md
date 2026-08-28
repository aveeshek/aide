---
id: column.ftgo.restaurant.supplier-profile.address
kind: Column
type: Column
title: address
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
declared_type: String
nullable: false
has_default: false
has_server_default: false
constructor: Column
line: 17
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/restaurant/src/models/supplier.py
  symbol: models.supplier.Supplier.address
  line_start: 17
  line_end: 17
  evidence_type: implemented
inbound_relations:
- type: CONTAINS
  source: table.ftgo.restaurant.supplier-profile
  column_name: address
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/restaurant/src/models/supplier.py
  symbol: models.supplier.Supplier.address
  line_start: 17
  line_end: 17
  evidence_type: implemented
---

# supplier_profile.address

Candidate column extracted from an ORM mapping in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Table: `table.ftgo.restaurant.supplier-profile`
- Declared by: `models.supplier.Supplier`
- Declared in: `backend/microservices/restaurant/src/models/supplier.py` (lines 17-17)
- Evidence class: `implemented`

## Review notes

This page is a candidate awaiting review. Only the presence of a default is recorded, never its value.

