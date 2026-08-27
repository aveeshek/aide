---
id: schema.ftgo.gateway.application.schemas.order.feedback.createorderratingrequest
kind: Schema
type: Schema
title: CreateOrderRatingRequest
status: candidate
review_status: pending
candidate_of: fastapi-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: fastapi
service: service.ftgo.gateway
owner: aide-ftgo-cohort
qualified_name: application.schemas.order.feedback.CreateOrderRatingRequest
pydantic_confirmed: true
base_resolution: pydantic_basemodel
bases:
- BaseModel
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/schemas/order/feedback.py
  symbol: application.schemas.order.feedback.CreateOrderRatingRequest
  line_start: 44
  line_end: 47
  evidence_type: implemented
inbound_relations:
- type: USES_SCHEMA
  source: endpoint.ftgo.gateway.post.feedback.order.rating.create
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
fields:
- name: order_id
  annotation: str
  default_expression: uuid_field()
  line: 45
- name: rating
  annotation: int
  default_expression: Field(..., ge=1, le=5)
  line: 46
- name: comment
  annotation: str
  default_expression: Field(..., max_length=500)
  line: 47
---

# CreateOrderRatingRequest

Candidate schema extracted from a class definition in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Qualified name: `application.schemas.order.feedback.CreateOrderRatingRequest`
- Declared in: `backend/gateway/src/application/schemas/order/feedback.py` (lines 44-47)
- Pydantic BaseModel confirmed in source: `True`
- Base resolution: `pydantic_basemodel`
- Used as: `request`
- Evidence class: `implemented`

## Review notes

This page is a candidate awaiting review. Field annotations are recorded as source text and never evaluated; credential-shaped defaults are redacted at extraction time.

