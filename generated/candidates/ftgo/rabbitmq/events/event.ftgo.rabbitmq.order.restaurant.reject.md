---
id: event.ftgo.rabbitmq.order.restaurant.reject
kind: Event
type: Event
title: order.restaurant.reject
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
- service.ftgo.order
owner: aide-ftgo-cohort
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/order/src/events.py
  symbol: events.register_events
  line_start: 45
  line_end: 45
  evidence_type: implemented
inbound_relations:
- type: PUBLISHES
  source: service.ftgo.gateway
  role: publisher
  operation: call
  broker_library: rabbitmq_rpc
  mechanism: rpc
  call_sites:
  - backend/gateway/src/services/order.py:27
  via_wrapper: services.base.Microservice._call_rpc
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/order.py
  symbol: services.order.OrderService.restaurant_reject
  line_start: 27
  line_end: 27
  evidence_type: implemented
- type: CONSUMES
  source: service.ftgo.order
  role: consumer
  operation: register_event
  broker_library: rabbitmq_rpc
  mechanism: rpc
  call_sites:
  - backend/microservices/order/src/events.py:45
  handlers:
  - RestaurantService.reject_order
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/order/src/events.py
  symbol: events.register_events
  line_start: 45
  line_end: 45
  evidence_type: implemented
attributes:
  identity: order.restaurant.reject
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
  - RestaurantService.reject_order
---

# order.restaurant.reject

Candidate RabbitMQ/RPC interaction extracted from Python source in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Broker identity: `order.restaurant.reject`
- Correlation: `matched`
- Mechanism: `rpc`
- Broker library: `rabbitmq_rpc`
- Declared in: `backend/microservices/order/src/events.py` (lines 45-45)
- Evidence class: `implemented`

## Publishers

- `service.ftgo.gateway` `PUBLISHES` -> `event.ftgo.rabbitmq.order.restaurant.reject`

## Consumers

- `service.ftgo.order` `CONSUMES` -> `event.ftgo.rabbitmq.order.restaurant.reject`

## Review notes

This page is a candidate awaiting review. Every publisher and consumer above is rooted in a call whose receiver traces statically to a broker library; nothing was inferred from a method or service name.

