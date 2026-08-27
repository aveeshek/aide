---
id: endpoint.ftgo.gateway.post.order.update
kind: Endpoint
type: Endpoint
title: POST /order/update
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
effective_path: /order/update
path_resolution: partial
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/order/order.py
  symbol: application.routes.order.order.update_order
  line_start: 70
  line_end: 93
  evidence_type: implemented
inbound_relations:
- type: CONTAINS
  source: api.ftgo.gateway
  method: POST
  path: backend/gateway/src/application/routes/order/order.py
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  symbol: application.routes.order.order.update_order
  line_start: 70
  line_end: 93
  evidence_type: implemented
relations:
- type: USES_SCHEMA
  target: schema.ftgo.gateway.application.schemas.common.successresponse
  role: response
  symbol: application.routes.order.order.update_order
  type_expression: SuccessResponse
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/order/order.py
  line_start: 70
  line_end: 70
  evidence_type: implemented
- type: USES_SCHEMA
  target: schema.ftgo.gateway.application.schemas.order.order.updateorderrequest
  role: request
  symbol: application.routes.order.order.update_order.request_data
  type_expression: UpdateOrderRequest
  parameter: request_data
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/order/order.py
  line_start: 71
  line_end: 71
  evidence_type: implemented
attributes:
  method: POST
  effective_path: /order/update
  decorator_path: /update
  router_prefix: /order
  path_resolution: partial
  decorator: router.post("/update", response_model=SuccessResponse)
  handler: application.routes.order.order.update_order
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

# POST /order/update

Candidate HTTP endpoint extracted from a FastAPI route decorator in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Method: `POST`
- Effective path: `/order/update`
- Path resolution: `partial`
- Handler: `application.routes.order.order.update_order`
- Declared in: `backend/gateway/src/application/routes/order/order.py` (lines 70-93)
- Evidence class: `implemented`

## Unresolved mount prefix

The effective path above omits a mount prefix that is not a string literal in source, so the served path depends on configuration:

- `service_config.api_prefix`

## Schemas

- `response` `USES_SCHEMA` -> `schema.ftgo.gateway.application.schemas.common.successresponse`
- `request` `USES_SCHEMA` -> `schema.ftgo.gateway.application.schemas.order.order.updateorderrequest`

## Review notes

This page is a candidate awaiting review. Method and path come from the decorator shown in `attributes.decorator`; nothing was inferred from names.

