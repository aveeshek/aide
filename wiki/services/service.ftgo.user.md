---
id: service.ftgo.user
kind: Service
type: Service
title: user_service
status: approved
review_status: approved
candidate_of: compose-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: compose
role: application
compose_service: user_service
owner: aide-ftgo-cohort
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/docker-compose.yaml
  pointer: /services/user_service
  evidence_type: implemented
relations:
- type: DEPENDS_ON
  target: database.ftgo.user-postgres
  config_key: POSTGRES_HOST
  referenced_host: user_postgres
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/docker-compose.yaml
  pointer: /services/user_service/environment/POSTGRES_HOST
  evidence_type: implemented
- type: DEPENDS_ON
  target: component.ftgo.rabbitmq
  config_key: RABBITMQ_HOST
  referenced_host: rabbitmq
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/docker-compose.yaml
  pointer: /services/user_service/environment/RABBITMQ_HOST
  evidence_type: implemented
- type: DEPENDS_ON
  target: component.ftgo.user-redis
  config_key: REDIS_HOST
  referenced_host: user_redis
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/docker-compose.yaml
  pointer: /services/user_service/environment/REDIS_HOST
  evidence_type: implemented
- type: CONSUMES
  target: event.ftgo.rabbitmq.driver.vehicle.delete
  role: consumer
  operation: register_event
  broker_library: rabbitmq_rpc
  mechanism: rpc
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/user/src/events.py
  symbol: events.register_events
  line_start: 39
  line_end: 39
  evidence_type: implemented
  call_sites:
  - backend/microservices/user/src/events.py:39
  handlers:
  - VehicleService.delete_vehicle
- type: CONSUMES
  target: event.ftgo.rabbitmq.driver.vehicle.get-info
  role: consumer
  operation: register_event
  broker_library: rabbitmq_rpc
  mechanism: rpc
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/user/src/events.py
  symbol: events.register_events
  line_start: 39
  line_end: 39
  evidence_type: implemented
  call_sites:
  - backend/microservices/user/src/events.py:39
  handlers:
  - VehicleService.get_vehicle_info
- type: CONSUMES
  target: event.ftgo.rabbitmq.driver.vehicle.register
  role: consumer
  operation: register_event
  broker_library: rabbitmq_rpc
  mechanism: rpc
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/user/src/events.py
  symbol: events.register_events
  line_start: 39
  line_end: 39
  evidence_type: implemented
  call_sites:
  - backend/microservices/user/src/events.py:39
  handlers:
  - VehicleService.register_vehicle
- type: CONSUMES
  target: event.ftgo.rabbitmq.user.address.add-address
  role: consumer
  operation: register_event
  broker_library: rabbitmq_rpc
  mechanism: rpc
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/user/src/events.py
  symbol: events.register_events
  line_start: 39
  line_end: 39
  evidence_type: implemented
  call_sites:
  - backend/microservices/user/src/events.py:39
  handlers:
  - AddressService.add_address
- type: CONSUMES
  target: event.ftgo.rabbitmq.user.address.delete
  role: consumer
  operation: register_event
  broker_library: rabbitmq_rpc
  mechanism: rpc
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/user/src/events.py
  symbol: events.register_events
  line_start: 39
  line_end: 39
  evidence_type: implemented
  call_sites:
  - backend/microservices/user/src/events.py:39
  handlers:
  - AddressService.delete_address
- type: CONSUMES
  target: event.ftgo.rabbitmq.user.address.get-address-info
  role: consumer
  operation: register_event
  broker_library: rabbitmq_rpc
  mechanism: rpc
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/user/src/events.py
  symbol: events.register_events
  line_start: 39
  line_end: 39
  evidence_type: implemented
  call_sites:
  - backend/microservices/user/src/events.py:39
  handlers:
  - AddressService.get_address_info
- type: CONSUMES
  target: event.ftgo.rabbitmq.user.address.get-all-addresses
  role: consumer
  operation: register_event
  broker_library: rabbitmq_rpc
  mechanism: rpc
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/user/src/events.py
  symbol: events.register_events
  line_start: 39
  line_end: 39
  evidence_type: implemented
  call_sites:
  - backend/microservices/user/src/events.py:39
  handlers:
  - AddressService.get_all_addresses
- type: CONSUMES
  target: event.ftgo.rabbitmq.user.address.get-default-address
  role: consumer
  operation: register_event
  broker_library: rabbitmq_rpc
  mechanism: rpc
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/user/src/events.py
  symbol: events.register_events
  line_start: 39
  line_end: 39
  evidence_type: implemented
  call_sites:
  - backend/microservices/user/src/events.py:39
  handlers:
  - AddressService.get_default_address
- type: CONSUMES
  target: event.ftgo.rabbitmq.user.address.set-preferred-address
  role: consumer
  operation: register_event
  broker_library: rabbitmq_rpc
  mechanism: rpc
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/user/src/events.py
  symbol: events.register_events
  line_start: 39
  line_end: 39
  evidence_type: implemented
  call_sites:
  - backend/microservices/user/src/events.py:39
  handlers:
  - AddressService.set_preferred_address
- type: CONSUMES
  target: event.ftgo.rabbitmq.user.address.update-information
  role: consumer
  operation: register_event
  broker_library: rabbitmq_rpc
  mechanism: rpc
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/user/src/events.py
  symbol: events.register_events
  line_start: 39
  line_end: 39
  evidence_type: implemented
  call_sites:
  - backend/microservices/user/src/events.py:39
  handlers:
  - AddressService.update_information
- type: CONSUMES
  target: event.ftgo.rabbitmq.user.profile.create
  role: consumer
  operation: register_event
  broker_library: rabbitmq_rpc
  mechanism: rpc
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/user/src/events.py
  symbol: events.register_events
  line_start: 39
  line_end: 39
  evidence_type: implemented
  call_sites:
  - backend/microservices/user/src/events.py:39
  handlers:
  - ProfileService.register
- type: CONSUMES
  target: event.ftgo.rabbitmq.user.profile.delete-account
  role: consumer
  operation: register_event
  broker_library: rabbitmq_rpc
  mechanism: rpc
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/user/src/events.py
  symbol: events.register_events
  line_start: 39
  line_end: 39
  evidence_type: implemented
  call_sites:
  - backend/microservices/user/src/events.py:39
  handlers:
  - ProfileService.delete_account
- type: CONSUMES
  target: event.ftgo.rabbitmq.user.profile.get-info
  role: consumer
  operation: register_event
  broker_library: rabbitmq_rpc
  mechanism: rpc
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/user/src/events.py
  symbol: events.register_events
  line_start: 39
  line_end: 39
  evidence_type: implemented
  call_sites:
  - backend/microservices/user/src/events.py:39
  handlers:
  - ProfileService.get_info
- type: CONSUMES
  target: event.ftgo.rabbitmq.user.profile.login
  role: consumer
  operation: register_event
  broker_library: rabbitmq_rpc
  mechanism: rpc
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/user/src/events.py
  symbol: events.register_events
  line_start: 39
  line_end: 39
  evidence_type: implemented
  call_sites:
  - backend/microservices/user/src/events.py:39
  handlers:
  - ProfileService.login
- type: CONSUMES
  target: event.ftgo.rabbitmq.user.profile.logout
  role: consumer
  operation: register_event
  broker_library: rabbitmq_rpc
  mechanism: rpc
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/user/src/events.py
  symbol: events.register_events
  line_start: 39
  line_end: 39
  evidence_type: implemented
  call_sites:
  - backend/microservices/user/src/events.py:39
  handlers:
  - ProfileService.logout
- type: CONSUMES
  target: event.ftgo.rabbitmq.user.profile.resend-auth-code
  role: consumer
  operation: register_event
  broker_library: rabbitmq_rpc
  mechanism: rpc
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/user/src/events.py
  symbol: events.register_events
  line_start: 39
  line_end: 39
  evidence_type: implemented
  call_sites:
  - backend/microservices/user/src/events.py:39
  handlers:
  - ProfileService.resend_auth_code
- type: CONSUMES
  target: event.ftgo.rabbitmq.user.profile.update-profile
  role: consumer
  operation: register_event
  broker_library: rabbitmq_rpc
  mechanism: rpc
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/user/src/events.py
  symbol: events.register_events
  line_start: 39
  line_end: 39
  evidence_type: implemented
  call_sites:
  - backend/microservices/user/src/events.py:39
  handlers:
  - ProfileService.update_profile
- type: CONSUMES
  target: event.ftgo.rabbitmq.user.profile.verify-account
  role: consumer
  operation: register_event
  broker_library: rabbitmq_rpc
  mechanism: rpc
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/user/src/events.py
  symbol: events.register_events
  line_start: 39
  line_end: 39
  evidence_type: implemented
  call_sites:
  - backend/microservices/user/src/events.py:39
  handlers:
  - ProfileService.verify_account
attributes:
  build_context: ./microservices/user
  build_dockerfile: Dockerfile
  container_name: user_service
  networks:
  - backend-network
  env_file:
  - ./microservices/user/.env
  environment:
    ENVIRONMENT: test
    DEBUG: 'true'
    RABBITMQ_USER: rabbitmq_user
    RABBITMQ_PASS: '[redacted]'
    RABBITMQ_VHOST: /
    RABBITMQ_HOST: rabbitmq
    RABBITMQ_PORT: '5672'
    REDIS_HOST: user_redis
    REDIS_PORT: '6379'
    REDIS_DB: '0'
    REDIS_PASSWORD: '[redacted]'
    POSTGRES_HOST: user_postgres
    POSTGRES_PORT: '5432'
    POSTGRES_USER: user_user
    POSTGRES_PASSWORD: '[redacted]'
    POSTGRES_DB: user_database
---

# user_service

Candidate extracted from Docker Compose evidence in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Compose service: `user_service`
- Declared in: `backend/docker-compose.yaml`
- YAML pointer: `/services/user_service`
- Evidence class: `implemented`

## Runtime dependencies

- `DEPENDS_ON` -> `database.ftgo.user-postgres` (from `POSTGRES_HOST=user_postgres`)
- `DEPENDS_ON` -> `component.ftgo.rabbitmq` (from `RABBITMQ_HOST=rabbitmq`)
- `DEPENDS_ON` -> `component.ftgo.user-redis` (from `REDIS_HOST=user_redis`)

## Review notes

This page is a candidate awaiting review. It is not canonical knowledge and secret values are redacted at extraction time.

