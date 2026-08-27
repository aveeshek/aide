---
id: schema.ftgo.gateway.application.schemas.account.profile.userinfo
kind: Schema
type: Schema
title: UserInfo
status: approved
review_status: approved
candidate_of: fastapi-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: fastapi
service: service.ftgo.gateway
owner: aide-ftgo-cohort
qualified_name: application.schemas.account.profile.UserInfo
pydantic_confirmed: false
base_resolution: external_base
bases:
- UserInfoMixin
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/schemas/account/profile.py
  symbol: application.schemas.account.profile.UserInfo
  line_start: 28
  line_end: 29
  evidence_type: implemented
inbound_relations:
- type: USES_SCHEMA
  source: endpoint.ftgo.gateway.put.profile.update
  role: response
  symbol: application.routes.account.profile.update_profile
  type_expression: UserInfo
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/account/profile.py
  line_start: 85
  line_end: 85
  evidence_type: implemented
fields:
- name: role
  annotation: str
  default_expression: Field(..., min_length=1, max_length=20)
  line: 29
---

# UserInfo

Candidate schema extracted from a class definition in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Qualified name: `application.schemas.account.profile.UserInfo`
- Declared in: `backend/gateway/src/application/schemas/account/profile.py` (lines 28-29)
- Pydantic BaseModel confirmed in source: `False`
- Base resolution: `external_base`
- Used as: `response`
- Evidence class: `implemented`

## Review notes

This page is a candidate awaiting review. Field annotations are recorded as source text and never evaluated; credential-shaped defaults are redacted at extraction time.

