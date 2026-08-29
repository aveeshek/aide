---
id: step.ftgo.gateway.get.address.get-all-info.publish.ftgo.rabbitmq.user.address.get-all-addresses
kind: FlowStep
type: FlowStep
title: publish user.address.get_all_addresses
status: approved
review_status: approved
candidate_of: user-flow-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: user-flow
owner: aide-ftgo-cohort
role: event_publish
flow: flow.ftgo.gateway.get.address.get-all-info
service: service.ftgo.gateway
derived_from: event.ftgo.rabbitmq.user.address.get-all-addresses
derived_from_kind: Event
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/user.py
  symbol: services.user.UserService.get_all_addresses
  line_start: 67
  line_end: 67
  evidence_type: implemented
relations:
- type: DERIVED_FROM
  target: event.ftgo.rabbitmq.user.address.get-all-addresses
  anchor_kind: Event
  role: event_publish
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/user.py
  symbol: services.user.UserService.get_all_addresses
  line_start: 67
  line_end: 67
  evidence_type: implemented
- type: IMPLEMENTS
  target: service.ftgo.gateway
  role: event_publish
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/user.py
  symbol: services.user.UserService.get_all_addresses
  line_start: 67
  line_end: 67
  evidence_type: implemented
- type: PRECEDES
  target: step.ftgo.gateway.get.address.get-all-info.consume.user.user.address.get-all-addresses
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
  source: flow.ftgo.gateway.get.address.get-all-info
  role: event_publish
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/user.py
  symbol: services.user.UserService.get_all_addresses
  line_start: 67
  line_end: 67
  evidence_type: implemented
- type: PRECEDES
  source: step.ftgo.gateway.get.address.get-all-info.dispatch.services.user.userservice.get-all-addresses
  established_by: publisher call site
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/user.py
  symbol: services.user.UserService.get_all_addresses
  line_start: 67
  line_end: 67
  evidence_type: implemented
attributes:
  event_identity: user.address.get_all_addresses
  operation: call
  mechanism: rpc
  broker_library: rabbitmq_rpc
  via_wrapper: services.base.Microservice._call_rpc
  correlation: matched
---

# publish user.address.get_all_addresses

Canonical execution step extracted from call evidence in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Role: `event_publish`
- Flow: `flow.ftgo.gateway.get.address.get-all-info`
- Performed by: `service.ftgo.gateway`
- Anchored on: `event.ftgo.rabbitmq.user.address.get-all-addresses` (`Event`)
- Declared in: `backend/gateway/src/services/user.py` (lines 67-67)
- Evidence class: `implemented`

## Review notes

This approved canonical page records a source-backed execution step. The step exists because a concrete call site proves it, and its ordering edges carry that call site as evidence.

