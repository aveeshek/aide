---
id: endpoint.ftgo.gateway.post.restaurant.register
kind: Endpoint
type: Endpoint
title: POST /restaurant/register
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
effective_path: /restaurant/register
path_resolution: partial
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/restaurant/restaurant.py
  symbol: application.routes.restaurant.restaurant.register
  line_start: 22
  line_end: 44
  evidence_type: implemented
inbound_relations:
- type: CONTAINS
  source: api.ftgo.gateway
  method: POST
  path: backend/gateway/src/application/routes/restaurant/restaurant.py
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  symbol: application.routes.restaurant.restaurant.register
  line_start: 22
  line_end: 44
  evidence_type: implemented
relations:
- type: USES_SCHEMA
  target: schema.ftgo.gateway.application.schemas.restaurant.restaurant.registerrestaurantrequest
  role: request
  symbol: application.routes.restaurant.restaurant.register.request_data
  type_expression: RegisterRestaurantRequest
  parameter: request_data
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/restaurant/restaurant.py
  line_start: 23
  line_end: 23
  evidence_type: implemented
- type: USES_SCHEMA
  target: schema.ftgo.gateway.application.schemas.restaurant.restaurant.registerrestaurantresponse
  role: response
  symbol: application.routes.restaurant.restaurant.register
  type_expression: RegisterRestaurantResponse
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/restaurant/restaurant.py
  line_start: 22
  line_end: 22
  evidence_type: implemented
attributes:
  method: POST
  effective_path: /restaurant/register
  decorator_path: /register
  router_prefix: /restaurant
  path_resolution: partial
  decorator: router.post("/register", response_model=RegisterRestaurantResponse)
  handler: application.routes.restaurant.restaurant.register
  router: application.routes.restaurant.restaurant:router
  mount_path:
  - main:app
  - application.app:router
  - application.routes.restaurant.restaurant:router
  tags:
  - restaurant
  response_model: RegisterRestaurantResponse
  unresolved_prefix_expressions:
  - service_config.api_prefix
---

# POST /restaurant/register

Candidate HTTP endpoint extracted from a FastAPI route decorator in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Method: `POST`
- Effective path: `/restaurant/register`
- Path resolution: `partial`
- Handler: `application.routes.restaurant.restaurant.register`
- Declared in: `backend/gateway/src/application/routes/restaurant/restaurant.py` (lines 22-44)
- Evidence class: `implemented`

## Unresolved mount prefix

The effective path above omits a mount prefix that is not a string literal in source, so the served path depends on configuration:

- `service_config.api_prefix`

## Schemas

- `request` `USES_SCHEMA` -> `schema.ftgo.gateway.application.schemas.restaurant.restaurant.registerrestaurantrequest`
- `response` `USES_SCHEMA` -> `schema.ftgo.gateway.application.schemas.restaurant.restaurant.registerrestaurantresponse`

## Review notes

This page is a candidate awaiting review. Method and path come from the decorator shown in `attributes.decorator`; nothing was inferred from names.

