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

This page is a candidate awaiting review. It is not canonical knowledge and secret values are redacted at extraction time.

