---
id: endpoint.ftgo.gateway.post.location.submit
kind: Endpoint
type: Endpoint
title: POST /location/submit
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
effective_path: /location/submit
path_resolution: partial
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/driver/location.py
  symbol: application.routes.driver.location.submit_location
  line_start: 16
  line_end: 38
  evidence_type: implemented
inbound_relations:
- type: CONTAINS
  source: api.ftgo.gateway
  method: POST
  path: backend/gateway/src/application/routes/driver/location.py
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  symbol: application.routes.driver.location.submit_location
  line_start: 16
  line_end: 38
  evidence_type: implemented
relations:
- type: USES_SCHEMA
  target: schema.ftgo.gateway.application.schemas.common.successresponse
  role: response
  symbol: application.routes.driver.location.submit_location
  type_expression: SuccessResponse
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/driver/location.py
  line_start: 16
  line_end: 16
  evidence_type: implemented
- type: USES_SCHEMA
  target: schema.ftgo.gateway.application.schemas.driver.location.locationsschema
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
attributes:
  method: POST
  effective_path: /location/submit
  decorator_path: /submit
  router_prefix: /location
  path_resolution: partial
  decorator: router.post("/submit", response_model=SuccessResponse)
  handler: application.routes.driver.location.submit_location
  router: application.routes.driver.location:router
  mount_path:
  - main:app
  - application.app:router
  - application.routes.driver.location:router
  tags:
  - driver_location_service
  response_model: SuccessResponse
  unresolved_prefix_expressions:
  - service_config.api_prefix
---

# POST /location/submit

Candidate HTTP endpoint extracted from a FastAPI route decorator in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Method: `POST`
- Effective path: `/location/submit`
- Path resolution: `partial`
- Handler: `application.routes.driver.location.submit_location`
- Declared in: `backend/gateway/src/application/routes/driver/location.py` (lines 16-38)
- Evidence class: `implemented`

## Unresolved mount prefix

The effective path above omits a mount prefix that is not a string literal in source, so the served path depends on configuration:

- `service_config.api_prefix`

## Schemas

- `response` `USES_SCHEMA` -> `schema.ftgo.gateway.application.schemas.common.successresponse`
- `request` `USES_SCHEMA` -> `schema.ftgo.gateway.application.schemas.driver.location.locationsschema`

## Review notes

This page is a candidate awaiting review. Method and path come from the decorator shown in `attributes.decorator`; nothing was inferred from names.

