---
id: schema.ftgo.gateway.application.schemas.restaurant.restaurant.updaterestaurantresponse
kind: Schema
type: Schema
title: UpdateRestaurantResponse
status: approved
review_status: approved
candidate_of: fastapi-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: fastapi
service: service.ftgo.gateway
owner: aide-ftgo-cohort
qualified_name: application.schemas.restaurant.restaurant.UpdateRestaurantResponse
pydantic_confirmed: true
base_resolution: pydantic_basemodel
bases:
- BaseModel
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/schemas/restaurant/restaurant.py
  symbol: application.schemas.restaurant.restaurant.UpdateRestaurantResponse
  line_start: 53
  line_end: 54
  evidence_type: implemented
inbound_relations:
- type: USES_SCHEMA
  source: endpoint.ftgo.gateway.put.restaurant.update
  role: response
  symbol: application.routes.restaurant.restaurant.update_information
  type_expression: UpdateRestaurantResponse
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/restaurant/restaurant.py
  line_start: 115
  line_end: 115
  evidence_type: implemented
fields:
- name: restaurant_id
  annotation: str
  default_expression: uuid_field()
  line: 54
---

# UpdateRestaurantResponse

Candidate schema extracted from a class definition in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Qualified name: `application.schemas.restaurant.restaurant.UpdateRestaurantResponse`
- Declared in: `backend/gateway/src/application/schemas/restaurant/restaurant.py` (lines 53-54)
- Pydantic BaseModel confirmed in source: `True`
- Base resolution: `pydantic_basemodel`
- Used as: `response`
- Evidence class: `implemented`

## Review notes

This page is a candidate awaiting review. Field annotations are recorded as source text and never evaluated; credential-shaped defaults are redacted at extraction time.

