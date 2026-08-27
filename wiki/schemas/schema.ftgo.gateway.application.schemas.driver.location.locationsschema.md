---
id: schema.ftgo.gateway.application.schemas.driver.location.locationsschema
kind: Schema
type: Schema
title: LocationsSchema
status: approved
review_status: approved
candidate_of: fastapi-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: fastapi
service: service.ftgo.gateway
owner: aide-ftgo-cohort
qualified_name: application.schemas.driver.location.LocationsSchema
pydantic_confirmed: false
base_resolution: external_base
bases:
- BaseSchema
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/schemas/driver/location.py
  symbol: application.schemas.driver.location.LocationsSchema
  line_start: 7
  line_end: 8
  evidence_type: implemented
inbound_relations:
- type: USES_SCHEMA
  source: endpoint.ftgo.gateway.post.location.submit
  role: request
  symbol: application.routes.driver.location.submit_location.request_data
  type_expression: LocationsSchema
  parameter: request_data
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/driver/location.py
  line_start: 17
  line_end: 17
  evidence_type: implemented
fields:
- name: locations
  annotation: List[LocationMixin]
  default_expression: Field(..., min_items=1)
  line: 8
---

# LocationsSchema

Candidate schema extracted from a class definition in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Qualified name: `application.schemas.driver.location.LocationsSchema`
- Declared in: `backend/gateway/src/application/schemas/driver/location.py` (lines 7-8)
- Pydantic BaseModel confirmed in source: `False`
- Base resolution: `external_base`
- Used as: `request`
- Evidence class: `implemented`

## Review notes

This page is a candidate awaiting review. Field annotations are recorded as source text and never evaluated; credential-shaped defaults are redacted at extraction time.

