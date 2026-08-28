---
id: event.ftgo.rabbitmq.order.history
kind: Event
type: Event
title: order.history
status: approved
review_status: approved
candidate_of: rabbitmq-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: rabbitmq
correlation: publisher_only
publishers:
- service.ftgo.gateway
consumers: []
owner: aide-ftgo-cohort
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/order.py
  symbol: services.order.OrderService.get_order_history
  line_start: 11
  line_end: 11
  evidence_type: implemented
inbound_relations:
- type: PUBLISHES
  source: service.ftgo.gateway
  role: publisher
  operation: call
  broker_library: rabbitmq_rpc
  mechanism: rpc
  call_sites:
  - backend/gateway/src/services/order.py:11
  via_wrapper: services.base.Microservice._call_rpc
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/order.py
  symbol: services.order.OrderService.get_order_history
  line_start: 11
  line_end: 11
  evidence_type: implemented
attributes:
  identity: order.history
  mechanism:
  - rpc
  broker_libraries:
  - rabbitmq_rpc
  operations:
  - call
  identity_sources:
  - literal
  correlation: publisher_only
  publisher_call_sites: 1
  consumer_binding_sites: 0
---

# order.history

Canonical RabbitMQ/RPC interaction extracted from Python source in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Broker identity: `order.history`
- Correlation: `publisher_only`
- Mechanism: `rpc`
- Broker library: `rabbitmq_rpc`
- Declared in: `backend/gateway/src/services/order.py` (lines 11-11)
- Evidence class: `implemented`

## Publishers

- `service.ftgo.gateway` `PUBLISHES` -> `event.ftgo.rabbitmq.order.history`

## Unmatched interaction

A publisher was proven but no consumer binding for this exact identity was found in scanned source. The consumer side is deliberately not invented.

## Review notes

This page was promoted to canonical knowledge after review. Every publisher and consumer above is rooted in a call whose receiver traces statically to a broker library; nothing was inferred from a method or service name.

