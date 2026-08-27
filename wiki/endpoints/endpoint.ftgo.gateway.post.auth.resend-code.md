---
id: endpoint.ftgo.gateway.post.auth.resend-code
kind: Endpoint
type: Endpoint
title: POST /auth/resend_code
status: approved
review_status: approved
candidate_of: fastapi-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: fastapi
service: service.ftgo.gateway
owner: aide-ftgo-cohort
api: api.ftgo.gateway
method: POST
effective_path: /auth/resend_code
path_resolution: partial
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/auth/registration.py
  symbol: application.routes.auth.registration.resend_auth_code
  line_start: 60
  line_end: 76
  evidence_type: implemented
inbound_relations:
- type: CONTAINS
  source: api.ftgo.gateway
  method: POST
  path: backend/gateway/src/application/routes/auth/registration.py
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  symbol: application.routes.auth.registration.resend_auth_code
  line_start: 60
  line_end: 76
  evidence_type: implemented
relations:
- type: USES_SCHEMA
  target: schema.ftgo.gateway.application.schemas.auth.registration.userauthcodeschema
  role: response
  symbol: application.routes.auth.registration.resend_auth_code
  type_expression: UserAuthCodeSchema
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/auth/registration.py
  line_start: 60
  line_end: 60
  evidence_type: implemented
attributes:
  method: POST
  effective_path: /auth/resend_code
  decorator_path: /resend_code
  router_prefix: /auth
  path_resolution: partial
  decorator: router.post("/resend_code", response_model=UserAuthCodeSchema)
  handler: application.routes.auth.registration.resend_auth_code
  router: application.routes.auth.registration:router
  mount_path:
  - main:app
  - application.app:router
  - application.routes.auth.registration:router
  tags:
  - user_profile
  response_model: UserAuthCodeSchema
  unresolved_prefix_expressions:
  - service_config.api_prefix
---

# POST /auth/resend_code

Candidate HTTP endpoint extracted from a FastAPI route decorator in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Method: `POST`
- Effective path: `/auth/resend_code`
- Path resolution: `partial`
- Handler: `application.routes.auth.registration.resend_auth_code`
- Declared in: `backend/gateway/src/application/routes/auth/registration.py` (lines 60-76)
- Evidence class: `implemented`

## Unresolved mount prefix

The effective path above omits a mount prefix that is not a string literal in source, so the served path depends on configuration:

- `service_config.api_prefix`

## Schemas

- `response` `USES_SCHEMA` -> `schema.ftgo.gateway.application.schemas.auth.registration.userauthcodeschema`

## Review notes

This page is a candidate awaiting review. Method and path come from the decorator shown in `attributes.decorator`; nothing was inferred from names.

