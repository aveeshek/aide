---
id: endpoint.ftgo.gateway.put.restaurant.update
kind: Endpoint
type: Endpoint
title: PUT /restaurant/update
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
effective_path: /restaurant/update
path_resolution: partial
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/restaurant/restaurant.py
  symbol: application.routes.restaurant.restaurant.update_information
  line_start: 115
  line_end: 133
  evidence_type: implemented
inbound_relations:
- type: CONTAINS
  source: api.ftgo.gateway
  method: PUT
  path: backend/gateway/src/application/routes/restaurant/restaurant.py
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  symbol: application.routes.restaurant.restaurant.update_information
  line_start: 115
  line_end: 133
  evidence_type: implemented
relations:
- type: USES_SCHEMA
  target: schema.ftgo.gateway.application.schemas.restaurant.restaurant.updaterestaurantrequest
  role: request
  symbol: application.routes.restaurant.restaurant.update_information.request_data
  type_expression: UpdateRestaurantRequest
  parameter: request_data
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/restaurant/restaurant.py
  line_start: 116
  line_end: 116
  evidence_type: implemented
- type: USES_SCHEMA
  target: schema.ftgo.gateway.application.schemas.restaurant.restaurant.updaterestaurantresponse
  role: response
  symbol: application.routes.restaurant.restaurant.update_information
  type_expression: UpdateRestaurantResponse
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/restaurant/restaurant.py
  line_start: 115
  line_end: 115
  evidence_type: implemented
attributes:
  method: PUT
  effective_path: /restaurant/update
  decorator_path: /update
  router_prefix: /restaurant
  path_resolution: partial
  decorator: router.put("/update", response_model=UpdateRestaurantResponse)
  handler: application.routes.restaurant.restaurant.update_information
  router: application.routes.restaurant.restaurant:router
  mount_path:
  - main:app
  - application.app:router
  - application.routes.restaurant.restaurant:router
  tags:
  - restaurant
  response_model: UpdateRestaurantResponse
  unresolved_prefix_expressions:
  - service_config.api_prefix
---

# PUT /restaurant/update

Candidate HTTP endpoint extracted from a FastAPI route decorator in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Method: `PUT`
- Effective path: `/restaurant/update`
- Path resolution: `partial`
- Handler: `application.routes.restaurant.restaurant.update_information`
- Declared in: `backend/gateway/src/application/routes/restaurant/restaurant.py` (lines 115-133)
- Evidence class: `implemented`

## Unresolved mount prefix

The effective path above omits a mount prefix that is not a string literal in source, so the served path depends on configuration:

- `service_config.api_prefix`

## Schemas

- `request` `USES_SCHEMA` -> `schema.ftgo.gateway.application.schemas.restaurant.restaurant.updaterestaurantrequest`
- `response` `USES_SCHEMA` -> `schema.ftgo.gateway.application.schemas.restaurant.restaurant.updaterestaurantresponse`

## Review notes

This page is a candidate awaiting review. Method and path come from the decorator shown in `attributes.decorator`; nothing was inferred from names.

