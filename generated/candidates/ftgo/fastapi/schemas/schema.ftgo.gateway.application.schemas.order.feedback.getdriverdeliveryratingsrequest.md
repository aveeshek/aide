---
id: schema.ftgo.gateway.application.schemas.order.feedback.getdriverdeliveryratingsrequest
kind: Schema
type: Schema
title: GetDriverDeliveryRatingsRequest
status: candidate
review_status: pending
candidate_of: fastapi-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: fastapi
service: service.ftgo.gateway
owner: aide-ftgo-cohort
qualified_name: application.schemas.order.feedback.GetDriverDeliveryRatingsRequest
pydantic_confirmed: true
base_resolution: pydantic_basemodel
bases:
- BaseModel
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/schemas/order/feedback.py
  symbol: application.schemas.order.feedback.GetDriverDeliveryRatingsRequest
  line_start: 36
  line_end: 37
  evidence_type: implemented
inbound_relations:
- type: USES_SCHEMA
  source: endpoint.ftgo.gateway.get.feedback.delivery.rating.driver
  role: request
  symbol: application.routes.order.feedback.get_driver_delivery_ratings.request_data
  type_expression: GetDriverDeliveryRatingsRequest
  parameter: request_data
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/order/feedback.py
  line_start: 110
  line_end: 110
  evidence_type: implemented
fields:
- name: driver_id
  annotation: str
  default_expression: uuid_field()
  line: 37
---

# GetDriverDeliveryRatingsRequest

Candidate schema extracted from a class definition in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Qualified name: `application.schemas.order.feedback.GetDriverDeliveryRatingsRequest`
- Declared in: `backend/gateway/src/application/schemas/order/feedback.py` (lines 36-37)
- Pydantic BaseModel confirmed in source: `True`
- Base resolution: `pydantic_basemodel`
- Used as: `request`
- Evidence class: `implemented`

## Review notes

This page is a candidate awaiting review. Field annotations are recorded as source text and never evaluated; credential-shaped defaults are redacted at extraction time.

