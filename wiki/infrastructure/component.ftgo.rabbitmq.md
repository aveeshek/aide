---
id: component.ftgo.rabbitmq
kind: Component
type: Component
title: rabbitmq
status: approved
review_status: approved
candidate_of: compose-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: compose
role: infrastructure
compose_service: message_broker
engine: rabbitmq
network_aliases:
- message_broker
- rabbitmq
owner: aide-ftgo-cohort
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/infra/rabbitmq/docker-compose.yaml
  pointer: /services/message_broker
  evidence_type: implemented
attributes:
  image: rabbitmq:3-management
  container_name: message_broker
  hostname: rabbitmq
  restart: always
  ports:
  - 15673:15672
  - 5673:5672
  networks:
  - backend-network
  volumes:
  - message_broker_data:/var/lib/rabbitmq
  environment:
    RABBITMQ_DEFAULT_USER: rabbitmq_user
    RABBITMQ_DEFAULT_PASS: '[redacted]'
    RABBITMQ_DEFAULT_VHOST: /
---

# rabbitmq

Candidate extracted from Docker Compose evidence in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Compose service: `message_broker`
- Declared in: `backend/infra/rabbitmq/docker-compose.yaml`
- YAML pointer: `/services/message_broker`
- Evidence class: `implemented`

## Review notes

This page is a candidate awaiting review. It is not canonical knowledge and secret values are redacted at extraction time.

