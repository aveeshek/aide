---
id: service.ftgo.feedback
kind: Service
type: Service
title: feedback_service
status: approved
review_status: approved
candidate_of: compose-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: compose
role: application
compose_service: feedback_service
owner: aide-ftgo-cohort
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/docker-compose.yaml
  pointer: /services/feedback_service
  evidence_type: implemented
relations:
- type: DEPENDS_ON
  target: database.ftgo.feedback-mongo
  config_key: MONGO_HOST
  referenced_host: feedback_mongo
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/docker-compose.yaml
  pointer: /services/feedback_service/environment/MONGO_HOST
  evidence_type: implemented
- type: DEPENDS_ON
  target: component.ftgo.rabbitmq
  config_key: RABBITMQ_HOST
  referenced_host: rabbitmq
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/docker-compose.yaml
  pointer: /services/feedback_service/environment/RABBITMQ_HOST
  evidence_type: implemented
- type: CONSUMES
  target: event.ftgo.rabbitmq.delivery.rating.create
  role: consumer
  operation: register_event
  broker_library: rabbitmq_rpc
  mechanism: rpc
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/feedback/src/events.py
  symbol: events.register_events
  line_start: 37
  line_end: 37
  evidence_type: implemented
  call_sites:
  - backend/microservices/feedback/src/events.py:37
  handlers:
  - DeliveryRatingService.create_delivery_rating
- type: CONSUMES
  target: event.ftgo.rabbitmq.delivery.rating.get-customer-ratings
  role: consumer
  operation: register_event
  broker_library: rabbitmq_rpc
  mechanism: rpc
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/feedback/src/events.py
  symbol: events.register_events
  line_start: 37
  line_end: 37
  evidence_type: implemented
  call_sites:
  - backend/microservices/feedback/src/events.py:37
  handlers:
  - DeliveryRatingService.get_customer_delivery_ratings
- type: CONSUMES
  target: event.ftgo.rabbitmq.delivery.rating.get-details
  role: consumer
  operation: register_event
  broker_library: rabbitmq_rpc
  mechanism: rpc
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/feedback/src/events.py
  symbol: events.register_events
  line_start: 37
  line_end: 37
  evidence_type: implemented
  call_sites:
  - backend/microservices/feedback/src/events.py:37
  handlers:
  - DeliveryRatingService.get_delivery_rating
- type: CONSUMES
  target: event.ftgo.rabbitmq.delivery.rating.get-driver-ratings
  role: consumer
  operation: register_event
  broker_library: rabbitmq_rpc
  mechanism: rpc
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/feedback/src/events.py
  symbol: events.register_events
  line_start: 37
  line_end: 37
  evidence_type: implemented
  call_sites:
  - backend/microservices/feedback/src/events.py:37
  handlers:
  - DeliveryRatingService.get_driver_delivery_ratings
- type: CONSUMES
  target: event.ftgo.rabbitmq.delivery.rating.update
  role: consumer
  operation: register_event
  broker_library: rabbitmq_rpc
  mechanism: rpc
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/feedback/src/events.py
  symbol: events.register_events
  line_start: 37
  line_end: 37
  evidence_type: implemented
  call_sites:
  - backend/microservices/feedback/src/events.py:37
  handlers:
  - DeliveryRatingService.update_delivery_rating
- type: CONSUMES
  target: event.ftgo.rabbitmq.order.rating.create
  role: consumer
  operation: register_event
  broker_library: rabbitmq_rpc
  mechanism: rpc
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/feedback/src/events.py
  symbol: events.register_events
  line_start: 37
  line_end: 37
  evidence_type: implemented
  call_sites:
  - backend/microservices/feedback/src/events.py:37
  handlers:
  - OrderRatingService.create_order_rating
- type: CONSUMES
  target: event.ftgo.rabbitmq.order.rating.get-customer-ratings
  role: consumer
  operation: register_event
  broker_library: rabbitmq_rpc
  mechanism: rpc
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/feedback/src/events.py
  symbol: events.register_events
  line_start: 37
  line_end: 37
  evidence_type: implemented
  call_sites:
  - backend/microservices/feedback/src/events.py:37
  handlers:
  - OrderRatingService.get_customer_order_ratings
- type: CONSUMES
  target: event.ftgo.rabbitmq.order.rating.get-details
  role: consumer
  operation: register_event
  broker_library: rabbitmq_rpc
  mechanism: rpc
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/feedback/src/events.py
  symbol: events.register_events
  line_start: 37
  line_end: 37
  evidence_type: implemented
  call_sites:
  - backend/microservices/feedback/src/events.py:37
  handlers:
  - OrderRatingService.get_order_rating
- type: CONSUMES
  target: event.ftgo.rabbitmq.order.rating.get-restaurant-ratings
  role: consumer
  operation: register_event
  broker_library: rabbitmq_rpc
  mechanism: rpc
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/feedback/src/events.py
  symbol: events.register_events
  line_start: 37
  line_end: 37
  evidence_type: implemented
  call_sites:
  - backend/microservices/feedback/src/events.py:37
  handlers:
  - OrderRatingService.get_restaurant_order_ratings
- type: CONSUMES
  target: event.ftgo.rabbitmq.order.rating.update
  role: consumer
  operation: register_event
  broker_library: rabbitmq_rpc
  mechanism: rpc
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/feedback/src/events.py
  symbol: events.register_events
  line_start: 37
  line_end: 37
  evidence_type: implemented
  call_sites:
  - backend/microservices/feedback/src/events.py:37
  handlers:
  - OrderRatingService.update_order_rating
- type: READS
  target: collection.ftgo.feedback.delivery-ratings
  role: read
  target_kind: Collection
  persistence_library: beanie
  call_site_count: 2
  call_sites:
  - operation: find_all
    resolution: direct_model_reference
    call: DeliveryRatingModel.find_all(customer_id=customer_id)
    repository: ftgo
    commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
    path: backend/microservices/feedback/src/domain/delivery_rating.py
    symbol: domain.delivery_rating.DeliveryRatingHandler.get_customer_delivery_ratings
    line_start: 51
    line_end: 51
    evidence_type: implemented
  - operation: find_all
    resolution: direct_model_reference
    call: DeliveryRatingModel.find_all(driver_id=driver_id)
    repository: ftgo
    commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
    path: backend/microservices/feedback/src/domain/delivery_rating.py
    symbol: domain.delivery_rating.DeliveryRatingHandler.get_driver_delivery_ratings
    line_start: 61
    line_end: 61
    evidence_type: implemented
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/feedback/src/domain/delivery_rating.py
  symbol: domain.delivery_rating.DeliveryRatingHandler.get_customer_delivery_ratings
  line_start: 51
  line_end: 51
  evidence_type: implemented
- type: READS
  target: collection.ftgo.feedback.order-ratings
  role: read
  target_kind: Collection
  persistence_library: beanie
  call_site_count: 2
  call_sites:
  - operation: find_all
    resolution: direct_model_reference
    call: OrderRatingModel.find_all(customer_id=customer_id)
    repository: ftgo
    commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
    path: backend/microservices/feedback/src/domain/order_rating.py
    symbol: domain.order_rating.OrderRatingHandler.get_customer_order_ratings
    line_start: 57
    line_end: 57
    evidence_type: implemented
  - operation: find_all
    resolution: direct_model_reference
    call: OrderRatingModel.find_all(restaurant_id=restaurant_id)
    repository: ftgo
    commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
    path: backend/microservices/feedback/src/domain/order_rating.py
    symbol: domain.order_rating.OrderRatingHandler.get_restaurant_order_ratings
    line_start: 67
    line_end: 67
    evidence_type: implemented
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/feedback/src/domain/order_rating.py
  symbol: domain.order_rating.OrderRatingHandler.get_customer_order_ratings
  line_start: 57
  line_end: 57
  evidence_type: implemented
attributes:
  build_context: ./microservices/feedback
  build_dockerfile: Dockerfile
  container_name: feedback_service
  networks:
  - backend-network
  env_file:
  - ./microservices/feedback/.env
  environment:
    ENVIRONMENT: dev
    DEBUG: 'true'
    REDIS_HOST: feedback_redis
    REDIS_PORT: '6379'
    REDIS_DB: '0'
    REDIS_PASSWORD: '[redacted]'
    RABBITMQ_USER: rabbitmq_user
    RABBITMQ_PASS: '[redacted]'
    RABBITMQ_VHOST: /
    RABBITMQ_HOST: rabbitmq
    RABBITMQ_PORT: '5672'
    MONGO_HOST: feedback_mongo
    MONGO_PORT: '27017'
    MONGO_USERNAME: feedback_user
    MONGO_PASSWORD: '[redacted]'
    MONGO_DATABASE: feedback_database
---

# feedback_service

Candidate extracted from Docker Compose evidence in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Compose service: `feedback_service`
- Declared in: `backend/docker-compose.yaml`
- YAML pointer: `/services/feedback_service`
- Evidence class: `implemented`

## Runtime dependencies

- `DEPENDS_ON` -> `database.ftgo.feedback-mongo` (from `MONGO_HOST=feedback_mongo`)
- `DEPENDS_ON` -> `component.ftgo.rabbitmq` (from `RABBITMQ_HOST=rabbitmq`)

## Review notes

This page is approved canonical knowledge. Secret values are redacted at extraction time.

