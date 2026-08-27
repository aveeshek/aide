---
id: schema.ftgo.gateway.application.schemas.restaurant.menu.addmenuitemrequest
kind: Schema
type: Schema
title: AddMenuItemRequest
status: approved
review_status: approved
candidate_of: fastapi-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: fastapi
service: service.ftgo.gateway
owner: aide-ftgo-cohort
qualified_name: application.schemas.restaurant.menu.AddMenuItemRequest
pydantic_confirmed: true
base_resolution: pydantic_basemodel
bases:
- BaseModel
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/schemas/restaurant/menu.py
  symbol: application.schemas.restaurant.menu.AddMenuItemRequest
  line_start: 8
  line_end: 13
  evidence_type: implemented
inbound_relations:
- type: USES_SCHEMA
  source: endpoint.ftgo.gateway.post.menu.add
  role: request
  symbol: application.routes.restaurant.menu.add_item.request_data
  type_expression: AddMenuItemRequest
  parameter: request_data
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/restaurant/menu.py
  line_start: 22
  line_end: 22
  evidence_type: implemented
fields:
- name: restaurant_id
  annotation: str
  default_expression: uuid_field()
  line: 9
- name: name
  annotation: str
  default_expression: Field(..., min_length=1, max_length=100)
  line: 10
- name: price
  annotation: float
  line: 11
- name: count
  annotation: int
  line: 12
- name: description
  annotation: str
  default_expression: Field(..., min_length=1, max_length=500)
  line: 13
---

# AddMenuItemRequest

Candidate schema extracted from a class definition in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Qualified name: `application.schemas.restaurant.menu.AddMenuItemRequest`
- Declared in: `backend/gateway/src/application/schemas/restaurant/menu.py` (lines 8-13)
- Pydantic BaseModel confirmed in source: `True`
- Base resolution: `pydantic_basemodel`
- Used as: `request`
- Evidence class: `implemented`

## Review notes

This page is a candidate awaiting review. Field annotations are recorded as source text and never evaluated; credential-shaped defaults are redacted at extraction time.

