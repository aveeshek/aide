---
id: endpoint.ftgo.gateway.delete.address.delete
kind: Endpoint
type: Endpoint
title: DELETE /address/delete
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
effective_path: /address/delete
path_resolution: partial
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/customer/address.py
  symbol: application.routes.customer.address.delete_address
  line_start: 66
  line_end: 85
  evidence_type: implemented
inbound_relations:
- type: CONTAINS
  source: api.ftgo.gateway
  method: DELETE
  path: backend/gateway/src/application/routes/customer/address.py
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  symbol: application.routes.customer.address.delete_address
  line_start: 66
  line_end: 85
  evidence_type: implemented
relations:
- type: USES_SCHEMA
  target: schema.ftgo.gateway.application.schemas.account.address.addressidschema
  role: request
  symbol: application.routes.customer.address.delete_address.request_data
  type_expression: AddressIdSchema
  parameter: request_data
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/customer/address.py
  line_start: 67
  line_end: 67
  evidence_type: implemented
- type: USES_SCHEMA
  target: schema.ftgo.gateway.application.schemas.common.successresponse
  role: response
  symbol: application.routes.customer.address.delete_address
  type_expression: SuccessResponse
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/customer/address.py
  line_start: 66
  line_end: 66
  evidence_type: implemented
attributes:
  method: DELETE
  effective_path: /address/delete
  decorator_path: /delete
  router_prefix: /address
  path_resolution: partial
  decorator: router.delete("/delete", response_model=SuccessResponse)
  handler: application.routes.customer.address.delete_address
  router: application.routes.customer.address:router
  mount_path:
  - main:app
  - application.app:router
  - application.routes.customer.address:router
  tags:
  - user_address
  response_model: SuccessResponse
  unresolved_prefix_expressions:
  - service_config.api_prefix
---

# DELETE /address/delete

Candidate HTTP endpoint extracted from a FastAPI route decorator in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Method: `DELETE`
- Effective path: `/address/delete`
- Path resolution: `partial`
- Handler: `application.routes.customer.address.delete_address`
- Declared in: `backend/gateway/src/application/routes/customer/address.py` (lines 66-85)
- Evidence class: `implemented`

## Unresolved mount prefix

The effective path above omits a mount prefix that is not a string literal in source, so the served path depends on configuration:

- `service_config.api_prefix`

## Schemas

- `request` `USES_SCHEMA` -> `schema.ftgo.gateway.application.schemas.account.address.addressidschema`
- `response` `USES_SCHEMA` -> `schema.ftgo.gateway.application.schemas.common.successresponse`

## Review notes

This page is a candidate awaiting review. Method and path come from the decorator shown in `attributes.decorator`; nothing was inferred from names.

