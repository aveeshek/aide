---
id: schema.ftgo.gateway.application.schemas.account.address.addressidschema
kind: Schema
type: Schema
title: AddressIdSchema
status: candidate
review_status: pending
candidate_of: fastapi-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: fastapi
service: service.ftgo.gateway
owner: aide-ftgo-cohort
qualified_name: application.schemas.account.address.AddressIdSchema
pydantic_confirmed: false
base_resolution: external_base
bases:
- BaseSchema
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/schemas/account/address.py
  symbol: application.schemas.account.address.AddressIdSchema
  line_start: 15
  line_end: 16
  evidence_type: implemented
inbound_relations:
- type: USES_SCHEMA
  source: endpoint.ftgo.gateway.delete.address.delete
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
fields:
- name: address_id
  annotation: str
  default_expression: uuid_field()
  line: 16
---

# AddressIdSchema

Candidate schema extracted from a class definition in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Qualified name: `application.schemas.account.address.AddressIdSchema`
- Declared in: `backend/gateway/src/application/schemas/account/address.py` (lines 15-16)
- Pydantic BaseModel confirmed in source: `False`
- Base resolution: `external_base`
- Used as: `request`
- Evidence class: `implemented`

## Review notes

This page is a candidate awaiting review. Field annotations are recorded as source text and never evaluated; credential-shaped defaults are redacted at extraction time.

