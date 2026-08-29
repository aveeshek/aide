---
id: flow.ftgo.gateway.get.status.get
kind: UserFlow
type: UserFlow
title: GET /status/get execution flow
status: approved
review_status: approved
candidate_of: user-flow-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: user-flow
owner: aide-ftgo-cohort
entry_endpoint: endpoint.ftgo.gateway.get.status.get
http_method: GET
path: /status/get
path_resolution: partial
completeness: partial
handler: application.routes.driver.online_status.get_status
participating_services:
- service.ftgo.gateway
- service.ftgo.location
events:
- event.ftgo.rabbitmq.driver.status.get
persistence_targets: []
unresolved_segments:
- persistence:driver.status.get
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/driver/online_status.py
  symbol: application.routes.driver.online_status.get_status
  line_start: 50
  line_end: 66
  evidence_type: implemented
relations:
- type: CONTAINS
  target: step.ftgo.gateway.get.status.get.consume.location.driver.status.get
  role: event_consume
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/location/src/events.py
  symbol: events.register_events
  line_start: 29
  line_end: 29
  evidence_type: implemented
- type: CONTAINS
  target: step.ftgo.gateway.get.status.get.dispatch.services.location.locationservice.get-driver-status
  role: service_dispatch
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/driver/online_status.py
  symbol: application.routes.driver.online_status.get_status
  line_start: 54
  line_end: 54
  evidence_type: implemented
- type: CONTAINS
  target: step.ftgo.gateway.get.status.get.http-ingress
  role: http_ingress
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/driver/online_status.py
  symbol: application.routes.driver.online_status.get_status
  line_start: 50
  line_end: 66
  evidence_type: implemented
- type: CONTAINS
  target: step.ftgo.gateway.get.status.get.publish.ftgo.rabbitmq.driver.status.get
  role: event_publish
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/location.py
  symbol: services.location.LocationService.get_driver_status
  line_start: 31
  line_end: 31
  evidence_type: implemented
inbound_relations:
- type: PARTICIPATES_IN
  source: service.ftgo.gateway
  completeness: partial
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/driver/online_status.py
  symbol: application.routes.driver.online_status.get_status
  line_start: 50
  line_end: 66
  evidence_type: implemented
- type: PARTICIPATES_IN
  source: service.ftgo.location
  completeness: partial
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/driver/online_status.py
  symbol: application.routes.driver.online_status.get_status
  line_start: 50
  line_end: 66
  evidence_type: implemented
attributes:
  step_count: 4
  classification_reason: publish and consume are proven but a later segment is unresolved
  max_call_depth: 3
---

# GET /status/get execution flow

Canonical execution flow stitched from source-backed call evidence in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Entry endpoint: `endpoint.ftgo.gateway.get.status.get`
- Completeness: `partial`
- Handler: `application.routes.driver.online_status.get_status`
- Declared in: `backend/gateway/src/application/routes/driver/online_status.py` (lines 50-66)
- Evidence class: `implemented`

## Steps

- `http_ingress` `step.ftgo.gateway.get.status.get.http-ingress`
- `service_dispatch` `step.ftgo.gateway.get.status.get.dispatch.services.location.locationservice.get-driver-status`
- `event_publish` `step.ftgo.gateway.get.status.get.publish.ftgo.rabbitmq.driver.status.get`
- `event_consume` `step.ftgo.gateway.get.status.get.consume.location.driver.status.get`

## Unresolved segments

This flow is not complete. The following segments could not be proven from source and are deliberately not invented:

- `persistence:driver.status.get`

## Review notes

This approved canonical page records a source-backed execution flow. Every step is backed by a bounded call trace of at most 3 hops; no segment was inferred from similarity between an endpoint path and an event name.

