---
id: step.ftgo.gateway.get.feedback.delivery.rating.customer.http-ingress
kind: FlowStep
type: FlowStep
title: GET /feedback/delivery/rating/customer ingress
status: approved
review_status: approved
candidate_of: user-flow-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: user-flow
owner: aide-ftgo-cohort
role: http_ingress
flow: flow.ftgo.gateway.get.feedback.delivery.rating.customer
service: service.ftgo.gateway
derived_from: endpoint.ftgo.gateway.get.feedback.delivery.rating.customer
derived_from_kind: Endpoint
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/order/feedback.py
  symbol: application.routes.order.feedback.get_customer_delivery_ratings
  line_start: 89
  line_end: 107
  evidence_type: implemented
relations:
- type: DERIVED_FROM
  target: endpoint.ftgo.gateway.get.feedback.delivery.rating.customer
  anchor_kind: Endpoint
  role: http_ingress
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/order/feedback.py
  symbol: application.routes.order.feedback.get_customer_delivery_ratings
  line_start: 89
  line_end: 107
  evidence_type: implemented
- type: IMPLEMENTS
  target: service.ftgo.gateway
  role: http_ingress
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/order/feedback.py
  symbol: application.routes.order.feedback.get_customer_delivery_ratings
  line_start: 89
  line_end: 107
  evidence_type: implemented
- type: PRECEDES
  target: step.ftgo.gateway.get.feedback.delivery.rating.customer.dispatch.services.feedback.feedbackservice.get-customer-delivery-ratings
  established_by: handler call site
  call_depth: 1
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/order/feedback.py
  symbol: application.routes.order.feedback.get_customer_delivery_ratings
  line_start: 95
  line_end: 95
  evidence_type: implemented
inbound_relations:
- type: CONTAINS
  source: flow.ftgo.gateway.get.feedback.delivery.rating.customer
  role: http_ingress
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/order/feedback.py
  symbol: application.routes.order.feedback.get_customer_delivery_ratings
  line_start: 89
  line_end: 107
  evidence_type: implemented
attributes:
  http_method: GET
  path: /feedback/delivery/rating/customer
  path_resolution: partial
  handler: application.routes.order.feedback.get_customer_delivery_ratings
---

# GET /feedback/delivery/rating/customer ingress

Canonical execution step extracted from call evidence in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Role: `http_ingress`
- Flow: `flow.ftgo.gateway.get.feedback.delivery.rating.customer`
- Performed by: `service.ftgo.gateway`
- Anchored on: `endpoint.ftgo.gateway.get.feedback.delivery.rating.customer` (`Endpoint`)
- Declared in: `backend/gateway/src/application/routes/order/feedback.py` (lines 89-107)
- Evidence class: `implemented`

## Review notes

This approved canonical page records a source-backed execution step. The step exists because a concrete call site proves it, and its ordering edges carry that call site as evidence.

