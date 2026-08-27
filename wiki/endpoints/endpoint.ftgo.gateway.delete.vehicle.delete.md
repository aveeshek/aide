---
id: endpoint.ftgo.gateway.delete.vehicle.delete
kind: Endpoint
type: Endpoint
title: DELETE /vehicle/delete
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
method: DELETE
effective_path: /vehicle/delete
path_resolution: partial
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/driver/vehicle.py
  symbol: application.routes.driver.vehicle.delete
  line_start: 63
  line_end: 83
  evidence_type: implemented
inbound_relations:
- type: CONTAINS
  source: api.ftgo.gateway
  method: DELETE
  path: backend/gateway/src/application/routes/driver/vehicle.py
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  symbol: application.routes.driver.vehicle.delete
  line_start: 63
  line_end: 83
  evidence_type: implemented
relations:
- type: USES_SCHEMA
  target: schema.ftgo.gateway.application.schemas.driver.vehicle.deletevehicleresponse
  role: response
  symbol: application.routes.driver.vehicle.delete
  type_expression: DeleteVehicleResponse
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/driver/vehicle.py
  line_start: 63
  line_end: 63
  evidence_type: implemented
attributes:
  method: DELETE
  effective_path: /vehicle/delete
  decorator_path: /delete
  router_prefix: /vehicle
  path_resolution: partial
  decorator: router.delete("/delete", response_model=DeleteVehicleResponse)
  handler: application.routes.driver.vehicle.delete
  router: application.routes.driver.vehicle:router
  mount_path:
  - main:app
  - application.app:router
  - application.routes.driver.vehicle:router
  tags:
  - vehicle
  response_model: DeleteVehicleResponse
  unresolved_prefix_expressions:
  - service_config.api_prefix
---

# DELETE /vehicle/delete

Candidate HTTP endpoint extracted from a FastAPI route decorator in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Method: `DELETE`
- Effective path: `/vehicle/delete`
- Path resolution: `partial`
- Handler: `application.routes.driver.vehicle.delete`
- Declared in: `backend/gateway/src/application/routes/driver/vehicle.py` (lines 63-83)
- Evidence class: `implemented`

## Unresolved mount prefix

The effective path above omits a mount prefix that is not a string literal in source, so the served path depends on configuration:

- `service_config.api_prefix`

## Schemas

- `response` `USES_SCHEMA` -> `schema.ftgo.gateway.application.schemas.driver.vehicle.deletevehicleresponse`

## Review notes

This page is a candidate awaiting review. Method and path come from the decorator shown in `attributes.decorator`; nothing was inferred from names.

