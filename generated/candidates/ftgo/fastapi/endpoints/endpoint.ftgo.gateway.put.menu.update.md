---
id: endpoint.ftgo.gateway.put.menu.update
kind: Endpoint
type: Endpoint
title: PUT /menu/update
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
effective_path: /menu/update
path_resolution: partial
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/restaurant/menu.py
  symbol: application.routes.restaurant.menu.update_item
  line_start: 66
  line_end: 85
  evidence_type: implemented
inbound_relations:
- type: CONTAINS
  source: api.ftgo.gateway
  method: PUT
  path: backend/gateway/src/application/routes/restaurant/menu.py
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  symbol: application.routes.restaurant.menu.update_item
  line_start: 66
  line_end: 85
  evidence_type: implemented
relations:
- type: USES_SCHEMA
  target: schema.ftgo.gateway.application.schemas.restaurant.menu.updatemenuitemrequest
  role: request
  symbol: application.routes.restaurant.menu.update_item.request_data
  type_expression: UpdateMenuItemRequest
  parameter: request_data
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/restaurant/menu.py
  line_start: 67
  line_end: 67
  evidence_type: implemented
- type: USES_SCHEMA
  target: schema.ftgo.gateway.application.schemas.restaurant.menu.updatemenuitemresponse
  role: response
  symbol: application.routes.restaurant.menu.update_item
  type_expression: UpdateMenuItemResponse
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/restaurant/menu.py
  line_start: 66
  line_end: 66
  evidence_type: implemented
attributes:
  method: PUT
  effective_path: /menu/update
  decorator_path: /update
  router_prefix: /menu
  path_resolution: partial
  decorator: router.put("/update", response_model=UpdateMenuItemResponse)
  handler: application.routes.restaurant.menu.update_item
  router: application.routes.restaurant.menu:router
  mount_path:
  - main:app
  - application.app:router
  - application.routes.restaurant.menu:router
  tags:
  - menu
  response_model: UpdateMenuItemResponse
  unresolved_prefix_expressions:
  - service_config.api_prefix
---

# PUT /menu/update

Candidate HTTP endpoint extracted from a FastAPI route decorator in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Method: `PUT`
- Effective path: `/menu/update`
- Path resolution: `partial`
- Handler: `application.routes.restaurant.menu.update_item`
- Declared in: `backend/gateway/src/application/routes/restaurant/menu.py` (lines 66-85)
- Evidence class: `implemented`

## Unresolved mount prefix

The effective path above omits a mount prefix that is not a string literal in source, so the served path depends on configuration:

- `service_config.api_prefix`

## Schemas

- `request` `USES_SCHEMA` -> `schema.ftgo.gateway.application.schemas.restaurant.menu.updatemenuitemrequest`
- `response` `USES_SCHEMA` -> `schema.ftgo.gateway.application.schemas.restaurant.menu.updatemenuitemresponse`

## Review notes

This page is a candidate awaiting review. Method and path come from the decorator shown in `attributes.decorator`; nothing was inferred from names.

