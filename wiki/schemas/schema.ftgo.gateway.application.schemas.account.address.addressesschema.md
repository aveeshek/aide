---
id: schema.ftgo.gateway.application.schemas.account.address.addressesschema
kind: Schema
type: Schema
title: AddressesSchema
status: approved
review_status: approved
candidate_of: fastapi-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: fastapi
service: service.ftgo.gateway
owner: aide-ftgo-cohort
qualified_name: application.schemas.account.address.AddressesSchema
pydantic_confirmed: false
base_resolution: external_base
bases:
- BaseSchema
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/schemas/account/address.py
  symbol: application.schemas.account.address.AddressesSchema
  line_start: 12
  line_end: 13
  evidence_type: implemented
inbound_relations:
- type: USES_SCHEMA
  source: endpoint.ftgo.gateway.get.address.get-all-info
  role: response
  symbol: application.routes.customer.address.get_all_addresses
  type_expression: AddressesSchema
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/customer/address.py
  line_start: 22
  line_end: 22
  evidence_type: implemented
fields:
- name: addresses
  annotation: list[AddressMixin]
  default_expression: Field(...)
  line: 13
---

# AddressesSchema

Candidate schema extracted from a class definition in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Qualified name: `application.schemas.account.address.AddressesSchema`
- Declared in: `backend/gateway/src/application/schemas/account/address.py` (lines 12-13)
- Pydantic BaseModel confirmed in source: `False`
- Base resolution: `external_base`
- Used as: `response`
- Evidence class: `implemented`

## Review notes

This page is a candidate awaiting review. Field annotations are recorded as source text and never evaluated; credential-shaped defaults are redacted at extraction time.

