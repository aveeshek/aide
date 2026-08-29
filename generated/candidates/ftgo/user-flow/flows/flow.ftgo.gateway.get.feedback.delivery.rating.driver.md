---
id: flow.ftgo.gateway.get.feedback.delivery.rating.driver
kind: UserFlow
type: UserFlow
title: GET /feedback/delivery/rating/driver execution flow
status: candidate
review_status: pending
candidate_of: user-flow-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: user-flow
owner: aide-ftgo-cohort
entry_endpoint: endpoint.ftgo.gateway.get.feedback.delivery.rating.driver
http_method: GET
path: /feedback/delivery/rating/driver
path_resolution: partial
completeness: resolved
handler: application.routes.order.feedback.get_driver_delivery_ratings
participating_services:
- service.ftgo.feedback
- service.ftgo.gateway
events:
- event.ftgo.rabbitmq.delivery.rating.get-driver-ratings
persistence_targets:
- collection.ftgo.feedback.delivery-ratings
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/order/feedback.py
  symbol: application.routes.order.feedback.get_driver_delivery_ratings
  line_start: 109
  line_end: 127
  evidence_type: implemented
relations:
- type: CONTAINS
  target: step.ftgo.gateway.get.feedback.delivery.rating.driver.consume.feedback.delivery.rating.get-driver-ratings
  role: event_consume
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/feedback/src/events.py
  symbol: events.register_events
  line_start: 37
  line_end: 37
  evidence_type: implemented
- type: CONTAINS
  target: step.ftgo.gateway.get.feedback.delivery.rating.driver.dispatch.services.feedback.feedbackservice.get-driver-delivery-ratings
  role: service_dispatch
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/order/feedback.py
  symbol: application.routes.order.feedback.get_driver_delivery_ratings
  line_start: 115
  line_end: 115
  evidence_type: implemented
- type: CONTAINS
  target: step.ftgo.gateway.get.feedback.delivery.rating.driver.http-ingress
  role: http_ingress
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/order/feedback.py
  symbol: application.routes.order.feedback.get_driver_delivery_ratings
  line_start: 109
  line_end: 127
  evidence_type: implemented
- type: CONTAINS
  target: step.ftgo.gateway.get.feedback.delivery.rating.driver.publish.ftgo.rabbitmq.delivery.rating.get-driver-ratings
  role: event_publish
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/feedback.py
  symbol: services.feedback.FeedbackService.get_driver_delivery_ratings
  line_start: 28
  line_end: 28
  evidence_type: implemented
- type: CONTAINS
  target: step.ftgo.gateway.get.feedback.delivery.rating.driver.read.ftgo.feedback.delivery-ratings
  role: persistence_read
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/feedback/src/domain/delivery_rating.py
  symbol: domain.delivery_rating.DeliveryRatingHandler.get_driver_delivery_ratings
  line_start: 61
  line_end: 61
  evidence_type: implemented
inbound_relations:
- type: PARTICIPATES_IN
  source: service.ftgo.feedback
  completeness: resolved
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/order/feedback.py
  symbol: application.routes.order.feedback.get_driver_delivery_ratings
  line_start: 109
  line_end: 127
  evidence_type: implemented
- type: PARTICIPATES_IN
  source: service.ftgo.gateway
  completeness: resolved
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/order/feedback.py
  symbol: application.routes.order.feedback.get_driver_delivery_ratings
  line_start: 109
  line_end: 127
  evidence_type: implemented
attributes:
  step_count: 5
  classification_reason: endpoint, publish, consume and persistence are all source-backed
  max_call_depth: 3
---

# GET /feedback/delivery/rating/driver execution flow

Candidate execution flow stitched from source-backed call evidence in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Entry endpoint: `endpoint.ftgo.gateway.get.feedback.delivery.rating.driver`
- Completeness: `resolved`
- Handler: `application.routes.order.feedback.get_driver_delivery_ratings`
- Declared in: `backend/gateway/src/application/routes/order/feedback.py` (lines 109-127)
- Evidence class: `implemented`

## Steps

- `http_ingress` `step.ftgo.gateway.get.feedback.delivery.rating.driver.http-ingress`
- `service_dispatch` `step.ftgo.gateway.get.feedback.delivery.rating.driver.dispatch.services.feedback.feedbackservice.get-driver-delivery-ratings`
- `event_publish` `step.ftgo.gateway.get.feedback.delivery.rating.driver.publish.ftgo.rabbitmq.delivery.rating.get-driver-ratings`
- `event_consume` `step.ftgo.gateway.get.feedback.delivery.rating.driver.consume.feedback.delivery.rating.get-driver-ratings`
- `persistence_read` `step.ftgo.gateway.get.feedback.delivery.rating.driver.read.ftgo.feedback.delivery-ratings`

## Review notes

This page is a candidate awaiting review. Every step is backed by a bounded call trace of at most 3 hops; no segment was inferred from the similarity between an endpoint path and an event name.

