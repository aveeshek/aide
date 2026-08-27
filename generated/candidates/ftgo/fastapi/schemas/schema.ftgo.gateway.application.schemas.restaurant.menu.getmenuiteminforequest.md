---
id: schema.ftgo.gateway.application.schemas.restaurant.menu.getmenuiteminforequest
kind: Schema
type: Schema
title: GetMenuItemInfoRequest
status: candidate
review_status: pending
candidate_of: fastapi-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: fastapi
service: service.ftgo.gateway
owner: aide-ftgo-cohort
qualified_name: application.schemas.restaurant.menu.GetMenuItemInfoRequest
pydantic_confirmed: true
base_resolution: pydantic_basemodel
bases:
- BaseModel
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/schemas/restaurant/menu.py
  symbol: application.schemas.restaurant.menu.GetMenuItemInfoRequest
  line_start: 20
  line_end: 26
  evidence_type: implemented
inbound_relations:
- type: USES_SCHEMA
  source: endpoint.ftgo.gateway.get.menu.get-info
  role: request
  symbol: application.routes.restaurant.menu.get_info.request_data
  type_expression: GetMenuItemInfoRequest
  parameter: request_data
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/restaurant/menu.py
  line_start: 44
  line_end: 44
  evidence_type: implemented
fields:
- name: item_id
  annotation: str
  default_expression: uuid_field()
  line: 21
- name: restaurant_id
  annotation: str
  default_expression: uuid_field()
  line: 22
- name: name
  annotation: str
  default_expression: Field(..., min_length=1, max_length=100)
  line: 23
- name: price
  annotation: float
  line: 24
- name: count
  annotation: int
  default_expression: Field(..., gt=0)
  line: 25
- name: description
  annotation: str
  default_expression: Field(..., min_length=1, max_length=500)
  line: 26
---

# GetMenuItemInfoRequest

Candidate schema extracted from a class definition in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Qualified name: `application.schemas.restaurant.menu.GetMenuItemInfoRequest`
- Declared in: `backend/gateway/src/application/schemas/restaurant/menu.py` (lines 20-26)
- Pydantic BaseModel confirmed in source: `True`
- Base resolution: `pydantic_basemodel`
- Used as: `request`
- Evidence class: `implemented`

## Review notes

This page is a candidate awaiting review. Field annotations are recorded as source text and never evaluated; credential-shaped defaults are redacted at extraction time.

