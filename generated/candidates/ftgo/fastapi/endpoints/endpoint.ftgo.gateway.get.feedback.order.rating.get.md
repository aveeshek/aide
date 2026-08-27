---
id: endpoint.ftgo.gateway.get.feedback.order.rating.get
kind: Endpoint
type: Endpoint
title: GET /feedback/order/rating/get
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
effective_path: /feedback/order/rating/get
path_resolution: partial
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/order/feedback.py
  symbol: application.routes.order.feedback.get_order_rating
  line_start: 171
  line_end: 189
  evidence_type: implemented
inbound_relations:
- type: CONTAINS
  source: api.ftgo.gateway
  method: GET
  path: backend/gateway/src/application/routes/order/feedback.py
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  symbol: application.routes.order.feedback.get_order_rating
  line_start: 171
  line_end: 189
  evidence_type: implemented
relations:
- type: USES_SCHEMA
  target: schema.ftgo.gateway.application.schemas.order.feedback.getorderratingrequest
  role: request
  symbol: application.routes.order.feedback.get_order_rating.request_data
  type_expression: GetOrderRatingRequest
  parameter: request_data
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/order/feedback.py
  line_start: 172
  line_end: 172
  evidence_type: implemented
- type: USES_SCHEMA
  target: schema.ftgo.gateway.application.schemas.order.feedback.getorderratingresponse
  role: response
  symbol: application.routes.order.feedback.get_order_rating
  type_expression: GetOrderRatingResponse
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/order/feedback.py
  line_start: 171
  line_end: 171
  evidence_type: implemented
attributes:
  method: GET
  effective_path: /feedback/order/rating/get
  decorator_path: /order/rating/get
  router_prefix: /feedback
  path_resolution: partial
  decorator: router.get("/order/rating/get", response_model=GetOrderRatingResponse)
  handler: application.routes.order.feedback.get_order_rating
  router: application.routes.order.feedback:router
  mount_path:
  - main:app
  - application.app:router
  - application.routes.order.feedback:router
  tags:
  - feedback
  response_model: GetOrderRatingResponse
  unresolved_prefix_expressions:
  - service_config.api_prefix
---

# GET /feedback/order/rating/get

Candidate HTTP endpoint extracted from a FastAPI route decorator in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Method: `GET`
- Effective path: `/feedback/order/rating/get`
- Path resolution: `partial`
- Handler: `application.routes.order.feedback.get_order_rating`
- Declared in: `backend/gateway/src/application/routes/order/feedback.py` (lines 171-189)
- Evidence class: `implemented`

## Unresolved mount prefix

The effective path above omits a mount prefix that is not a string literal in source, so the served path depends on configuration:

- `service_config.api_prefix`

## Schemas

- `request` `USES_SCHEMA` -> `schema.ftgo.gateway.application.schemas.order.feedback.getorderratingrequest`
- `response` `USES_SCHEMA` -> `schema.ftgo.gateway.application.schemas.order.feedback.getorderratingresponse`

## Review notes

This page is a candidate awaiting review. Method and path come from the decorator shown in `attributes.decorator`; nothing was inferred from names.

