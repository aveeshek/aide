---
id: event.ftgo.rabbitmq.user.address.get-default-address
kind: Event
type: Event
title: user.address.get_default_address
status: approved
review_status: approved
candidate_of: rabbitmq-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: rabbitmq
correlation: matched
publishers:
- service.ftgo.gateway
consumers:
- service.ftgo.user
owner: aide-ftgo-cohort
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/user/src/events.py
  symbol: events.register_events
  line_start: 39
  line_end: 39
  evidence_type: implemented
inbound_relations:
- type: PUBLISHES
  source: service.ftgo.gateway
  role: publisher
  operation: call
  broker_library: rabbitmq_rpc
  mechanism: rpc
  call_sites:
  - backend/gateway/src/services/user.py:51
  via_wrapper: services.base.Microservice._call_rpc
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/user.py
  symbol: services.user.UserService.get_default_address
  line_start: 51
  line_end: 51
  evidence_type: implemented
- type: CONSUMES
  source: service.ftgo.user
  role: consumer
  operation: register_event
  broker_library: rabbitmq_rpc
  mechanism: rpc
  call_sites:
  - backend/microservices/user/src/events.py:39
  handlers:
  - AddressService.get_default_address
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/user/src/events.py
  symbol: events.register_events
  line_start: 39
  line_end: 39
  evidence_type: implemented
attributes:
  identity: user.address.get_default_address
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
  - AddressService.get_default_address
---

# user.address.get_default_address

Canonical RabbitMQ/RPC interaction extracted from Python source in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Broker identity: `user.address.get_default_address`
- Correlation: `matched`
- Mechanism: `rpc`
- Broker library: `rabbitmq_rpc`
- Declared in: `backend/microservices/user/src/events.py` (lines 39-39)
- Evidence class: `implemented`

## Publishers

- `service.ftgo.gateway` `PUBLISHES` -> `event.ftgo.rabbitmq.user.address.get-default-address`

## Consumers

- `service.ftgo.user` `CONSUMES` -> `event.ftgo.rabbitmq.user.address.get-default-address`

## Review notes

This page was promoted to canonical knowledge after review. Every publisher and consumer above is rooted in a call whose receiver traces statically to a broker library; nothing was inferred from a method or service name.

