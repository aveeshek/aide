---
id: component.ftgo.order-redis
kind: Component
type: Component
title: order_redis
status: candidate
review_status: pending
candidate_of: compose-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: compose
role: infrastructure
compose_service: order_redis
engine: redis
network_aliases:
- order_redis
owner: aide-ftgo-cohort
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/infra/redis/docker-compose.yaml
  pointer: /services/order_redis
  evidence_type: implemented
attributes:
  image: redis:7.2.5
  container_name: order_redis
  hostname: order_redis
  restart: always
  ports:
  - 6301:6379
  networks:
  - backend-network
  volumes:
  - order_redis_data:/data
  environment:
    REDIS_PORT: '6379'
    REDIS_DB: '0'
    ALLOW_EMPTY_PASSWORD: '[redacted]'
    REDIS_PASSWORD: '[redacted]'
  omitted_for_secret_safety:
  - command
---

# order_redis

Candidate extracted from Docker Compose evidence in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Compose service: `order_redis`
- Declared in: `backend/infra/redis/docker-compose.yaml`
- YAML pointer: `/services/order_redis`
- Evidence class: `implemented`

## Review notes

This page is a candidate awaiting review. It is not canonical knowledge and secret values are redacted at extraction time.
