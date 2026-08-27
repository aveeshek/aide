---
id: service.ftgo.gateway
kind: Service
type: Service
title: gateway_service
status: approved
review_status: approved
candidate_of: compose-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: compose
role: application
compose_service: gateway_service
owner: aide-ftgo-cohort
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/docker-compose.yaml
  pointer: /services/gateway_service
  evidence_type: implemented
relations:
- type: DEPENDS_ON
  target: component.ftgo.rabbitmq
  config_key: RABBITMQ_HOST
  referenced_host: rabbitmq
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/docker-compose.yaml
  pointer: /services/gateway_service/environment/RABBITMQ_HOST
  evidence_type: implemented
- type: DEPENDS_ON
  target: component.ftgo.gateway-redis
  config_key: REDIS_HOST
  referenced_host: gateway_redis
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/docker-compose.yaml
  pointer: /services/gateway_service/environment/REDIS_HOST
  evidence_type: implemented
- type: EXPOSES
  target: api.ftgo.gateway
  framework: fastapi
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/main.py
  symbol: main.app
  line_start: 24
  line_end: 28
  evidence_type: implemented
attributes:
  build_context: ./gateway
  build_dockerfile: Dockerfile
  container_name: gateway_service
  ports:
  - 8000:8000
  networks:
  - backend-network
  - frontend-network
  env_file:
  - ./gateway/.env
  environment:
    ENVIRONMENT: test
    DEBUG: 'true'
    RABBITMQ_USER: rabbitmq_user
    RABBITMQ_PASS: '[redacted]'
    RABBITMQ_VHOST: /
    RABBITMQ_HOST: rabbitmq
    RABBITMQ_PORT: '5672'
    REDIS_HOST: gateway_redis
    REDIS_PORT: '6379'
    REDIS_DB: '0'
    REDIS_PASSWORD: '[redacted]'
    TOKEN_SECRET_KEY: '[redacted]'
    API_PREFIX: /api/v1
    SERVICE_HOST: 0.0.0.0
    SERVICE_PORT: '8000'
---

# gateway_service

Candidate extracted from Docker Compose evidence in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Compose service: `gateway_service`
- Declared in: `backend/docker-compose.yaml`
- YAML pointer: `/services/gateway_service`
- Evidence class: `implemented`

## Runtime dependencies

- `DEPENDS_ON` -> `component.ftgo.rabbitmq` (from `RABBITMQ_HOST=rabbitmq`)
- `DEPENDS_ON` -> `component.ftgo.gateway-redis` (from `REDIS_HOST=gateway_redis`)

## Review notes

This page is a candidate awaiting review. It is not canonical knowledge and secret values are redacted at extraction time.

