---
id: schema.ftgo.gateway.application.schemas.auth.registration.userauthcodeschema
kind: Schema
type: Schema
title: UserAuthCodeSchema
status: candidate
review_status: pending
candidate_of: fastapi-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: fastapi
service: service.ftgo.gateway
owner: aide-ftgo-cohort
qualified_name: application.schemas.auth.registration.UserAuthCodeSchema
pydantic_confirmed: false
base_resolution: external_base
bases:
- UserIdMixin
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/schemas/auth/registration.py
  symbol: application.schemas.auth.registration.UserAuthCodeSchema
  line_start: 15
  line_end: 16
  evidence_type: implemented
inbound_relations:
- type: USES_SCHEMA
  source: endpoint.ftgo.gateway.post.auth.register
  role: response
  symbol: application.routes.auth.registration.register
  type_expression: UserAuthCodeSchema
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/auth/registration.py
  line_start: 21
  line_end: 21
  evidence_type: implemented
- type: USES_SCHEMA
  source: endpoint.ftgo.gateway.post.auth.resend-code
  role: response
  symbol: application.routes.auth.registration.resend_auth_code
  type_expression: UserAuthCodeSchema
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/auth/registration.py
  line_start: 60
  line_end: 60
  evidence_type: implemented
- type: USES_SCHEMA
  source: endpoint.ftgo.gateway.post.auth.verify
  role: request
  symbol: application.routes.auth.registration.verify_account.request_data
  type_expression: UserAuthCodeSchema
  parameter: request_data
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/auth/registration.py
  line_start: 43
  line_end: 43
  evidence_type: implemented
fields:
- name: auth_code
  annotation: str
  default_expression: '[redacted]'
  redacted: true
  line: 16
---

# UserAuthCodeSchema

Candidate schema extracted from a class definition in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Qualified name: `application.schemas.auth.registration.UserAuthCodeSchema`
- Declared in: `backend/gateway/src/application/schemas/auth/registration.py` (lines 15-16)
- Pydantic BaseModel confirmed in source: `False`
- Base resolution: `external_base`
- Used as: `request, response`
- Evidence class: `implemented`

## Review notes

This page is a candidate awaiting review. Field annotations are recorded as source text and never evaluated; credential-shaped defaults are redacted at extraction time.

