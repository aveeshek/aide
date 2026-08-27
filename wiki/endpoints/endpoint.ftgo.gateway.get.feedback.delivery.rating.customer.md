---
id: endpoint.ftgo.gateway.get.feedback.delivery.rating.customer
kind: Endpoint
type: Endpoint
title: GET /feedback/delivery/rating/customer
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
method: GET
effective_path: /feedback/delivery/rating/customer
path_resolution: partial
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/order/feedback.py
  symbol: application.routes.order.feedback.get_customer_delivery_ratings
  line_start: 89
  line_end: 107
  evidence_type: implemented
inbound_relations:
- type: CONTAINS
  source: api.ftgo.gateway
  method: GET
  path: backend/gateway/src/application/routes/order/feedback.py
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  symbol: application.routes.order.feedback.get_customer_delivery_ratings
  line_start: 89
  line_end: 107
  evidence_type: implemented
relations:
- type: USES_SCHEMA
  target: schema.ftgo.gateway.application.schemas.order.feedback.getcustomerdeliveryratingsrequest
  role: request
  symbol: application.routes.order.feedback.get_customer_delivery_ratings.request_data
  type_expression: GetCustomerDeliveryRatingsRequest
  parameter: request_data
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/order/feedback.py
  line_start: 90
  line_end: 90
  evidence_type: implemented
- type: USES_SCHEMA
  target: schema.ftgo.gateway.application.schemas.order.feedback.getcustomerdeliveryratingsresponse
  role: response
  symbol: application.routes.order.feedback.get_customer_delivery_ratings
  type_expression: GetCustomerDeliveryRatingsResponse
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/order/feedback.py
  line_start: 89
  line_end: 89
  evidence_type: implemented
attributes:
  method: GET
  effective_path: /feedback/delivery/rating/customer
  decorator_path: /delivery/rating/customer
  router_prefix: /feedback
  path_resolution: partial
  decorator: router.get("/delivery/rating/customer", response_model=GetCustomerDeliveryRatingsResponse)
  handler: application.routes.order.feedback.get_customer_delivery_ratings
  router: application.routes.order.feedback:router
  mount_path:
  - main:app
  - application.app:router
  - application.routes.order.feedback:router
  tags:
  - feedback
  response_model: GetCustomerDeliveryRatingsResponse
  unresolved_prefix_expressions:
  - service_config.api_prefix
---

# GET /feedback/delivery/rating/customer

Candidate HTTP endpoint extracted from a FastAPI route decorator in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Method: `GET`
- Effective path: `/feedback/delivery/rating/customer`
- Path resolution: `partial`
- Handler: `application.routes.order.feedback.get_customer_delivery_ratings`
- Declared in: `backend/gateway/src/application/routes/order/feedback.py` (lines 89-107)
- Evidence class: `implemented`

## Unresolved mount prefix

The effective path above omits a mount prefix that is not a string literal in source, so the served path depends on configuration:

- `service_config.api_prefix`

## Schemas

- `request` `USES_SCHEMA` -> `schema.ftgo.gateway.application.schemas.order.feedback.getcustomerdeliveryratingsrequest`
- `response` `USES_SCHEMA` -> `schema.ftgo.gateway.application.schemas.order.feedback.getcustomerdeliveryratingsresponse`

## Review notes

This page is a candidate awaiting review. Method and path come from the decorator shown in `attributes.decorator`; nothing was inferred from names.

