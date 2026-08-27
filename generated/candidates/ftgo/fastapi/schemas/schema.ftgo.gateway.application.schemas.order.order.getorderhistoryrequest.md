---
id: schema.ftgo.gateway.application.schemas.order.order.getorderhistoryrequest
kind: Schema
type: Schema
title: GetOrderHistoryRequest
status: candidate
review_status: pending
candidate_of: fastapi-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: fastapi
service: service.ftgo.gateway
owner: aide-ftgo-cohort
qualified_name: application.schemas.order.order.GetOrderHistoryRequest
pydantic_confirmed: false
base_resolution: external_base
bases:
- BaseSchema
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/schemas/order/order.py
  symbol: application.schemas.order.order.GetOrderHistoryRequest
  line_start: 17
  line_end: 18
  evidence_type: implemented
inbound_relations:
- type: USES_SCHEMA
  source: endpoint.ftgo.gateway.post.order.history
  role: request
  symbol: application.routes.order.order.get_order_history.request_data
  type_expression: GetOrderHistoryRequest
  parameter: request_data
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/order/order.py
  line_start: 20
  line_end: 20
  evidence_type: implemented
fields:
- name: order_id
  annotation: str
  default_expression: uuid_field()
  line: 18
---

# GetOrderHistoryRequest

Candidate schema extracted from a class definition in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Qualified name: `application.schemas.order.order.GetOrderHistoryRequest`
- Declared in: `backend/gateway/src/application/schemas/order/order.py` (lines 17-18)
- Pydantic BaseModel confirmed in source: `False`
- Base resolution: `external_base`
- Used as: `request`
- Evidence class: `implemented`

## Review notes

This page is a candidate awaiting review. Field annotations are recorded as source text and never evaluated; credential-shaped defaults are redacted at extraction time.

