---
id: endpoint.ftgo.gateway.put.profile.update
kind: Endpoint
type: Endpoint
title: PUT /profile/update
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
method: PUT
effective_path: /profile/update
path_resolution: partial
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/account/profile.py
  symbol: application.routes.account.profile.update_profile
  line_start: 85
  line_end: 106
  evidence_type: implemented
inbound_relations:
- type: CONTAINS
  source: api.ftgo.gateway
  method: PUT
  path: backend/gateway/src/application/routes/account/profile.py
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  symbol: application.routes.account.profile.update_profile
  line_start: 85
  line_end: 106
  evidence_type: implemented
relations:
- type: USES_SCHEMA
  target: schema.ftgo.gateway.application.schemas.account.profile.updateuserrequest
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
- type: USES_SCHEMA
  target: schema.ftgo.gateway.application.schemas.account.profile.userinfo
  role: response
  symbol: application.routes.account.profile.update_profile
  type_expression: UserInfo
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/account/profile.py
  line_start: 85
  line_end: 85
  evidence_type: implemented
attributes:
  method: PUT
  effective_path: /profile/update
  decorator_path: /update
  router_prefix: /profile
  path_resolution: partial
  decorator: router.put("/update", response_model=UserInfo)
  handler: application.routes.account.profile.update_profile
  router: application.routes.account.profile:router
  mount_path:
  - main:app
  - application.app:router
  - application.routes.account.profile:router
  tags:
  - user_profile
  response_model: UserInfo
  unresolved_prefix_expressions:
  - service_config.api_prefix
---

# PUT /profile/update

Candidate HTTP endpoint extracted from a FastAPI route decorator in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Method: `PUT`
- Effective path: `/profile/update`
- Path resolution: `partial`
- Handler: `application.routes.account.profile.update_profile`
- Declared in: `backend/gateway/src/application/routes/account/profile.py` (lines 85-106)
- Evidence class: `implemented`

## Unresolved mount prefix

The effective path above omits a mount prefix that is not a string literal in source, so the served path depends on configuration:

- `service_config.api_prefix`

## Schemas

- `request` `USES_SCHEMA` -> `schema.ftgo.gateway.application.schemas.account.profile.updateuserrequest`
- `response` `USES_SCHEMA` -> `schema.ftgo.gateway.application.schemas.account.profile.userinfo`

## Review notes

This page is a candidate awaiting review. Method and path come from the decorator shown in `attributes.decorator`; nothing was inferred from names.

