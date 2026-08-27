---
id: schema.ftgo.gateway.application.schemas.driver.vehicle.registervehicleresponse
kind: Schema
type: Schema
title: RegisterVehicleResponse
status: approved
review_status: approved
candidate_of: fastapi-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: fastapi
service: service.ftgo.gateway
owner: aide-ftgo-cohort
qualified_name: application.schemas.driver.vehicle.RegisterVehicleResponse
pydantic_confirmed: true
base_resolution: pydantic_basemodel
bases:
- BaseModel
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/schemas/driver/vehicle.py
  symbol: application.schemas.driver.vehicle.RegisterVehicleResponse
  line_start: 13
  line_end: 14
  evidence_type: implemented
inbound_relations:
- type: USES_SCHEMA
  source: endpoint.ftgo.gateway.post.vehicle.register
  role: response
  symbol: application.routes.driver.vehicle.register
  type_expression: RegisterVehicleResponse
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/driver/vehicle.py
  line_start: 17
  line_end: 17
  evidence_type: implemented
fields:
- name: vehicle_id
  annotation: str
  default_expression: uuid_field()
  line: 14
---

# RegisterVehicleResponse

Candidate schema extracted from a class definition in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Qualified name: `application.schemas.driver.vehicle.RegisterVehicleResponse`
- Declared in: `backend/gateway/src/application/schemas/driver/vehicle.py` (lines 13-14)
- Pydantic BaseModel confirmed in source: `True`
- Base resolution: `pydantic_basemodel`
- Used as: `response`
- Evidence class: `implemented`

## Review notes

This page is a candidate awaiting review. Field annotations are recorded as source text and never evaluated; credential-shaped defaults are redacted at extraction time.

