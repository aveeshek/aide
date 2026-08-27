---
id: endpoint.ftgo.gateway.delete.restaurant.delete
kind: Endpoint
type: Endpoint
title: DELETE /restaurant/delete
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
effective_path: /restaurant/delete
path_resolution: partial
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/restaurant/restaurant.py
  symbol: application.routes.restaurant.restaurant.delete_restaurant
  line_start: 93
  line_end: 112
  evidence_type: implemented
inbound_relations:
- type: CONTAINS
  source: api.ftgo.gateway
  method: DELETE
  path: backend/gateway/src/application/routes/restaurant/restaurant.py
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  symbol: application.routes.restaurant.restaurant.delete_restaurant
  line_start: 93
  line_end: 112
  evidence_type: implemented
relations:
- type: USES_SCHEMA
  target: schema.ftgo.gateway.application.schemas.restaurant.restaurant.deleterestaurantrequest
  role: request
  symbol: application.routes.restaurant.restaurant.delete_restaurant.request_data
  type_expression: DeleteRestaurantRequest
  parameter: request_data
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/restaurant/restaurant.py
  line_start: 94
  line_end: 94
  evidence_type: implemented
- type: USES_SCHEMA
  target: schema.ftgo.gateway.application.schemas.restaurant.restaurant.deleterestaurantresponse
  role: response
  symbol: application.routes.restaurant.restaurant.delete_restaurant
  type_expression: DeleteRestaurantResponse
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/restaurant/restaurant.py
  line_start: 93
  line_end: 93
  evidence_type: implemented
attributes:
  method: DELETE
  effective_path: /restaurant/delete
  decorator_path: /delete
  router_prefix: /restaurant
  path_resolution: partial
  decorator: router.delete("/delete", response_model=DeleteRestaurantResponse)
  handler: application.routes.restaurant.restaurant.delete_restaurant
  router: application.routes.restaurant.restaurant:router
  mount_path:
  - main:app
  - application.app:router
  - application.routes.restaurant.restaurant:router
  tags:
  - restaurant
  response_model: DeleteRestaurantResponse
  unresolved_prefix_expressions:
  - service_config.api_prefix
---

# DELETE /restaurant/delete

Candidate HTTP endpoint extracted from a FastAPI route decorator in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Method: `DELETE`
- Effective path: `/restaurant/delete`
- Path resolution: `partial`
- Handler: `application.routes.restaurant.restaurant.delete_restaurant`
- Declared in: `backend/gateway/src/application/routes/restaurant/restaurant.py` (lines 93-112)
- Evidence class: `implemented`

## Unresolved mount prefix

The effective path above omits a mount prefix that is not a string literal in source, so the served path depends on configuration:

- `service_config.api_prefix`

## Schemas

- `request` `USES_SCHEMA` -> `schema.ftgo.gateway.application.schemas.restaurant.restaurant.deleterestaurantrequest`
- `response` `USES_SCHEMA` -> `schema.ftgo.gateway.application.schemas.restaurant.restaurant.deleterestaurantresponse`

## Review notes

This page is a candidate awaiting review. Method and path come from the decorator shown in `attributes.decorator`; nothing was inferred from names.

