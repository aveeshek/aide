---
id: endpoint.ftgo.gateway.get.location.get
kind: Endpoint
type: Endpoint
title: GET /location/get
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
effective_path: /location/get
path_resolution: partial
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/driver/location.py
  symbol: application.routes.driver.location.get_location
  line_start: 41
  line_end: 62
  evidence_type: implemented
inbound_relations:
- type: CONTAINS
  source: api.ftgo.gateway
  method: GET
  path: backend/gateway/src/application/routes/driver/location.py
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  symbol: application.routes.driver.location.get_location
  line_start: 41
  line_end: 62
  evidence_type: implemented
attributes:
  method: GET
  effective_path: /location/get
  decorator_path: /get
  router_prefix: /location
  path_resolution: partial
  decorator: router.get("/get", response_model=LocationPointMixin)
  handler: application.routes.driver.location.get_location
  router: application.routes.driver.location:router
  mount_path:
  - main:app
  - application.app:router
  - application.routes.driver.location:router
  tags:
  - driver_location_service
  response_model: LocationPointMixin
  unresolved_prefix_expressions:
  - service_config.api_prefix
---

# GET /location/get

Candidate HTTP endpoint extracted from a FastAPI route decorator in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Method: `GET`
- Effective path: `/location/get`
- Path resolution: `partial`
- Handler: `application.routes.driver.location.get_location`
- Declared in: `backend/gateway/src/application/routes/driver/location.py` (lines 41-62)
- Evidence class: `implemented`

## Unresolved mount prefix

The effective path above omits a mount prefix that is not a string literal in source, so the served path depends on configuration:

- `service_config.api_prefix`

## Review notes

This page is a candidate awaiting review. Method and path come from the decorator shown in `attributes.decorator`; nothing was inferred from names.

