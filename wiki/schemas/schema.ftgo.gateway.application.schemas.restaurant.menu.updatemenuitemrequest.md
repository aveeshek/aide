---
id: schema.ftgo.gateway.application.schemas.restaurant.menu.updatemenuitemrequest
kind: Schema
type: Schema
title: UpdateMenuItemRequest
status: approved
review_status: approved
candidate_of: fastapi-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: fastapi
service: service.ftgo.gateway
owner: aide-ftgo-cohort
qualified_name: application.schemas.restaurant.menu.UpdateMenuItemRequest
pydantic_confirmed: true
base_resolution: pydantic_basemodel
bases:
- BaseModel
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/schemas/restaurant/menu.py
  symbol: application.schemas.restaurant.menu.UpdateMenuItemRequest
  line_start: 38
  line_end: 43
  evidence_type: implemented
inbound_relations:
- type: USES_SCHEMA
  source: endpoint.ftgo.gateway.put.menu.update
  role: request
  symbol: application.routes.restaurant.menu.update_item.request_data
  type_expression: UpdateMenuItemRequest
  parameter: request_data
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/restaurant/menu.py
  line_start: 67
  line_end: 67
  evidence_type: implemented
fields:
- name: item_id
  annotation: str
  default_expression: uuid_field()
  line: 39
- name: name
  annotation: str
  default_expression: Field(..., min_length=1, max_length=100)
  line: 40
- name: price
  annotation: float
  line: 41
- name: count
  annotation: int
  default_expression: Field(..., gt=0)
  line: 42
- name: description
  annotation: str
  default_expression: Field(..., min_length=1, max_length=500)
  line: 43
---

# UpdateMenuItemRequest

Candidate schema extracted from a class definition in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Qualified name: `application.schemas.restaurant.menu.UpdateMenuItemRequest`
- Declared in: `backend/gateway/src/application/schemas/restaurant/menu.py` (lines 38-43)
- Pydantic BaseModel confirmed in source: `True`
- Base resolution: `pydantic_basemodel`
- Used as: `request`
- Evidence class: `implemented`

## Review notes

This page is a candidate awaiting review. Field annotations are recorded as source text and never evaluated; credential-shaped defaults are redacted at extraction time.

