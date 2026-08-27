---
id: schema.ftgo.gateway.application.schemas.restaurant.restaurant.getrestaurantinforesponse
kind: Schema
type: Schema
title: GetRestaurantInfoResponse
status: candidate
review_status: pending
candidate_of: fastapi-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: fastapi
service: service.ftgo.gateway
owner: aide-ftgo-cohort
qualified_name: application.schemas.restaurant.restaurant.GetRestaurantInfoResponse
pydantic_confirmed: true
base_resolution: pydantic_basemodel
bases:
- BaseModel
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/schemas/restaurant/restaurant.py
  symbol: application.schemas.restaurant.restaurant.GetRestaurantInfoResponse
  line_start: 21
  line_end: 29
  evidence_type: implemented
inbound_relations:
- type: USES_SCHEMA
  source: endpoint.ftgo.gateway.get.restaurant.get-supplier-restaurant-info
  role: response
  symbol: application.routes.restaurant.restaurant.get_supplier_restaurant_info
  type_expression: GetRestaurantInfoResponse
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/restaurant/restaurant.py
  line_start: 46
  line_end: 46
  evidence_type: implemented
fields:
- name: id
  annotation: str
  default_expression: uuid_field()
  line: 22
- name: owner_user_id
  annotation: str
  default_expression: uuid_field()
  line: 23
- name: name
  annotation: str
  default_expression: Field(..., min_length=1, max_length=100)
  line: 24
- name: postal_code
  annotation: str
  default_expression: Field(..., min_length=1, max_length=100)
  line: 25
- name: address
  annotation: str
  default_expression: Field(..., min_length=1, max_length=300)
  line: 26
- name: address_lat
  annotation: float
  line: 27
- name: address_lng
  annotation: float
  line: 28
- name: restaurant_licence_id
  annotation: str
  default_expression: Field(..., min_length=1, max_length=100)
  line: 29
---

# GetRestaurantInfoResponse

Candidate schema extracted from a class definition in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Qualified name: `application.schemas.restaurant.restaurant.GetRestaurantInfoResponse`
- Declared in: `backend/gateway/src/application/schemas/restaurant/restaurant.py` (lines 21-29)
- Pydantic BaseModel confirmed in source: `True`
- Base resolution: `pydantic_basemodel`
- Used as: `response`
- Evidence class: `implemented`

## Review notes

This page is a candidate awaiting review. Field annotations are recorded as source text and never evaluated; credential-shaped defaults are redacted at extraction time.

