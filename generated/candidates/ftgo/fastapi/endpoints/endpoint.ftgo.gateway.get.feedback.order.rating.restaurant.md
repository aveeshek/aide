---
id: endpoint.ftgo.gateway.get.feedback.order.rating.restaurant
kind: Endpoint
type: Endpoint
title: GET /feedback/order/rating/restaurant
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
effective_path: /feedback/order/rating/restaurant
path_resolution: partial
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/order/feedback.py
  symbol: application.routes.order.feedback.get_restaurant_order_ratings
  line_start: 211
  line_end: 229
  evidence_type: implemented
inbound_relations:
- type: CONTAINS
  source: api.ftgo.gateway
  method: GET
  path: backend/gateway/src/application/routes/order/feedback.py
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  symbol: application.routes.order.feedback.get_restaurant_order_ratings
  line_start: 211
  line_end: 229
  evidence_type: implemented
relations:
- type: USES_SCHEMA
  target: schema.ftgo.gateway.application.schemas.order.feedback.getrestaurantorderratingsrequest
  role: request
  symbol: application.routes.order.feedback.get_restaurant_order_ratings.request_data
  type_expression: GetRestaurantOrderRatingsRequest
  parameter: request_data
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/order/feedback.py
  line_start: 212
  line_end: 212
  evidence_type: implemented
- type: USES_SCHEMA
  target: schema.ftgo.gateway.application.schemas.order.feedback.getrestaurantorderratingsresponse
  role: response
  symbol: application.routes.order.feedback.get_restaurant_order_ratings
  type_expression: GetRestaurantOrderRatingsResponse
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/order/feedback.py
  line_start: 211
  line_end: 211
  evidence_type: implemented
attributes:
  method: GET
  effective_path: /feedback/order/rating/restaurant
  decorator_path: /order/rating/restaurant
  router_prefix: /feedback
  path_resolution: partial
  decorator: router.get("/order/rating/restaurant", response_model=GetRestaurantOrderRatingsResponse)
  handler: application.routes.order.feedback.get_restaurant_order_ratings
  router: application.routes.order.feedback:router
  mount_path:
  - main:app
  - application.app:router
  - application.routes.order.feedback:router
  tags:
  - feedback
  response_model: GetRestaurantOrderRatingsResponse
  unresolved_prefix_expressions:
  - service_config.api_prefix
---

# GET /feedback/order/rating/restaurant

Candidate HTTP endpoint extracted from a FastAPI route decorator in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Method: `GET`
- Effective path: `/feedback/order/rating/restaurant`
- Path resolution: `partial`
- Handler: `application.routes.order.feedback.get_restaurant_order_ratings`
- Declared in: `backend/gateway/src/application/routes/order/feedback.py` (lines 211-229)
- Evidence class: `implemented`

## Unresolved mount prefix

The effective path above omits a mount prefix that is not a string literal in source, so the served path depends on configuration:

- `service_config.api_prefix`

## Schemas

- `request` `USES_SCHEMA` -> `schema.ftgo.gateway.application.schemas.order.feedback.getrestaurantorderratingsrequest`
- `response` `USES_SCHEMA` -> `schema.ftgo.gateway.application.schemas.order.feedback.getrestaurantorderratingsresponse`

## Review notes

This page is a candidate awaiting review. Method and path come from the decorator shown in `attributes.decorator`; nothing was inferred from names.

