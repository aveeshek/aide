---
id: schema.ftgo.gateway.application.schemas.restaurant.menu.updatemenuitemresponse
kind: Schema
type: Schema
title: UpdateMenuItemResponse
status: candidate
review_status: pending
candidate_of: fastapi-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: fastapi
service: service.ftgo.gateway
owner: aide-ftgo-cohort
qualified_name: application.schemas.restaurant.menu.UpdateMenuItemResponse
pydantic_confirmed: true
base_resolution: pydantic_basemodel
bases:
- BaseModel
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/schemas/restaurant/menu.py
  symbol: application.schemas.restaurant.menu.UpdateMenuItemResponse
  line_start: 46
  line_end: 47
  evidence_type: implemented
inbound_relations:
- type: USES_SCHEMA
  source: endpoint.ftgo.gateway.put.menu.update
  role: response
  symbol: application.routes.restaurant.menu.update_item
  type_expression: UpdateMenuItemResponse
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/restaurant/menu.py
  line_start: 66
  line_end: 66
  evidence_type: implemented
fields:
- name: restaurant_id
  annotation: str
  default_expression: uuid_field()
  line: 47
---

# UpdateMenuItemResponse

Candidate schema extracted from a class definition in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Qualified name: `application.schemas.restaurant.menu.UpdateMenuItemResponse`
- Declared in: `backend/gateway/src/application/schemas/restaurant/menu.py` (lines 46-47)
- Pydantic BaseModel confirmed in source: `True`
- Base resolution: `pydantic_basemodel`
- Used as: `response`
- Evidence class: `implemented`

## Review notes

This page is a candidate awaiting review. Field annotations are recorded as source text and never evaluated; credential-shaped defaults are redacted at extraction time.

