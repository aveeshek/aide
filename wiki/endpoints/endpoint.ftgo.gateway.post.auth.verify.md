---
id: endpoint.ftgo.gateway.post.auth.verify
kind: Endpoint
type: Endpoint
title: POST /auth/verify
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
effective_path: /auth/verify
path_resolution: partial
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/auth/registration.py
  symbol: application.routes.auth.registration.verify_account
  line_start: 42
  line_end: 58
  evidence_type: implemented
inbound_relations:
- type: CONTAINS
  source: api.ftgo.gateway
  method: POST
  path: backend/gateway/src/application/routes/auth/registration.py
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  symbol: application.routes.auth.registration.verify_account
  line_start: 42
  line_end: 58
  evidence_type: implemented
relations:
- type: USES_SCHEMA
  target: schema.ftgo.gateway.application.schemas.auth.registration.userauthcodeschema
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
- type: USES_SCHEMA
  target: schema.ftgo.gateway.application.schemas.common.successresponse
  role: response
  symbol: application.routes.auth.registration.verify_account
  type_expression: SuccessResponse
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/auth/registration.py
  line_start: 42
  line_end: 42
  evidence_type: implemented
attributes:
  method: POST
  effective_path: /auth/verify
  decorator_path: /verify
  router_prefix: /auth
  path_resolution: partial
  decorator: router.post("/verify", response_model=SuccessResponse)
  handler: application.routes.auth.registration.verify_account
  router: application.routes.auth.registration:router
  mount_path:
  - main:app
  - application.app:router
  - application.routes.auth.registration:router
  tags:
  - user_profile
  response_model: SuccessResponse
  unresolved_prefix_expressions:
  - service_config.api_prefix
---

# POST /auth/verify

Candidate HTTP endpoint extracted from a FastAPI route decorator in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Method: `POST`
- Effective path: `/auth/verify`
- Path resolution: `partial`
- Handler: `application.routes.auth.registration.verify_account`
- Declared in: `backend/gateway/src/application/routes/auth/registration.py` (lines 42-58)
- Evidence class: `implemented`

## Unresolved mount prefix

The effective path above omits a mount prefix that is not a string literal in source, so the served path depends on configuration:

- `service_config.api_prefix`

## Schemas

- `request` `USES_SCHEMA` -> `schema.ftgo.gateway.application.schemas.auth.registration.userauthcodeschema`
- `response` `USES_SCHEMA` -> `schema.ftgo.gateway.application.schemas.common.successresponse`

## Review notes

This page is a candidate awaiting review. Method and path come from the decorator shown in `attributes.decorator`; nothing was inferred from names.

