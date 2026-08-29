---
id: step.ftgo.gateway.get.feedback.order.rating.customer.read.ftgo.feedback.order-ratings
kind: FlowStep
type: FlowStep
title: read collection.ftgo.feedback.order-ratings
status: candidate
review_status: pending
candidate_of: user-flow-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: user-flow
owner: aide-ftgo-cohort
role: persistence_read
flow: flow.ftgo.gateway.get.feedback.order.rating.customer
service: service.ftgo.feedback
derived_from: collection.ftgo.feedback.order-ratings
derived_from_kind: Collection
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/feedback/src/domain/order_rating.py
  symbol: domain.order_rating.OrderRatingHandler.get_customer_order_ratings
  line_start: 57
  line_end: 57
  evidence_type: implemented
traces:
- target: domain.order_rating.OrderRatingHandler.get_customer_order_ratings
  depth: 1
  hops:
  - caller: application.order.OrderRatingService.get_customer_order_ratings
    callee: domain.order_rating.OrderRatingHandler.get_customer_order_ratings
    call: OrderRatingHandler.get_customer_order_ratings
    repository: ftgo
    commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
    path: backend/microservices/feedback/src/application/order.py
    symbol: application.order.OrderRatingService.get_customer_order_ratings
    line_start: 43
    line_end: 43
    evidence_type: implemented
relations:
- type: DERIVED_FROM
  target: collection.ftgo.feedback.order-ratings
  anchor_kind: Collection
  role: persistence_read
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/feedback/src/domain/order_rating.py
  symbol: domain.order_rating.OrderRatingHandler.get_customer_order_ratings
  line_start: 57
  line_end: 57
  evidence_type: implemented
- type: IMPLEMENTS
  target: service.ftgo.feedback
  role: persistence_read
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/feedback/src/domain/order_rating.py
  symbol: domain.order_rating.OrderRatingHandler.get_customer_order_ratings
  line_start: 57
  line_end: 57
  evidence_type: implemented
inbound_relations:
- type: CONTAINS
  source: flow.ftgo.gateway.get.feedback.order.rating.customer
  role: persistence_read
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/feedback/src/domain/order_rating.py
  symbol: domain.order_rating.OrderRatingHandler.get_customer_order_ratings
  line_start: 57
  line_end: 57
  evidence_type: implemented
- type: PRECEDES
  source: step.ftgo.gateway.get.feedback.order.rating.customer.consume.feedback.order.rating.get-customer-ratings
  established_by: consumer call trace
  call_depth: 1
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/feedback/src/domain/order_rating.py
  symbol: domain.order_rating.OrderRatingHandler.get_customer_order_ratings
  line_start: 57
  line_end: 57
  evidence_type: implemented
attributes:
  operation: find_all
  persistence_library: beanie
  resolution: direct_model_reference
  call_depth: 1
  event_identity: order.rating.get_customer_ratings
---

# read collection.ftgo.feedback.order-ratings

Candidate execution step extracted from call evidence in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Role: `persistence_read`
- Flow: `flow.ftgo.gateway.get.feedback.order.rating.customer`
- Performed by: `service.ftgo.feedback`
- Anchored on: `collection.ftgo.feedback.order-ratings` (`Collection`)
- Declared in: `backend/microservices/feedback/src/domain/order_rating.py` (lines 57-57)
- Evidence class: `implemented`

## Call trace

- `application.order.OrderRatingService.get_customer_order_ratings` -> `domain.order_rating.OrderRatingHandler.get_customer_order_ratings` (`backend/microservices/feedback/src/application/order.py:43`)

## Review notes

This page is a candidate awaiting review. The step exists because a concrete call site proves it, and its ordering edges carry that call site as evidence.

