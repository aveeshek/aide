---
id: endpoint.ftgo.gateway.post.auth.login
kind: Endpoint
type: Endpoint
title: POST /auth/login
status: candidate
review_status: pending
candidate_of: fastapi-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: fastapi
service: service.ftgo.gateway
owner: aide-ftgo-cohort
api: api.ftgo.gateway
method: POST
effective_path: /auth/login
path_resolution: partial
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/auth/registration.py
  symbol: application.routes.auth.registration.login
  line_start: 78
  line_end: 100
  evidence_type: implemented
inbound_relations:
- type: CONTAINS
  source: api.ftgo.gateway
  method: POST
  path: backend/gateway/src/application/routes/auth/registration.py
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  symbol: application.routes.auth.registration.login
  line_start: 78
  line_end: 100
  evidence_type: implemented
relations:
- type: USES_SCHEMA
  target: schema.ftgo.gateway.application.schemas.auth.registration.loggedinuserschema
  role: response
  symbol: application.routes.auth.registration.login
  type_expression: LoggedInUserSchema
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/auth/registration.py
  line_start: 78
  line_end: 78
  evidence_type: implemented
- type: USES_SCHEMA
  target: schema.ftgo.gateway.application.schemas.auth.registration.loginschema
  role: request
  symbol: application.routes.auth.registration.login.request_data
  type_expression: LoginSchema
  parameter: request_data
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/auth/registration.py
  line_start: 79
  line_end: 79
  evidence_type: implemented
attributes:
  method: POST
  effective_path: /auth/login
  decorator_path: /login
  router_prefix: /auth
  path_resolution: partial
  decorator: router.post("/login", response_model=LoggedInUserSchema)
  handler: application.routes.auth.registration.login
  router: application.routes.auth.registration:router
  mount_path:
  - main:app
  - application.app:router
  - application.routes.auth.registration:router
  tags:
  - user_profile
  response_model: LoggedInUserSchema
  unresolved_prefix_expressions:
  - service_config.api_prefix
---

# POST /auth/login

Candidate HTTP endpoint extracted from a FastAPI route decorator in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Method: `POST`
- Effective path: `/auth/login`
- Path resolution: `partial`
- Handler: `application.routes.auth.registration.login`
- Declared in: `backend/gateway/src/application/routes/auth/registration.py` (lines 78-100)
- Evidence class: `implemented`

## Unresolved mount prefix

The effective path above omits a mount prefix that is not a string literal in source, so the served path depends on configuration:

- `service_config.api_prefix`

## Schemas

- `response` `USES_SCHEMA` -> `schema.ftgo.gateway.application.schemas.auth.registration.loggedinuserschema`
- `request` `USES_SCHEMA` -> `schema.ftgo.gateway.application.schemas.auth.registration.loginschema`

## Review notes

This page is a candidate awaiting review. Method and path come from the decorator shown in `attributes.decorator`; nothing was inferred from names.

