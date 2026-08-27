---
id: schema.ftgo.gateway.application.schemas.order.feedback.updateorderratingresponse
kind: Schema
type: Schema
title: UpdateOrderRatingResponse
status: approved
review_status: approved
candidate_of: fastapi-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: fastapi
service: service.ftgo.gateway
owner: aide-ftgo-cohort
qualified_name: application.schemas.order.feedback.UpdateOrderRatingResponse
pydantic_confirmed: true
base_resolution: pydantic_basemodel
bases:
- BaseModel
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/schemas/order/feedback.py
  symbol: application.schemas.order.feedback.UpdateOrderRatingResponse
  line_start: 57
  line_end: 58
  evidence_type: implemented
inbound_relations:
- type: USES_SCHEMA
  source: endpoint.ftgo.gateway.put.feedback.order.rating.update
  role: response
  symbol: application.routes.order.feedback.update_order_rating
  type_expression: UpdateOrderRatingResponse
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/order/feedback.py
  line_start: 151
  line_end: 151
  evidence_type: implemented
fields:
- name: rating_id
  annotation: str
  default_expression: uuid_field()
  line: 58
---

# UpdateOrderRatingResponse

Candidate schema extracted from a class definition in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Qualified name: `application.schemas.order.feedback.UpdateOrderRatingResponse`
- Declared in: `backend/gateway/src/application/schemas/order/feedback.py` (lines 57-58)
- Pydantic BaseModel confirmed in source: `True`
- Base resolution: `pydantic_basemodel`
- Used as: `response`
- Evidence class: `implemented`

## Review notes

This page is a candidate awaiting review. Field annotations are recorded as source text and never evaluated; credential-shaped defaults are redacted at extraction time.

