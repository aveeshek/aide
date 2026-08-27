---
id: schema.ftgo.gateway.application.schemas.order.order.rejectorderrequest
kind: Schema
type: Schema
title: RejectOrderRequest
status: candidate
review_status: pending
candidate_of: fastapi-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: fastapi
service: service.ftgo.gateway
owner: aide-ftgo-cohort
qualified_name: application.schemas.order.order.RejectOrderRequest
pydantic_confirmed: false
base_resolution: external_base
bases:
- BaseSchema
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/schemas/order/order.py
  symbol: application.schemas.order.order.RejectOrderRequest
  line_start: 40
  line_end: 42
  evidence_type: implemented
inbound_relations:
- type: USES_SCHEMA
  source: endpoint.ftgo.gateway.post.order.reject
  role: request
  symbol: application.routes.order.order.restaurant_reject.request_data
  type_expression: RejectOrderRequest
  parameter: request_data
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/order/order.py
  line_start: 122
  line_end: 122
  evidence_type: implemented
fields:
- name: order_id
  annotation: str
  default_expression: uuid_field()
  line: 41
- name: restaurant_id
  annotation: str
  default_expression: uuid_field()
  line: 42
---

# RejectOrderRequest

Candidate schema extracted from a class definition in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Qualified name: `application.schemas.order.order.RejectOrderRequest`
- Declared in: `backend/gateway/src/application/schemas/order/order.py` (lines 40-42)
- Pydantic BaseModel confirmed in source: `False`
- Base resolution: `external_base`
- Used as: `request`
- Evidence class: `implemented`

## Review notes

This page is a candidate awaiting review. Field annotations are recorded as source text and never evaluated; credential-shaped defaults are redacted at extraction time.

