---
id: step.ftgo.gateway.put.feedback.delivery.rating.update.publish.ftgo.rabbitmq.delivery.rating.update
kind: FlowStep
type: FlowStep
title: publish delivery.rating.update
status: approved
review_status: approved
candidate_of: user-flow-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: user-flow
owner: aide-ftgo-cohort
role: event_publish
flow: flow.ftgo.gateway.put.feedback.delivery.rating.update
service: service.ftgo.gateway
derived_from: event.ftgo.rabbitmq.delivery.rating.update
derived_from_kind: Event
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/feedback.py
  symbol: services.feedback.FeedbackService.update_delivery_rating
  line_start: 16
  line_end: 16
  evidence_type: implemented
relations:
- type: DERIVED_FROM
  target: event.ftgo.rabbitmq.delivery.rating.update
  anchor_kind: Event
  role: event_publish
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/feedback.py
  symbol: services.feedback.FeedbackService.update_delivery_rating
  line_start: 16
  line_end: 16
  evidence_type: implemented
- type: IMPLEMENTS
  target: service.ftgo.gateway
  role: event_publish
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/feedback.py
  symbol: services.feedback.FeedbackService.update_delivery_rating
  line_start: 16
  line_end: 16
  evidence_type: implemented
- type: PRECEDES
  target: step.ftgo.gateway.put.feedback.delivery.rating.update.consume.feedback.delivery.rating.update
  established_by: handler registration
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/feedback/src/events.py
  symbol: events.register_events
  line_start: 37
  line_end: 37
  evidence_type: implemented
inbound_relations:
- type: CONTAINS
  source: flow.ftgo.gateway.put.feedback.delivery.rating.update
  role: event_publish
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/feedback.py
  symbol: services.feedback.FeedbackService.update_delivery_rating
  line_start: 16
  line_end: 16
  evidence_type: implemented
- type: PRECEDES
  source: step.ftgo.gateway.put.feedback.delivery.rating.update.dispatch.services.feedback.feedbackservice.update-delivery-rating
  established_by: publisher call site
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/feedback.py
  symbol: services.feedback.FeedbackService.update_delivery_rating
  line_start: 16
  line_end: 16
  evidence_type: implemented
attributes:
  event_identity: delivery.rating.update
  operation: call
  mechanism: rpc
  broker_library: rabbitmq_rpc
  via_wrapper: services.base.Microservice._call_rpc
  correlation: matched
---

# publish delivery.rating.update

Canonical execution step extracted from call evidence in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Role: `event_publish`
- Flow: `flow.ftgo.gateway.put.feedback.delivery.rating.update`
- Performed by: `service.ftgo.gateway`
- Anchored on: `event.ftgo.rabbitmq.delivery.rating.update` (`Event`)
- Declared in: `backend/gateway/src/services/feedback.py` (lines 16-16)
- Evidence class: `implemented`

## Review notes

This approved canonical page records a source-backed execution step. The step exists because a concrete call site proves it, and its ordering edges carry that call site as evidence.

