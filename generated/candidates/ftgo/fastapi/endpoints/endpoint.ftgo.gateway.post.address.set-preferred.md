---
id: endpoint.ftgo.gateway.post.address.set-preferred
kind: Endpoint
type: Endpoint
title: POST /address/set-preferred
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
method: POST
effective_path: /address/set-preferred
path_resolution: partial
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/customer/address.py
  symbol: application.routes.customer.address.set_address_preferency
  line_start: 88
  line_end: 110
  evidence_type: implemented
inbound_relations:
- type: CONTAINS
  source: api.ftgo.gateway
  method: POST
  path: backend/gateway/src/application/routes/customer/address.py
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  symbol: application.routes.customer.address.set_address_preferency
  line_start: 88
  line_end: 110
  evidence_type: implemented
relations:
- type: USES_SCHEMA
  target: schema.ftgo.gateway.application.schemas.account.address.addressidpreferencyschema
  role: request
  symbol: application.routes.customer.address.set_address_preferency.request_data
  type_expression: AddressIdPreferencySchema
  parameter: request_data
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/customer/address.py
  line_start: 89
  line_end: 89
  evidence_type: implemented
attributes:
  method: POST
  effective_path: /address/set-preferred
  decorator_path: /set-preferred
  router_prefix: /address
  path_resolution: partial
  decorator: router.post("/set-preferred", response_model=AddressMixin)
  handler: application.routes.customer.address.set_address_preferency
  router: application.routes.customer.address:router
  mount_path:
  - main:app
  - application.app:router
  - application.routes.customer.address:router
  tags:
  - user_address
  response_model: AddressMixin
  unresolved_prefix_expressions:
  - service_config.api_prefix
---

# POST /address/set-preferred

Candidate HTTP endpoint extracted from a FastAPI route decorator in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Method: `POST`
- Effective path: `/address/set-preferred`
- Path resolution: `partial`
- Handler: `application.routes.customer.address.set_address_preferency`
- Declared in: `backend/gateway/src/application/routes/customer/address.py` (lines 88-110)
- Evidence class: `implemented`

## Unresolved mount prefix

The effective path above omits a mount prefix that is not a string literal in source, so the served path depends on configuration:

- `service_config.api_prefix`

## Schemas

- `request` `USES_SCHEMA` -> `schema.ftgo.gateway.application.schemas.account.address.addressidpreferencyschema`

## Review notes

This page is a candidate awaiting review. Method and path come from the decorator shown in `attributes.decorator`; nothing was inferred from names.

