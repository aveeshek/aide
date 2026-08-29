---
id: step.ftgo.gateway.get.feedback.order.rating.get.http-ingress
kind: FlowStep
type: FlowStep
title: GET /feedback/order/rating/get ingress
status: candidate
review_status: pending
candidate_of: user-flow-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: user-flow
owner: aide-ftgo-cohort
role: http_ingress
flow: flow.ftgo.gateway.get.feedback.order.rating.get
service: service.ftgo.gateway
derived_from: endpoint.ftgo.gateway.get.feedback.order.rating.get
derived_from_kind: Endpoint
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/order/feedback.py
  symbol: application.routes.order.feedback.get_order_rating
  line_start: 171
  line_end: 189
  evidence_type: implemented
relations:
- type: DERIVED_FROM
  target: endpoint.ftgo.gateway.get.feedback.order.rating.get
  anchor_kind: Endpoint
  role: http_ingress
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/order/feedback.py
  symbol: application.routes.order.feedback.get_order_rating
  line_start: 171
  line_end: 189
  evidence_type: implemented
- type: IMPLEMENTS
  target: service.ftgo.gateway
  role: http_ingress
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/order/feedback.py
  symbol: application.routes.order.feedback.get_order_rating
  line_start: 171
  line_end: 189
  evidence_type: implemented
- type: PRECEDES
  target: step.ftgo.gateway.get.feedback.order.rating.get.dispatch.services.feedback.feedbackservice.get-order-rating
  established_by: handler call site
  call_depth: 1
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/order/feedback.py
  symbol: application.routes.order.feedback.get_order_rating
  line_start: 177
  line_end: 177
  evidence_type: implemented
inbound_relations:
- type: CONTAINS
  source: flow.ftgo.gateway.get.feedback.order.rating.get
  role: http_ingress
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/order/feedback.py
  symbol: application.routes.order.feedback.get_order_rating
  line_start: 171
  line_end: 189
  evidence_type: implemented
attributes:
  http_method: GET
  path: /feedback/order/rating/get
  path_resolution: partial
  handler: application.routes.order.feedback.get_order_rating
---

# GET /feedback/order/rating/get ingress

Candidate execution step extracted from call evidence in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Role: `http_ingress`
- Flow: `flow.ftgo.gateway.get.feedback.order.rating.get`
- Performed by: `service.ftgo.gateway`
- Anchored on: `endpoint.ftgo.gateway.get.feedback.order.rating.get` (`Endpoint`)
- Declared in: `backend/gateway/src/application/routes/order/feedback.py` (lines 171-189)
- Evidence class: `implemented`

## Review notes

This page is a candidate awaiting review. The step exists because a concrete call site proves it, and its ordering edges carry that call site as evidence.

