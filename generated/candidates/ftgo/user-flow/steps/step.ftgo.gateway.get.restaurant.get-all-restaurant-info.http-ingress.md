---
id: step.ftgo.gateway.get.restaurant.get-all-restaurant-info.http-ingress
kind: FlowStep
type: FlowStep
title: GET /restaurant/get_all_restaurant_info ingress
status: candidate
review_status: pending
candidate_of: user-flow-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: user-flow
owner: aide-ftgo-cohort
role: http_ingress
flow: flow.ftgo.gateway.get.restaurant.get-all-restaurant-info
service: service.ftgo.gateway
derived_from: endpoint.ftgo.gateway.get.restaurant.get-all-restaurant-info
derived_from_kind: Endpoint
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/restaurant/restaurant.py
  symbol: application.routes.restaurant.restaurant.get_all_restaurant_info
  line_start: 74
  line_end: 91
  evidence_type: implemented
relations:
- type: DERIVED_FROM
  target: endpoint.ftgo.gateway.get.restaurant.get-all-restaurant-info
  anchor_kind: Endpoint
  role: http_ingress
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/restaurant/restaurant.py
  symbol: application.routes.restaurant.restaurant.get_all_restaurant_info
  line_start: 74
  line_end: 91
  evidence_type: implemented
- type: IMPLEMENTS
  target: service.ftgo.gateway
  role: http_ingress
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/restaurant/restaurant.py
  symbol: application.routes.restaurant.restaurant.get_all_restaurant_info
  line_start: 74
  line_end: 91
  evidence_type: implemented
- type: PRECEDES
  target: step.ftgo.gateway.get.restaurant.get-all-restaurant-info.dispatch.services.restaurant.restaurantservice.get-all-restaurant-info
  established_by: handler call site
  call_depth: 1
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/restaurant/restaurant.py
  symbol: application.routes.restaurant.restaurant.get_all_restaurant_info
  line_start: 77
  line_end: 77
  evidence_type: implemented
inbound_relations:
- type: CONTAINS
  source: flow.ftgo.gateway.get.restaurant.get-all-restaurant-info
  role: http_ingress
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/restaurant/restaurant.py
  symbol: application.routes.restaurant.restaurant.get_all_restaurant_info
  line_start: 74
  line_end: 91
  evidence_type: implemented
attributes:
  http_method: GET
  path: /restaurant/get_all_restaurant_info
  path_resolution: partial
  handler: application.routes.restaurant.restaurant.get_all_restaurant_info
---

# GET /restaurant/get_all_restaurant_info ingress

Candidate execution step extracted from call evidence in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Role: `http_ingress`
- Flow: `flow.ftgo.gateway.get.restaurant.get-all-restaurant-info`
- Performed by: `service.ftgo.gateway`
- Anchored on: `endpoint.ftgo.gateway.get.restaurant.get-all-restaurant-info` (`Endpoint`)
- Declared in: `backend/gateway/src/application/routes/restaurant/restaurant.py` (lines 74-91)
- Evidence class: `implemented`

## Review notes

This page is a candidate awaiting review. The step exists because a concrete call site proves it, and its ordering edges carry that call site as evidence.

