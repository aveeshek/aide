---
id: step.ftgo.gateway.post.order.reject.http-ingress
kind: FlowStep
type: FlowStep
title: POST /order/reject ingress
status: candidate
review_status: pending
candidate_of: user-flow-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: user-flow
owner: aide-ftgo-cohort
role: http_ingress
flow: flow.ftgo.gateway.post.order.reject
service: service.ftgo.gateway
derived_from: endpoint.ftgo.gateway.post.order.reject
derived_from_kind: Endpoint
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/order/order.py
  symbol: application.routes.order.order.restaurant_reject
  line_start: 121
  line_end: 143
  evidence_type: implemented
relations:
- type: DERIVED_FROM
  target: endpoint.ftgo.gateway.post.order.reject
  anchor_kind: Endpoint
  role: http_ingress
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/order/order.py
  symbol: application.routes.order.order.restaurant_reject
  line_start: 121
  line_end: 143
  evidence_type: implemented
- type: IMPLEMENTS
  target: service.ftgo.gateway
  role: http_ingress
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/order/order.py
  symbol: application.routes.order.order.restaurant_reject
  line_start: 121
  line_end: 143
  evidence_type: implemented
- type: PRECEDES
  target: step.ftgo.gateway.post.order.reject.dispatch.services.order.orderservice.create-order
  established_by: handler call site
  call_depth: 1
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/order/order.py
  symbol: application.routes.order.order.restaurant_reject
  line_start: 128
  line_end: 128
  evidence_type: implemented
inbound_relations:
- type: CONTAINS
  source: flow.ftgo.gateway.post.order.reject
  role: http_ingress
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/order/order.py
  symbol: application.routes.order.order.restaurant_reject
  line_start: 121
  line_end: 143
  evidence_type: implemented
attributes:
  http_method: POST
  path: /order/reject
  path_resolution: partial
  handler: application.routes.order.order.restaurant_reject
---

# POST /order/reject ingress

Candidate execution step extracted from call evidence in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Role: `http_ingress`
- Flow: `flow.ftgo.gateway.post.order.reject`
- Performed by: `service.ftgo.gateway`
- Anchored on: `endpoint.ftgo.gateway.post.order.reject` (`Endpoint`)
- Declared in: `backend/gateway/src/application/routes/order/order.py` (lines 121-143)
- Evidence class: `implemented`

## Review notes

This page is a candidate awaiting review. The step exists because a concrete call site proves it, and its ordering edges carry that call site as evidence.

