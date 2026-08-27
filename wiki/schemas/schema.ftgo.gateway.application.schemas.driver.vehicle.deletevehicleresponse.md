---
id: schema.ftgo.gateway.application.schemas.driver.vehicle.deletevehicleresponse
kind: Schema
type: Schema
title: DeleteVehicleResponse
status: approved
review_status: approved
candidate_of: fastapi-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: fastapi
service: service.ftgo.gateway
owner: aide-ftgo-cohort
qualified_name: application.schemas.driver.vehicle.DeleteVehicleResponse
pydantic_confirmed: true
base_resolution: pydantic_basemodel
bases:
- BaseModel
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/schemas/driver/vehicle.py
  symbol: application.schemas.driver.vehicle.DeleteVehicleResponse
  line_start: 25
  line_end: 26
  evidence_type: implemented
inbound_relations:
- type: USES_SCHEMA
  source: endpoint.ftgo.gateway.delete.vehicle.delete
  role: response
  symbol: application.routes.driver.vehicle.delete
  type_expression: DeleteVehicleResponse
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/driver/vehicle.py
  line_start: 63
  line_end: 63
  evidence_type: implemented
fields:
- name: vehicle_id
  annotation: str
  default_expression: uuid_field()
  line: 26
---

# DeleteVehicleResponse

Candidate schema extracted from a class definition in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Qualified name: `application.schemas.driver.vehicle.DeleteVehicleResponse`
- Declared in: `backend/gateway/src/application/schemas/driver/vehicle.py` (lines 25-26)
- Pydantic BaseModel confirmed in source: `True`
- Base resolution: `pydantic_basemodel`
- Used as: `response`
- Evidence class: `implemented`

## Review notes

This page is a candidate awaiting review. Field annotations are recorded as source text and never evaluated; credential-shaped defaults are redacted at extraction time.

