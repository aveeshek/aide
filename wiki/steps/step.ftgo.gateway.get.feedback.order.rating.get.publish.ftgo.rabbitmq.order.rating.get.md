---
id: step.ftgo.gateway.get.feedback.order.rating.get.publish.ftgo.rabbitmq.order.rating.get
kind: FlowStep
type: FlowStep
title: publish order.rating.get
status: approved
review_status: approved
candidate_of: user-flow-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: user-flow
owner: aide-ftgo-cohort
role: event_publish
flow: flow.ftgo.gateway.get.feedback.order.rating.get
service: service.ftgo.gateway
derived_from: event.ftgo.rabbitmq.order.rating.get
derived_from_kind: Event
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/feedback.py
  symbol: services.feedback.FeedbackService.get_order_rating
  line_start: 41
  line_end: 41
  evidence_type: implemented
relations:
- type: DERIVED_FROM
  target: event.ftgo.rabbitmq.order.rating.get
  anchor_kind: Event
  role: event_publish
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/feedback.py
  symbol: services.feedback.FeedbackService.get_order_rating
  line_start: 41
  line_end: 41
  evidence_type: implemented
- type: IMPLEMENTS
  target: service.ftgo.gateway
  role: event_publish
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/feedback.py
  symbol: services.feedback.FeedbackService.get_order_rating
  line_start: 41
  line_end: 41
  evidence_type: implemented
inbound_relations:
- type: CONTAINS
  source: flow.ftgo.gateway.get.feedback.order.rating.get
  role: event_publish
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/feedback.py
  symbol: services.feedback.FeedbackService.get_order_rating
  line_start: 41
  line_end: 41
  evidence_type: implemented
- type: PRECEDES
  source: step.ftgo.gateway.get.feedback.order.rating.get.dispatch.services.feedback.feedbackservice.get-order-rating
  established_by: publisher call site
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/feedback.py
  symbol: services.feedback.FeedbackService.get_order_rating
  line_start: 41
  line_end: 41
  evidence_type: implemented
attributes:
  event_identity: order.rating.get
  operation: call
  mechanism: rpc
  broker_library: rabbitmq_rpc
  via_wrapper: services.base.Microservice._call_rpc
  correlation: publisher_only
---

# publish order.rating.get

Canonical execution step extracted from call evidence in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Role: `event_publish`
- Flow: `flow.ftgo.gateway.get.feedback.order.rating.get`
- Performed by: `service.ftgo.gateway`
- Anchored on: `event.ftgo.rabbitmq.order.rating.get` (`Event`)
- Declared in: `backend/gateway/src/services/feedback.py` (lines 41-41)
- Evidence class: `implemented`

## Review notes

This approved canonical page records a source-backed execution step. The step exists because a concrete call site proves it, and its ordering edges carry that call site as evidence.

