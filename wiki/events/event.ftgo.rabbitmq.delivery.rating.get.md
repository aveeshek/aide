---
id: event.ftgo.rabbitmq.delivery.rating.get
kind: Event
type: Event
title: delivery.rating.get
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
  path: backend/gateway/src/services/feedback.py
  symbol: services.feedback.FeedbackService.get_delivery_rating
  line_start: 20
  line_end: 20
  evidence_type: implemented
inbound_relations:
- type: PUBLISHES
  source: service.ftgo.gateway
  role: publisher
  operation: call
  broker_library: rabbitmq_rpc
  mechanism: rpc
  call_sites:
  - backend/gateway/src/services/feedback.py:20
  via_wrapper: services.base.Microservice._call_rpc
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/feedback.py
  symbol: services.feedback.FeedbackService.get_delivery_rating
  line_start: 20
  line_end: 20
  evidence_type: implemented
attributes:
  identity: delivery.rating.get
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

# delivery.rating.get

Canonical RabbitMQ/RPC interaction extracted from Python source in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Broker identity: `delivery.rating.get`
- Correlation: `publisher_only`
- Mechanism: `rpc`
- Broker library: `rabbitmq_rpc`
- Declared in: `backend/gateway/src/services/feedback.py` (lines 20-20)
- Evidence class: `implemented`

## Publishers

- `service.ftgo.gateway` `PUBLISHES` -> `event.ftgo.rabbitmq.delivery.rating.get`

## Unmatched interaction

A publisher was proven but no consumer binding for this exact identity was found in scanned source. The consumer side is deliberately not invented.

## Review notes

This page was promoted to canonical knowledge after review. Every publisher and consumer above is rooted in a call whose receiver traces statically to a broker library; nothing was inferred from a method or service name.

