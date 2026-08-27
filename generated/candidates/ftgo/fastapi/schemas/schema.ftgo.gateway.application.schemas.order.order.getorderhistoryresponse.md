---
id: schema.ftgo.gateway.application.schemas.order.order.getorderhistoryresponse
kind: Schema
type: Schema
title: GetOrderHistoryResponse
status: candidate
review_status: pending
candidate_of: fastapi-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: fastapi
service: service.ftgo.gateway
owner: aide-ftgo-cohort
qualified_name: application.schemas.order.order.GetOrderHistoryResponse
pydantic_confirmed: false
base_resolution: external_base
bases:
- BaseSchema
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/schemas/order/order.py
  symbol: application.schemas.order.order.GetOrderHistoryResponse
  line_start: 21
  line_end: 26
  evidence_type: implemented
inbound_relations:
- type: USES_SCHEMA
  source: endpoint.ftgo.gateway.post.order.history
  role: response
  symbol: application.routes.order.order.get_order_history
  type_expression: GetOrderHistoryResponse
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/order/order.py
  line_start: 19
  line_end: 19
  evidence_type: implemented
fields:
- name: customer_id
  annotation: str
  default_expression: uuid_field()
  line: 22
- name: restaurant_id
  annotation: str
  default_expression: uuid_field()
  line: 23
- name: total_amount
  annotation: float
  default_expression: Field(..., gt=0)
  line: 24
- name: order_items
  annotation: list[dict[str, Any]]
  line: 25
- name: status_history
  annotation: list
  line: 26
---

# GetOrderHistoryResponse

Candidate schema extracted from a class definition in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Qualified name: `application.schemas.order.order.GetOrderHistoryResponse`
- Declared in: `backend/gateway/src/application/schemas/order/order.py` (lines 21-26)
- Pydantic BaseModel confirmed in source: `False`
- Base resolution: `external_base`
- Used as: `response`
- Evidence class: `implemented`

## Review notes

This page is a candidate awaiting review. Field annotations are recorded as source text and never evaluated; credential-shaped defaults are redacted at extraction time.

