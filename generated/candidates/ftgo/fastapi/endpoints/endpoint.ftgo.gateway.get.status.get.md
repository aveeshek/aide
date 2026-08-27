---
id: endpoint.ftgo.gateway.get.status.get
kind: Endpoint
type: Endpoint
title: GET /status/get
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
effective_path: /status/get
path_resolution: partial
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/driver/online_status.py
  symbol: application.routes.driver.online_status.get_status
  line_start: 50
  line_end: 66
  evidence_type: implemented
inbound_relations:
- type: CONTAINS
  source: api.ftgo.gateway
  method: GET
  path: backend/gateway/src/application/routes/driver/online_status.py
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  symbol: application.routes.driver.online_status.get_status
  line_start: 50
  line_end: 66
  evidence_type: implemented
relations:
- type: USES_SCHEMA
  target: schema.ftgo.gateway.application.schemas.driver.status.driverstatusschema
  role: response
  symbol: application.routes.driver.online_status.get_status
  type_expression: DriverStatusSchema
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/driver/online_status.py
  line_start: 50
  line_end: 50
  evidence_type: implemented
attributes:
  method: GET
  effective_path: /status/get
  decorator_path: /get
  router_prefix: /status
  path_resolution: partial
  decorator: router.get("/get", response_model=DriverStatusSchema)
  handler: application.routes.driver.online_status.get_status
  router: application.routes.driver.online_status:router
  mount_path:
  - main:app
  - application.app:router
  - application.routes.driver.online_status:router
  tags:
  - driver_location_service
  response_model: DriverStatusSchema
  unresolved_prefix_expressions:
  - service_config.api_prefix
---

# GET /status/get

Candidate HTTP endpoint extracted from a FastAPI route decorator in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Method: `GET`
- Effective path: `/status/get`
- Path resolution: `partial`
- Handler: `application.routes.driver.online_status.get_status`
- Declared in: `backend/gateway/src/application/routes/driver/online_status.py` (lines 50-66)
- Evidence class: `implemented`

## Unresolved mount prefix

The effective path above omits a mount prefix that is not a string literal in source, so the served path depends on configuration:

- `service_config.api_prefix`

## Schemas

- `response` `USES_SCHEMA` -> `schema.ftgo.gateway.application.schemas.driver.status.driverstatusschema`

## Review notes

This page is a candidate awaiting review. Method and path come from the decorator shown in `attributes.decorator`; nothing was inferred from names.

