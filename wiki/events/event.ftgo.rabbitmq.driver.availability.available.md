---
id: event.ftgo.rabbitmq.driver.availability.available
kind: Event
type: Event
title: driver.availability.available
status: approved
review_status: approved
candidate_of: rabbitmq-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: rabbitmq
correlation: consumer_only
publishers: []
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
- type: CONSUMES
  source: service.ftgo.location
  role: consumer
  operation: register_event
  broker_library: rabbitmq_rpc
  mechanism: rpc
  call_sites:
  - backend/microservices/location/src/events.py:29
  handlers:
  - DriverService.set_driver_available
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/location/src/events.py
  symbol: events.register_events
  line_start: 29
  line_end: 29
  evidence_type: implemented
attributes:
  identity: driver.availability.available
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
  - DriverService.set_driver_available
---

# driver.availability.available

Canonical RabbitMQ/RPC interaction extracted from Python source in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Broker identity: `driver.availability.available`
- Correlation: `consumer_only`
- Mechanism: `rpc`
- Broker library: `rabbitmq_rpc`
- Declared in: `backend/microservices/location/src/events.py` (lines 29-29)
- Evidence class: `implemented`

## Consumers

- `service.ftgo.location` `CONSUMES` -> `event.ftgo.rabbitmq.driver.availability.available`

## Unmatched interaction

A consumer binding was proven but no publisher call for this exact identity was found in scanned source. The publisher side is deliberately not invented.

## Review notes

This page was promoted to canonical knowledge after review. Every publisher and consumer above is rooted in a call whose receiver traces statically to a broker library; nothing was inferred from a method or service name.

