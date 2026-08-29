---
id: step.ftgo.gateway.get.address.get-all-info.http-ingress
kind: FlowStep
type: FlowStep
title: GET /address/get_all_info ingress
status: candidate
review_status: pending
candidate_of: user-flow-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: user-flow
owner: aide-ftgo-cohort
role: http_ingress
flow: flow.ftgo.gateway.get.address.get-all-info
service: service.ftgo.gateway
derived_from: endpoint.ftgo.gateway.get.address.get-all-info
derived_from_kind: Endpoint
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/customer/address.py
  symbol: application.routes.customer.address.get_all_addresses
  line_start: 22
  line_end: 39
  evidence_type: implemented
relations:
- type: DERIVED_FROM
  target: endpoint.ftgo.gateway.get.address.get-all-info
  anchor_kind: Endpoint
  role: http_ingress
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/customer/address.py
  symbol: application.routes.customer.address.get_all_addresses
  line_start: 22
  line_end: 39
  evidence_type: implemented
- type: IMPLEMENTS
  target: service.ftgo.gateway
  role: http_ingress
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/customer/address.py
  symbol: application.routes.customer.address.get_all_addresses
  line_start: 22
  line_end: 39
  evidence_type: implemented
- type: PRECEDES
  target: step.ftgo.gateway.get.address.get-all-info.dispatch.services.user.userservice.get-all-addresses
  established_by: handler call site
  call_depth: 1
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/customer/address.py
  symbol: application.routes.customer.address.get_all_addresses
  line_start: 26
  line_end: 26
  evidence_type: implemented
inbound_relations:
- type: CONTAINS
  source: flow.ftgo.gateway.get.address.get-all-info
  role: http_ingress
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/customer/address.py
  symbol: application.routes.customer.address.get_all_addresses
  line_start: 22
  line_end: 39
  evidence_type: implemented
attributes:
  http_method: GET
  path: /address/get_all_info
  path_resolution: partial
  handler: application.routes.customer.address.get_all_addresses
---

# GET /address/get_all_info ingress

Candidate execution step extracted from call evidence in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Role: `http_ingress`
- Flow: `flow.ftgo.gateway.get.address.get-all-info`
- Performed by: `service.ftgo.gateway`
- Anchored on: `endpoint.ftgo.gateway.get.address.get-all-info` (`Endpoint`)
- Declared in: `backend/gateway/src/application/routes/customer/address.py` (lines 22-39)
- Evidence class: `implemented`

## Review notes

This page is a candidate awaiting review. The step exists because a concrete call site proves it, and its ordering edges carry that call site as evidence.

