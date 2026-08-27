---
id: schema.ftgo.gateway.application.schemas.restaurant.menu.getallmenuitemresponse
kind: Schema
type: Schema
title: GetAllMenuItemResponse
status: candidate
review_status: pending
candidate_of: fastapi-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: fastapi
service: service.ftgo.gateway
owner: aide-ftgo-cohort
qualified_name: application.schemas.restaurant.menu.GetAllMenuItemResponse
pydantic_confirmed: true
base_resolution: pydantic_basemodel
bases:
- BaseModel
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/schemas/restaurant/menu.py
  symbol: application.schemas.restaurant.menu.GetAllMenuItemResponse
  line_start: 63
  line_end: 64
  evidence_type: implemented
inbound_relations:
- type: USES_SCHEMA
  source: endpoint.ftgo.gateway.post.menu.get-all-menu-item
  role: response
  symbol: application.routes.restaurant.menu.get_all_menu_item
  type_expression: GetAllMenuItemResponse
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/restaurant/menu.py
  line_start: 109
  line_end: 109
  evidence_type: implemented
fields:
- name: menu
  annotation: list[GetMenuItemInfoResponse]
  default_expression: Field(...)
  line: 64
---

# GetAllMenuItemResponse

Candidate schema extracted from a class definition in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Qualified name: `application.schemas.restaurant.menu.GetAllMenuItemResponse`
- Declared in: `backend/gateway/src/application/schemas/restaurant/menu.py` (lines 63-64)
- Pydantic BaseModel confirmed in source: `True`
- Base resolution: `pydantic_basemodel`
- Used as: `response`
- Evidence class: `implemented`

## Review notes

This page is a candidate awaiting review. Field annotations are recorded as source text and never evaluated; credential-shaped defaults are redacted at extraction time.

