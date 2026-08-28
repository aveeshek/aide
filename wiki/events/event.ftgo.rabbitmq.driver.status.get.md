---
id: event.ftgo.rabbitmq.driver.status.get
kind: Event
type: Event
title: driver.status.get
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
- service.ftgo.location
owner: aide-ftgo-cohort
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/location/src/events.py
  symbol: events.register_events
  line_start: 29
  line_end: 29
  evidence_type: implemented
inbound_relations:
- type: PUBLISHES
  source: service.ftgo.gateway
  role: publisher
  operation: call
  broker_library: rabbitmq_rpc
  mechanism: rpc
  call_sites:
  - backend/gateway/src/services/location.py:31
  via_wrapper: services.base.Microservice._call_rpc
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/location.py
  symbol: services.location.LocationService.get_driver_status
  line_start: 31
  line_end: 31
  evidence_type: implemented
- type: CONSUMES
  source: service.ftgo.location
  role: consumer
  operation: register_event
  broker_library: rabbitmq_rpc
  mechanism: rpc
  call_sites:
  - backend/microservices/location/src/events.py:29
  handlers:
  - DriverService.get_driver_status
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/location/src/events.py
  symbol: events.register_events
  line_start: 29
  line_end: 29
  evidence_type: implemented
attributes:
  identity: driver.status.get
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
  - DriverService.get_driver_status
---

# driver.status.get

Canonical RabbitMQ/RPC interaction extracted from Python source in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Broker identity: `driver.status.get`
- Correlation: `matched`
- Mechanism: `rpc`
- Broker library: `rabbitmq_rpc`
- Declared in: `backend/microservices/location/src/events.py` (lines 29-29)
- Evidence class: `implemented`

## Publishers

- `service.ftgo.gateway` `PUBLISHES` -> `event.ftgo.rabbitmq.driver.status.get`

## Consumers

- `service.ftgo.location` `CONSUMES` -> `event.ftgo.rabbitmq.driver.status.get`

## Review notes

This page was promoted to canonical knowledge after review. Every publisher and consumer above is rooted in a call whose receiver traces statically to a broker library; nothing was inferred from a method or service name.

