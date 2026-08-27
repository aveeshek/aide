---
id: endpoint.ftgo.gateway.post.order.history
kind: Endpoint
type: Endpoint
title: POST /order/history
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
effective_path: /order/history
path_resolution: partial
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/order/order.py
  symbol: application.routes.order.order.get_order_history
  line_start: 19
  line_end: 40
  evidence_type: implemented
inbound_relations:
- type: CONTAINS
  source: api.ftgo.gateway
  method: POST
  path: backend/gateway/src/application/routes/order/order.py
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  symbol: application.routes.order.order.get_order_history
  line_start: 19
  line_end: 40
  evidence_type: implemented
relations:
- type: USES_SCHEMA
  target: schema.ftgo.gateway.application.schemas.order.order.getorderhistoryrequest
  role: request
  symbol: application.routes.order.order.get_order_history.request_data
  type_expression: GetOrderHistoryRequest
  parameter: request_data
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/order/order.py
  line_start: 20
  line_end: 20
  evidence_type: implemented
- type: USES_SCHEMA
  target: schema.ftgo.gateway.application.schemas.order.order.getorderhistoryresponse
  role: response
  symbol: application.routes.order.order.get_order_history
  type_expression: GetOrderHistoryResponse
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/order/order.py
  line_start: 19
  line_end: 19
  evidence_type: implemented
attributes:
  method: POST
  effective_path: /order/history
  decorator_path: /history
  router_prefix: /order
  path_resolution: partial
  decorator: router.post("/history", response_model=GetOrderHistoryResponse)
  handler: application.routes.order.order.get_order_history
  router: application.routes.order.order:router
  mount_path:
  - main:app
  - application.app:router
  - application.routes.order.order:router
  tags:
  - order_service
  response_model: GetOrderHistoryResponse
  unresolved_prefix_expressions:
  - service_config.api_prefix
---

# POST /order/history

Candidate HTTP endpoint extracted from a FastAPI route decorator in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Method: `POST`
- Effective path: `/order/history`
- Path resolution: `partial`
- Handler: `application.routes.order.order.get_order_history`
- Declared in: `backend/gateway/src/application/routes/order/order.py` (lines 19-40)
- Evidence class: `implemented`

## Unresolved mount prefix

The effective path above omits a mount prefix that is not a string literal in source, so the served path depends on configuration:

- `service_config.api_prefix`

## Schemas

- `request` `USES_SCHEMA` -> `schema.ftgo.gateway.application.schemas.order.order.getorderhistoryrequest`
- `response` `USES_SCHEMA` -> `schema.ftgo.gateway.application.schemas.order.order.getorderhistoryresponse`

## Review notes

This page is a candidate awaiting review. Method and path come from the decorator shown in `attributes.decorator`; nothing was inferred from names.

