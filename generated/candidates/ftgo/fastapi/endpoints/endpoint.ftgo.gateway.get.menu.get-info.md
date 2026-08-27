---
id: endpoint.ftgo.gateway.get.menu.get-info
kind: Endpoint
type: Endpoint
title: GET /menu/get_info
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
method: GET
effective_path: /menu/get_info
path_resolution: partial
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/restaurant/menu.py
  symbol: application.routes.restaurant.menu.get_info
  line_start: 43
  line_end: 63
  evidence_type: implemented
inbound_relations:
- type: CONTAINS
  source: api.ftgo.gateway
  method: GET
  path: backend/gateway/src/application/routes/restaurant/menu.py
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  symbol: application.routes.restaurant.menu.get_info
  line_start: 43
  line_end: 63
  evidence_type: implemented
relations:
- type: USES_SCHEMA
  target: schema.ftgo.gateway.application.schemas.restaurant.menu.getmenuiteminforequest
  role: request
  symbol: application.routes.restaurant.menu.get_info.request_data
  type_expression: GetMenuItemInfoRequest
  parameter: request_data
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/restaurant/menu.py
  line_start: 44
  line_end: 44
  evidence_type: implemented
- type: USES_SCHEMA
  target: schema.ftgo.gateway.application.schemas.restaurant.menu.getmenuiteminforesponse
  role: response
  symbol: application.routes.restaurant.menu.get_info
  type_expression: GetMenuItemInfoResponse
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/restaurant/menu.py
  line_start: 43
  line_end: 43
  evidence_type: implemented
attributes:
  method: GET
  effective_path: /menu/get_info
  decorator_path: /get_info
  router_prefix: /menu
  path_resolution: partial
  decorator: router.get("/get_info", response_model=GetMenuItemInfoResponse)
  handler: application.routes.restaurant.menu.get_info
  router: application.routes.restaurant.menu:router
  mount_path:
  - main:app
  - application.app:router
  - application.routes.restaurant.menu:router
  tags:
  - menu
  response_model: GetMenuItemInfoResponse
  unresolved_prefix_expressions:
  - service_config.api_prefix
---

# GET /menu/get_info

Candidate HTTP endpoint extracted from a FastAPI route decorator in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Method: `GET`
- Effective path: `/menu/get_info`
- Path resolution: `partial`
- Handler: `application.routes.restaurant.menu.get_info`
- Declared in: `backend/gateway/src/application/routes/restaurant/menu.py` (lines 43-63)
- Evidence class: `implemented`

## Unresolved mount prefix

The effective path above omits a mount prefix that is not a string literal in source, so the served path depends on configuration:

- `service_config.api_prefix`

## Schemas

- `request` `USES_SCHEMA` -> `schema.ftgo.gateway.application.schemas.restaurant.menu.getmenuiteminforequest`
- `response` `USES_SCHEMA` -> `schema.ftgo.gateway.application.schemas.restaurant.menu.getmenuiteminforesponse`

## Review notes

This page is a candidate awaiting review. Method and path come from the decorator shown in `attributes.decorator`; nothing was inferred from names.

