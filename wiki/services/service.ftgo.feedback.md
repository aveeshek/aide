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

This page is a candidate awaiting review. It is not canonical knowledge and secret values are redacted at extraction time.

