---
id: endpoint.ftgo.gateway.put.feedback.delivery.rating.update
kind: Endpoint
type: Endpoint
title: PUT /feedback/delivery/rating/update
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
effective_path: /feedback/delivery/rating/update
path_resolution: partial
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/order/feedback.py
  symbol: application.routes.order.feedback.update_delivery_rating
  line_start: 50
  line_end: 68
  evidence_type: implemented
inbound_relations:
- type: CONTAINS
  source: api.ftgo.gateway
  method: PUT
  path: backend/gateway/src/application/routes/order/feedback.py
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  symbol: application.routes.order.feedback.update_delivery_rating
  line_start: 50
  line_end: 68
  evidence_type: implemented
relations:
- type: USES_SCHEMA
  target: schema.ftgo.gateway.application.schemas.order.feedback.updatedeliveryratingrequest
  role: request
  symbol: application.routes.order.feedback.update_delivery_rating.request_data
  type_expression: UpdateDeliveryRatingRequest
  parameter: request_data
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/order/feedback.py
  line_start: 51
  line_end: 51
  evidence_type: implemented
- type: USES_SCHEMA
  target: schema.ftgo.gateway.application.schemas.order.feedback.updatedeliveryratingresponse
  role: response
  symbol: application.routes.order.feedback.update_delivery_rating
  type_expression: UpdateDeliveryRatingResponse
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/order/feedback.py
  line_start: 50
  line_end: 50
  evidence_type: implemented
attributes:
  method: PUT
  effective_path: /feedback/delivery/rating/update
  decorator_path: /delivery/rating/update
  router_prefix: /feedback
  path_resolution: partial
  decorator: router.put("/delivery/rating/update", response_model=UpdateDeliveryRatingResponse)
  handler: application.routes.order.feedback.update_delivery_rating
  router: application.routes.order.feedback:router
  mount_path:
  - main:app
  - application.app:router
  - application.routes.order.feedback:router
  tags:
  - feedback
  response_model: UpdateDeliveryRatingResponse
  unresolved_prefix_expressions:
  - service_config.api_prefix
---

# PUT /feedback/delivery/rating/update

Candidate HTTP endpoint extracted from a FastAPI route decorator in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Method: `PUT`
- Effective path: `/feedback/delivery/rating/update`
- Path resolution: `partial`
- Handler: `application.routes.order.feedback.update_delivery_rating`
- Declared in: `backend/gateway/src/application/routes/order/feedback.py` (lines 50-68)
- Evidence class: `implemented`

## Unresolved mount prefix

The effective path above omits a mount prefix that is not a string literal in source, so the served path depends on configuration:

- `service_config.api_prefix`

## Schemas

- `request` `USES_SCHEMA` -> `schema.ftgo.gateway.application.schemas.order.feedback.updatedeliveryratingrequest`
- `response` `USES_SCHEMA` -> `schema.ftgo.gateway.application.schemas.order.feedback.updatedeliveryratingresponse`

## Review notes

This page is a candidate awaiting review. Method and path come from the decorator shown in `attributes.decorator`; nothing was inferred from names.

