---
id: endpoint.ftgo.gateway.post.address.add
kind: Endpoint
type: Endpoint
title: POST /address/add
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
effective_path: /address/add
path_resolution: partial
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/customer/address.py
  symbol: application.routes.customer.address.add_address
  line_start: 42
  line_end: 63
  evidence_type: implemented
inbound_relations:
- type: CONTAINS
  source: api.ftgo.gateway
  method: POST
  path: backend/gateway/src/application/routes/customer/address.py
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  symbol: application.routes.customer.address.add_address
  line_start: 42
  line_end: 63
  evidence_type: implemented
attributes:
  method: POST
  effective_path: /address/add
  decorator_path: /add
  router_prefix: /address
  path_resolution: partial
  decorator: router.post("/add", response_model=AddressMixin)
  handler: application.routes.customer.address.add_address
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

# POST /address/add

Candidate HTTP endpoint extracted from a FastAPI route decorator in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Method: `POST`
- Effective path: `/address/add`
- Path resolution: `partial`
- Handler: `application.routes.customer.address.add_address`
- Declared in: `backend/gateway/src/application/routes/customer/address.py` (lines 42-63)
- Evidence class: `implemented`

## Unresolved mount prefix

The effective path above omits a mount prefix that is not a string literal in source, so the served path depends on configuration:

- `service_config.api_prefix`

## Review notes

This page is a candidate awaiting review. Method and path come from the decorator shown in `attributes.decorator`; nothing was inferred from names.

