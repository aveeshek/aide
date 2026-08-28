---
id: event.ftgo.rabbitmq.user.address.get-address-info
kind: Event
type: Event
title: user.address.get_address_info
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
  - backend/gateway/src/services/user.py:63
  via_wrapper: services.base.Microservice._call_rpc
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/user.py
  symbol: services.user.UserService.get_address_info
  line_start: 63
  line_end: 63
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
  - AddressService.get_address_info
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/user/src/events.py
  symbol: events.register_events
  line_start: 39
  line_end: 39
  evidence_type: implemented
attributes:
  identity: user.address.get_address_info
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
  - AddressService.get_address_info
---

# user.address.get_address_info

Canonical RabbitMQ/RPC interaction extracted from Python source in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Broker identity: `user.address.get_address_info`
- Correlation: `matched`
- Mechanism: `rpc`
- Broker library: `rabbitmq_rpc`
- Declared in: `backend/microservices/user/src/events.py` (lines 39-39)
- Evidence class: `implemented`

## Publishers

- `service.ftgo.gateway` `PUBLISHES` -> `event.ftgo.rabbitmq.user.address.get-address-info`

## Consumers

- `service.ftgo.user` `CONSUMES` -> `event.ftgo.rabbitmq.user.address.get-address-info`

## Review notes

This page was promoted to canonical knowledge after review. Every publisher and consumer above is rooted in a call whose receiver traces statically to a broker library; nothing was inferred from a method or service name.

