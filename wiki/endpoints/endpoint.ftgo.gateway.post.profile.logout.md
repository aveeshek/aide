---
id: endpoint.ftgo.gateway.post.profile.logout
kind: Endpoint
type: Endpoint
title: POST /profile/logout
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
effective_path: /profile/logout
path_resolution: partial
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/account/profile.py
  symbol: application.routes.account.profile.logout
  line_start: 21
  line_end: 37
  evidence_type: implemented
inbound_relations:
- type: CONTAINS
  source: api.ftgo.gateway
  method: POST
  path: backend/gateway/src/application/routes/account/profile.py
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  symbol: application.routes.account.profile.logout
  line_start: 21
  line_end: 37
  evidence_type: implemented
relations:
- type: USES_SCHEMA
  target: schema.ftgo.gateway.application.schemas.common.successresponse
  role: response
  symbol: application.routes.account.profile.logout
  type_expression: SuccessResponse
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/account/profile.py
  line_start: 21
  line_end: 21
  evidence_type: implemented
attributes:
  method: POST
  effective_path: /profile/logout
  decorator_path: /logout
  router_prefix: /profile
  path_resolution: partial
  decorator: router.post("/logout", response_model=SuccessResponse)
  handler: application.routes.account.profile.logout
  router: application.routes.account.profile:router
  mount_path:
  - main:app
  - application.app:router
  - application.routes.account.profile:router
  tags:
  - user_profile
  response_model: SuccessResponse
  unresolved_prefix_expressions:
  - service_config.api_prefix
---

# POST /profile/logout

Candidate HTTP endpoint extracted from a FastAPI route decorator in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Method: `POST`
- Effective path: `/profile/logout`
- Path resolution: `partial`
- Handler: `application.routes.account.profile.logout`
- Declared in: `backend/gateway/src/application/routes/account/profile.py` (lines 21-37)
- Evidence class: `implemented`

## Unresolved mount prefix

The effective path above omits a mount prefix that is not a string literal in source, so the served path depends on configuration:

- `service_config.api_prefix`

## Schemas

- `response` `USES_SCHEMA` -> `schema.ftgo.gateway.application.schemas.common.successresponse`

## Review notes

This page is a candidate awaiting review. Method and path come from the decorator shown in `attributes.decorator`; nothing was inferred from names.

