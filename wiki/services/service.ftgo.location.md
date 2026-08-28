---
id: service.ftgo.location
kind: Service
type: Service
title: location_service
status: approved
review_status: approved
candidate_of: compose-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: compose
role: application
compose_service: location_service
owner: aide-ftgo-cohort
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/docker-compose.yaml
  pointer: /services/location_service
  evidence_type: implemented
relations:
- type: DEPENDS_ON
  target: database.ftgo.location-postgres
  config_key: POSTGRES_HOST
  referenced_host: location_postgres
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/docker-compose.yaml
  pointer: /services/location_service/environment/POSTGRES_HOST
  evidence_type: implemented
- type: DEPENDS_ON
  target: component.ftgo.rabbitmq
  config_key: RABBITMQ_HOST
  referenced_host: rabbitmq
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/docker-compose.yaml
  pointer: /services/location_service/environment/RABBITMQ_HOST
  evidence_type: implemented
- type: DEPENDS_ON
  target: component.ftgo.location-redis
  config_key: REDIS_HOST
  referenced_host: location_redis
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/docker-compose.yaml
  pointer: /services/location_service/environment/REDIS_HOST
  evidence_type: implemented
- type: CONSUMES
  target: event.ftgo.rabbitmq.driver.availability.available
  role: consumer
  operation: register_event
  broker_library: rabbitmq_rpc
  mechanism: rpc
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/location/src/events.py
  symbol: events.register_events
  line_start: 29
  line_end: 29
  evidence_type: implemented
  call_sites:
  - backend/microservices/location/src/events.py:29
  handlers:
  - DriverService.set_driver_available
- type: CONSUMES
  target: event.ftgo.rabbitmq.driver.availability.occupied
  role: consumer
  operation: register_event
  broker_library: rabbitmq_rpc
  mechanism: rpc
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/location/src/events.py
  symbol: events.register_events
  line_start: 29
  line_end: 29
  evidence_type: implemented
  call_sites:
  - backend/microservices/location/src/events.py:29
  handlers:
  - DriverService.set_driver_occupied
- type: CONSUMES
  target: event.ftgo.rabbitmq.driver.location.get
  role: consumer
  operation: register_event
  broker_library: rabbitmq_rpc
  mechanism: rpc
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/location/src/events.py
  symbol: events.register_events
  line_start: 29
  line_end: 29
  evidence_type: implemented
  call_sites:
  - backend/microservices/location/src/events.py:29
  handlers:
  - DriverService.get_last_location
- type: CONSUMES
  target: event.ftgo.rabbitmq.driver.location.submit
  role: consumer
  operation: register_event
  broker_library: rabbitmq_rpc
  mechanism: rpc
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/location/src/events.py
  symbol: events.register_events
  line_start: 29
  line_end: 29
  evidence_type: implemented
  call_sites:
  - backend/microservices/location/src/events.py:29
  handlers:
  - DriverService.submit_location
- type: CONSUMES
  target: event.ftgo.rabbitmq.driver.status.get
  role: consumer
  operation: register_event
  broker_library: rabbitmq_rpc
  mechanism: rpc
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/location/src/events.py
  symbol: events.register_events
  line_start: 29
  line_end: 29
  evidence_type: implemented
  call_sites:
  - backend/microservices/location/src/events.py:29
  handlers:
  - DriverService.get_driver_status
- type: CONSUMES
  target: event.ftgo.rabbitmq.driver.status.offline
  role: consumer
  operation: register_event
  broker_library: rabbitmq_rpc
  mechanism: rpc
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/location/src/events.py
  symbol: events.register_events
  line_start: 29
  line_end: 29
  evidence_type: implemented
  call_sites:
  - backend/microservices/location/src/events.py:29
  handlers:
  - DriverService.change_status_offline
- type: CONSUMES
  target: event.ftgo.rabbitmq.driver.status.online
  role: consumer
  operation: register_event
  broker_library: rabbitmq_rpc
  mechanism: rpc
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/location/src/events.py
  symbol: events.register_events
  line_start: 29
  line_end: 29
  evidence_type: implemented
  call_sites:
  - backend/microservices/location/src/events.py:29
  handlers:
  - DriverService.change_status_online
- type: CONSUMES
  target: event.ftgo.rabbitmq.location.drivers.get-nearest
  role: consumer
  operation: register_event
  broker_library: rabbitmq_rpc
  mechanism: rpc
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/location/src/events.py
  symbol: events.register_events
  line_start: 29
  line_end: 29
  evidence_type: implemented
  call_sites:
  - backend/microservices/location/src/events.py:29
  handlers:
  - TrackerService.get_nearest_drivers
attributes:
  build_context: ./microservices/location
  build_dockerfile: Dockerfile
  container_name: location_service
  networks:
  - backend-network
  env_file:
  - ./microservices/location/.env
  environment:
    ENVIRONMENT: test
    DEBUG: 'true'
    RABBITMQ_USER: rabbitmq_user
    RABBITMQ_PASS: '[redacted]'
    RABBITMQ_VHOST: /
    RABBITMQ_HOST: rabbitmq
    RABBITMQ_PORT: '5672'
    REDIS_HOST: location_redis
    REDIS_PORT: '6379'
    REDIS_DB: '0'
    REDIS_PASSWORD: '[redacted]'
    POSTGRES_HOST: location_postgres
    POSTGRES_PORT: '5432'
    POSTGRES_USER: location_user
    POSTGRES_PASSWORD: '[redacted]'
    POSTGRES_DB: location_database
---

# location_service

Candidate extracted from Docker Compose evidence in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Compose service: `location_service`
- Declared in: `backend/docker-compose.yaml`
- YAML pointer: `/services/location_service`
- Evidence class: `implemented`

## Runtime dependencies

- `DEPENDS_ON` -> `database.ftgo.location-postgres` (from `POSTGRES_HOST=location_postgres`)
- `DEPENDS_ON` -> `component.ftgo.rabbitmq` (from `RABBITMQ_HOST=rabbitmq`)
- `DEPENDS_ON` -> `component.ftgo.location-redis` (from `REDIS_HOST=location_redis`)

## Review notes

This page is a candidate awaiting review. It is not canonical knowledge and secret values are redacted at extraction time.

