---
id: flow.ftgo.gateway.put.feedback.delivery.rating.update
kind: UserFlow
type: UserFlow
title: PUT /feedback/delivery/rating/update execution flow
status: candidate
review_status: pending
candidate_of: user-flow-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: user-flow
owner: aide-ftgo-cohort
entry_endpoint: endpoint.ftgo.gateway.put.feedback.delivery.rating.update
http_method: PUT
path: /feedback/delivery/rating/update
path_resolution: partial
completeness: partial
handler: application.routes.order.feedback.update_delivery_rating
participating_services:
- service.ftgo.feedback
- service.ftgo.gateway
events:
- event.ftgo.rabbitmq.delivery.rating.update
persistence_targets: []
unresolved_segments:
- persistence:delivery.rating.update
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/order/feedback.py
  symbol: application.routes.order.feedback.update_delivery_rating
  line_start: 50
  line_end: 68
  evidence_type: implemented
relations:
- type: CONTAINS
  target: step.ftgo.gateway.put.feedback.delivery.rating.update.consume.feedback.delivery.rating.update
  role: event_consume
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/feedback/src/events.py
  symbol: events.register_events
  line_start: 37
  line_end: 37
  evidence_type: implemented
- type: CONTAINS
  target: step.ftgo.gateway.put.feedback.delivery.rating.update.dispatch.services.feedback.feedbackservice.update-delivery-rating
  role: service_dispatch
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/order/feedback.py
  symbol: application.routes.order.feedback.update_delivery_rating
  line_start: 56
  line_end: 56
  evidence_type: implemented
- type: CONTAINS
  target: step.ftgo.gateway.put.feedback.delivery.rating.update.http-ingress
  role: http_ingress
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/order/feedback.py
  symbol: application.routes.order.feedback.update_delivery_rating
  line_start: 50
  line_end: 68
  evidence_type: implemented
- type: CONTAINS
  target: step.ftgo.gateway.put.feedback.delivery.rating.update.publish.ftgo.rabbitmq.delivery.rating.update
  role: event_publish
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/feedback.py
  symbol: services.feedback.FeedbackService.update_delivery_rating
  line_start: 16
  line_end: 16
  evidence_type: implemented
inbound_relations:
- type: PARTICIPATES_IN
  source: service.ftgo.feedback
  completeness: partial
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/order/feedback.py
  symbol: application.routes.order.feedback.update_delivery_rating
  line_start: 50
  line_end: 68
  evidence_type: implemented
- type: PARTICIPATES_IN
  source: service.ftgo.gateway
  completeness: partial
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/order/feedback.py
  symbol: application.routes.order.feedback.update_delivery_rating
  line_start: 50
  line_end: 68
  evidence_type: implemented
attributes:
  step_count: 4
  classification_reason: publish and consume are proven but a later segment is unresolved
  max_call_depth: 3
---

# PUT /feedback/delivery/rating/update execution flow

Candidate execution flow stitched from source-backed call evidence in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Entry endpoint: `endpoint.ftgo.gateway.put.feedback.delivery.rating.update`
- Completeness: `partial`
- Handler: `application.routes.order.feedback.update_delivery_rating`
- Declared in: `backend/gateway/src/application/routes/order/feedback.py` (lines 50-68)
- Evidence class: `implemented`

## Steps

- `http_ingress` `step.ftgo.gateway.put.feedback.delivery.rating.update.http-ingress`
- `service_dispatch` `step.ftgo.gateway.put.feedback.delivery.rating.update.dispatch.services.feedback.feedbackservice.update-delivery-rating`
- `event_publish` `step.ftgo.gateway.put.feedback.delivery.rating.update.publish.ftgo.rabbitmq.delivery.rating.update`
- `event_consume` `step.ftgo.gateway.put.feedback.delivery.rating.update.consume.feedback.delivery.rating.update`

## Unresolved segments

This flow is not complete. The following segments could not be proven from source and are deliberately not invented:

- `persistence:delivery.rating.update`

## Review notes

This page is a candidate awaiting review. Every step is backed by a bounded call trace of at most 3 hops; no segment was inferred from the similarity between an endpoint path and an event name.

