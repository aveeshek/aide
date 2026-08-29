---
id: flow.ftgo.gateway.get.location.get
kind: UserFlow
type: UserFlow
title: GET /location/get execution flow
status: approved
review_status: approved
candidate_of: user-flow-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: user-flow
owner: aide-ftgo-cohort
entry_endpoint: endpoint.ftgo.gateway.get.location.get
http_method: GET
path: /location/get
path_resolution: partial
completeness: partial
handler: application.routes.driver.location.get_location
participating_services:
- service.ftgo.gateway
- service.ftgo.location
events:
- event.ftgo.rabbitmq.driver.location.get
persistence_targets: []
unresolved_segments:
- persistence:driver.location.get
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/driver/location.py
  symbol: application.routes.driver.location.get_location
  line_start: 41
  line_end: 62
  evidence_type: implemented
relations:
- type: CONTAINS
  target: step.ftgo.gateway.get.location.get.consume.location.driver.location.get
  role: event_consume
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/location/src/events.py
  symbol: events.register_events
  line_start: 29
  line_end: 29
  evidence_type: implemented
- type: CONTAINS
  target: step.ftgo.gateway.get.location.get.dispatch.services.location.locationservice.get-last-location
  role: service_dispatch
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/driver/location.py
  symbol: application.routes.driver.location.get_location
  line_start: 45
  line_end: 45
  evidence_type: implemented
- type: CONTAINS
  target: step.ftgo.gateway.get.location.get.http-ingress
  role: http_ingress
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/driver/location.py
  symbol: application.routes.driver.location.get_location
  line_start: 41
  line_end: 62
  evidence_type: implemented
- type: CONTAINS
  target: step.ftgo.gateway.get.location.get.publish.ftgo.rabbitmq.driver.location.get
  role: event_publish
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/location.py
  symbol: services.location.LocationService.get_last_location
  line_start: 27
  line_end: 27
  evidence_type: implemented
inbound_relations:
- type: PARTICIPATES_IN
  source: service.ftgo.gateway
  completeness: partial
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/driver/location.py
  symbol: application.routes.driver.location.get_location
  line_start: 41
  line_end: 62
  evidence_type: implemented
- type: PARTICIPATES_IN
  source: service.ftgo.location
  completeness: partial
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/driver/location.py
  symbol: application.routes.driver.location.get_location
  line_start: 41
  line_end: 62
  evidence_type: implemented
attributes:
  step_count: 4
  classification_reason: publish and consume are proven but a later segment is unresolved
  max_call_depth: 3
---

# GET /location/get execution flow

Canonical execution flow stitched from source-backed call evidence in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Entry endpoint: `endpoint.ftgo.gateway.get.location.get`
- Completeness: `partial`
- Handler: `application.routes.driver.location.get_location`
- Declared in: `backend/gateway/src/application/routes/driver/location.py` (lines 41-62)
- Evidence class: `implemented`

## Steps

- `http_ingress` `step.ftgo.gateway.get.location.get.http-ingress`
- `service_dispatch` `step.ftgo.gateway.get.location.get.dispatch.services.location.locationservice.get-last-location`
- `event_publish` `step.ftgo.gateway.get.location.get.publish.ftgo.rabbitmq.driver.location.get`
- `event_consume` `step.ftgo.gateway.get.location.get.consume.location.driver.location.get`

## Unresolved segments

This flow is not complete. The following segments could not be proven from source and are deliberately not invented:

- `persistence:driver.location.get`

## Review notes

This approved canonical page records a source-backed execution flow. Every step is backed by a bounded call trace of at most 3 hops; no segment was inferred from similarity between an endpoint path and an event name.

