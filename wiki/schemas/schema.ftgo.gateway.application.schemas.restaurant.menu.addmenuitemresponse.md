---
id: schema.ftgo.gateway.application.schemas.restaurant.menu.addmenuitemresponse
kind: Schema
type: Schema
title: AddMenuItemResponse
status: approved
review_status: approved
candidate_of: fastapi-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: fastapi
service: service.ftgo.gateway
owner: aide-ftgo-cohort
qualified_name: application.schemas.restaurant.menu.AddMenuItemResponse
pydantic_confirmed: true
base_resolution: pydantic_basemodel
bases:
- BaseModel
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/schemas/restaurant/menu.py
  symbol: application.schemas.restaurant.menu.AddMenuItemResponse
  line_start: 16
  line_end: 17
  evidence_type: implemented
inbound_relations:
- type: USES_SCHEMA
  source: endpoint.ftgo.gateway.post.menu.add
  role: response
  symbol: application.routes.restaurant.menu.add_item
  type_expression: AddMenuItemResponse
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/restaurant/menu.py
  line_start: 21
  line_end: 21
  evidence_type: implemented
fields:
- name: item_id
  annotation: str
  default_expression: uuid_field()
  line: 17
---

# AddMenuItemResponse

Candidate schema extracted from a class definition in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Qualified name: `application.schemas.restaurant.menu.AddMenuItemResponse`
- Declared in: `backend/gateway/src/application/schemas/restaurant/menu.py` (lines 16-17)
- Pydantic BaseModel confirmed in source: `True`
- Base resolution: `pydantic_basemodel`
- Used as: `response`
- Evidence class: `implemented`

## Review notes

This page is a candidate awaiting review. Field annotations are recorded as source text and never evaluated; credential-shaped defaults are redacted at extraction time.

