---
id: schema.ftgo.gateway.application.schemas.restaurant.restaurant.registerrestaurantrequest
kind: Schema
type: Schema
title: RegisterRestaurantRequest
status: candidate
review_status: pending
candidate_of: fastapi-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: fastapi
service: service.ftgo.gateway
owner: aide-ftgo-cohort
qualified_name: application.schemas.restaurant.restaurant.RegisterRestaurantRequest
pydantic_confirmed: true
base_resolution: pydantic_basemodel
bases:
- BaseModel
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/schemas/restaurant/restaurant.py
  symbol: application.schemas.restaurant.restaurant.RegisterRestaurantRequest
  line_start: 8
  line_end: 14
  evidence_type: implemented
inbound_relations:
- type: USES_SCHEMA
  source: endpoint.ftgo.gateway.post.restaurant.register
  role: request
  symbol: application.routes.restaurant.restaurant.register.request_data
  type_expression: RegisterRestaurantRequest
  parameter: request_data
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/restaurant/restaurant.py
  line_start: 23
  line_end: 23
  evidence_type: implemented
fields:
- name: name
  annotation: str
  default_expression: Field(..., min_length=1, max_length=100)
  line: 9
- name: postal_code
  annotation: str
  default_expression: Field(..., min_length=1, max_length=100)
  line: 10
- name: address
  annotation: str
  default_expression: Field(..., min_length=1, max_length=300)
  line: 11
- name: address_lat
  annotation: float
  line: 12
- name: address_lng
  annotation: float
  line: 13
- name: restaurant_licence_id
  annotation: str
  default_expression: Field(..., min_length=1, max_length=100)
  line: 14
---

# RegisterRestaurantRequest

Candidate schema extracted from a class definition in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Qualified name: `application.schemas.restaurant.restaurant.RegisterRestaurantRequest`
- Declared in: `backend/gateway/src/application/schemas/restaurant/restaurant.py` (lines 8-14)
- Pydantic BaseModel confirmed in source: `True`
- Base resolution: `pydantic_basemodel`
- Used as: `request`
- Evidence class: `implemented`

## Review notes

This page is a candidate awaiting review. Field annotations are recorded as source text and never evaluated; credential-shaped defaults are redacted at extraction time.

