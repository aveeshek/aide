---
id: endpoint.ftgo.gateway.post.status.online
kind: Endpoint
type: Endpoint
title: POST /status/online
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
effective_path: /status/online
path_resolution: partial
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/driver/online_status.py
  symbol: application.routes.driver.online_status.change_status_online
  line_start: 34
  line_end: 40
  evidence_type: implemented
inbound_relations:
- type: CONTAINS
  source: api.ftgo.gateway
  method: POST
  path: backend/gateway/src/application/routes/driver/online_status.py
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  symbol: application.routes.driver.online_status.change_status_online
  line_start: 34
  line_end: 40
  evidence_type: implemented
relations:
- type: USES_SCHEMA
  target: schema.ftgo.gateway.application.schemas.common.successresponse
  role: response
  symbol: application.routes.driver.online_status.change_status_online
  type_expression: SuccessResponse
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/driver/online_status.py
  line_start: 34
  line_end: 34
  evidence_type: implemented
attributes:
  method: POST
  effective_path: /status/online
  decorator_path: /online
  router_prefix: /status
  path_resolution: partial
  decorator: router.post("/online", response_model=SuccessResponse)
  handler: application.routes.driver.online_status.change_status_online
  router: application.routes.driver.online_status:router
  mount_path:
  - main:app
  - application.app:router
  - application.routes.driver.online_status:router
  tags:
  - driver_location_service
  response_model: SuccessResponse
  unresolved_prefix_expressions:
  - service_config.api_prefix
---

# POST /status/online

Candidate HTTP endpoint extracted from a FastAPI route decorator in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Method: `POST`
- Effective path: `/status/online`
- Path resolution: `partial`
- Handler: `application.routes.driver.online_status.change_status_online`
- Declared in: `backend/gateway/src/application/routes/driver/online_status.py` (lines 34-40)
- Evidence class: `implemented`

## Unresolved mount prefix

The effective path above omits a mount prefix that is not a string literal in source, so the served path depends on configuration:

- `service_config.api_prefix`

## Schemas

- `response` `USES_SCHEMA` -> `schema.ftgo.gateway.application.schemas.common.successresponse`

## Review notes

This page is a candidate awaiting review. Method and path come from the decorator shown in `attributes.decorator`; nothing was inferred from names.

