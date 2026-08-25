---
id: service.ftgo.restaurant
kind: Service
type: Service
title: restaurant_service
status: candidate
review_status: pending
candidate_of: compose-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: compose
role: application
compose_service: restaurant_service
owner: aide-ftgo-cohort
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/docker-compose.yaml
  pointer: /services/restaurant_service
  evidence_type: implemented
relations:
- type: DEPENDS_ON
  target: database.ftgo.restaurant-postgres
  config_key: POSTGRES_HOST
  referenced_host: restaurant_postgres
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/docker-compose.yaml
  pointer: /services/restaurant_service/environment/POSTGRES_HOST
  evidence_type: implemented
- type: DEPENDS_ON
  target: component.ftgo.rabbitmq
  config_key: RABBITMQ_HOST
  referenced_host: rabbitmq
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/docker-compose.yaml
  pointer: /services/restaurant_service/environment/RABBITMQ_HOST
  evidence_type: implemented
- type: DEPENDS_ON
  target: component.ftgo.restaurant-redis
  config_key: REDIS_HOST
  referenced_host: restaurant_redis
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/docker-compose.yaml
  pointer: /services/restaurant_service/environment/REDIS_HOST
  evidence_type: implemented
attributes:
  build_context: ./microservices/restaurant
  build_dockerfile: Dockerfile
  container_name: restaurant_service
  networks:
  - backend-network
  env_file:
  - ./microservices/restaurant/.env
  environment:
    ENVIRONMENT: test
    DEBUG: 'true'
    RABBITMQ_USER: rabbitmq_user
    RABBITMQ_PASS: '[redacted]'
    RABBITMQ_VHOST: /
    RABBITMQ_HOST: rabbitmq
    RABBITMQ_PORT: '5672'
    REDIS_HOST: restaurant_redis
    REDIS_PORT: '6379'
    REDIS_DB: '0'
    REDIS_PASSWORD: '[redacted]'
    POSTGRES_HOST: restaurant_postgres
    POSTGRES_PORT: '5432'
    POSTGRES_USER: restaurant_user
    POSTGRES_PASSWORD: '[redacted]'
    POSTGRES_DB: restaurant_database
---

# restaurant_service

Candidate extracted from Docker Compose evidence in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Compose service: `restaurant_service`
- Declared in: `backend/docker-compose.yaml`
- YAML pointer: `/services/restaurant_service`
- Evidence class: `implemented`

## Runtime dependencies

- `DEPENDS_ON` -> `database.ftgo.restaurant-postgres` (from `POSTGRES_HOST=restaurant_postgres`)
- `DEPENDS_ON` -> `component.ftgo.rabbitmq` (from `RABBITMQ_HOST=rabbitmq`)
- `DEPENDS_ON` -> `component.ftgo.restaurant-redis` (from `REDIS_HOST=restaurant_redis`)

## Review notes

This page is a candidate awaiting review. It is not canonical knowledge and secret values are redacted at extraction time.
