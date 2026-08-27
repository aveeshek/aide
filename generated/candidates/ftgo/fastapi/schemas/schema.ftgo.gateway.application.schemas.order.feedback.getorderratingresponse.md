---
id: schema.ftgo.gateway.application.schemas.order.feedback.getorderratingresponse
kind: Schema
type: Schema
title: GetOrderRatingResponse
status: candidate
review_status: pending
candidate_of: fastapi-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: fastapi
service: service.ftgo.gateway
owner: aide-ftgo-cohort
qualified_name: application.schemas.order.feedback.GetOrderRatingResponse
pydantic_confirmed: true
base_resolution: pydantic_basemodel
bases:
- BaseModel
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/schemas/order/feedback.py
  symbol: application.schemas.order.feedback.GetOrderRatingResponse
  line_start: 63
  line_end: 66
  evidence_type: implemented
inbound_relations:
- type: USES_SCHEMA
  source: endpoint.ftgo.gateway.get.feedback.order.rating.get
  role: response
  symbol: application.routes.order.feedback.get_order_rating
  type_expression: GetOrderRatingResponse
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/order/feedback.py
  line_start: 171
  line_end: 171
  evidence_type: implemented
fields:
- name: order_id
  annotation: str
  default_expression: uuid_field()
  line: 64
- name: rating
  annotation: int
  line: 65
- name: comment
  annotation: str
  line: 66
---

# GetOrderRatingResponse

Candidate schema extracted from a class definition in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Qualified name: `application.schemas.order.feedback.GetOrderRatingResponse`
- Declared in: `backend/gateway/src/application/schemas/order/feedback.py` (lines 63-66)
- Pydantic BaseModel confirmed in source: `True`
- Base resolution: `pydantic_basemodel`
- Used as: `response`
- Evidence class: `implemented`

## Review notes

This page is a candidate awaiting review. Field annotations are recorded as source text and never evaluated; credential-shaped defaults are redacted at extraction time.

