---
id: schema.ftgo.gateway.application.schemas.order.feedback.getcustomerorderratingsrequest
kind: Schema
type: Schema
title: GetCustomerOrderRatingsRequest
status: approved
review_status: approved
candidate_of: fastapi-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: fastapi
service: service.ftgo.gateway
owner: aide-ftgo-cohort
qualified_name: application.schemas.order.feedback.GetCustomerOrderRatingsRequest
pydantic_confirmed: true
base_resolution: pydantic_basemodel
bases:
- BaseModel
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/schemas/order/feedback.py
  symbol: application.schemas.order.feedback.GetCustomerOrderRatingsRequest
  line_start: 68
  line_end: 69
  evidence_type: implemented
inbound_relations:
- type: USES_SCHEMA
  source: endpoint.ftgo.gateway.get.feedback.order.rating.customer
  role: request
  symbol: application.routes.order.feedback.get_customer_order_ratings.request_data
  type_expression: GetCustomerOrderRatingsRequest
  parameter: request_data
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/order/feedback.py
  line_start: 192
  line_end: 192
  evidence_type: implemented
---

# GetCustomerOrderRatingsRequest

Candidate schema extracted from a class definition in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Qualified name: `application.schemas.order.feedback.GetCustomerOrderRatingsRequest`
- Declared in: `backend/gateway/src/application/schemas/order/feedback.py` (lines 68-69)
- Pydantic BaseModel confirmed in source: `True`
- Base resolution: `pydantic_basemodel`
- Used as: `request`
- Evidence class: `implemented`

## Review notes

This page is a candidate awaiting review. Field annotations are recorded as source text and never evaluated; credential-shaped defaults are redacted at extraction time.

