---
id: endpoint.ftgo.gateway.get.address.get-all-info
kind: Endpoint
type: Endpoint
title: GET /address/get_all_info
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
effective_path: /address/get_all_info
path_resolution: partial
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/customer/address.py
  symbol: application.routes.customer.address.get_all_addresses
  line_start: 22
  line_end: 39
  evidence_type: implemented
inbound_relations:
- type: CONTAINS
  source: api.ftgo.gateway
  method: GET
  path: backend/gateway/src/application/routes/customer/address.py
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  symbol: application.routes.customer.address.get_all_addresses
  line_start: 22
  line_end: 39
  evidence_type: implemented
relations:
- type: USES_SCHEMA
  target: schema.ftgo.gateway.application.schemas.account.address.addressesschema
  role: response
  symbol: application.routes.customer.address.get_all_addresses
  type_expression: AddressesSchema
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/customer/address.py
  line_start: 22
  line_end: 22
  evidence_type: implemented
attributes:
  method: GET
  effective_path: /address/get_all_info
  decorator_path: /get_all_info
  router_prefix: /address
  path_resolution: partial
  decorator: router.get("/get_all_info", response_model=AddressesSchema)
  handler: application.routes.customer.address.get_all_addresses
  router: application.routes.customer.address:router
  mount_path:
  - main:app
  - application.app:router
  - application.routes.customer.address:router
  tags:
  - user_address
  response_model: AddressesSchema
  unresolved_prefix_expressions:
  - service_config.api_prefix
---

# GET /address/get_all_info

Candidate HTTP endpoint extracted from a FastAPI route decorator in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Method: `GET`
- Effective path: `/address/get_all_info`
- Path resolution: `partial`
- Handler: `application.routes.customer.address.get_all_addresses`
- Declared in: `backend/gateway/src/application/routes/customer/address.py` (lines 22-39)
- Evidence class: `implemented`

## Unresolved mount prefix

The effective path above omits a mount prefix that is not a string literal in source, so the served path depends on configuration:

- `service_config.api_prefix`

## Schemas

- `response` `USES_SCHEMA` -> `schema.ftgo.gateway.application.schemas.account.address.addressesschema`

## Review notes

This page is a candidate awaiting review. Method and path come from the decorator shown in `attributes.decorator`; nothing was inferred from names.

