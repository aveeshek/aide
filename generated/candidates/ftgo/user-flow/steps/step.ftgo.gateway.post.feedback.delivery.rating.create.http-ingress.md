---
id: step.ftgo.gateway.post.feedback.delivery.rating.create.http-ingress
kind: FlowStep
type: FlowStep
title: POST /feedback/delivery/rating/create ingress
status: candidate
review_status: pending
candidate_of: user-flow-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: user-flow
owner: aide-ftgo-cohort
role: http_ingress
flow: flow.ftgo.gateway.post.feedback.delivery.rating.create
service: service.ftgo.gateway
derived_from: endpoint.ftgo.gateway.post.feedback.delivery.rating.create
derived_from_kind: Endpoint
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/order/feedback.py
  symbol: application.routes.order.feedback.create_delivery_rating
  line_start: 30
  line_end: 48
  evidence_type: implemented
relations:
- type: DERIVED_FROM
  target: endpoint.ftgo.gateway.post.feedback.delivery.rating.create
  anchor_kind: Endpoint
  role: http_ingress
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/order/feedback.py
  symbol: application.routes.order.feedback.create_delivery_rating
  line_start: 30
  line_end: 48
  evidence_type: implemented
- type: IMPLEMENTS
  target: service.ftgo.gateway
  role: http_ingress
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/order/feedback.py
  symbol: application.routes.order.feedback.create_delivery_rating
  line_start: 30
  line_end: 48
  evidence_type: implemented
- type: PRECEDES
  target: step.ftgo.gateway.post.feedback.delivery.rating.create.dispatch.services.feedback.feedbackservice.create-delivery-rating
  established_by: handler call site
  call_depth: 1
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/order/feedback.py
  symbol: application.routes.order.feedback.create_delivery_rating
  line_start: 36
  line_end: 36
  evidence_type: implemented
inbound_relations:
- type: CONTAINS
  source: flow.ftgo.gateway.post.feedback.delivery.rating.create
  role: http_ingress
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/order/feedback.py
  symbol: application.routes.order.feedback.create_delivery_rating
  line_start: 30
  line_end: 48
  evidence_type: implemented
attributes:
  http_method: POST
  path: /feedback/delivery/rating/create
  path_resolution: partial
  handler: application.routes.order.feedback.create_delivery_rating
---

# POST /feedback/delivery/rating/create ingress

Candidate execution step extracted from call evidence in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Role: `http_ingress`
- Flow: `flow.ftgo.gateway.post.feedback.delivery.rating.create`
- Performed by: `service.ftgo.gateway`
- Anchored on: `endpoint.ftgo.gateway.post.feedback.delivery.rating.create` (`Endpoint`)
- Declared in: `backend/gateway/src/application/routes/order/feedback.py` (lines 30-48)
- Evidence class: `implemented`

## Review notes

This page is a candidate awaiting review. The step exists because a concrete call site proves it, and its ordering edges carry that call site as evidence.

