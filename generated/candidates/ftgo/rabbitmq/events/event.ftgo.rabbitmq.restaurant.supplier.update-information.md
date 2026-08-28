---
id: event.ftgo.rabbitmq.restaurant.supplier.update-information
kind: Event
type: Event
title: restaurant.supplier.update_information
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
- service.ftgo.restaurant
owner: aide-ftgo-cohort
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/restaurant/src/events.py
  symbol: events.register_events
  line_start: 32
  line_end: 32
  evidence_type: implemented
inbound_relations:
- type: PUBLISHES
  source: service.ftgo.gateway
  role: publisher
  operation: call
  broker_library: rabbitmq_rpc
  mechanism: rpc
  call_sites:
  - backend/gateway/src/services/restaurant.py:27
  via_wrapper: services.base.Microservice._call_rpc
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/restaurant.py
  symbol: services.restaurant.RestaurantService.update_information
  line_start: 27
  line_end: 27
  evidence_type: implemented
- type: CONSUMES
  source: service.ftgo.restaurant
  role: consumer
  operation: register_event
  broker_library: rabbitmq_rpc
  mechanism: rpc
  call_sites:
  - backend/microservices/restaurant/src/events.py:32
  handlers:
  - RestaurantService.update_information
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/restaurant/src/events.py
  symbol: events.register_events
  line_start: 32
  line_end: 32
  evidence_type: implemented
attributes:
  identity: restaurant.supplier.update_information
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
  - RestaurantService.update_information
---

# restaurant.supplier.update_information

Candidate RabbitMQ/RPC interaction extracted from Python source in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Broker identity: `restaurant.supplier.update_information`
- Correlation: `matched`
- Mechanism: `rpc`
- Broker library: `rabbitmq_rpc`
- Declared in: `backend/microservices/restaurant/src/events.py` (lines 32-32)
- Evidence class: `implemented`

## Publishers

- `service.ftgo.gateway` `PUBLISHES` -> `event.ftgo.rabbitmq.restaurant.supplier.update-information`

## Consumers

- `service.ftgo.restaurant` `CONSUMES` -> `event.ftgo.rabbitmq.restaurant.supplier.update-information`

## Review notes

This page is a candidate awaiting review. Every publisher and consumer above is rooted in a call whose receiver traces statically to a broker library; nothing was inferred from a method or service name.

