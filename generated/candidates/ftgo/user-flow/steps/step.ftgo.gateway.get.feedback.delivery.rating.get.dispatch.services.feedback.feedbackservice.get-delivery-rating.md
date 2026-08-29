---
id: step.ftgo.gateway.get.feedback.delivery.rating.get.dispatch.services.feedback.feedbackservice.get-delivery-rating
kind: FlowStep
type: FlowStep
title: services.feedback.FeedbackService.get_delivery_rating dispatch
status: candidate
review_status: pending
candidate_of: user-flow-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: user-flow
owner: aide-ftgo-cohort
role: service_dispatch
flow: flow.ftgo.gateway.get.feedback.delivery.rating.get
service: service.ftgo.gateway
derived_from: endpoint.ftgo.gateway.get.feedback.delivery.rating.get
derived_from_kind: Endpoint
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/order/feedback.py
  symbol: application.routes.order.feedback.get_delivery_rating
  line_start: 75
  line_end: 75
  evidence_type: implemented
traces:
- target: services.feedback.FeedbackService.get_delivery_rating
  depth: 1
  hops:
  - caller: application.routes.order.feedback.get_delivery_rating
    callee: services.feedback.FeedbackService.get_delivery_rating
    call: FeedbackService.get_delivery_rating
    repository: ftgo
    commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
    path: backend/gateway/src/application/routes/order/feedback.py
    symbol: application.routes.order.feedback.get_delivery_rating
    line_start: 75
    line_end: 75
    evidence_type: implemented
relations:
- type: DERIVED_FROM
  target: endpoint.ftgo.gateway.get.feedback.delivery.rating.get
  anchor_kind: Endpoint
  role: service_dispatch
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/order/feedback.py
  symbol: application.routes.order.feedback.get_delivery_rating
  line_start: 75
  line_end: 75
  evidence_type: implemented
- type: IMPLEMENTS
  target: service.ftgo.gateway
  role: service_dispatch
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/order/feedback.py
  symbol: application.routes.order.feedback.get_delivery_rating
  line_start: 75
  line_end: 75
  evidence_type: implemented
- type: PRECEDES
  target: step.ftgo.gateway.get.feedback.delivery.rating.get.publish.ftgo.rabbitmq.delivery.rating.get
  established_by: publisher call site
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/feedback.py
  symbol: services.feedback.FeedbackService.get_delivery_rating
  line_start: 20
  line_end: 20
  evidence_type: implemented
inbound_relations:
- type: CONTAINS
  source: flow.ftgo.gateway.get.feedback.delivery.rating.get
  role: service_dispatch
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/order/feedback.py
  symbol: application.routes.order.feedback.get_delivery_rating
  line_start: 75
  line_end: 75
  evidence_type: implemented
- type: PRECEDES
  source: step.ftgo.gateway.get.feedback.delivery.rating.get.http-ingress
  established_by: handler call site
  call_depth: 1
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/order/feedback.py
  symbol: application.routes.order.feedback.get_delivery_rating
  line_start: 75
  line_end: 75
  evidence_type: implemented
attributes:
  gateway_symbol: services.feedback.FeedbackService.get_delivery_rating
  call_depth: 1
---

# services.feedback.FeedbackService.get_delivery_rating dispatch

Candidate execution step extracted from call evidence in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Role: `service_dispatch`
- Flow: `flow.ftgo.gateway.get.feedback.delivery.rating.get`
- Performed by: `service.ftgo.gateway`
- Anchored on: `endpoint.ftgo.gateway.get.feedback.delivery.rating.get` (`Endpoint`)
- Declared in: `backend/gateway/src/application/routes/order/feedback.py` (lines 75-75)
- Evidence class: `implemented`

## Call trace

- `application.routes.order.feedback.get_delivery_rating` -> `services.feedback.FeedbackService.get_delivery_rating` (`backend/gateway/src/application/routes/order/feedback.py:75`)

## Review notes

This page is a candidate awaiting review. The step exists because a concrete call site proves it, and its ordering edges carry that call site as evidence.

