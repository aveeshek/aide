---
id: schema.ftgo.gateway.application.schemas.account.profile.updateuserrequest
kind: Schema
type: Schema
title: UpdateUserRequest
status: candidate
review_status: pending
candidate_of: fastapi-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: fastapi
service: service.ftgo.gateway
owner: aide-ftgo-cohort
qualified_name: application.schemas.account.profile.UpdateUserRequest
pydantic_confirmed: true
base_resolution: pydantic_basemodel
bases:
- BaseModel
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/schemas/account/profile.py
  symbol: application.schemas.account.profile.UpdateUserRequest
  line_start: 32
  line_end: 34
  evidence_type: implemented
inbound_relations:
- type: USES_SCHEMA
  source: endpoint.ftgo.gateway.put.profile.update
  role: request
  symbol: application.routes.account.profile.update_profile.request_data
  type_expression: UpdateUserRequest
  parameter: request_data
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/account/profile.py
  line_start: 86
  line_end: 86
  evidence_type: implemented
fields:
- name: first_name
  annotation: str
  default_expression: Field(..., min_length=1, max_length=100)
  line: 33
- name: last_name
  annotation: str
  default_expression: Field(..., min_length=1, max_length=100)
  line: 34
---

# UpdateUserRequest

Candidate schema extracted from a class definition in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Qualified name: `application.schemas.account.profile.UpdateUserRequest`
- Declared in: `backend/gateway/src/application/schemas/account/profile.py` (lines 32-34)
- Pydantic BaseModel confirmed in source: `True`
- Base resolution: `pydantic_basemodel`
- Used as: `request`
- Evidence class: `implemented`

## Review notes

This page is a candidate awaiting review. Field annotations are recorded as source text and never evaluated; credential-shaped defaults are redacted at extraction time.

