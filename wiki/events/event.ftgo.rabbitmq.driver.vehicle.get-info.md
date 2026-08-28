---
id: event.ftgo.rabbitmq.driver.vehicle.get-info
kind: Event
type: Event
title: driver.vehicle.get_info
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
  - backend/gateway/src/services/user.py:75
  - backend/gateway/src/services/vehicle.py:15
  via_wrapper: services.base.Microservice._call_rpc
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/user.py
  symbol: services.user.UserService.get_vehicle_info
  line_start: 75
  line_end: 75
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
  - VehicleService.get_vehicle_info
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/user/src/events.py
  symbol: events.register_events
  line_start: 39
  line_end: 39
  evidence_type: implemented
attributes:
  identity: driver.vehicle.get_info
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
  publisher_call_sites: 2
  consumer_binding_sites: 1
  handlers:
  - VehicleService.get_vehicle_info
---

# driver.vehicle.get_info

Canonical RabbitMQ/RPC interaction extracted from Python source in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Broker identity: `driver.vehicle.get_info`
- Correlation: `matched`
- Mechanism: `rpc`
- Broker library: `rabbitmq_rpc`
- Declared in: `backend/microservices/user/src/events.py` (lines 39-39)
- Evidence class: `implemented`

## Publishers

- `service.ftgo.gateway` `PUBLISHES` -> `event.ftgo.rabbitmq.driver.vehicle.get-info`

## Consumers

- `service.ftgo.user` `CONSUMES` -> `event.ftgo.rabbitmq.driver.vehicle.get-info`

## Review notes

This page was promoted to canonical knowledge after review. Every publisher and consumer above is rooted in a call whose receiver traces statically to a broker library; nothing was inferred from a method or service name.

