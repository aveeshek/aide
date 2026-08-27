---
id: schema.ftgo.gateway.application.schemas.order.feedback.getrestaurantorderratingsrequest
kind: Schema
type: Schema
title: GetRestaurantOrderRatingsRequest
status: candidate
review_status: pending
candidate_of: fastapi-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: fastapi
service: service.ftgo.gateway
owner: aide-ftgo-cohort
qualified_name: application.schemas.order.feedback.GetRestaurantOrderRatingsRequest
pydantic_confirmed: true
base_resolution: pydantic_basemodel
bases:
- BaseModel
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/schemas/order/feedback.py
  symbol: application.schemas.order.feedback.GetRestaurantOrderRatingsRequest
  line_start: 74
  line_end: 75
  evidence_type: implemented
inbound_relations:
- type: USES_SCHEMA
  source: endpoint.ftgo.gateway.get.feedback.order.rating.restaurant
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
fields:
- name: restaurant_id
  annotation: str
  default_expression: uuid_field()
  line: 75
---

# GetRestaurantOrderRatingsRequest

Candidate schema extracted from a class definition in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Qualified name: `application.schemas.order.feedback.GetRestaurantOrderRatingsRequest`
- Declared in: `backend/gateway/src/application/schemas/order/feedback.py` (lines 74-75)
- Pydantic BaseModel confirmed in source: `True`
- Base resolution: `pydantic_basemodel`
- Used as: `request`
- Evidence class: `implemented`

## Review notes

This page is a candidate awaiting review. Field annotations are recorded as source text and never evaluated; credential-shaped defaults are redacted at extraction time.

