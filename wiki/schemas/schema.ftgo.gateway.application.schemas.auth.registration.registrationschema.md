---
id: schema.ftgo.gateway.application.schemas.auth.registration.registrationschema
kind: Schema
type: Schema
title: RegistrationSchema
status: approved
review_status: approved
candidate_of: fastapi-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: fastapi
service: service.ftgo.gateway
owner: aide-ftgo-cohort
qualified_name: application.schemas.auth.registration.RegistrationSchema
pydantic_confirmed: false
base_resolution: external_base
bases:
- UserInfoMixin
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/schemas/auth/registration.py
  symbol: application.schemas.auth.registration.RegistrationSchema
  line_start: 10
  line_end: 13
  evidence_type: implemented
inbound_relations:
- type: USES_SCHEMA
  source: endpoint.ftgo.gateway.post.auth.register
  role: request
  symbol: application.routes.auth.registration.register.request_data
  type_expression: RegistrationSchema
  parameter: request_data
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/auth/registration.py
  line_start: 22
  line_end: 22
  evidence_type: implemented
fields:
- name: role
  annotation: str
  default_expression: Field(..., min_length=1, max_length=20)
  line: 12
- name: password
  annotation: str
  default_expression: '[redacted]'
  redacted: true
  line: 13
---

# RegistrationSchema

Candidate schema extracted from a class definition in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Qualified name: `application.schemas.auth.registration.RegistrationSchema`
- Declared in: `backend/gateway/src/application/schemas/auth/registration.py` (lines 10-13)
- Pydantic BaseModel confirmed in source: `False`
- Base resolution: `external_base`
- Used as: `request`
- Evidence class: `implemented`

## Review notes

This page is a candidate awaiting review. Field annotations are recorded as source text and never evaluated; credential-shaped defaults are redacted at extraction time.

