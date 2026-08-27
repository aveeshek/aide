---
id: schema.ftgo.gateway.application.schemas.order.order.updateorderrequest
kind: Schema
type: Schema
title: UpdateOrderRequest
status: approved
review_status: approved
candidate_of: fastapi-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: fastapi
service: service.ftgo.gateway
owner: aide-ftgo-cohort
qualified_name: application.schemas.order.order.UpdateOrderRequest
pydantic_confirmed: false
base_resolution: external_base
bases:
- BaseSchema
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/schemas/order/order.py
  symbol: application.schemas.order.order.UpdateOrderRequest
  line_start: 29
  line_end: 32
  evidence_type: implemented
inbound_relations:
- type: USES_SCHEMA
  source: endpoint.ftgo.gateway.post.order.update
  role: request
  symbol: application.routes.order.order.update_order.request_data
  type_expression: UpdateOrderRequest
  parameter: request_data
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/order/order.py
  line_start: 71
  line_end: 71
  evidence_type: implemented
fields:
- name: items
  annotation: list[dict[str, Any]]
  line: 30
- name: status_history
  annotation: list
  line: 31
- name: total_amount
  annotation: float
  default_expression: Field(..., gt=0)
  line: 32
---

# UpdateOrderRequest

Candidate schema extracted from a class definition in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Qualified name: `application.schemas.order.order.UpdateOrderRequest`
- Declared in: `backend/gateway/src/application/schemas/order/order.py` (lines 29-32)
- Pydantic BaseModel confirmed in source: `False`
- Base resolution: `external_base`
- Used as: `request`
- Evidence class: `implemented`

## Review notes

This page is a candidate awaiting review. Field annotations are recorded as source text and never evaluated; credential-shaped defaults are redacted at extraction time.

