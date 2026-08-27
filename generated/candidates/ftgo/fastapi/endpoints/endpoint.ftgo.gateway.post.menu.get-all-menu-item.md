---
id: endpoint.ftgo.gateway.post.menu.get-all-menu-item
kind: Endpoint
type: Endpoint
title: POST /menu/get_all_menu_item
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
effective_path: /menu/get_all_menu_item
path_resolution: partial
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/restaurant/menu.py
  symbol: application.routes.restaurant.menu.get_all_menu_item
  line_start: 109
  line_end: 128
  evidence_type: implemented
inbound_relations:
- type: CONTAINS
  source: api.ftgo.gateway
  method: POST
  path: backend/gateway/src/application/routes/restaurant/menu.py
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  symbol: application.routes.restaurant.menu.get_all_menu_item
  line_start: 109
  line_end: 128
  evidence_type: implemented
relations:
- type: USES_SCHEMA
  target: schema.ftgo.gateway.application.schemas.restaurant.menu.getallmenuitemrequest
  role: request
  symbol: application.routes.restaurant.menu.get_all_menu_item.request_data
  type_expression: GetAllMenuItemRequest
  parameter: request_data
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/restaurant/menu.py
  line_start: 110
  line_end: 110
  evidence_type: implemented
- type: USES_SCHEMA
  target: schema.ftgo.gateway.application.schemas.restaurant.menu.getallmenuitemresponse
  role: response
  symbol: application.routes.restaurant.menu.get_all_menu_item
  type_expression: GetAllMenuItemResponse
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/restaurant/menu.py
  line_start: 109
  line_end: 109
  evidence_type: implemented
attributes:
  method: POST
  effective_path: /menu/get_all_menu_item
  decorator_path: /get_all_menu_item
  router_prefix: /menu
  path_resolution: partial
  decorator: router.post("/get_all_menu_item", response_model=GetAllMenuItemResponse)
  handler: application.routes.restaurant.menu.get_all_menu_item
  router: application.routes.restaurant.menu:router
  mount_path:
  - main:app
  - application.app:router
  - application.routes.restaurant.menu:router
  tags:
  - menu
  response_model: GetAllMenuItemResponse
  unresolved_prefix_expressions:
  - service_config.api_prefix
---

# POST /menu/get_all_menu_item

Candidate HTTP endpoint extracted from a FastAPI route decorator in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Method: `POST`
- Effective path: `/menu/get_all_menu_item`
- Path resolution: `partial`
- Handler: `application.routes.restaurant.menu.get_all_menu_item`
- Declared in: `backend/gateway/src/application/routes/restaurant/menu.py` (lines 109-128)
- Evidence class: `implemented`

## Unresolved mount prefix

The effective path above omits a mount prefix that is not a string literal in source, so the served path depends on configuration:

- `service_config.api_prefix`

## Schemas

- `request` `USES_SCHEMA` -> `schema.ftgo.gateway.application.schemas.restaurant.menu.getallmenuitemrequest`
- `response` `USES_SCHEMA` -> `schema.ftgo.gateway.application.schemas.restaurant.menu.getallmenuitemresponse`

## Review notes

This page is a candidate awaiting review. Method and path come from the decorator shown in `attributes.decorator`; nothing was inferred from names.

