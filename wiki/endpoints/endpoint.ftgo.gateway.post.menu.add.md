---
id: endpoint.ftgo.gateway.post.menu.add
kind: Endpoint
type: Endpoint
title: POST /menu/add
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
effective_path: /menu/add
path_resolution: partial
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/restaurant/menu.py
  symbol: application.routes.restaurant.menu.add_item
  line_start: 21
  line_end: 40
  evidence_type: implemented
inbound_relations:
- type: CONTAINS
  source: api.ftgo.gateway
  method: POST
  path: backend/gateway/src/application/routes/restaurant/menu.py
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  symbol: application.routes.restaurant.menu.add_item
  line_start: 21
  line_end: 40
  evidence_type: implemented
relations:
- type: USES_SCHEMA
  target: schema.ftgo.gateway.application.schemas.restaurant.menu.addmenuitemrequest
  role: request
  symbol: application.routes.restaurant.menu.add_item.request_data
  type_expression: AddMenuItemRequest
  parameter: request_data
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/restaurant/menu.py
  line_start: 22
  line_end: 22
  evidence_type: implemented
- type: USES_SCHEMA
  target: schema.ftgo.gateway.application.schemas.restaurant.menu.addmenuitemresponse
  role: response
  symbol: application.routes.restaurant.menu.add_item
  type_expression: AddMenuItemResponse
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/restaurant/menu.py
  line_start: 21
  line_end: 21
  evidence_type: implemented
attributes:
  method: POST
  effective_path: /menu/add
  decorator_path: /add
  router_prefix: /menu
  path_resolution: partial
  decorator: router.post("/add", response_model=AddMenuItemResponse)
  handler: application.routes.restaurant.menu.add_item
  router: application.routes.restaurant.menu:router
  mount_path:
  - main:app
  - application.app:router
  - application.routes.restaurant.menu:router
  tags:
  - menu
  response_model: AddMenuItemResponse
  unresolved_prefix_expressions:
  - service_config.api_prefix
---

# POST /menu/add

Candidate HTTP endpoint extracted from a FastAPI route decorator in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Method: `POST`
- Effective path: `/menu/add`
- Path resolution: `partial`
- Handler: `application.routes.restaurant.menu.add_item`
- Declared in: `backend/gateway/src/application/routes/restaurant/menu.py` (lines 21-40)
- Evidence class: `implemented`

## Unresolved mount prefix

The effective path above omits a mount prefix that is not a string literal in source, so the served path depends on configuration:

- `service_config.api_prefix`

## Schemas

- `request` `USES_SCHEMA` -> `schema.ftgo.gateway.application.schemas.restaurant.menu.addmenuitemrequest`
- `response` `USES_SCHEMA` -> `schema.ftgo.gateway.application.schemas.restaurant.menu.addmenuitemresponse`

## Review notes

This page is a candidate awaiting review. Method and path come from the decorator shown in `attributes.decorator`; nothing was inferred from names.

