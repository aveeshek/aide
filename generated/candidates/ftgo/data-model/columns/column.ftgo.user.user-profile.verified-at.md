---
id: column.ftgo.user.user-profile.verified-at
kind: Column
type: Column
title: verified_at
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
declared_type: DateTime(timezone=True)
annotation: Mapped[Optional[DateTime]]
nullable: true
has_default: false
has_server_default: false
constructor: mapped_column
line: 21
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/user/src/data_access/models/profile.py
  symbol: data_access.models.profile.Profile.verified_at
  line_start: 21
  line_end: 21
  evidence_type: implemented
inbound_relations:
- type: CONTAINS
  source: table.ftgo.user.user-profile
  column_name: verified_at
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/user/src/data_access/models/profile.py
  symbol: data_access.models.profile.Profile.verified_at
  line_start: 21
  line_end: 21
  evidence_type: implemented
---

# user_profile.verified_at

Candidate column extracted from an ORM mapping in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Table: `table.ftgo.user.user-profile`
- Declared by: `data_access.models.profile.Profile`
- Declared in: `backend/microservices/user/src/data_access/models/profile.py` (lines 21-21)
- Evidence class: `implemented`

## Review notes

This page is a candidate awaiting review. Only the presence of a default is recorded, never its value.

