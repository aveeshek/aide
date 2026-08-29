---
id: flow.ftgo.gateway.post.feedback.delivery.rating.create
kind: UserFlow
type: UserFlow
title: POST /feedback/delivery/rating/create execution flow
status: candidate
review_status: pending
candidate_of: user-flow-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: user-flow
owner: aide-ftgo-cohort
entry_endpoint: endpoint.ftgo.gateway.post.feedback.delivery.rating.create
http_method: POST
path: /feedback/delivery/rating/create
path_resolution: partial
completeness: partial
handler: application.routes.order.feedback.create_delivery_rating
participating_services:
- service.ftgo.feedback
- service.ftgo.gateway
events:
- event.ftgo.rabbitmq.delivery.rating.create
persistence_targets: []
unresolved_segments:
- persistence:delivery.rating.create
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/order/feedback.py
  symbol: application.routes.order.feedback.create_delivery_rating
  line_start: 30
  line_end: 48
  evidence_type: implemented
relations:
- type: CONTAINS
  target: step.ftgo.gateway.post.feedback.delivery.rating.create.consume.feedback.delivery.rating.create
  role: event_consume
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/feedback/src/events.py
  symbol: events.register_events
  line_start: 37
  line_end: 37
  evidence_type: implemented
- type: CONTAINS
  target: step.ftgo.gateway.post.feedback.delivery.rating.create.dispatch.services.feedback.feedbackservice.create-delivery-rating
  role: service_dispatch
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/order/feedback.py
  symbol: application.routes.order.feedback.create_delivery_rating
  line_start: 36
  line_end: 36
  evidence_type: implemented
- type: CONTAINS
  target: step.ftgo.gateway.post.feedback.delivery.rating.create.http-ingress
  role: http_ingress
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/order/feedback.py
  symbol: application.routes.order.feedback.create_delivery_rating
  line_start: 30
  line_end: 48
  evidence_type: implemented
- type: CONTAINS
  target: step.ftgo.gateway.post.feedback.delivery.rating.create.publish.ftgo.rabbitmq.delivery.rating.create
  role: event_publish
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/feedback.py
  symbol: services.feedback.FeedbackService.create_delivery_rating
  line_start: 12
  line_end: 12
  evidence_type: implemented
inbound_relations:
- type: PARTICIPATES_IN
  source: service.ftgo.feedback
  completeness: partial
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/order/feedback.py
  symbol: application.routes.order.feedback.create_delivery_rating
  line_start: 30
  line_end: 48
  evidence_type: implemented
- type: PARTICIPATES_IN
  source: service.ftgo.gateway
  completeness: partial
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/order/feedback.py
  symbol: application.routes.order.feedback.create_delivery_rating
  line_start: 30
  line_end: 48
  evidence_type: implemented
attributes:
  step_count: 4
  classification_reason: publish and consume are proven but a later segment is unresolved
  max_call_depth: 3
---

# POST /feedback/delivery/rating/create execution flow

Candidate execution flow stitched from source-backed call evidence in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Entry endpoint: `endpoint.ftgo.gateway.post.feedback.delivery.rating.create`
- Completeness: `partial`
- Handler: `application.routes.order.feedback.create_delivery_rating`
- Declared in: `backend/gateway/src/application/routes/order/feedback.py` (lines 30-48)
- Evidence class: `implemented`

## Steps

- `http_ingress` `step.ftgo.gateway.post.feedback.delivery.rating.create.http-ingress`
- `service_dispatch` `step.ftgo.gateway.post.feedback.delivery.rating.create.dispatch.services.feedback.feedbackservice.create-delivery-rating`
- `event_publish` `step.ftgo.gateway.post.feedback.delivery.rating.create.publish.ftgo.rabbitmq.delivery.rating.create`
- `event_consume` `step.ftgo.gateway.post.feedback.delivery.rating.create.consume.feedback.delivery.rating.create`

## Unresolved segments

This flow is not complete. The following segments could not be proven from source and are deliberately not invented:

- `persistence:delivery.rating.create`

## Review notes

This page is a candidate awaiting review. Every step is backed by a bounded call trace of at most 3 hops; no segment was inferred from the similarity between an endpoint path and an event name.

