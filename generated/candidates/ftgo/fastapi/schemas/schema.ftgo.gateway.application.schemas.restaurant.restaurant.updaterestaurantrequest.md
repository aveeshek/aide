---
id: schema.ftgo.gateway.application.schemas.restaurant.restaurant.updaterestaurantrequest
kind: Schema
type: Schema
title: UpdateRestaurantRequest
status: candidate
review_status: pending
candidate_of: fastapi-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: fastapi
service: service.ftgo.gateway
owner: aide-ftgo-cohort
qualified_name: application.schemas.restaurant.restaurant.UpdateRestaurantRequest
pydantic_confirmed: true
base_resolution: pydantic_basemodel
bases:
- BaseModel
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/schemas/restaurant/restaurant.py
  symbol: application.schemas.restaurant.restaurant.UpdateRestaurantRequest
  line_start: 44
  line_end: 50
  evidence_type: implemented
inbound_relations:
- type: USES_SCHEMA
  source: endpoint.ftgo.gateway.put.restaurant.update
  role: request
  symbol: application.routes.restaurant.restaurant.update_information.request_data
  type_expression: UpdateRestaurantRequest
  parameter: request_data
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/restaurant/restaurant.py
  line_start: 116
  line_end: 116
  evidence_type: implemented
fields:
- name: restaurant_id
  annotation: str
  default_expression: uuid_field()
  line: 45
- name: name
  annotation: str
  default_expression: Field(..., min_length=1, max_length=100)
  line: 46
- name: postal_code
  annotation: str
  default_expression: Field(..., min_length=1, max_length=100)
  line: 47
- name: address
  annotation: str
  default_expression: Field(..., min_length=1, max_length=300)
  line: 48
- name: address_lat
  annotation: float
  line: 49
- name: address_lng
  annotation: float
  line: 50
---

# UpdateRestaurantRequest

Candidate schema extracted from a class definition in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Qualified name: `application.schemas.restaurant.restaurant.UpdateRestaurantRequest`
- Declared in: `backend/gateway/src/application/schemas/restaurant/restaurant.py` (lines 44-50)
- Pydantic BaseModel confirmed in source: `True`
- Base resolution: `pydantic_basemodel`
- Used as: `request`
- Evidence class: `implemented`

## Review notes

This page is a candidate awaiting review. Field annotations are recorded as source text and never evaluated; credential-shaped defaults are redacted at extraction time.

