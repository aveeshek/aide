---
id: schema.ftgo.gateway.application.schemas.restaurant.menu.getmenuiteminforesponse
kind: Schema
type: Schema
title: GetMenuItemInfoResponse
status: approved
review_status: approved
candidate_of: fastapi-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: fastapi
service: service.ftgo.gateway
owner: aide-ftgo-cohort
qualified_name: application.schemas.restaurant.menu.GetMenuItemInfoResponse
pydantic_confirmed: true
base_resolution: pydantic_basemodel
bases:
- BaseModel
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/schemas/restaurant/menu.py
  symbol: application.schemas.restaurant.menu.GetMenuItemInfoResponse
  line_start: 29
  line_end: 35
  evidence_type: implemented
inbound_relations:
- type: USES_SCHEMA
  source: endpoint.ftgo.gateway.get.menu.get-info
  role: response
  symbol: application.routes.restaurant.menu.get_info
  type_expression: GetMenuItemInfoResponse
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/restaurant/menu.py
  line_start: 43
  line_end: 43
  evidence_type: implemented
fields:
- name: item_id
  annotation: str
  default_expression: uuid_field()
  line: 30
- name: restaurant_id
  annotation: str
  default_expression: uuid_field()
  line: 31
- name: name
  annotation: str
  default_expression: Field(..., min_length=1, max_length=100)
  line: 32
- name: price
  annotation: float
  line: 33
- name: count
  annotation: int
  default_expression: Field(..., gt=0)
  line: 34
- name: description
  annotation: str
  default_expression: Field(..., min_length=1, max_length=500)
  line: 35
---

# GetMenuItemInfoResponse

Candidate schema extracted from a class definition in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Qualified name: `application.schemas.restaurant.menu.GetMenuItemInfoResponse`
- Declared in: `backend/gateway/src/application/schemas/restaurant/menu.py` (lines 29-35)
- Pydantic BaseModel confirmed in source: `True`
- Base resolution: `pydantic_basemodel`
- Used as: `response`
- Evidence class: `implemented`

## Review notes

This page is a candidate awaiting review. Field annotations are recorded as source text and never evaluated; credential-shaped defaults are redacted at extraction time.

