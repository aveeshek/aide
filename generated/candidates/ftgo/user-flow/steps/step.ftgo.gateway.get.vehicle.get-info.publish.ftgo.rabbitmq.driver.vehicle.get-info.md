---
id: step.ftgo.gateway.get.vehicle.get-info.publish.ftgo.rabbitmq.driver.vehicle.get-info
kind: FlowStep
type: FlowStep
title: publish driver.vehicle.get_info
status: candidate
review_status: pending
candidate_of: user-flow-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: user-flow
owner: aide-ftgo-cohort
role: event_publish
flow: flow.ftgo.gateway.get.vehicle.get-info
service: service.ftgo.gateway
derived_from: event.ftgo.rabbitmq.driver.vehicle.get-info
derived_from_kind: Event
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/vehicle.py
  symbol: services.vehicle.VehicleService.get_info
  line_start: 15
  line_end: 15
  evidence_type: implemented
relations:
- type: DERIVED_FROM
  target: event.ftgo.rabbitmq.driver.vehicle.get-info
  anchor_kind: Event
  role: event_publish
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/vehicle.py
  symbol: services.vehicle.VehicleService.get_info
  line_start: 15
  line_end: 15
  evidence_type: implemented
- type: IMPLEMENTS
  target: service.ftgo.gateway
  role: event_publish
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/vehicle.py
  symbol: services.vehicle.VehicleService.get_info
  line_start: 15
  line_end: 15
  evidence_type: implemented
- type: PRECEDES
  target: step.ftgo.gateway.get.vehicle.get-info.consume.user.driver.vehicle.get-info
  established_by: handler registration
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/user/src/events.py
  symbol: events.register_events
  line_start: 39
  line_end: 39
  evidence_type: implemented
inbound_relations:
- type: CONTAINS
  source: flow.ftgo.gateway.get.vehicle.get-info
  role: event_publish
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/vehicle.py
  symbol: services.vehicle.VehicleService.get_info
  line_start: 15
  line_end: 15
  evidence_type: implemented
- type: PRECEDES
  source: step.ftgo.gateway.get.vehicle.get-info.dispatch.services.vehicle.vehicleservice.get-info
  established_by: publisher call site
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/vehicle.py
  symbol: services.vehicle.VehicleService.get_info
  line_start: 15
  line_end: 15
  evidence_type: implemented
attributes:
  event_identity: driver.vehicle.get_info
  operation: call
  mechanism: rpc
  broker_library: rabbitmq_rpc
  via_wrapper: services.base.Microservice._call_rpc
  correlation: matched
---

# publish driver.vehicle.get_info

Candidate execution step extracted from call evidence in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Role: `event_publish`
- Flow: `flow.ftgo.gateway.get.vehicle.get-info`
- Performed by: `service.ftgo.gateway`
- Anchored on: `event.ftgo.rabbitmq.driver.vehicle.get-info` (`Event`)
- Declared in: `backend/gateway/src/services/vehicle.py` (lines 15-15)
- Evidence class: `implemented`

## Review notes

This page is a candidate awaiting review. The step exists because a concrete call site proves it, and its ordering edges carry that call site as evidence.

