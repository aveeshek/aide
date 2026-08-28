---
id: column.ftgo.user.customer-address.longitude
kind: Column
type: Column
title: longitude
status: approved
review_status: approved
candidate_of: data-model-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: data-model
service: service.ftgo.user
owner: aide-ftgo-cohort
table: table.ftgo.user.customer-address
table_name: customer_address
declaring_class: data_access.models.address.Address
primary_key: false
declared_type: Float
annotation: Mapped[float]
nullable: false
has_default: false
has_server_default: false
constructor: mapped_column
line: 13
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/user/src/data_access/models/address.py
  symbol: data_access.models.address.Address.longitude
  line_start: 13
  line_end: 13
  evidence_type: implemented
inbound_relations:
- type: CONTAINS
  source: table.ftgo.user.customer-address
  column_name: longitude
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/user/src/data_access/models/address.py
  symbol: data_access.models.address.Address.longitude
  line_start: 13
  line_end: 13
  evidence_type: implemented
---

# customer_address.longitude

Canonical column extracted from an ORM mapping in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Table: `table.ftgo.user.customer-address`
- Declared by: `data_access.models.address.Address`
- Declared in: `backend/microservices/user/src/data_access/models/address.py` (lines 13-13)
- Evidence class: `implemented`

## Review notes

This page was promoted to canonical knowledge after review. Only the presence of a default is recorded, never its value.

