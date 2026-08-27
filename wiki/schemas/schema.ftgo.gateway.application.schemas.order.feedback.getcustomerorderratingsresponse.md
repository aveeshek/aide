---
id: schema.ftgo.gateway.application.schemas.order.feedback.getcustomerorderratingsresponse
kind: Schema
type: Schema
title: GetCustomerOrderRatingsResponse
status: approved
review_status: approved
candidate_of: fastapi-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: fastapi
service: service.ftgo.gateway
owner: aide-ftgo-cohort
qualified_name: application.schemas.order.feedback.GetCustomerOrderRatingsResponse
pydantic_confirmed: true
base_resolution: pydantic_basemodel
bases:
- BaseModel
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/schemas/order/feedback.py
  symbol: application.schemas.order.feedback.GetCustomerOrderRatingsResponse
  line_start: 71
  line_end: 72
  evidence_type: implemented
inbound_relations:
- type: USES_SCHEMA
  source: endpoint.ftgo.gateway.get.feedback.order.rating.customer
  role: response
  symbol: application.routes.order.feedback.get_customer_order_ratings
  type_expression: GetCustomerOrderRatingsResponse
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/order/feedback.py
  line_start: 191
  line_end: 191
  evidence_type: implemented
fields:
- name: ratings
  annotation: list[GetOrderRatingResponse]
  line: 72
---

# GetCustomerOrderRatingsResponse

Candidate schema extracted from a class definition in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Qualified name: `application.schemas.order.feedback.GetCustomerOrderRatingsResponse`
- Declared in: `backend/gateway/src/application/schemas/order/feedback.py` (lines 71-72)
- Pydantic BaseModel confirmed in source: `True`
- Base resolution: `pydantic_basemodel`
- Used as: `response`
- Evidence class: `implemented`

## Review notes

This page is a candidate awaiting review. Field annotations are recorded as source text and never evaluated; credential-shaped defaults are redacted at extraction time.

