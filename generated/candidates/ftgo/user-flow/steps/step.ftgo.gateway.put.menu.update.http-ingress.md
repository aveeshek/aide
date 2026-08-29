---
id: step.ftgo.gateway.put.menu.update.http-ingress
kind: FlowStep
type: FlowStep
title: PUT /menu/update ingress
status: candidate
review_status: pending
candidate_of: user-flow-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: user-flow
owner: aide-ftgo-cohort
role: http_ingress
flow: flow.ftgo.gateway.put.menu.update
service: service.ftgo.gateway
derived_from: endpoint.ftgo.gateway.put.menu.update
derived_from_kind: Endpoint
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/restaurant/menu.py
  symbol: application.routes.restaurant.menu.update_item
  line_start: 66
  line_end: 85
  evidence_type: implemented
relations:
- type: DERIVED_FROM
  target: endpoint.ftgo.gateway.put.menu.update
  anchor_kind: Endpoint
  role: http_ingress
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/restaurant/menu.py
  symbol: application.routes.restaurant.menu.update_item
  line_start: 66
  line_end: 85
  evidence_type: implemented
- type: IMPLEMENTS
  target: service.ftgo.gateway
  role: http_ingress
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/restaurant/menu.py
  symbol: application.routes.restaurant.menu.update_item
  line_start: 66
  line_end: 85
  evidence_type: implemented
- type: PRECEDES
  target: step.ftgo.gateway.put.menu.update.dispatch.services.menu.menuservice.update-item
  established_by: handler call site
  call_depth: 1
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/restaurant/menu.py
  symbol: application.routes.restaurant.menu.update_item
  line_start: 70
  line_end: 70
  evidence_type: implemented
inbound_relations:
- type: CONTAINS
  source: flow.ftgo.gateway.put.menu.update
  role: http_ingress
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/restaurant/menu.py
  symbol: application.routes.restaurant.menu.update_item
  line_start: 66
  line_end: 85
  evidence_type: implemented
attributes:
  http_method: PUT
  path: /menu/update
  path_resolution: partial
  handler: application.routes.restaurant.menu.update_item
---

# PUT /menu/update ingress

Candidate execution step extracted from call evidence in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Role: `http_ingress`
- Flow: `flow.ftgo.gateway.put.menu.update`
- Performed by: `service.ftgo.gateway`
- Anchored on: `endpoint.ftgo.gateway.put.menu.update` (`Endpoint`)
- Declared in: `backend/gateway/src/application/routes/restaurant/menu.py` (lines 66-85)
- Evidence class: `implemented`

## Review notes

This page is a candidate awaiting review. The step exists because a concrete call site proves it, and its ordering edges carry that call site as evidence.

