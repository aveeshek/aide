---
id: endpoint.ftgo.gateway.post.feedback.order.rating.create
kind: Endpoint
type: Endpoint
title: POST /feedback/order/rating/create
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
effective_path: /feedback/order/rating/create
path_resolution: partial
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/order/feedback.py
  symbol: application.routes.order.feedback.create_order_rating
  line_start: 131
  line_end: 149
  evidence_type: implemented
inbound_relations:
- type: CONTAINS
  source: api.ftgo.gateway
  method: POST
  path: backend/gateway/src/application/routes/order/feedback.py
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  symbol: application.routes.order.feedback.create_order_rating
  line_start: 131
  line_end: 149
  evidence_type: implemented
relations:
- type: USES_SCHEMA
  target: schema.ftgo.gateway.application.schemas.order.feedback.createorderratingrequest
  role: request
  symbol: application.routes.order.feedback.create_order_rating.request_data
  type_expression: CreateOrderRatingRequest
  parameter: request_data
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/order/feedback.py
  line_start: 132
  line_end: 132
  evidence_type: implemented
- type: USES_SCHEMA
  target: schema.ftgo.gateway.application.schemas.order.feedback.createorderratingresponse
  role: response
  symbol: application.routes.order.feedback.create_order_rating
  type_expression: CreateOrderRatingResponse
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/order/feedback.py
  line_start: 131
  line_end: 131
  evidence_type: implemented
attributes:
  method: POST
  effective_path: /feedback/order/rating/create
  decorator_path: /order/rating/create
  router_prefix: /feedback
  path_resolution: partial
  decorator: router.post("/order/rating/create", response_model=CreateOrderRatingResponse)
  handler: application.routes.order.feedback.create_order_rating
  router: application.routes.order.feedback:router
  mount_path:
  - main:app
  - application.app:router
  - application.routes.order.feedback:router
  tags:
  - feedback
  response_model: CreateOrderRatingResponse
  unresolved_prefix_expressions:
  - service_config.api_prefix
---

# POST /feedback/order/rating/create

Candidate HTTP endpoint extracted from a FastAPI route decorator in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Method: `POST`
- Effective path: `/feedback/order/rating/create`
- Path resolution: `partial`
- Handler: `application.routes.order.feedback.create_order_rating`
- Declared in: `backend/gateway/src/application/routes/order/feedback.py` (lines 131-149)
- Evidence class: `implemented`

## Unresolved mount prefix

The effective path above omits a mount prefix that is not a string literal in source, so the served path depends on configuration:

- `service_config.api_prefix`

## Schemas

- `request` `USES_SCHEMA` -> `schema.ftgo.gateway.application.schemas.order.feedback.createorderratingrequest`
- `response` `USES_SCHEMA` -> `schema.ftgo.gateway.application.schemas.order.feedback.createorderratingresponse`

## Review notes

This page is a candidate awaiting review. Method and path come from the decorator shown in `attributes.decorator`; nothing was inferred from names.

