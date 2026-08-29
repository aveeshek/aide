---
id: flow.ftgo.gateway.get.feedback.delivery.rating.get
kind: UserFlow
type: UserFlow
title: GET /feedback/delivery/rating/get execution flow
status: approved
review_status: approved
candidate_of: user-flow-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: user-flow
owner: aide-ftgo-cohort
entry_endpoint: endpoint.ftgo.gateway.get.feedback.delivery.rating.get
http_method: GET
path: /feedback/delivery/rating/get
path_resolution: partial
completeness: partial
handler: application.routes.order.feedback.get_delivery_rating
participating_services:
- service.ftgo.gateway
events:
- event.ftgo.rabbitmq.delivery.rating.get
persistence_targets: []
unresolved_segments:
- consume:delivery.rating.get
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/order/feedback.py
  symbol: application.routes.order.feedback.get_delivery_rating
  line_start: 70
  line_end: 87
  evidence_type: implemented
relations:
- type: CONTAINS
  target: step.ftgo.gateway.get.feedback.delivery.rating.get.dispatch.services.feedback.feedbackservice.get-delivery-rating
  role: service_dispatch
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/order/feedback.py
  symbol: application.routes.order.feedback.get_delivery_rating
  line_start: 75
  line_end: 75
  evidence_type: implemented
- type: CONTAINS
  target: step.ftgo.gateway.get.feedback.delivery.rating.get.http-ingress
  role: http_ingress
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/order/feedback.py
  symbol: application.routes.order.feedback.get_delivery_rating
  line_start: 70
  line_end: 87
  evidence_type: implemented
- type: CONTAINS
  target: step.ftgo.gateway.get.feedback.delivery.rating.get.publish.ftgo.rabbitmq.delivery.rating.get
  role: event_publish
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/feedback.py
  symbol: services.feedback.FeedbackService.get_delivery_rating
  line_start: 20
  line_end: 20
  evidence_type: implemented
inbound_relations:
- type: PARTICIPATES_IN
  source: service.ftgo.gateway
  completeness: partial
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/order/feedback.py
  symbol: application.routes.order.feedback.get_delivery_rating
  line_start: 70
  line_end: 87
  evidence_type: implemented
attributes:
  step_count: 3
  classification_reason: publish is proven but no consumer binding exists for the identity
  max_call_depth: 3
---

# GET /feedback/delivery/rating/get execution flow

Canonical execution flow stitched from source-backed call evidence in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Entry endpoint: `endpoint.ftgo.gateway.get.feedback.delivery.rating.get`
- Completeness: `partial`
- Handler: `application.routes.order.feedback.get_delivery_rating`
- Declared in: `backend/gateway/src/application/routes/order/feedback.py` (lines 70-87)
- Evidence class: `implemented`

## Steps

- `http_ingress` `step.ftgo.gateway.get.feedback.delivery.rating.get.http-ingress`
- `service_dispatch` `step.ftgo.gateway.get.feedback.delivery.rating.get.dispatch.services.feedback.feedbackservice.get-delivery-rating`
- `event_publish` `step.ftgo.gateway.get.feedback.delivery.rating.get.publish.ftgo.rabbitmq.delivery.rating.get`

## Unresolved segments

This flow is not complete. The following segments could not be proven from source and are deliberately not invented:

- `consume:delivery.rating.get`

## Review notes

This approved canonical page records a source-backed execution flow. Every step is backed by a bounded call trace of at most 3 hops; no segment was inferred from similarity between an endpoint path and an event name.

