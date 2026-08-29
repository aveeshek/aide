---
id: step.ftgo.gateway.get.menu.get-info.dispatch.services.menu.menuservice.get-item-info
kind: FlowStep
type: FlowStep
title: services.menu.MenuService.get_item_info dispatch
status: candidate
review_status: pending
candidate_of: user-flow-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: user-flow
owner: aide-ftgo-cohort
role: service_dispatch
flow: flow.ftgo.gateway.get.menu.get-info
service: service.ftgo.gateway
derived_from: endpoint.ftgo.gateway.get.menu.get-info
derived_from_kind: Endpoint
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/restaurant/menu.py
  symbol: application.routes.restaurant.menu.get_info
  line_start: 48
  line_end: 48
  evidence_type: implemented
traces:
- target: services.menu.MenuService.get_item_info
  depth: 1
  hops:
  - caller: application.routes.restaurant.menu.get_info
    callee: services.menu.MenuService.get_item_info
    call: MenuService.get_item_info
    repository: ftgo
    commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
    path: backend/gateway/src/application/routes/restaurant/menu.py
    symbol: application.routes.restaurant.menu.get_info
    line_start: 48
    line_end: 48
    evidence_type: implemented
relations:
- type: DERIVED_FROM
  target: endpoint.ftgo.gateway.get.menu.get-info
  anchor_kind: Endpoint
  role: service_dispatch
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/restaurant/menu.py
  symbol: application.routes.restaurant.menu.get_info
  line_start: 48
  line_end: 48
  evidence_type: implemented
- type: IMPLEMENTS
  target: service.ftgo.gateway
  role: service_dispatch
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/restaurant/menu.py
  symbol: application.routes.restaurant.menu.get_info
  line_start: 48
  line_end: 48
  evidence_type: implemented
- type: PRECEDES
  target: step.ftgo.gateway.get.menu.get-info.publish.ftgo.rabbitmq.restaurant.menu.get-item-info
  established_by: publisher call site
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/menu.py
  symbol: services.menu.MenuService.get_item_info
  line_start: 15
  line_end: 15
  evidence_type: implemented
inbound_relations:
- type: CONTAINS
  source: flow.ftgo.gateway.get.menu.get-info
  role: service_dispatch
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/restaurant/menu.py
  symbol: application.routes.restaurant.menu.get_info
  line_start: 48
  line_end: 48
  evidence_type: implemented
- type: PRECEDES
  source: step.ftgo.gateway.get.menu.get-info.http-ingress
  established_by: handler call site
  call_depth: 1
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/restaurant/menu.py
  symbol: application.routes.restaurant.menu.get_info
  line_start: 48
  line_end: 48
  evidence_type: implemented
attributes:
  gateway_symbol: services.menu.MenuService.get_item_info
  call_depth: 1
---

# services.menu.MenuService.get_item_info dispatch

Candidate execution step extracted from call evidence in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Role: `service_dispatch`
- Flow: `flow.ftgo.gateway.get.menu.get-info`
- Performed by: `service.ftgo.gateway`
- Anchored on: `endpoint.ftgo.gateway.get.menu.get-info` (`Endpoint`)
- Declared in: `backend/gateway/src/application/routes/restaurant/menu.py` (lines 48-48)
- Evidence class: `implemented`

## Call trace

- `application.routes.restaurant.menu.get_info` -> `services.menu.MenuService.get_item_info` (`backend/gateway/src/application/routes/restaurant/menu.py:48`)

## Review notes

This page is a candidate awaiting review. The step exists because a concrete call site proves it, and its ordering edges carry that call site as evidence.

