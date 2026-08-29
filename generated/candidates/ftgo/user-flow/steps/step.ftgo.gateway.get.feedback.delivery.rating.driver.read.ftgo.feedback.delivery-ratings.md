---
id: step.ftgo.gateway.get.feedback.delivery.rating.driver.read.ftgo.feedback.delivery-ratings
kind: FlowStep
type: FlowStep
title: read collection.ftgo.feedback.delivery-ratings
status: candidate
review_status: pending
candidate_of: user-flow-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: user-flow
owner: aide-ftgo-cohort
role: persistence_read
flow: flow.ftgo.gateway.get.feedback.delivery.rating.driver
service: service.ftgo.feedback
derived_from: collection.ftgo.feedback.delivery-ratings
derived_from_kind: Collection
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/feedback/src/domain/delivery_rating.py
  symbol: domain.delivery_rating.DeliveryRatingHandler.get_driver_delivery_ratings
  line_start: 61
  line_end: 61
  evidence_type: implemented
traces:
- target: domain.delivery_rating.DeliveryRatingHandler.get_driver_delivery_ratings
  depth: 1
  hops:
  - caller: application.delivery.DeliveryRatingService.get_driver_delivery_ratings
    callee: domain.delivery_rating.DeliveryRatingHandler.get_driver_delivery_ratings
    call: DeliveryRatingHandler.get_driver_delivery_ratings
    repository: ftgo
    commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
    path: backend/microservices/feedback/src/application/delivery.py
    symbol: application.delivery.DeliveryRatingService.get_driver_delivery_ratings
    line_start: 53
    line_end: 53
    evidence_type: implemented
relations:
- type: DERIVED_FROM
  target: collection.ftgo.feedback.delivery-ratings
  anchor_kind: Collection
  role: persistence_read
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/feedback/src/domain/delivery_rating.py
  symbol: domain.delivery_rating.DeliveryRatingHandler.get_driver_delivery_ratings
  line_start: 61
  line_end: 61
  evidence_type: implemented
- type: IMPLEMENTS
  target: service.ftgo.feedback
  role: persistence_read
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/feedback/src/domain/delivery_rating.py
  symbol: domain.delivery_rating.DeliveryRatingHandler.get_driver_delivery_ratings
  line_start: 61
  line_end: 61
  evidence_type: implemented
inbound_relations:
- type: CONTAINS
  source: flow.ftgo.gateway.get.feedback.delivery.rating.driver
  role: persistence_read
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/feedback/src/domain/delivery_rating.py
  symbol: domain.delivery_rating.DeliveryRatingHandler.get_driver_delivery_ratings
  line_start: 61
  line_end: 61
  evidence_type: implemented
- type: PRECEDES
  source: step.ftgo.gateway.get.feedback.delivery.rating.driver.consume.feedback.delivery.rating.get-driver-ratings
  established_by: consumer call trace
  call_depth: 1
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/feedback/src/domain/delivery_rating.py
  symbol: domain.delivery_rating.DeliveryRatingHandler.get_driver_delivery_ratings
  line_start: 61
  line_end: 61
  evidence_type: implemented
attributes:
  operation: find_all
  persistence_library: beanie
  resolution: direct_model_reference
  call_depth: 1
  event_identity: delivery.rating.get_driver_ratings
---

# read collection.ftgo.feedback.delivery-ratings

Candidate execution step extracted from call evidence in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Role: `persistence_read`
- Flow: `flow.ftgo.gateway.get.feedback.delivery.rating.driver`
- Performed by: `service.ftgo.feedback`
- Anchored on: `collection.ftgo.feedback.delivery-ratings` (`Collection`)
- Declared in: `backend/microservices/feedback/src/domain/delivery_rating.py` (lines 61-61)
- Evidence class: `implemented`

## Call trace

- `application.delivery.DeliveryRatingService.get_driver_delivery_ratings` -> `domain.delivery_rating.DeliveryRatingHandler.get_driver_delivery_ratings` (`backend/microservices/feedback/src/application/delivery.py:53`)

## Review notes

This page is a candidate awaiting review. The step exists because a concrete call site proves it, and its ordering edges carry that call site as evidence.

