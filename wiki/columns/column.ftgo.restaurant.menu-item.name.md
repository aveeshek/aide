---
id: column.ftgo.restaurant.menu-item.name
kind: Column
type: Column
title: name
status: approved
review_status: approved
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
declared_type: String
nullable: false
has_default: false
has_server_default: false
constructor: Column
line: 13
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/restaurant/src/models/menu.py
  symbol: models.menu.MenuItem.name
  line_start: 13
  line_end: 13
  evidence_type: implemented
inbound_relations:
- type: CONTAINS
  source: table.ftgo.restaurant.menu-item
  column_name: name
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/restaurant/src/models/menu.py
  symbol: models.menu.MenuItem.name
  line_start: 13
  line_end: 13
  evidence_type: implemented
---

# menu_item.name

Canonical column extracted from an ORM mapping in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Table: `table.ftgo.restaurant.menu-item`
- Declared by: `models.menu.MenuItem`
- Declared in: `backend/microservices/restaurant/src/models/menu.py` (lines 13-13)
- Evidence class: `implemented`

## Review notes

This page was promoted to canonical knowledge after review. Only the presence of a default is recorded, never its value.

