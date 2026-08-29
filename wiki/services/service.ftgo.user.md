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
- type: READS
  target: table.ftgo.user.customer-address
  role: read
  target_kind: Table
  persistence_library: sqlalchemy
  call_site_count: 3
  call_sites:
  - operation: select
    resolution: model_map_enumeration
    call: select(model_class)
    repository: ftgo
    commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
    path: backend/microservices/user/src/data_access/repository/db_repository.py
    symbol: data_access.repository.db_repository.DatabaseRepository.fetch
    line_start: 55
    line_end: 55
    evidence_type: implemented
  - operation: select
    resolution: model_map_enumeration
    call: select(model_class)
    repository: ftgo
    commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
    path: backend/microservices/user/src/data_access/repository/db_repository.py
    symbol: data_access.repository.db_repository.DatabaseRepository.update
    line_start: 97
    line_end: 97
    evidence_type: implemented
  - operation: select
    resolution: model_map_enumeration
    call: select(model_class)
    repository: ftgo
    commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
    path: backend/microservices/user/src/data_access/repository/db_repository.py
    symbol: data_access.repository.db_repository.DatabaseRepository.delete
    line_start: 121
    line_end: 121
    evidence_type: implemented
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/user/src/data_access/repository/db_repository.py
  symbol: data_access.repository.db_repository.DatabaseRepository.fetch
  line_start: 55
  line_end: 55
  evidence_type: implemented
- type: READS
  target: table.ftgo.user.user-profile
  role: read
  target_kind: Table
  persistence_library: sqlalchemy
  call_site_count: 3
  call_sites:
  - operation: select
    resolution: model_map_enumeration
    call: select(model_class)
    repository: ftgo
    commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
    path: backend/microservices/user/src/data_access/repository/db_repository.py
    symbol: data_access.repository.db_repository.DatabaseRepository.fetch
    line_start: 55
    line_end: 55
    evidence_type: implemented
  - operation: select
    resolution: model_map_enumeration
    call: select(model_class)
    repository: ftgo
    commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
    path: backend/microservices/user/src/data_access/repository/db_repository.py
    symbol: data_access.repository.db_repository.DatabaseRepository.update
    line_start: 97
    line_end: 97
    evidence_type: implemented
  - operation: select
    resolution: model_map_enumeration
    call: select(model_class)
    repository: ftgo
    commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
    path: backend/microservices/user/src/data_access/repository/db_repository.py
    symbol: data_access.repository.db_repository.DatabaseRepository.delete
    line_start: 121
    line_end: 121
    evidence_type: implemented
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/user/src/data_access/repository/db_repository.py
  symbol: data_access.repository.db_repository.DatabaseRepository.fetch
  line_start: 55
  line_end: 55
  evidence_type: implemented
- type: READS
  target: table.ftgo.user.vehicle-info
  role: read
  target_kind: Table
  persistence_library: sqlalchemy
  call_site_count: 3
  call_sites:
  - operation: select
    resolution: model_map_enumeration
    call: select(model_class)
    repository: ftgo
    commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
    path: backend/microservices/user/src/data_access/repository/db_repository.py
    symbol: data_access.repository.db_repository.DatabaseRepository.fetch
    line_start: 55
    line_end: 55
    evidence_type: implemented
  - operation: select
    resolution: model_map_enumeration
    call: select(model_class)
    repository: ftgo
    commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
    path: backend/microservices/user/src/data_access/repository/db_repository.py
    symbol: data_access.repository.db_repository.DatabaseRepository.update
    line_start: 97
    line_end: 97
    evidence_type: implemented
  - operation: select
    resolution: model_map_enumeration
    call: select(model_class)
    repository: ftgo
    commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
    path: backend/microservices/user/src/data_access/repository/db_repository.py
    symbol: data_access.repository.db_repository.DatabaseRepository.delete
    line_start: 121
    line_end: 121
    evidence_type: implemented
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/user/src/data_access/repository/db_repository.py
  symbol: data_access.repository.db_repository.DatabaseRepository.fetch
  line_start: 55
  line_end: 55
  evidence_type: implemented
- type: WRITES
  target: table.ftgo.user.customer-address
  role: write
  target_kind: Table
  persistence_library: asyncpg_client
  call_site_count: 3
  call_sites:
  - operation: add_all
    resolution: model_map_enumeration
    call: session.add_all(model_instances)
    repository: ftgo
    commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
    path: backend/microservices/user/src/data_access/repository/db_repository.py
    symbol: data_access.repository.db_repository.DatabaseRepository.insert
    line_start: 74
    line_end: 74
    evidence_type: implemented
  - operation: add
    resolution: model_map_enumeration
    call: session.add(record)
    repository: ftgo
    commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
    path: backend/microservices/user/src/data_access/repository/db_repository.py
    symbol: data_access.repository.db_repository.DatabaseRepository.update
    line_start: 105
    line_end: 105
    evidence_type: implemented
  - operation: delete
    resolution: model_map_enumeration
    call: session.delete(record)
    repository: ftgo
    commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
    path: backend/microservices/user/src/data_access/repository/db_repository.py
    symbol: data_access.repository.db_repository.DatabaseRepository.delete
    line_start: 127
    line_end: 127
    evidence_type: implemented
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/user/src/data_access/repository/db_repository.py
  symbol: data_access.repository.db_repository.DatabaseRepository.insert
  line_start: 74
  line_end: 74
  evidence_type: implemented
- type: WRITES
  target: table.ftgo.user.user-profile
  role: write
  target_kind: Table
  persistence_library: asyncpg_client
  call_site_count: 3
  call_sites:
  - operation: add_all
    resolution: model_map_enumeration
    call: session.add_all(model_instances)
    repository: ftgo
    commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
    path: backend/microservices/user/src/data_access/repository/db_repository.py
    symbol: data_access.repository.db_repository.DatabaseRepository.insert
    line_start: 74
    line_end: 74
    evidence_type: implemented
  - operation: add
    resolution: model_map_enumeration
    call: session.add(record)
    repository: ftgo
    commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
    path: backend/microservices/user/src/data_access/repository/db_repository.py
    symbol: data_access.repository.db_repository.DatabaseRepository.update
    line_start: 105
    line_end: 105
    evidence_type: implemented
  - operation: delete
    resolution: model_map_enumeration
    call: session.delete(record)
    repository: ftgo
    commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
    path: backend/microservices/user/src/data_access/repository/db_repository.py
    symbol: data_access.repository.db_repository.DatabaseRepository.delete
    line_start: 127
    line_end: 127
    evidence_type: implemented
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/user/src/data_access/repository/db_repository.py
  symbol: data_access.repository.db_repository.DatabaseRepository.insert
  line_start: 74
  line_end: 74
  evidence_type: implemented
- type: WRITES
  target: table.ftgo.user.vehicle-info
  role: write
  target_kind: Table
  persistence_library: asyncpg_client
  call_site_count: 3
  call_sites:
  - operation: add_all
    resolution: model_map_enumeration
    call: session.add_all(model_instances)
    repository: ftgo
    commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
    path: backend/microservices/user/src/data_access/repository/db_repository.py
    symbol: data_access.repository.db_repository.DatabaseRepository.insert
    line_start: 74
    line_end: 74
    evidence_type: implemented
  - operation: add
    resolution: model_map_enumeration
    call: session.add(record)
    repository: ftgo
    commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
    path: backend/microservices/user/src/data_access/repository/db_repository.py
    symbol: data_access.repository.db_repository.DatabaseRepository.update
    line_start: 105
    line_end: 105
    evidence_type: implemented
  - operation: delete
    resolution: model_map_enumeration
    call: session.delete(record)
    repository: ftgo
    commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
    path: backend/microservices/user/src/data_access/repository/db_repository.py
    symbol: data_access.repository.db_repository.DatabaseRepository.delete
    line_start: 127
    line_end: 127
    evidence_type: implemented
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/user/src/data_access/repository/db_repository.py
  symbol: data_access.repository.db_repository.DatabaseRepository.insert
  line_start: 74
  line_end: 74
  evidence_type: implemented
- type: PARTICIPATES_IN
  target: flow.ftgo.gateway.delete.address.delete
  completeness: resolved
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/customer/address.py
  symbol: application.routes.customer.address.delete_address
  line_start: 66
  line_end: 85
  evidence_type: implemented
- type: PARTICIPATES_IN
  target: flow.ftgo.gateway.delete.profile.delete
  completeness: resolved
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/account/profile.py
  symbol: application.routes.account.profile.delete_account
  line_start: 65
  line_end: 81
  evidence_type: implemented
- type: PARTICIPATES_IN
  target: flow.ftgo.gateway.delete.vehicle.delete
  completeness: resolved
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/driver/vehicle.py
  symbol: application.routes.driver.vehicle.delete
  line_start: 63
  line_end: 83
  evidence_type: implemented
- type: PARTICIPATES_IN
  target: flow.ftgo.gateway.get.address.get-all-info
  completeness: resolved
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/customer/address.py
  symbol: application.routes.customer.address.get_all_addresses
  line_start: 22
  line_end: 39
  evidence_type: implemented
- type: PARTICIPATES_IN
  target: flow.ftgo.gateway.get.profile.user-info
  completeness: resolved
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/account/profile.py
  symbol: application.routes.account.profile.get_info
  line_start: 39
  line_end: 63
  evidence_type: implemented
- type: PARTICIPATES_IN
  target: flow.ftgo.gateway.get.vehicle.get-info
  completeness: resolved
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/driver/vehicle.py
  symbol: application.routes.driver.vehicle.get_info
  line_start: 42
  line_end: 60
  evidence_type: implemented
- type: PARTICIPATES_IN
  target: flow.ftgo.gateway.post.address.add
  completeness: resolved
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/customer/address.py
  symbol: application.routes.customer.address.add_address
  line_start: 42
  line_end: 63
  evidence_type: implemented
- type: PARTICIPATES_IN
  target: flow.ftgo.gateway.post.address.set-preferred
  completeness: resolved
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/customer/address.py
  symbol: application.routes.customer.address.set_address_preferency
  line_start: 88
  line_end: 110
  evidence_type: implemented
- type: PARTICIPATES_IN
  target: flow.ftgo.gateway.post.auth.login
  completeness: resolved
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/auth/registration.py
  symbol: application.routes.auth.registration.login
  line_start: 78
  line_end: 100
  evidence_type: implemented
- type: PARTICIPATES_IN
  target: flow.ftgo.gateway.post.auth.register
  completeness: resolved
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/auth/registration.py
  symbol: application.routes.auth.registration.register
  line_start: 21
  line_end: 40
  evidence_type: implemented
- type: PARTICIPATES_IN
  target: flow.ftgo.gateway.post.auth.resend-code
  completeness: partial
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/auth/registration.py
  symbol: application.routes.auth.registration.resend_auth_code
  line_start: 60
  line_end: 76
  evidence_type: implemented
- type: PARTICIPATES_IN
  target: flow.ftgo.gateway.post.auth.verify
  completeness: resolved
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/auth/registration.py
  symbol: application.routes.auth.registration.verify_account
  line_start: 42
  line_end: 58
  evidence_type: implemented
- type: PARTICIPATES_IN
  target: flow.ftgo.gateway.post.profile.logout
  completeness: resolved
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/account/profile.py
  symbol: application.routes.account.profile.logout
  line_start: 21
  line_end: 37
  evidence_type: implemented
- type: PARTICIPATES_IN
  target: flow.ftgo.gateway.post.vehicle.register
  completeness: resolved
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/driver/vehicle.py
  symbol: application.routes.driver.vehicle.register
  line_start: 17
  line_end: 39
  evidence_type: implemented
- type: PARTICIPATES_IN
  target: flow.ftgo.gateway.put.profile.update
  completeness: resolved
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/account/profile.py
  symbol: application.routes.account.profile.update_profile
  line_start: 85
  line_end: 106
  evidence_type: implemented
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

This page is approved canonical knowledge. Secret values are redacted at extraction time.

