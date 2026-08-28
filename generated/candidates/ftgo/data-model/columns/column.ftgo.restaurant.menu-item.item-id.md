---
id: column.ftgo.restaurant.menu-item.item-id
kind: Column
type: Column
title: item_id
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
primary_key: true
declared_type: String
has_default: true
has_server_default: false
constructor: Column
line: 11
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/restaurant/src/models/menu.py
  symbol: models.menu.MenuItem.item_id
  line_start: 11
  line_end: 11
  evidence_type: implemented
inbound_relations:
- type: CONTAINS
  source: table.ftgo.restaurant.menu-item
  column_name: item_id
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/restaurant/src/models/menu.py
  symbol: models.menu.MenuItem.item_id
  line_start: 11
  line_end: 11
  evidence_type: implemented
---

# menu_item.item_id

Candidate column extracted from an ORM mapping in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Table: `table.ftgo.restaurant.menu-item`
- Declared by: `models.menu.MenuItem`
- Declared in: `backend/microservices/restaurant/src/models/menu.py` (lines 11-11)
- Evidence class: `implemented`

## Review notes

This page is a candidate awaiting review. Only the presence of a default is recorded, never its value.

