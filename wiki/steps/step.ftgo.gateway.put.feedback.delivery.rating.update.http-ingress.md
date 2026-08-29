---
id: step.ftgo.gateway.put.feedback.delivery.rating.update.http-ingress
kind: FlowStep
type: FlowStep
title: PUT /feedback/delivery/rating/update ingress
status: approved
review_status: approved
candidate_of: user-flow-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: user-flow
owner: aide-ftgo-cohort
role: http_ingress
flow: flow.ftgo.gateway.put.feedback.delivery.rating.update
service: service.ftgo.gateway
derived_from: endpoint.ftgo.gateway.put.feedback.delivery.rating.update
derived_from_kind: Endpoint
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/order/feedback.py
  symbol: application.routes.order.feedback.update_delivery_rating
  line_start: 50
  line_end: 68
  evidence_type: implemented
relations:
- type: DERIVED_FROM
  target: endpoint.ftgo.gateway.put.feedback.delivery.rating.update
  anchor_kind: Endpoint
  role: http_ingress
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/order/feedback.py
  symbol: application.routes.order.feedback.update_delivery_rating
  line_start: 50
  line_end: 68
  evidence_type: implemented
- type: IMPLEMENTS
  target: service.ftgo.gateway
  role: http_ingress
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/order/feedback.py
  symbol: application.routes.order.feedback.update_delivery_rating
  line_start: 50
  line_end: 68
  evidence_type: implemented
- type: PRECEDES
  target: step.ftgo.gateway.put.feedback.delivery.rating.update.dispatch.services.feedback.feedbackservice.update-delivery-rating
  established_by: handler call site
  call_depth: 1
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/order/feedback.py
  symbol: application.routes.order.feedback.update_delivery_rating
  line_start: 56
  line_end: 56
  evidence_type: implemented
inbound_relations:
- type: CONTAINS
  source: flow.ftgo.gateway.put.feedback.delivery.rating.update
  role: http_ingress
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/order/feedback.py
  symbol: application.routes.order.feedback.update_delivery_rating
  line_start: 50
  line_end: 68
  evidence_type: implemented
attributes:
  http_method: PUT
  path: /feedback/delivery/rating/update
  path_resolution: partial
  handler: application.routes.order.feedback.update_delivery_rating
---

# PUT /feedback/delivery/rating/update ingress

Canonical execution step extracted from call evidence in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Role: `http_ingress`
- Flow: `flow.ftgo.gateway.put.feedback.delivery.rating.update`
- Performed by: `service.ftgo.gateway`
- Anchored on: `endpoint.ftgo.gateway.put.feedback.delivery.rating.update` (`Endpoint`)
- Declared in: `backend/gateway/src/application/routes/order/feedback.py` (lines 50-68)
- Evidence class: `implemented`

## Review notes

This approved canonical page records a source-backed execution step. The step exists because a concrete call site proves it, and its ordering edges carry that call site as evidence.

