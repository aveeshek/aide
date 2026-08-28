---
id: column.ftgo.user.user-profile.phone-number
kind: Column
type: Column
title: phone_number
status: candidate
review_status: pending
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
line: 13
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/user/src/data_access/models/profile.py
  symbol: data_access.models.profile.Profile.phone_number
  line_start: 13
  line_end: 13
  evidence_type: implemented
inbound_relations:
- type: CONTAINS
  source: table.ftgo.user.user-profile
  column_name: phone_number
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/user/src/data_access/models/profile.py
  symbol: data_access.models.profile.Profile.phone_number
  line_start: 13
  line_end: 13
  evidence_type: implemented
---

# user_profile.phone_number

Candidate column extracted from an ORM mapping in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Table: `table.ftgo.user.user-profile`
- Declared by: `data_access.models.profile.Profile`
- Declared in: `backend/microservices/user/src/data_access/models/profile.py` (lines 13-13)
- Evidence class: `implemented`

## Review notes

This page is a candidate awaiting review. Only the presence of a default is recorded, never its value.

