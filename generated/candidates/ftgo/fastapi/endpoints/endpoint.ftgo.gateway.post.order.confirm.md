---
id: endpoint.ftgo.gateway.post.order.confirm
kind: Endpoint
type: Endpoint
title: POST /order/confirm
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
effective_path: /order/confirm
path_resolution: partial
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/order/order.py
  symbol: application.routes.order.order.restaurant_confirm
  line_start: 96
  line_end: 118
  evidence_type: implemented
inbound_relations:
- type: CONTAINS
  source: api.ftgo.gateway
  method: POST
  path: backend/gateway/src/application/routes/order/order.py
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  symbol: application.routes.order.order.restaurant_confirm
  line_start: 96
  line_end: 118
  evidence_type: implemented
relations:
- type: USES_SCHEMA
  target: schema.ftgo.gateway.application.schemas.common.successresponse
  role: response
  symbol: application.routes.order.order.restaurant_confirm
  type_expression: SuccessResponse
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/order/order.py
  line_start: 96
  line_end: 96
  evidence_type: implemented
- type: USES_SCHEMA
  target: schema.ftgo.gateway.application.schemas.order.order.confirmorderrequest
  role: request
  symbol: application.routes.order.order.restaurant_confirm.request_data
  type_expression: ConfirmOrderRequest
  parameter: request_data
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/order/order.py
  line_start: 97
  line_end: 97
  evidence_type: implemented
attributes:
  method: POST
  effective_path: /order/confirm
  decorator_path: /confirm
  router_prefix: /order
  path_resolution: partial
  decorator: router.post("/confirm", response_model=SuccessResponse)
  handler: application.routes.order.order.restaurant_confirm
  router: application.routes.order.order:router
  mount_path:
  - main:app
  - application.app:router
  - application.routes.order.order:router
  tags:
  - order_service
  response_model: SuccessResponse
  unresolved_prefix_expressions:
  - service_config.api_prefix
---

# POST /order/confirm

Candidate HTTP endpoint extracted from a FastAPI route decorator in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Method: `POST`
- Effective path: `/order/confirm`
- Path resolution: `partial`
- Handler: `application.routes.order.order.restaurant_confirm`
- Declared in: `backend/gateway/src/application/routes/order/order.py` (lines 96-118)
- Evidence class: `implemented`

## Unresolved mount prefix

The effective path above omits a mount prefix that is not a string literal in source, so the served path depends on configuration:

- `service_config.api_prefix`

## Schemas

- `response` `USES_SCHEMA` -> `schema.ftgo.gateway.application.schemas.common.successresponse`
- `request` `USES_SCHEMA` -> `schema.ftgo.gateway.application.schemas.order.order.confirmorderrequest`

## Review notes

This page is a candidate awaiting review. Method and path come from the decorator shown in `attributes.decorator`; nothing was inferred from names.

