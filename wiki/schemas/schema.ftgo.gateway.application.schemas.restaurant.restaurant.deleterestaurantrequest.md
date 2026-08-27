---
id: schema.ftgo.gateway.application.schemas.restaurant.restaurant.deleterestaurantrequest
kind: Schema
type: Schema
title: DeleteRestaurantRequest
status: approved
review_status: approved
candidate_of: fastapi-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: fastapi
service: service.ftgo.gateway
owner: aide-ftgo-cohort
qualified_name: application.schemas.restaurant.restaurant.DeleteRestaurantRequest
pydantic_confirmed: true
base_resolution: pydantic_basemodel
bases:
- BaseModel
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/schemas/restaurant/restaurant.py
  symbol: application.schemas.restaurant.restaurant.DeleteRestaurantRequest
  line_start: 36
  line_end: 37
  evidence_type: implemented
inbound_relations:
- type: USES_SCHEMA
  source: endpoint.ftgo.gateway.delete.restaurant.delete
  role: request
  symbol: application.routes.restaurant.restaurant.delete_restaurant.request_data
  type_expression: DeleteRestaurantRequest
  parameter: request_data
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/restaurant/restaurant.py
  line_start: 94
  line_end: 94
  evidence_type: implemented
fields:
- name: restaurant_id
  annotation: str
  default_expression: uuid_field()
  line: 37
---

# DeleteRestaurantRequest

Candidate schema extracted from a class definition in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Qualified name: `application.schemas.restaurant.restaurant.DeleteRestaurantRequest`
- Declared in: `backend/gateway/src/application/schemas/restaurant/restaurant.py` (lines 36-37)
- Pydantic BaseModel confirmed in source: `True`
- Base resolution: `pydantic_basemodel`
- Used as: `request`
- Evidence class: `implemented`

## Review notes

This page is a candidate awaiting review. Field annotations are recorded as source text and never evaluated; credential-shaped defaults are redacted at extraction time.

