---
id: schema.ftgo.gateway.application.schemas.driver.status.driverstatusschema
kind: Schema
type: Schema
title: DriverStatusSchema
status: approved
review_status: approved
candidate_of: fastapi-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: fastapi
service: service.ftgo.gateway
owner: aide-ftgo-cohort
qualified_name: application.schemas.driver.status.DriverStatusSchema
pydantic_confirmed: false
base_resolution: external_base
bases:
- BaseSchema
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/schemas/driver/status.py
  symbol: application.schemas.driver.status.DriverStatusSchema
  line_start: 5
  line_end: 6
  evidence_type: implemented
inbound_relations:
- type: USES_SCHEMA
  source: endpoint.ftgo.gateway.get.status.get
  role: response
  symbol: application.routes.driver.online_status.get_status
  type_expression: DriverStatusSchema
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/driver/online_status.py
  line_start: 50
  line_end: 50
  evidence_type: implemented
fields:
- name: is_online
  annotation: bool
  default_expression: Field(...)
  line: 6
---

# DriverStatusSchema

Candidate schema extracted from a class definition in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Qualified name: `application.schemas.driver.status.DriverStatusSchema`
- Declared in: `backend/gateway/src/application/schemas/driver/status.py` (lines 5-6)
- Pydantic BaseModel confirmed in source: `False`
- Base resolution: `external_base`
- Used as: `response`
- Evidence class: `implemented`

## Review notes

This page is a candidate awaiting review. Field annotations are recorded as source text and never evaluated; credential-shaped defaults are redacted at extraction time.

