---
id: endpoint.ftgo.gateway.post.vehicle.register
kind: Endpoint
type: Endpoint
title: POST /vehicle/register
status: approved
review_status: approved
candidate_of: fastapi-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: fastapi
service: service.ftgo.gateway
owner: aide-ftgo-cohort
api: api.ftgo.gateway
method: POST
effective_path: /vehicle/register
path_resolution: partial
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/driver/vehicle.py
  symbol: application.routes.driver.vehicle.register
  line_start: 17
  line_end: 39
  evidence_type: implemented
inbound_relations:
- type: CONTAINS
  source: api.ftgo.gateway
  method: POST
  path: backend/gateway/src/application/routes/driver/vehicle.py
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  symbol: application.routes.driver.vehicle.register
  line_start: 17
  line_end: 39
  evidence_type: implemented
relations:
- type: USES_SCHEMA
  target: schema.ftgo.gateway.application.schemas.driver.vehicle.registervehiclerequest
  role: request
  symbol: application.routes.driver.vehicle.register.request_data
  type_expression: RegisterVehicleRequest
  parameter: request_data
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/driver/vehicle.py
  line_start: 18
  line_end: 18
  evidence_type: implemented
- type: USES_SCHEMA
  target: schema.ftgo.gateway.application.schemas.driver.vehicle.registervehicleresponse
  role: response
  symbol: application.routes.driver.vehicle.register
  type_expression: RegisterVehicleResponse
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/driver/vehicle.py
  line_start: 17
  line_end: 17
  evidence_type: implemented
attributes:
  method: POST
  effective_path: /vehicle/register
  decorator_path: /register
  router_prefix: /vehicle
  path_resolution: partial
  decorator: router.post("/register", response_model=RegisterVehicleResponse)
  handler: application.routes.driver.vehicle.register
  router: application.routes.driver.vehicle:router
  mount_path:
  - main:app
  - application.app:router
  - application.routes.driver.vehicle:router
  tags:
  - vehicle
  response_model: RegisterVehicleResponse
  unresolved_prefix_expressions:
  - service_config.api_prefix
---

# POST /vehicle/register

Candidate HTTP endpoint extracted from a FastAPI route decorator in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Method: `POST`
- Effective path: `/vehicle/register`
- Path resolution: `partial`
- Handler: `application.routes.driver.vehicle.register`
- Declared in: `backend/gateway/src/application/routes/driver/vehicle.py` (lines 17-39)
- Evidence class: `implemented`

## Unresolved mount prefix

The effective path above omits a mount prefix that is not a string literal in source, so the served path depends on configuration:

- `service_config.api_prefix`

## Schemas

- `request` `USES_SCHEMA` -> `schema.ftgo.gateway.application.schemas.driver.vehicle.registervehiclerequest`
- `response` `USES_SCHEMA` -> `schema.ftgo.gateway.application.schemas.driver.vehicle.registervehicleresponse`

## Review notes

This page is a candidate awaiting review. Method and path come from the decorator shown in `attributes.decorator`; nothing was inferred from names.

