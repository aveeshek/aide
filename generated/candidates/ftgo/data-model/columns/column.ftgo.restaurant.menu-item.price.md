---
id: column.ftgo.restaurant.menu-item.price
kind: Column
type: Column
title: price
status: candidate
review_status: pending
candidate_of: data-model-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: data-model
service: service.ftgo.restaurant
owner: aide-ftgo-cohort
table: table.ftgo.restaurant.menu-item
table_name: menu_item
declaring_class: models.menu.MenuItem
primary_key: false
declared_type: Float
nullable: false
has_default: false
has_server_default: false
constructor: Column
line: 14
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/restaurant/src/models/menu.py
  symbol: models.menu.MenuItem.price
  line_start: 14
  line_end: 14
  evidence_type: implemented
inbound_relations:
- type: CONTAINS
  source: table.ftgo.restaurant.menu-item
  column_name: price
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/restaurant/src/models/menu.py
  symbol: models.menu.MenuItem.price
  line_start: 14
  line_end: 14
  evidence_type: implemented
---

# menu_item.price

Candidate column extracted from an ORM mapping in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Table: `table.ftgo.restaurant.menu-item`
- Declared by: `models.menu.MenuItem`
- Declared in: `backend/microservices/restaurant/src/models/menu.py` (lines 14-14)
- Evidence class: `implemented`

## Review notes

This page is a candidate awaiting review. Only the presence of a default is recorded, never its value.

