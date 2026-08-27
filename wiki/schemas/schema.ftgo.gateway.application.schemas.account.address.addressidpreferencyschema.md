---
id: schema.ftgo.gateway.application.schemas.account.address.addressidpreferencyschema
kind: Schema
type: Schema
title: AddressIdPreferencySchema
status: approved
review_status: approved
candidate_of: fastapi-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: fastapi
service: service.ftgo.gateway
owner: aide-ftgo-cohort
qualified_name: application.schemas.account.address.AddressIdPreferencySchema
pydantic_confirmed: false
base_resolution: local_non_model_base
bases:
- AddressIdSchema
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/schemas/account/address.py
  symbol: application.schemas.account.address.AddressIdPreferencySchema
  line_start: 18
  line_end: 19
  evidence_type: implemented
inbound_relations:
- type: USES_SCHEMA
  source: endpoint.ftgo.gateway.post.address.set-preferred
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
fields:
- name: is_default
  annotation: Optional[bool]
  default_expression: Field(False)
  line: 19
---

# AddressIdPreferencySchema

Candidate schema extracted from a class definition in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Qualified name: `application.schemas.account.address.AddressIdPreferencySchema`
- Declared in: `backend/gateway/src/application/schemas/account/address.py` (lines 18-19)
- Pydantic BaseModel confirmed in source: `False`
- Base resolution: `local_non_model_base`
- Used as: `request`
- Evidence class: `implemented`

## Review notes

This page is a candidate awaiting review. Field annotations are recorded as source text and never evaluated; credential-shaped defaults are redacted at extraction time.

