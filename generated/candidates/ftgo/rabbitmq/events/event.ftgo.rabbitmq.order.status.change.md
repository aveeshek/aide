---
id: event.ftgo.rabbitmq.order.status.change
kind: Event
type: Event
title: order.status.change
status: candidate
review_status: pending
candidate_of: rabbitmq-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: rabbitmq
correlation: consumer_only
publishers: []
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
- type: CONSUMES
  source: service.ftgo.order
  role: consumer
  operation: register_event
  broker_library: rabbitmq_rpc
  mechanism: rpc
  call_sites:
  - backend/microservices/order/src/events.py:45
  handlers:
  - OrderStatusService.change_order_status
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/order/src/events.py
  symbol: events.register_events
  line_start: 45
  line_end: 45
  evidence_type: implemented
attributes:
  identity: order.status.change
  mechanism:
  - rpc
  broker_libraries:
  - rabbitmq_rpc
  operations:
  - register_event
  identity_sources:
  - iteration
  correlation: consumer_only
  publisher_call_sites: 0
  consumer_binding_sites: 1
  handlers:
  - OrderStatusService.change_order_status
---

# order.status.change

Candidate RabbitMQ/RPC interaction extracted from Python source in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Broker identity: `order.status.change`
- Correlation: `consumer_only`
- Mechanism: `rpc`
- Broker library: `rabbitmq_rpc`
- Declared in: `backend/microservices/order/src/events.py` (lines 45-45)
- Evidence class: `implemented`

## Consumers

- `service.ftgo.order` `CONSUMES` -> `event.ftgo.rabbitmq.order.status.change`

## Unmatched interaction

A consumer binding was proven but no publisher call for this exact identity was found in scanned source. The publisher side is deliberately not invented.

## Review notes

This page is a candidate awaiting review. Every publisher and consumer above is rooted in a call whose receiver traces statically to a broker library; nothing was inferred from a method or service name.

