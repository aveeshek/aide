---
id: step.ftgo.gateway.delete.menu.delete.dispatch.services.menu.menuservice.delete-item
kind: FlowStep
type: FlowStep
title: services.menu.MenuService.delete_item dispatch
status: candidate
review_status: pending
candidate_of: user-flow-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: user-flow
owner: aide-ftgo-cohort
role: service_dispatch
flow: flow.ftgo.gateway.delete.menu.delete
service: service.ftgo.gateway
derived_from: endpoint.ftgo.gateway.delete.menu.delete
derived_from_kind: Endpoint
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/restaurant/menu.py
  symbol: application.routes.restaurant.menu.delete_item
  line_start: 92
  line_end: 92
  evidence_type: implemented
traces:
- target: services.menu.MenuService.delete_item
  depth: 1
  hops:
  - caller: application.routes.restaurant.menu.delete_item
    callee: services.menu.MenuService.delete_item
    call: MenuService.delete_item
    repository: ftgo
    commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
    path: backend/gateway/src/application/routes/restaurant/menu.py
    symbol: application.routes.restaurant.menu.delete_item
    line_start: 92
    line_end: 92
    evidence_type: implemented
relations:
- type: DERIVED_FROM
  target: endpoint.ftgo.gateway.delete.menu.delete
  anchor_kind: Endpoint
  role: service_dispatch
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/restaurant/menu.py
  symbol: application.routes.restaurant.menu.delete_item
  line_start: 92
  line_end: 92
  evidence_type: implemented
- type: IMPLEMENTS
  target: service.ftgo.gateway
  role: service_dispatch
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/restaurant/menu.py
  symbol: application.routes.restaurant.menu.delete_item
  line_start: 92
  line_end: 92
  evidence_type: implemented
- type: PRECEDES
  target: step.ftgo.gateway.delete.menu.delete.publish.ftgo.rabbitmq.restaurant.menu.delete-item
  established_by: publisher call site
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/menu.py
  symbol: services.menu.MenuService.delete_item
  line_start: 23
  line_end: 23
  evidence_type: implemented
inbound_relations:
- type: CONTAINS
  source: flow.ftgo.gateway.delete.menu.delete
  role: service_dispatch
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/restaurant/menu.py
  symbol: application.routes.restaurant.menu.delete_item
  line_start: 92
  line_end: 92
  evidence_type: implemented
- type: PRECEDES
  source: step.ftgo.gateway.delete.menu.delete.http-ingress
  established_by: handler call site
  call_depth: 1
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/restaurant/menu.py
  symbol: application.routes.restaurant.menu.delete_item
  line_start: 92
  line_end: 92
  evidence_type: implemented
attributes:
  gateway_symbol: services.menu.MenuService.delete_item
  call_depth: 1
---

# services.menu.MenuService.delete_item dispatch

Candidate execution step extracted from call evidence in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Role: `service_dispatch`
- Flow: `flow.ftgo.gateway.delete.menu.delete`
- Performed by: `service.ftgo.gateway`
- Anchored on: `endpoint.ftgo.gateway.delete.menu.delete` (`Endpoint`)
- Declared in: `backend/gateway/src/application/routes/restaurant/menu.py` (lines 92-92)
- Evidence class: `implemented`

## Call trace

- `application.routes.restaurant.menu.delete_item` -> `services.menu.MenuService.delete_item` (`backend/gateway/src/application/routes/restaurant/menu.py:92`)

## Review notes

This page is a candidate awaiting review. The step exists because a concrete call site proves it, and its ordering edges carry that call site as evidence.

