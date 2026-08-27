---
id: schema.ftgo.gateway.application.schemas.restaurant.restaurant.getallrestaurantinforesponse
kind: Schema
type: Schema
title: GetAllRestaurantInfoResponse
status: candidate
review_status: pending
candidate_of: fastapi-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: fastapi
service: service.ftgo.gateway
owner: aide-ftgo-cohort
qualified_name: application.schemas.restaurant.restaurant.GetAllRestaurantInfoResponse
pydantic_confirmed: true
base_resolution: pydantic_basemodel
bases:
- BaseModel
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/schemas/restaurant/restaurant.py
  symbol: application.schemas.restaurant.restaurant.GetAllRestaurantInfoResponse
  line_start: 32
  line_end: 33
  evidence_type: implemented
inbound_relations:
- type: USES_SCHEMA
  source: endpoint.ftgo.gateway.get.restaurant.get-all-restaurant-info
  role: response
  symbol: application.routes.restaurant.restaurant.get_all_restaurant_info
  type_expression: GetAllRestaurantInfoResponse
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/restaurant/restaurant.py
  line_start: 74
  line_end: 74
  evidence_type: implemented
fields:
- name: restaurants
  annotation: list[GetRestaurantInfoResponse]
  default_expression: Field(...)
  line: 33
---

# GetAllRestaurantInfoResponse

Candidate schema extracted from a class definition in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Qualified name: `application.schemas.restaurant.restaurant.GetAllRestaurantInfoResponse`
- Declared in: `backend/gateway/src/application/schemas/restaurant/restaurant.py` (lines 32-33)
- Pydantic BaseModel confirmed in source: `True`
- Base resolution: `pydantic_basemodel`
- Used as: `response`
- Evidence class: `implemented`

## Review notes

This page is a candidate awaiting review. Field annotations are recorded as source text and never evaluated; credential-shaped defaults are redacted at extraction time.

