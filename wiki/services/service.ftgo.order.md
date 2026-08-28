---
id: service.ftgo.order
kind: Service
type: Service
title: order_service
status: approved
review_status: approved
candidate_of: compose-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: compose
role: application
compose_service: order_service
owner: aide-ftgo-cohort
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/docker-compose.yaml
  pointer: /services/order_service
  evidence_type: implemented
relations:
- type: DEPENDS_ON
  target: database.ftgo.order-mongo
  config_key: MONGO_HOST
  referenced_host: order_mongo
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/docker-compose.yaml
  pointer: /services/order_service/environment/MONGO_HOST
  evidence_type: implemented
- type: DEPENDS_ON
  target: component.ftgo.rabbitmq
  config_key: RABBITMQ_HOST
  referenced_host: rabbitmq
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/docker-compose.yaml
  pointer: /services/order_service/environment/RABBITMQ_HOST
  evidence_type: implemented
- type: DEPENDS_ON
  target: component.ftgo.order-redis
  config_key: REDIS_HOST
  referenced_host: order_redis
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/docker-compose.yaml
  pointer: /services/order_service/environment/REDIS_HOST
  evidence_type: implemented
- type: CONSUMES
  target: event.ftgo.rabbitmq.order.cancel
  role: consumer
  operation: register_event
  broker_library: rabbitmq_rpc
  mechanism: rpc
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/order/src/events.py
  symbol: events.register_events
  line_start: 45
  line_end: 45
  evidence_type: implemented
  call_sites:
  - backend/microservices/order/src/events.py:45
  handlers:
  - OrderStatusService.cancel_order
- type: CONSUMES
  target: event.ftgo.rabbitmq.order.create
  role: consumer
  operation: register_event
  broker_library: rabbitmq_rpc
  mechanism: rpc
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/order/src/events.py
  symbol: events.register_events
  line_start: 45
  line_end: 45
  evidence_type: implemented
  call_sites:
  - backend/microservices/order/src/events.py:45
  handlers:
  - OrderService.create_order
- type: CONSUMES
  target: event.ftgo.rabbitmq.order.delivery.driver-found
  role: consumer
  operation: register_event
  broker_library: rabbitmq_rpc
  mechanism: rpc
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/order/src/events.py
  symbol: events.register_events
  line_start: 45
  line_end: 45
  evidence_type: implemented
  call_sites:
  - backend/microservices/order/src/events.py:45
  handlers:
  - DeliveryService.assign_driver_to_delivery
- type: CONSUMES
  target: event.ftgo.rabbitmq.order.delivery.get-details
  role: consumer
  operation: register_event
  broker_library: rabbitmq_rpc
  mechanism: rpc
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/order/src/events.py
  symbol: events.register_events
  line_start: 45
  line_end: 45
  evidence_type: implemented
  call_sites:
  - backend/microservices/order/src/events.py:45
  handlers:
  - DeliveryService.get_delivery_details
- type: CONSUMES
  target: event.ftgo.rabbitmq.order.delivery.update-status
  role: consumer
  operation: register_event
  broker_library: rabbitmq_rpc
  mechanism: rpc
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/order/src/events.py
  symbol: events.register_events
  line_start: 45
  line_end: 45
  evidence_type: implemented
  call_sites:
  - backend/microservices/order/src/events.py:45
  handlers:
  - DeliveryService.update_delivery_status
- type: CONSUMES
  target: event.ftgo.rabbitmq.order.get-details
  role: consumer
  operation: register_event
  broker_library: rabbitmq_rpc
  mechanism: rpc
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/order/src/events.py
  symbol: events.register_events
  line_start: 45
  line_end: 45
  evidence_type: implemented
  call_sites:
  - backend/microservices/order/src/events.py:45
  handlers:
  - OrderService.get_order_details
- type: CONSUMES
  target: event.ftgo.rabbitmq.order.restaurant.confirm
  role: consumer
  operation: register_event
  broker_library: rabbitmq_rpc
  mechanism: rpc
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/order/src/events.py
  symbol: events.register_events
  line_start: 45
  line_end: 45
  evidence_type: implemented
  call_sites:
  - backend/microservices/order/src/events.py:45
  handlers:
  - RestaurantService.confirm_order
- type: CONSUMES
  target: event.ftgo.rabbitmq.order.restaurant.reject
  role: consumer
  operation: register_event
  broker_library: rabbitmq_rpc
  mechanism: rpc
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/order/src/events.py
  symbol: events.register_events
  line_start: 45
  line_end: 45
  evidence_type: implemented
  call_sites:
  - backend/microservices/order/src/events.py:45
  handlers:
  - RestaurantService.reject_order
- type: CONSUMES
  target: event.ftgo.rabbitmq.order.status.change
  role: consumer
  operation: register_event
  broker_library: rabbitmq_rpc
  mechanism: rpc
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/order/src/events.py
  symbol: events.register_events
  line_start: 45
  line_end: 45
  evidence_type: implemented
  call_sites:
  - backend/microservices/order/src/events.py:45
  handlers:
  - OrderStatusService.change_order_status
- type: CONSUMES
  target: event.ftgo.rabbitmq.order.update
  role: consumer
  operation: register_event
  broker_library: rabbitmq_rpc
  mechanism: rpc
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/order/src/events.py
  symbol: events.register_events
  line_start: 45
  line_end: 45
  evidence_type: implemented
  call_sites:
  - backend/microservices/order/src/events.py:45
  handlers:
  - OrderService.update_order
- type: WRITES
  target: collection.ftgo.order.delivery-details
  role: write
  target_kind: Collection
  persistence_library: beanie
  call_site_count: 2
  call_sites:
  - operation: insert
    resolution: class_attribute
    call: self.document.insert()
    repository: ftgo
    commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
    path: backend/microservices/order/src/domain/entities/delivery.py
    symbol: domain.entities.delivery.Delivery.save
    line_start: 43
    line_end: 43
    evidence_type: implemented
  - operation: save
    resolution: class_attribute
    call: self.document.save()
    repository: ftgo
    commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
    path: backend/microservices/order/src/domain/entities/delivery.py
    symbol: domain.entities.delivery.Delivery.update_status
    line_start: 55
    line_end: 55
    evidence_type: implemented
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/order/src/domain/entities/delivery.py
  symbol: domain.entities.delivery.Delivery.save
  line_start: 43
  line_end: 43
  evidence_type: implemented
- type: WRITES
  target: collection.ftgo.order.order-items
  role: write
  target_kind: Collection
  persistence_library: beanie
  call_site_count: 3
  call_sites:
  - operation: insert
    resolution: class_attribute
    call: self.document.insert()
    repository: ftgo
    commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
    path: backend/microservices/order/src/domain/entities/order_item.py
    symbol: domain.entities.order_item.OrderItem.save
    line_start: 42
    line_end: 42
    evidence_type: implemented
  - operation: save
    resolution: class_attribute
    call: self.document.save()
    repository: ftgo
    commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
    path: backend/microservices/order/src/domain/entities/order_item.py
    symbol: domain.entities.order_item.OrderItem.update_quantity
    line_start: 52
    line_end: 52
    evidence_type: implemented
  - operation: save
    resolution: class_attribute
    call: self.document.save()
    repository: ftgo
    commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
    path: backend/microservices/order/src/domain/entities/order_item.py
    symbol: domain.entities.order_item.OrderItem.update_item_price
    line_start: 62
    line_end: 62
    evidence_type: implemented
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/order/src/domain/entities/order_item.py
  symbol: domain.entities.order_item.OrderItem.save
  line_start: 42
  line_end: 42
  evidence_type: implemented
- type: WRITES
  target: collection.ftgo.order.order-status
  role: write
  target_kind: Collection
  persistence_library: beanie
  call_site_count: 1
  call_sites:
  - operation: insert
    resolution: class_attribute
    call: self.document.insert()
    repository: ftgo
    commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
    path: backend/microservices/order/src/domain/entities/order_status.py
    symbol: domain.entities.order_status.OrderStatus.save
    line_start: 40
    line_end: 40
    evidence_type: implemented
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/order/src/domain/entities/order_status.py
  symbol: domain.entities.order_status.OrderStatus.save
  line_start: 40
  line_end: 40
  evidence_type: implemented
- type: WRITES
  target: collection.ftgo.order.orders
  role: write
  target_kind: Collection
  persistence_library: beanie
  call_site_count: 3
  call_sites:
  - operation: insert
    resolution: class_attribute
    call: self.document.insert()
    repository: ftgo
    commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
    path: backend/microservices/order/src/domain/entities/order.py
    symbol: domain.entities.order.Order.save
    line_start: 46
    line_end: 46
    evidence_type: implemented
  - operation: save
    resolution: class_attribute
    call: self.document.save()
    repository: ftgo
    commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
    path: backend/microservices/order/src/domain/entities/order.py
    symbol: domain.entities.order.Order.calculate_total
    line_start: 73
    line_end: 73
    evidence_type: implemented
  - operation: save
    resolution: class_attribute
    call: self.document.save()
    repository: ftgo
    commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
    path: backend/microservices/order/src/domain/entities/order.py
    symbol: domain.entities.order.Order.change_status
    line_start: 94
    line_end: 94
    evidence_type: implemented
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/order/src/domain/entities/order.py
  symbol: domain.entities.order.Order.save
  line_start: 46
  line_end: 46
  evidence_type: implemented
attributes:
  build_context: ./microservices/order
  build_dockerfile: Dockerfile
  container_name: order_service
  networks:
  - backend-network
  env_file:
  - ./microservices/order/.env
  environment:
    ENVIRONMENT: dev
    DEBUG: 'true'
    REDIS_HOST: order_redis
    REDIS_PORT: '6379'
    REDIS_DB: '0'
    REDIS_PASSWORD: '[redacted]'
    RABBITMQ_USER: rabbitmq_user
    RABBITMQ_PASS: '[redacted]'
    RABBITMQ_VHOST: /
    RABBITMQ_HOST: rabbitmq
    RABBITMQ_PORT: '5672'
    MONGO_HOST: order_mongo
    MONGO_PORT: '27017'
    MONGO_USERNAME: order_user
    MONGO_PASSWORD: '[redacted]'
    MONGO_DATABASE: order_database
---

# order_service

Candidate extracted from Docker Compose evidence in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Compose service: `order_service`
- Declared in: `backend/docker-compose.yaml`
- YAML pointer: `/services/order_service`
- Evidence class: `implemented`

## Runtime dependencies

- `DEPENDS_ON` -> `database.ftgo.order-mongo` (from `MONGO_HOST=order_mongo`)
- `DEPENDS_ON` -> `component.ftgo.rabbitmq` (from `RABBITMQ_HOST=rabbitmq`)
- `DEPENDS_ON` -> `component.ftgo.order-redis` (from `REDIS_HOST=order_redis`)

## Review notes

This page is approved canonical knowledge. Secret values are redacted at extraction time.

