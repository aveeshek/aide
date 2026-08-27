---
id: endpoint.ftgo.gateway.get.restaurant.get-all-restaurant-info
kind: Endpoint
type: Endpoint
title: GET /restaurant/get_all_restaurant_info
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
effective_path: /restaurant/get_all_restaurant_info
path_resolution: partial
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/restaurant/restaurant.py
  symbol: application.routes.restaurant.restaurant.get_all_restaurant_info
  line_start: 74
  line_end: 91
  evidence_type: implemented
inbound_relations:
- type: CONTAINS
  source: api.ftgo.gateway
  method: GET
  path: backend/gateway/src/application/routes/restaurant/restaurant.py
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  symbol: application.routes.restaurant.restaurant.get_all_restaurant_info
  line_start: 74
  line_end: 91
  evidence_type: implemented
relations:
- type: USES_SCHEMA
  target: schema.ftgo.gateway.application.schemas.restaurant.restaurant.getallrestaurantinforesponse
  role: response
  symbol: application.routes.restaurant.restaurant.get_all_restaurant_info
  type_expression: GetAllRestaurantInfoResponse
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/restaurant/restaurant.py
  line_start: 74
  line_end: 74
  evidence_type: implemented
attributes:
  method: GET
  effective_path: /restaurant/get_all_restaurant_info
  decorator_path: /get_all_restaurant_info
  router_prefix: /restaurant
  path_resolution: partial
  decorator: router.get("/get_all_restaurant_info", response_model=GetAllRestaurantInfoResponse)
  handler: application.routes.restaurant.restaurant.get_all_restaurant_info
  router: application.routes.restaurant.restaurant:router
  mount_path:
  - main:app
  - application.app:router
  - application.routes.restaurant.restaurant:router
  tags:
  - restaurant
  response_model: GetAllRestaurantInfoResponse
  unresolved_prefix_expressions:
  - service_config.api_prefix
---

# GET /restaurant/get_all_restaurant_info

Candidate HTTP endpoint extracted from a FastAPI route decorator in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Method: `GET`
- Effective path: `/restaurant/get_all_restaurant_info`
- Path resolution: `partial`
- Handler: `application.routes.restaurant.restaurant.get_all_restaurant_info`
- Declared in: `backend/gateway/src/application/routes/restaurant/restaurant.py` (lines 74-91)
- Evidence class: `implemented`

## Unresolved mount prefix

The effective path above omits a mount prefix that is not a string literal in source, so the served path depends on configuration:

- `service_config.api_prefix`

## Schemas

- `response` `USES_SCHEMA` -> `schema.ftgo.gateway.application.schemas.restaurant.restaurant.getallrestaurantinforesponse`

## Review notes

This page is a candidate awaiting review. Method and path come from the decorator shown in `attributes.decorator`; nothing was inferred from names.

