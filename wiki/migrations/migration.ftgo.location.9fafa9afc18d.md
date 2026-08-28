---
id: migration.ftgo.location.9fafa9afc18d
kind: Migration
type: Migration
title: initial
status: approved
review_status: approved
candidate_of: data-model-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: data-model
service: service.ftgo.location
owner: aide-ftgo-cohort
revision: 9fafa9afc18d
down_revision: null
tool: alembic
touched_tables:
- driver_location
operations:
- create_table
- drop_table
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/location/migrations/versions/9fafa9afc18d_initial.py
  symbol: migrations.versions.9fafa9afc18d_initial.revision
  line_start: 1
  line_end: 40
  evidence_type: implemented
inbound_relations:
- type: CHANGED_BY
  source: table.ftgo.location.driver-location
  revision: 9fafa9afc18d
  operations:
  - create_table
  - drop_table
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/location/migrations/versions/9fafa9afc18d_initial.py
  symbol: migrations.versions.9fafa9afc18d_initial.revision
  line_start: 1
  line_end: 40
  evidence_type: implemented
---

# initial

Canonical migration extracted from an Alembic revision in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Revision: `9fafa9afc18d`
- Previous revision: `none`
- Declared in: `backend/microservices/location/migrations/versions/9fafa9afc18d_initial.py`
- Evidence class: `implemented`

## Review notes

This page was promoted to canonical knowledge after review. Table linkage is created only for tables the migration names explicitly and that exist in scanned source.

