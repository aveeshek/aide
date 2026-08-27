---
id: schema.ftgo.gateway.application.schemas.order.feedback.getdeliveryratingresponse
kind: Schema
type: Schema
title: GetDeliveryRatingResponse
status: candidate
review_status: pending
candidate_of: fastapi-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: fastapi
service: service.ftgo.gateway
owner: aide-ftgo-cohort
qualified_name: application.schemas.order.feedback.GetDeliveryRatingResponse
pydantic_confirmed: true
base_resolution: pydantic_basemodel
bases:
- BaseModel
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/schemas/order/feedback.py
  symbol: application.schemas.order.feedback.GetDeliveryRatingResponse
  line_start: 25
  line_end: 28
  evidence_type: implemented
inbound_relations:
- type: USES_SCHEMA
  source: endpoint.ftgo.gateway.get.feedback.delivery.rating.get
  role: response
  symbol: application.routes.order.feedback.get_delivery_rating
  type_expression: GetDeliveryRatingResponse
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/order/feedback.py
  line_start: 70
  line_end: 70
  evidence_type: implemented
fields:
- name: delivery_id
  annotation: str
  default_expression: uuid_field()
  line: 26
- name: rating
  annotation: int
  line: 27
- name: comment
  annotation: str
  line: 28
---

# GetDeliveryRatingResponse

Candidate schema extracted from a class definition in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Qualified name: `application.schemas.order.feedback.GetDeliveryRatingResponse`
- Declared in: `backend/gateway/src/application/schemas/order/feedback.py` (lines 25-28)
- Pydantic BaseModel confirmed in source: `True`
- Base resolution: `pydantic_basemodel`
- Used as: `response`
- Evidence class: `implemented`

## Review notes

This page is a candidate awaiting review. Field annotations are recorded as source text and never evaluated; credential-shaped defaults are redacted at extraction time.

