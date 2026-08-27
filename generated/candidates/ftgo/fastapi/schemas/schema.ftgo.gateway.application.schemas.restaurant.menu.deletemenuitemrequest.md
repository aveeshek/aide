---
id: schema.ftgo.gateway.application.schemas.restaurant.menu.deletemenuitemrequest
kind: Schema
type: Schema
title: DeleteMenuItemRequest
status: candidate
review_status: pending
candidate_of: fastapi-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: fastapi
service: service.ftgo.gateway
owner: aide-ftgo-cohort
qualified_name: application.schemas.restaurant.menu.DeleteMenuItemRequest
pydantic_confirmed: true
base_resolution: pydantic_basemodel
bases:
- BaseModel
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/schemas/restaurant/menu.py
  symbol: application.schemas.restaurant.menu.DeleteMenuItemRequest
  line_start: 50
  line_end: 51
  evidence_type: implemented
inbound_relations:
- type: USES_SCHEMA
  source: endpoint.ftgo.gateway.delete.menu.delete
  role: request
  symbol: application.routes.restaurant.menu.delete_item.request_data
  type_expression: DeleteMenuItemRequest
  parameter: request_data
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/restaurant/menu.py
  line_start: 89
  line_end: 89
  evidence_type: implemented
fields:
- name: item_id
  annotation: str
  default_expression: uuid_field()
  line: 51
---

# DeleteMenuItemRequest

Candidate schema extracted from a class definition in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Qualified name: `application.schemas.restaurant.menu.DeleteMenuItemRequest`
- Declared in: `backend/gateway/src/application/schemas/restaurant/menu.py` (lines 50-51)
- Pydantic BaseModel confirmed in source: `True`
- Base resolution: `pydantic_basemodel`
- Used as: `request`
- Evidence class: `implemented`

## Review notes

This page is a candidate awaiting review. Field annotations are recorded as source text and never evaluated; credential-shaped defaults are redacted at extraction time.

