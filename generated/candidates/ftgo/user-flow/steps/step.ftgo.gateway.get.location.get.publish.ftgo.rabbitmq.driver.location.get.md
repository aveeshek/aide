---
id: step.ftgo.gateway.get.location.get.publish.ftgo.rabbitmq.driver.location.get
kind: FlowStep
type: FlowStep
title: publish driver.location.get
status: candidate
review_status: pending
candidate_of: user-flow-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: user-flow
owner: aide-ftgo-cohort
role: event_publish
flow: flow.ftgo.gateway.get.location.get
service: service.ftgo.gateway
derived_from: event.ftgo.rabbitmq.driver.location.get
derived_from_kind: Event
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/location.py
  symbol: services.location.LocationService.get_last_location
  line_start: 27
  line_end: 27
  evidence_type: implemented
relations:
- type: DERIVED_FROM
  target: event.ftgo.rabbitmq.driver.location.get
  anchor_kind: Event
  role: event_publish
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/location.py
  symbol: services.location.LocationService.get_last_location
  line_start: 27
  line_end: 27
  evidence_type: implemented
- type: IMPLEMENTS
  target: service.ftgo.gateway
  role: event_publish
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/location.py
  symbol: services.location.LocationService.get_last_location
  line_start: 27
  line_end: 27
  evidence_type: implemented
- type: PRECEDES
  target: step.ftgo.gateway.get.location.get.consume.location.driver.location.get
  established_by: handler registration
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/location/src/events.py
  symbol: events.register_events
  line_start: 29
  line_end: 29
  evidence_type: implemented
inbound_relations:
- type: CONTAINS
  source: flow.ftgo.gateway.get.location.get
  role: event_publish
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/location.py
  symbol: services.location.LocationService.get_last_location
  line_start: 27
  line_end: 27
  evidence_type: implemented
- type: PRECEDES
  source: step.ftgo.gateway.get.location.get.dispatch.services.location.locationservice.get-last-location
  established_by: publisher call site
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/location.py
  symbol: services.location.LocationService.get_last_location
  line_start: 27
  line_end: 27
  evidence_type: implemented
attributes:
  event_identity: driver.location.get
  operation: call
  mechanism: rpc
  broker_library: rabbitmq_rpc
  via_wrapper: services.base.Microservice._call_rpc
  correlation: matched
---

# publish driver.location.get

Candidate execution step extracted from call evidence in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Role: `event_publish`
- Flow: `flow.ftgo.gateway.get.location.get`
- Performed by: `service.ftgo.gateway`
- Anchored on: `event.ftgo.rabbitmq.driver.location.get` (`Event`)
- Declared in: `backend/gateway/src/services/location.py` (lines 27-27)
- Evidence class: `implemented`

## Review notes

This page is a candidate awaiting review. The step exists because a concrete call site proves it, and its ordering edges carry that call site as evidence.

