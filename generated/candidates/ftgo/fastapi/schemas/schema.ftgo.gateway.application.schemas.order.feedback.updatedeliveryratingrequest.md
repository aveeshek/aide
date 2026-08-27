---
id: schema.ftgo.gateway.application.schemas.order.feedback.updatedeliveryratingrequest
kind: Schema
type: Schema
title: UpdateDeliveryRatingRequest
status: candidate
review_status: pending
candidate_of: fastapi-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: fastapi
service: service.ftgo.gateway
owner: aide-ftgo-cohort
qualified_name: application.schemas.order.feedback.UpdateDeliveryRatingRequest
pydantic_confirmed: true
base_resolution: pydantic_basemodel
bases:
- BaseModel
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/schemas/order/feedback.py
  symbol: application.schemas.order.feedback.UpdateDeliveryRatingRequest
  line_start: 14
  line_end: 17
  evidence_type: implemented
inbound_relations:
- type: USES_SCHEMA
  source: endpoint.ftgo.gateway.put.feedback.delivery.rating.update
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
fields:
- name: rating_id
  annotation: str
  default_expression: uuid_field()
  line: 15
- name: rating
  annotation: int
  default_expression: Field(..., ge=1, le=5)
  line: 16
- name: comment
  annotation: str
  default_expression: Field(..., max_length=500)
  line: 17
---

# UpdateDeliveryRatingRequest

Candidate schema extracted from a class definition in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Qualified name: `application.schemas.order.feedback.UpdateDeliveryRatingRequest`
- Declared in: `backend/gateway/src/application/schemas/order/feedback.py` (lines 14-17)
- Pydantic BaseModel confirmed in source: `True`
- Base resolution: `pydantic_basemodel`
- Used as: `request`
- Evidence class: `implemented`

## Review notes

This page is a candidate awaiting review. Field annotations are recorded as source text and never evaluated; credential-shaped defaults are redacted at extraction time.

