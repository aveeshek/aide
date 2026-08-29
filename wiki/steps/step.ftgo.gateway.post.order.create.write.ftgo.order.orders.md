---
id: step.ftgo.gateway.post.order.create.write.ftgo.order.orders
kind: FlowStep
type: FlowStep
title: write collection.ftgo.order.orders
status: approved
review_status: approved
candidate_of: user-flow-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: user-flow
owner: aide-ftgo-cohort
role: persistence_write
flow: flow.ftgo.gateway.post.order.create
service: service.ftgo.order
derived_from: collection.ftgo.order.orders
derived_from_kind: Collection
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/order/src/domain/entities/order.py
  symbol: domain.entities.order.Order.save
  line_start: 46
  line_end: 46
  evidence_type: implemented
traces:
- target: domain.entities.order.Order.save
  depth: 2
  hops:
  - caller: application.order.OrderService.create_order
    callee: domain.order.OrderHandler.create_order
    call: OrderHandler.create_order
    repository: ftgo
    commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
    path: backend/microservices/order/src/application/order.py
    symbol: application.order.OrderService.create_order
    line_start: 13
    line_end: 19
    evidence_type: implemented
  - caller: domain.order.OrderHandler.create_order
    callee: domain.entities.order.Order.save
    call: order.save
    repository: ftgo
    commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
    path: backend/microservices/order/src/domain/order.py
    symbol: domain.order.OrderHandler.create_order
    line_start: 25
    line_end: 25
    evidence_type: implemented
- target: domain.entities.order.Order.calculate_total
  depth: 3
  hops:
  - caller: application.order.OrderService.create_order
    callee: domain.order.OrderHandler.create_order
    call: OrderHandler.create_order
    repository: ftgo
    commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
    path: backend/microservices/order/src/application/order.py
    symbol: application.order.OrderService.create_order
    line_start: 13
    line_end: 19
    evidence_type: implemented
  - caller: domain.order.OrderHandler.create_order
    callee: domain.entities.order.Order.add_order_item
    call: order.add_order_item
    repository: ftgo
    commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
    path: backend/microservices/order/src/domain/order.py
    symbol: domain.order.OrderHandler.create_order
    line_start: 23
    line_end: 23
    evidence_type: implemented
  - caller: domain.entities.order.Order.add_order_item
    callee: domain.entities.order.Order.calculate_total
    call: self.calculate_total
    repository: ftgo
    commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
    path: backend/microservices/order/src/domain/entities/order.py
    symbol: domain.entities.order.Order.add_order_item
    line_start: 55
    line_end: 55
    evidence_type: implemented
relations:
- type: DERIVED_FROM
  target: collection.ftgo.order.orders
  anchor_kind: Collection
  role: persistence_write
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/order/src/domain/entities/order.py
  symbol: domain.entities.order.Order.save
  line_start: 46
  line_end: 46
  evidence_type: implemented
- type: IMPLEMENTS
  target: service.ftgo.order
  role: persistence_write
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/order/src/domain/entities/order.py
  symbol: domain.entities.order.Order.save
  line_start: 46
  line_end: 46
  evidence_type: implemented
inbound_relations:
- type: CONTAINS
  source: flow.ftgo.gateway.post.order.create
  role: persistence_write
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/order/src/domain/entities/order.py
  symbol: domain.entities.order.Order.save
  line_start: 46
  line_end: 46
  evidence_type: implemented
- type: PRECEDES
  source: step.ftgo.gateway.post.order.create.consume.order.order.create
  established_by: consumer call trace
  call_depth: 3
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/order/src/domain/entities/order.py
  symbol: domain.entities.order.Order.calculate_total
  line_start: 73
  line_end: 73
  evidence_type: implemented
attributes:
  operation: insert
  persistence_library: beanie
  resolution: class_attribute
  call_depth: 2
  event_identity: order.create
---

# write collection.ftgo.order.orders

Canonical execution step extracted from call evidence in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Role: `persistence_write`
- Flow: `flow.ftgo.gateway.post.order.create`
- Performed by: `service.ftgo.order`
- Anchored on: `collection.ftgo.order.orders` (`Collection`)
- Declared in: `backend/microservices/order/src/domain/entities/order.py` (lines 46-46)
- Evidence class: `implemented`

## Call trace

- `application.order.OrderService.create_order` -> `domain.order.OrderHandler.create_order` (`backend/microservices/order/src/application/order.py:13`)
- `domain.order.OrderHandler.create_order` -> `domain.entities.order.Order.save` (`backend/microservices/order/src/domain/order.py:25`)
- `application.order.OrderService.create_order` -> `domain.order.OrderHandler.create_order` (`backend/microservices/order/src/application/order.py:13`)
- `domain.order.OrderHandler.create_order` -> `domain.entities.order.Order.add_order_item` (`backend/microservices/order/src/domain/order.py:23`)
- `domain.entities.order.Order.add_order_item` -> `domain.entities.order.Order.calculate_total` (`backend/microservices/order/src/domain/entities/order.py:55`)

## Review notes

This approved canonical page records a source-backed execution step. The step exists because a concrete call site proves it, and its ordering edges carry that call site as evidence.

