---
id: step.ftgo.gateway.get.restaurant.get-all-restaurant-info.publish.ftgo.rabbitmq.restaurant.supplier.get-all-restaurant-info
kind: FlowStep
type: FlowStep
title: publish restaurant.supplier.get_all_restaurant_info
status: candidate
review_status: pending
candidate_of: user-flow-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: user-flow
owner: aide-ftgo-cohort
role: event_publish
flow: flow.ftgo.gateway.get.restaurant.get-all-restaurant-info
service: service.ftgo.gateway
derived_from: event.ftgo.rabbitmq.restaurant.supplier.get-all-restaurant-info
derived_from_kind: Event
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/restaurant.py
  symbol: services.restaurant.RestaurantService.get_all_restaurant_info
  line_start: 19
  line_end: 19
  evidence_type: implemented
relations:
- type: DERIVED_FROM
  target: event.ftgo.rabbitmq.restaurant.supplier.get-all-restaurant-info
  anchor_kind: Event
  role: event_publish
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/restaurant.py
  symbol: services.restaurant.RestaurantService.get_all_restaurant_info
  line_start: 19
  line_end: 19
  evidence_type: implemented
- type: IMPLEMENTS
  target: service.ftgo.gateway
  role: event_publish
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/restaurant.py
  symbol: services.restaurant.RestaurantService.get_all_restaurant_info
  line_start: 19
  line_end: 19
  evidence_type: implemented
- type: PRECEDES
  target: step.ftgo.gateway.get.restaurant.get-all-restaurant-info.consume.restaurant.restaurant.supplier.get-all-restaurant-info
  established_by: handler registration
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/restaurant/src/events.py
  symbol: events.register_events
  line_start: 32
  line_end: 32
  evidence_type: implemented
inbound_relations:
- type: CONTAINS
  source: flow.ftgo.gateway.get.restaurant.get-all-restaurant-info
  role: event_publish
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/restaurant.py
  symbol: services.restaurant.RestaurantService.get_all_restaurant_info
  line_start: 19
  line_end: 19
  evidence_type: implemented
- type: PRECEDES
  source: step.ftgo.gateway.get.restaurant.get-all-restaurant-info.dispatch.services.restaurant.restaurantservice.get-all-restaurant-info
  established_by: publisher call site
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/restaurant.py
  symbol: services.restaurant.RestaurantService.get_all_restaurant_info
  line_start: 19
  line_end: 19
  evidence_type: implemented
attributes:
  event_identity: restaurant.supplier.get_all_restaurant_info
  operation: call
  mechanism: rpc
  broker_library: rabbitmq_rpc
  via_wrapper: services.base.Microservice._call_rpc
  correlation: matched
---

# publish restaurant.supplier.get_all_restaurant_info

Candidate execution step extracted from call evidence in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Role: `event_publish`
- Flow: `flow.ftgo.gateway.get.restaurant.get-all-restaurant-info`
- Performed by: `service.ftgo.gateway`
- Anchored on: `event.ftgo.rabbitmq.restaurant.supplier.get-all-restaurant-info` (`Event`)
- Declared in: `backend/gateway/src/services/restaurant.py` (lines 19-19)
- Evidence class: `implemented`

## Review notes

This page is a candidate awaiting review. The step exists because a concrete call site proves it, and its ordering edges carry that call site as evidence.

