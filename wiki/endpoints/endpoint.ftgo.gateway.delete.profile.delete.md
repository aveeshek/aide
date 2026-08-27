---
id: endpoint.ftgo.gateway.delete.profile.delete
kind: Endpoint
type: Endpoint
title: DELETE /profile/delete
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
method: DELETE
effective_path: /profile/delete
path_resolution: partial
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/account/profile.py
  symbol: application.routes.account.profile.delete_account
  line_start: 65
  line_end: 81
  evidence_type: implemented
inbound_relations:
- type: CONTAINS
  source: api.ftgo.gateway
  method: DELETE
  path: backend/gateway/src/application/routes/account/profile.py
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  symbol: application.routes.account.profile.delete_account
  line_start: 65
  line_end: 81
  evidence_type: implemented
relations:
- type: USES_SCHEMA
  target: schema.ftgo.gateway.application.schemas.common.successresponse
  role: response
  symbol: application.routes.account.profile.delete_account
  type_expression: SuccessResponse
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/account/profile.py
  line_start: 65
  line_end: 65
  evidence_type: implemented
attributes:
  method: DELETE
  effective_path: /profile/delete
  decorator_path: /delete
  router_prefix: /profile
  path_resolution: partial
  decorator: router.delete("/delete", response_model=SuccessResponse)
  handler: application.routes.account.profile.delete_account
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

# DELETE /profile/delete

Candidate HTTP endpoint extracted from a FastAPI route decorator in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Method: `DELETE`
- Effective path: `/profile/delete`
- Path resolution: `partial`
- Handler: `application.routes.account.profile.delete_account`
- Declared in: `backend/gateway/src/application/routes/account/profile.py` (lines 65-81)
- Evidence class: `implemented`

## Unresolved mount prefix

The effective path above omits a mount prefix that is not a string literal in source, so the served path depends on configuration:

- `service_config.api_prefix`

## Schemas

- `response` `USES_SCHEMA` -> `schema.ftgo.gateway.application.schemas.common.successresponse`

## Review notes

This page is a candidate awaiting review. Method and path come from the decorator shown in `attributes.decorator`; nothing was inferred from names.

