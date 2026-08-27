---
id: schema.ftgo.gateway.application.schemas.order.feedback.getdriverdeliveryratingsresponse
kind: Schema
type: Schema
title: GetDriverDeliveryRatingsResponse
status: approved
review_status: approved
candidate_of: fastapi-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: fastapi
service: service.ftgo.gateway
owner: aide-ftgo-cohort
qualified_name: application.schemas.order.feedback.GetDriverDeliveryRatingsResponse
pydantic_confirmed: true
base_resolution: pydantic_basemodel
bases:
- BaseModel
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/schemas/order/feedback.py
  symbol: application.schemas.order.feedback.GetDriverDeliveryRatingsResponse
  line_start: 39
  line_end: 40
  evidence_type: implemented
inbound_relations:
- type: USES_SCHEMA
  source: endpoint.ftgo.gateway.get.feedback.delivery.rating.driver
  role: response
  symbol: application.routes.order.feedback.get_driver_delivery_ratings
  type_expression: GetDriverDeliveryRatingsResponse
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/order/feedback.py
  line_start: 109
  line_end: 109
  evidence_type: implemented
fields:
- name: ratings
  annotation: list[GetDeliveryRatingResponse]
  line: 40
---

# GetDriverDeliveryRatingsResponse

Candidate schema extracted from a class definition in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Qualified name: `application.schemas.order.feedback.GetDriverDeliveryRatingsResponse`
- Declared in: `backend/gateway/src/application/schemas/order/feedback.py` (lines 39-40)
- Pydantic BaseModel confirmed in source: `True`
- Base resolution: `pydantic_basemodel`
- Used as: `response`
- Evidence class: `implemented`

## Review notes

This page is a candidate awaiting review. Field annotations are recorded as source text and never evaluated; credential-shaped defaults are redacted at extraction time.

