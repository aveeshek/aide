---
id: endpoint.ftgo.gateway.get.profile.user-info
kind: Endpoint
type: Endpoint
title: GET /profile/user_info
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
method: GET
effective_path: /profile/user_info
path_resolution: partial
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/account/profile.py
  symbol: application.routes.account.profile.get_info
  line_start: 39
  line_end: 63
  evidence_type: implemented
inbound_relations:
- type: CONTAINS
  source: api.ftgo.gateway
  method: GET
  path: backend/gateway/src/application/routes/account/profile.py
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  symbol: application.routes.account.profile.get_info
  line_start: 39
  line_end: 63
  evidence_type: implemented
attributes:
  method: GET
  effective_path: /profile/user_info
  decorator_path: /user_info
  router_prefix: /profile
  path_resolution: partial
  decorator: router.get("/user_info", response_model=UserInfoMixin)
  handler: application.routes.account.profile.get_info
  router: application.routes.account.profile:router
  mount_path:
  - main:app
  - application.app:router
  - application.routes.account.profile:router
  tags:
  - user_profile
  response_model: UserInfoMixin
  unresolved_prefix_expressions:
  - service_config.api_prefix
---

# GET /profile/user_info

Candidate HTTP endpoint extracted from a FastAPI route decorator in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Method: `GET`
- Effective path: `/profile/user_info`
- Path resolution: `partial`
- Handler: `application.routes.account.profile.get_info`
- Declared in: `backend/gateway/src/application/routes/account/profile.py` (lines 39-63)
- Evidence class: `implemented`

## Unresolved mount prefix

The effective path above omits a mount prefix that is not a string literal in source, so the served path depends on configuration:

- `service_config.api_prefix`

## Review notes

This page is a candidate awaiting review. Method and path come from the decorator shown in `attributes.decorator`; nothing was inferred from names.

