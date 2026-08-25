---
id: component.ftgo.restaurant-redis
kind: Component
type: Component
title: restaurant_redis
status: approved
review_status: approved
candidate_of: compose-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: compose
role: infrastructure
compose_service: restaurant_redis
engine: redis
network_aliases:
- restaurant_redis
owner: aide-ftgo-cohort
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/infra/redis/docker-compose.yaml
  pointer: /services/restaurant_redis
  evidence_type: implemented
attributes:
  image: redis:7.2.5
  container_name: restaurant_redis
  hostname: restaurant_redis
  restart: always
  ports:
  - 6236:6379
  networks:
  - backend-network
  volumes:
  - restaurant_redis_data:/data
  environment:
    REDIS_PORT: '6379'
    REDIS_DB: '0'
    ALLOW_EMPTY_PASSWORD: '[redacted]'
    REDIS_PASSWORD: '[redacted]'
  omitted_for_secret_safety:
  - command
---

# restaurant_redis

Candidate extracted from Docker Compose evidence in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Compose service: `restaurant_redis`
- Declared in: `backend/infra/redis/docker-compose.yaml`
- YAML pointer: `/services/restaurant_redis`
- Evidence class: `implemented`

## Review notes

This page is a candidate awaiting review. It is not canonical knowledge and secret values are redacted at extraction time.

