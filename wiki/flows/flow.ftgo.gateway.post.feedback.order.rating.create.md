---
id: flow.ftgo.gateway.post.feedback.order.rating.create
kind: UserFlow
type: UserFlow
title: POST /feedback/order/rating/create execution flow
status: approved
review_status: approved
candidate_of: user-flow-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: user-flow
owner: aide-ftgo-cohort
entry_endpoint: endpoint.ftgo.gateway.post.feedback.order.rating.create
http_method: POST
path: /feedback/order/rating/create
path_resolution: partial
completeness: partial
handler: application.routes.order.feedback.create_order_rating
participating_services:
- service.ftgo.feedback
- service.ftgo.gateway
events:
- event.ftgo.rabbitmq.order.rating.create
persistence_targets: []
unresolved_segments:
- persistence:order.rating.create
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/order/feedback.py
  symbol: application.routes.order.feedback.create_order_rating
  line_start: 131
  line_end: 149
  evidence_type: implemented
relations:
- type: CONTAINS
  target: step.ftgo.gateway.post.feedback.order.rating.create.consume.feedback.order.rating.create
  role: event_consume
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/feedback/src/events.py
  symbol: events.register_events
  line_start: 37
  line_end: 37
  evidence_type: implemented
- type: CONTAINS
  target: step.ftgo.gateway.post.feedback.order.rating.create.dispatch.services.feedback.feedbackservice.create-order-rating
  role: service_dispatch
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/order/feedback.py
  symbol: application.routes.order.feedback.create_order_rating
  line_start: 137
  line_end: 137
  evidence_type: implemented
- type: CONTAINS
  target: step.ftgo.gateway.post.feedback.order.rating.create.http-ingress
  role: http_ingress
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/order/feedback.py
  symbol: application.routes.order.feedback.create_order_rating
  line_start: 131
  line_end: 149
  evidence_type: implemented
- type: CONTAINS
  target: step.ftgo.gateway.post.feedback.order.rating.create.publish.ftgo.rabbitmq.order.rating.create
  role: event_publish
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/feedback.py
  symbol: services.feedback.FeedbackService.create_order_rating
  line_start: 33
  line_end: 33
  evidence_type: implemented
inbound_relations:
- type: PARTICIPATES_IN
  source: service.ftgo.feedback
  completeness: partial
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/order/feedback.py
  symbol: application.routes.order.feedback.create_order_rating
  line_start: 131
  line_end: 149
  evidence_type: implemented
- type: PARTICIPATES_IN
  source: service.ftgo.gateway
  completeness: partial
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/order/feedback.py
  symbol: application.routes.order.feedback.create_order_rating
  line_start: 131
  line_end: 149
  evidence_type: implemented
attributes:
  step_count: 4
  classification_reason: publish and consume are proven but a later segment is unresolved
  max_call_depth: 3
---

# POST /feedback/order/rating/create execution flow

Canonical execution flow stitched from source-backed call evidence in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Entry endpoint: `endpoint.ftgo.gateway.post.feedback.order.rating.create`
- Completeness: `partial`
- Handler: `application.routes.order.feedback.create_order_rating`
- Declared in: `backend/gateway/src/application/routes/order/feedback.py` (lines 131-149)
- Evidence class: `implemented`

## Steps

- `http_ingress` `step.ftgo.gateway.post.feedback.order.rating.create.http-ingress`
- `service_dispatch` `step.ftgo.gateway.post.feedback.order.rating.create.dispatch.services.feedback.feedbackservice.create-order-rating`
- `event_publish` `step.ftgo.gateway.post.feedback.order.rating.create.publish.ftgo.rabbitmq.order.rating.create`
- `event_consume` `step.ftgo.gateway.post.feedback.order.rating.create.consume.feedback.order.rating.create`

## Unresolved segments

This flow is not complete. The following segments could not be proven from source and are deliberately not invented:

- `persistence:order.rating.create`

## Review notes

This approved canonical page records a source-backed execution flow. Every step is backed by a bounded call trace of at most 3 hops; no segment was inferred from similarity between an endpoint path and an event name.

