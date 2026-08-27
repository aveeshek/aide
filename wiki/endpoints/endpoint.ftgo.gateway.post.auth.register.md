---
id: endpoint.ftgo.gateway.post.auth.register
kind: Endpoint
type: Endpoint
title: POST /auth/register
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
effective_path: /auth/register
path_resolution: partial
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/auth/registration.py
  symbol: application.routes.auth.registration.register
  line_start: 21
  line_end: 40
  evidence_type: implemented
inbound_relations:
- type: CONTAINS
  source: api.ftgo.gateway
  method: POST
  path: backend/gateway/src/application/routes/auth/registration.py
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  symbol: application.routes.auth.registration.register
  line_start: 21
  line_end: 40
  evidence_type: implemented
relations:
- type: USES_SCHEMA
  target: schema.ftgo.gateway.application.schemas.auth.registration.registrationschema
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
- type: USES_SCHEMA
  target: schema.ftgo.gateway.application.schemas.auth.registration.userauthcodeschema
  role: response
  symbol: application.routes.auth.registration.register
  type_expression: UserAuthCodeSchema
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/auth/registration.py
  line_start: 21
  line_end: 21
  evidence_type: implemented
attributes:
  method: POST
  effective_path: /auth/register
  decorator_path: /register
  router_prefix: /auth
  path_resolution: partial
  decorator: router.post("/register", response_model=UserAuthCodeSchema, status_code=status.HTTP_201_CREATED)
  handler: application.routes.auth.registration.register
  router: application.routes.auth.registration:router
  mount_path:
  - main:app
  - application.app:router
  - application.routes.auth.registration:router
  tags:
  - user_profile
  status_code_expression: status.HTTP_201_CREATED
  response_model: UserAuthCodeSchema
  unresolved_prefix_expressions:
  - service_config.api_prefix
---

# POST /auth/register

Candidate HTTP endpoint extracted from a FastAPI route decorator in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Method: `POST`
- Effective path: `/auth/register`
- Path resolution: `partial`
- Handler: `application.routes.auth.registration.register`
- Declared in: `backend/gateway/src/application/routes/auth/registration.py` (lines 21-40)
- Evidence class: `implemented`

## Unresolved mount prefix

The effective path above omits a mount prefix that is not a string literal in source, so the served path depends on configuration:

- `service_config.api_prefix`

## Schemas

- `request` `USES_SCHEMA` -> `schema.ftgo.gateway.application.schemas.auth.registration.registrationschema`
- `response` `USES_SCHEMA` -> `schema.ftgo.gateway.application.schemas.auth.registration.userauthcodeschema`

## Review notes

This page is a candidate awaiting review. Method and path come from the decorator shown in `attributes.decorator`; nothing was inferred from names.

