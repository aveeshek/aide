---
id: event.ftgo.rabbitmq.order.rating.get-customer-ratings
kind: Event
type: Event
title: order.rating.get_customer_ratings
status: candidate
review_status: pending
candidate_of: rabbitmq-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: rabbitmq
correlation: matched
publishers:
- service.ftgo.gateway
consumers:
- service.ftgo.feedback
owner: aide-ftgo-cohort
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/feedback/src/events.py
  symbol: events.register_events
  line_start: 37
  line_end: 37
  evidence_type: implemented
inbound_relations:
- type: CONSUMES
  source: service.ftgo.feedback
  role: consumer
  operation: register_event
  broker_library: rabbitmq_rpc
  mechanism: rpc
  call_sites:
  - backend/microservices/feedback/src/events.py:37
  handlers:
  - OrderRatingService.get_customer_order_ratings
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/feedback/src/events.py
  symbol: events.register_events
  line_start: 37
  line_end: 37
  evidence_type: implemented
- type: PUBLISHES
  source: service.ftgo.gateway
  role: publisher
  operation: call
  broker_library: rabbitmq_rpc
  mechanism: rpc
  call_sites:
  - backend/gateway/src/services/feedback.py:45
  via_wrapper: services.base.Microservice._call_rpc
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/feedback.py
  symbol: services.feedback.FeedbackService.get_customer_order_ratings
  line_start: 45
  line_end: 45
  evidence_type: implemented
attributes:
  identity: order.rating.get_customer_ratings
  mechanism:
  - rpc
  broker_libraries:
  - rabbitmq_rpc
  operations:
  - call
  - register_event
  identity_sources:
  - iteration
  - literal
  correlation: matched
  publisher_call_sites: 1
  consumer_binding_sites: 1
  handlers:
  - OrderRatingService.get_customer_order_ratings
---

# order.rating.get_customer_ratings

Candidate RabbitMQ/RPC interaction extracted from Python source in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Broker identity: `order.rating.get_customer_ratings`
- Correlation: `matched`
- Mechanism: `rpc`
- Broker library: `rabbitmq_rpc`
- Declared in: `backend/microservices/feedback/src/events.py` (lines 37-37)
- Evidence class: `implemented`

## Publishers

- `service.ftgo.gateway` `PUBLISHES` -> `event.ftgo.rabbitmq.order.rating.get-customer-ratings`

## Consumers

- `service.ftgo.feedback` `CONSUMES` -> `event.ftgo.rabbitmq.order.rating.get-customer-ratings`

## Review notes

This page is a candidate awaiting review. Every publisher and consumer above is rooted in a call whose receiver traces statically to a broker library; nothing was inferred from a method or service name.

