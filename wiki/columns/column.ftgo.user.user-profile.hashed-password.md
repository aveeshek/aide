---
id: column.ftgo.user.user-profile.hashed-password
kind: Column
type: Column
title: hashed_password
status: approved
review_status: approved
candidate_of: data-model-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: data-model
service: service.ftgo.user
owner: aide-ftgo-cohort
table: table.ftgo.user.user-profile
table_name: user_profile
declaring_class: data_access.models.profile.Profile
primary_key: false
declared_type: String
annotation: Mapped[str]
nullable: false
has_default: false
has_server_default: false
constructor: mapped_column
line: 14
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/user/src/data_access/models/profile.py
  symbol: data_access.models.profile.Profile.hashed_password
  line_start: 14
  line_end: 14
  evidence_type: implemented
inbound_relations:
- type: CONTAINS
  source: table.ftgo.user.user-profile
  column_name: hashed_password
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/user/src/data_access/models/profile.py
  symbol: data_access.models.profile.Profile.hashed_password
  line_start: 14
  line_end: 14
  evidence_type: implemented
---

# user_profile.hashed_password

Canonical column extracted from an ORM mapping in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Table: `table.ftgo.user.user-profile`
- Declared by: `data_access.models.profile.Profile`
- Declared in: `backend/microservices/user/src/data_access/models/profile.py` (lines 14-14)
- Evidence class: `implemented`

## Review notes

This page was promoted to canonical knowledge after review. Only the presence of a default is recorded, never its value.

