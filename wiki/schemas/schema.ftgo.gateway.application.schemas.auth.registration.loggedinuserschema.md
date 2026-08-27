---
id: schema.ftgo.gateway.application.schemas.auth.registration.loggedinuserschema
kind: Schema
type: Schema
title: LoggedInUserSchema
status: approved
review_status: approved
candidate_of: fastapi-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: fastapi
service: service.ftgo.gateway
owner: aide-ftgo-cohort
qualified_name: application.schemas.auth.registration.LoggedInUserSchema
pydantic_confirmed: false
base_resolution: external_base
bases:
- UserMixin
- TokenMixin
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/schemas/auth/registration.py
  symbol: application.schemas.auth.registration.LoggedInUserSchema
  line_start: 31
  line_end: 34
  evidence_type: implemented
inbound_relations:
- type: USES_SCHEMA
  source: endpoint.ftgo.gateway.post.auth.login
  role: response
  symbol: application.routes.auth.registration.login
  type_expression: LoggedInUserSchema
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/auth/registration.py
  line_start: 78
  line_end: 78
  evidence_type: implemented
fields:
- name: role
  annotation: str
  default_expression: Field(..., min_length=1, max_length=20)
  line: 33
---

# LoggedInUserSchema

Candidate schema extracted from a class definition in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Qualified name: `application.schemas.auth.registration.LoggedInUserSchema`
- Declared in: `backend/gateway/src/application/schemas/auth/registration.py` (lines 31-34)
- Pydantic BaseModel confirmed in source: `False`
- Base resolution: `external_base`
- Used as: `response`
- Evidence class: `implemented`

## Review notes

This page is a candidate awaiting review. Field annotations are recorded as source text and never evaluated; credential-shaped defaults are redacted at extraction time.

