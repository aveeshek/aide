---
id: schema.ftgo.gateway.application.schemas.common.successresponse
kind: Schema
type: Schema
title: SuccessResponse
status: approved
review_status: approved
candidate_of: fastapi-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: fastapi
service: service.ftgo.gateway
owner: aide-ftgo-cohort
qualified_name: application.schemas.common.SuccessResponse
pydantic_confirmed: false
base_resolution: external_base
bases:
- BaseSchema
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/schemas/common.py
  symbol: application.schemas.common.SuccessResponse
  line_start: 10
  line_end: 11
  evidence_type: implemented
inbound_relations:
- type: USES_SCHEMA
  source: endpoint.ftgo.gateway.delete.address.delete
  role: response
  symbol: application.routes.customer.address.delete_address
  type_expression: SuccessResponse
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/customer/address.py
  line_start: 66
  line_end: 66
  evidence_type: implemented
- type: USES_SCHEMA
  source: endpoint.ftgo.gateway.delete.profile.delete
  role: response
  symbol: application.routes.account.profile.delete_account
  type_expression: SuccessResponse
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/account/profile.py
  line_start: 65
  line_end: 65
  evidence_type: implemented
- type: USES_SCHEMA
  source: endpoint.ftgo.gateway.post.auth.verify
  role: response
  symbol: application.routes.auth.registration.verify_account
  type_expression: SuccessResponse
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/auth/registration.py
  line_start: 42
  line_end: 42
  evidence_type: implemented
- type: USES_SCHEMA
  source: endpoint.ftgo.gateway.post.location.submit
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
  source: endpoint.ftgo.gateway.post.order.confirm
  role: response
  symbol: application.routes.order.order.restaurant_confirm
  type_expression: SuccessResponse
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/order/order.py
  line_start: 96
  line_end: 96
  evidence_type: implemented
- type: USES_SCHEMA
  source: endpoint.ftgo.gateway.post.order.create
  role: response
  symbol: application.routes.order.order.create_order
  type_expression: SuccessResponse
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/order/order.py
  line_start: 44
  line_end: 44
  evidence_type: implemented
- type: USES_SCHEMA
  source: endpoint.ftgo.gateway.post.order.reject
  role: response
  symbol: application.routes.order.order.restaurant_reject
  type_expression: SuccessResponse
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/order/order.py
  line_start: 121
  line_end: 121
  evidence_type: implemented
- type: USES_SCHEMA
  source: endpoint.ftgo.gateway.post.order.update
  role: response
  symbol: application.routes.order.order.update_order
  type_expression: SuccessResponse
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/order/order.py
  line_start: 70
  line_end: 70
  evidence_type: implemented
- type: USES_SCHEMA
  source: endpoint.ftgo.gateway.post.profile.logout
  role: response
  symbol: application.routes.account.profile.logout
  type_expression: SuccessResponse
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/account/profile.py
  line_start: 21
  line_end: 21
  evidence_type: implemented
- type: USES_SCHEMA
  source: endpoint.ftgo.gateway.post.status.offline
  role: response
  symbol: application.routes.driver.online_status.change_status_offline
  type_expression: SuccessResponse
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/driver/online_status.py
  line_start: 42
  line_end: 42
  evidence_type: implemented
- type: USES_SCHEMA
  source: endpoint.ftgo.gateway.post.status.online
  role: response
  symbol: application.routes.driver.online_status.change_status_online
  type_expression: SuccessResponse
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/driver/online_status.py
  line_start: 34
  line_end: 34
  evidence_type: implemented
fields:
- name: success
  annotation: Optional[bool]
  default_expression: Field(True)
  line: 11
---

# SuccessResponse

Candidate schema extracted from a class definition in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Qualified name: `application.schemas.common.SuccessResponse`
- Declared in: `backend/gateway/src/application/schemas/common.py` (lines 10-11)
- Pydantic BaseModel confirmed in source: `False`
- Base resolution: `external_base`
- Used as: `response`
- Evidence class: `implemented`

## Review notes

This page is a candidate awaiting review. Field annotations are recorded as source text and never evaluated; credential-shaped defaults are redacted at extraction time.

