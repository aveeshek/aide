---
id: endpoint.ftgo.gateway.get.vehicle.get-info
kind: Endpoint
type: Endpoint
title: GET /vehicle/get_info
status: candidate
review_status: pending
candidate_of: fastapi-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: fastapi
service: service.ftgo.gateway
owner: aide-ftgo-cohort
api: api.ftgo.gateway
method: GET
effective_path: /vehicle/get_info
path_resolution: partial
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/driver/vehicle.py
  symbol: application.routes.driver.vehicle.get_info
  line_start: 42
  line_end: 60
  evidence_type: implemented
inbound_relations:
- type: CONTAINS
  source: api.ftgo.gateway
  method: GET
  path: backend/gateway/src/application/routes/driver/vehicle.py
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  symbol: application.routes.driver.vehicle.get_info
  line_start: 42
  line_end: 60
  evidence_type: implemented
relations:
- type: USES_SCHEMA
  target: schema.ftgo.gateway.application.schemas.driver.vehicle.getvehicleinforesponse
  role: response
  symbol: application.routes.driver.vehicle.get_info
  type_expression: GetVehicleInfoResponse
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/driver/vehicle.py
  line_start: 42
  line_end: 42
  evidence_type: implemented
attributes:
  method: GET
  effective_path: /vehicle/get_info
  decorator_path: /get_info
  router_prefix: /vehicle
  path_resolution: partial
  decorator: router.get("/get_info", response_model=GetVehicleInfoResponse)
  handler: application.routes.driver.vehicle.get_info
  router: application.routes.driver.vehicle:router
  mount_path:
  - main:app
  - application.app:router
  - application.routes.driver.vehicle:router
  tags:
  - vehicle
  response_model: GetVehicleInfoResponse
  unresolved_prefix_expressions:
  - service_config.api_prefix
---

# GET /vehicle/get_info

Candidate HTTP endpoint extracted from a FastAPI route decorator in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Method: `GET`
- Effective path: `/vehicle/get_info`
- Path resolution: `partial`
- Handler: `application.routes.driver.vehicle.get_info`
- Declared in: `backend/gateway/src/application/routes/driver/vehicle.py` (lines 42-60)
- Evidence class: `implemented`

## Unresolved mount prefix

The effective path above omits a mount prefix that is not a string literal in source, so the served path depends on configuration:

- `service_config.api_prefix`

## Schemas

- `response` `USES_SCHEMA` -> `schema.ftgo.gateway.application.schemas.driver.vehicle.getvehicleinforesponse`

## Review notes

This page is a candidate awaiting review. Method and path come from the decorator shown in `attributes.decorator`; nothing was inferred from names.

