---
id: service.ftgo.restaurant
kind: Service
type: Service
title: restaurant_service
status: approved
review_status: approved
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
- type: CONSUMES
  target: event.ftgo.rabbitmq.restaurant.menu.add-item
  role: consumer
  operation: register_event
  broker_library: rabbitmq_rpc
  mechanism: rpc
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/restaurant/src/events.py
  symbol: events.register_events
  line_start: 32
  line_end: 32
  evidence_type: implemented
  call_sites:
  - backend/microservices/restaurant/src/events.py:32
  handlers:
  - MenuService.add_item
- type: CONSUMES
  target: event.ftgo.rabbitmq.restaurant.menu.delete-item
  role: consumer
  operation: register_event
  broker_library: rabbitmq_rpc
  mechanism: rpc
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/restaurant/src/events.py
  symbol: events.register_events
  line_start: 32
  line_end: 32
  evidence_type: implemented
  call_sites:
  - backend/microservices/restaurant/src/events.py:32
  handlers:
  - MenuService.delete_item
- type: CONSUMES
  target: event.ftgo.rabbitmq.restaurant.menu.get-all-menu-item
  role: consumer
  operation: register_event
  broker_library: rabbitmq_rpc
  mechanism: rpc
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/restaurant/src/events.py
  symbol: events.register_events
  line_start: 32
  line_end: 32
  evidence_type: implemented
  call_sites:
  - backend/microservices/restaurant/src/events.py:32
  handlers:
  - MenuService.get_all_menu_item
- type: CONSUMES
  target: event.ftgo.rabbitmq.restaurant.menu.get-item-info
  role: consumer
  operation: register_event
  broker_library: rabbitmq_rpc
  mechanism: rpc
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/restaurant/src/events.py
  symbol: events.register_events
  line_start: 32
  line_end: 32
  evidence_type: implemented
  call_sites:
  - backend/microservices/restaurant/src/events.py:32
  handlers:
  - MenuService.get_item_info
- type: CONSUMES
  target: event.ftgo.rabbitmq.restaurant.menu.update-item
  role: consumer
  operation: register_event
  broker_library: rabbitmq_rpc
  mechanism: rpc
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/restaurant/src/events.py
  symbol: events.register_events
  line_start: 32
  line_end: 32
  evidence_type: implemented
  call_sites:
  - backend/microservices/restaurant/src/events.py:32
  handlers:
  - MenuService.update_item
- type: CONSUMES
  target: event.ftgo.rabbitmq.restaurant.supplier.delete-restaurant
  role: consumer
  operation: register_event
  broker_library: rabbitmq_rpc
  mechanism: rpc
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/restaurant/src/events.py
  symbol: events.register_events
  line_start: 32
  line_end: 32
  evidence_type: implemented
  call_sites:
  - backend/microservices/restaurant/src/events.py:32
  handlers:
  - RestaurantService.delete_restaurant
- type: CONSUMES
  target: event.ftgo.rabbitmq.restaurant.supplier.get-all-restaurant-info
  role: consumer
  operation: register_event
  broker_library: rabbitmq_rpc
  mechanism: rpc
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/restaurant/src/events.py
  symbol: events.register_events
  line_start: 32
  line_end: 32
  evidence_type: implemented
  call_sites:
  - backend/microservices/restaurant/src/events.py:32
  handlers:
  - RestaurantService.get_all_restaurant_info
- type: CONSUMES
  target: event.ftgo.rabbitmq.restaurant.supplier.get-restaurant-info
  role: consumer
  operation: register_event
  broker_library: rabbitmq_rpc
  mechanism: rpc
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/restaurant/src/events.py
  symbol: events.register_events
  line_start: 32
  line_end: 32
  evidence_type: implemented
  call_sites:
  - backend/microservices/restaurant/src/events.py:32
  handlers:
  - RestaurantService.get_restaurant_info
- type: CONSUMES
  target: event.ftgo.rabbitmq.restaurant.supplier.get-supplier-restaurant-info
  role: consumer
  operation: register_event
  broker_library: rabbitmq_rpc
  mechanism: rpc
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/restaurant/src/events.py
  symbol: events.register_events
  line_start: 32
  line_end: 32
  evidence_type: implemented
  call_sites:
  - backend/microservices/restaurant/src/events.py:32
  handlers:
  - RestaurantService.get_supplier_restaurant_info
- type: CONSUMES
  target: event.ftgo.rabbitmq.restaurant.supplier.register
  role: consumer
  operation: register_event
  broker_library: rabbitmq_rpc
  mechanism: rpc
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/restaurant/src/events.py
  symbol: events.register_events
  line_start: 32
  line_end: 32
  evidence_type: implemented
  call_sites:
  - backend/microservices/restaurant/src/events.py:32
  handlers:
  - RestaurantService.register
- type: CONSUMES
  target: event.ftgo.rabbitmq.restaurant.supplier.update-information
  role: consumer
  operation: register_event
  broker_library: rabbitmq_rpc
  mechanism: rpc
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/restaurant/src/events.py
  symbol: events.register_events
  line_start: 32
  line_end: 32
  evidence_type: implemented
  call_sites:
  - backend/microservices/restaurant/src/events.py:32
  handlers:
  - RestaurantService.update_information
- type: READS
  target: table.ftgo.restaurant.menu-item
  role: read
  target_kind: Table
  persistence_library: sqlalchemy
  call_site_count: 4
  call_sites:
  - operation: select
    resolution: wrapper_argument
    call: 'DatabaseRepository.fetch_by_query(MenuItem, query={"item_id": item_id},
      one_or_none=True)'
    repository: ftgo
    commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
    path: backend/microservices/restaurant/src/domain/menu.py
    symbol: domain.menu.MenuDomain.load
    line_start: 67
    line_end: 67
    evidence_type: implemented
  - operation: select
    resolution: wrapper_argument
    call: 'DatabaseRepository.update_by_query( MenuItem, query={"item_id": item_id},
      update_fields=update_fields, )'
    repository: ftgo
    commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
    path: backend/microservices/restaurant/src/domain/menu.py
    symbol: domain.menu.MenuDomain.update_item
    line_start: 95
    line_end: 99
    evidence_type: implemented
  - operation: select
    resolution: wrapper_argument
    call: 'DatabaseRepository.delete_by_query(MenuItem, query={"item_id": item_id})'
    repository: ftgo
    commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
    path: backend/microservices/restaurant/src/domain/menu.py
    symbol: domain.menu.MenuDomain.delete_item
    line_start: 113
    line_end: 113
    evidence_type: implemented
  - operation: select
    resolution: wrapper_argument
    call: 'DatabaseRepository.fetch_by_query(MenuItem, query={"restaurant_id": self.restaurant_id})'
    repository: ftgo
    commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
    path: backend/microservices/restaurant/src/domain/restaurant.py
    symbol: domain.restaurant.RestaurantDomain.load_all_menu_item
    line_start: 205
    line_end: 205
    evidence_type: implemented
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/restaurant/src/domain/menu.py
  symbol: domain.menu.MenuDomain.load
  line_start: 67
  line_end: 67
  evidence_type: implemented
- type: READS
  target: table.ftgo.restaurant.supplier-profile
  role: read
  target_kind: Table
  persistence_library: sqlalchemy
  call_site_count: 5
  call_sites:
  - operation: select
    resolution: wrapper_argument
    call: DatabaseRepository.fetch_by_query(Supplier, query=query_dict, one_or_none=True)
    repository: ftgo
    commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
    path: backend/microservices/restaurant/src/domain/restaurant.py
    symbol: domain.restaurant.RestaurantDomain.load
    line_start: 53
    line_end: 53
    evidence_type: implemented
  - operation: select
    resolution: wrapper_argument
    call: DatabaseRepository.fetch_by_query(Supplier, query={})
    repository: ftgo
    commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
    path: backend/microservices/restaurant/src/domain/restaurant.py
    symbol: domain.restaurant.RestaurantDomain.load_all
    line_start: 69
    line_end: 69
    evidence_type: implemented
  - operation: select
    resolution: wrapper_argument
    call: 'DatabaseRepository.fetch_by_query(Supplier, query={"owner_user_id": owner_user_id})'
    repository: ftgo
    commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
    path: backend/microservices/restaurant/src/domain/restaurant.py
    symbol: domain.restaurant.RestaurantDomain.register
    line_start: 88
    line_end: 88
    evidence_type: implemented
  - operation: select
    resolution: wrapper_argument
    call: 'DatabaseRepository.update_by_query( Supplier, query={"id": restaurant_id},
      update_fields=update_fields, )'
    repository: ftgo
    commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
    path: backend/microservices/restaurant/src/domain/restaurant.py
    symbol: domain.restaurant.RestaurantDomain.update_profile_information
    line_start: 139
    line_end: 143
    evidence_type: implemented
  - operation: select
    resolution: wrapper_argument
    call: 'DatabaseRepository.delete_by_query(Supplier, query={"id": self.restaurant_id})'
    repository: ftgo
    commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
    path: backend/microservices/restaurant/src/domain/restaurant.py
    symbol: domain.restaurant.RestaurantDomain.delete_restaurant
    line_start: 153
    line_end: 153
    evidence_type: implemented
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/restaurant/src/domain/restaurant.py
  symbol: domain.restaurant.RestaurantDomain.load
  line_start: 53
  line_end: 53
  evidence_type: implemented
- type: WRITES
  target: table.ftgo.restaurant.menu-item
  role: write
  target_kind: Table
  persistence_library: asyncpg_client
  call_site_count: 1
  call_sites:
  - operation: add
    resolution: wrapper_argument
    call: DatabaseRepository.insert(new_item)
    repository: ftgo
    commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
    path: backend/microservices/restaurant/src/domain/menu.py
    symbol: domain.menu.MenuDomain.add_item
    line_start: 50
    line_end: 50
    evidence_type: implemented
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/restaurant/src/domain/menu.py
  symbol: domain.menu.MenuDomain.add_item
  line_start: 50
  line_end: 50
  evidence_type: implemented
- type: WRITES
  target: table.ftgo.restaurant.supplier-profile
  role: write
  target_kind: Table
  persistence_library: asyncpg_client
  call_site_count: 1
  call_sites:
  - operation: add
    resolution: wrapper_argument
    call: DatabaseRepository.insert(new_profile)
    repository: ftgo
    commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
    path: backend/microservices/restaurant/src/domain/restaurant.py
    symbol: domain.restaurant.RestaurantDomain.register
    line_start: 105
    line_end: 105
    evidence_type: implemented
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/restaurant/src/domain/restaurant.py
  symbol: domain.restaurant.RestaurantDomain.register
  line_start: 105
  line_end: 105
  evidence_type: implemented
- type: PARTICIPATES_IN
  target: flow.ftgo.gateway.delete.menu.delete
  completeness: resolved
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/restaurant/menu.py
  symbol: application.routes.restaurant.menu.delete_item
  line_start: 88
  line_end: 107
  evidence_type: implemented
- type: PARTICIPATES_IN
  target: flow.ftgo.gateway.delete.restaurant.delete
  completeness: resolved
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/restaurant/restaurant.py
  symbol: application.routes.restaurant.restaurant.delete_restaurant
  line_start: 93
  line_end: 112
  evidence_type: implemented
- type: PARTICIPATES_IN
  target: flow.ftgo.gateway.get.menu.get-info
  completeness: resolved
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/restaurant/menu.py
  symbol: application.routes.restaurant.menu.get_info
  line_start: 43
  line_end: 63
  evidence_type: implemented
- type: PARTICIPATES_IN
  target: flow.ftgo.gateway.get.restaurant.get-all-restaurant-info
  completeness: resolved
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/restaurant/restaurant.py
  symbol: application.routes.restaurant.restaurant.get_all_restaurant_info
  line_start: 74
  line_end: 91
  evidence_type: implemented
- type: PARTICIPATES_IN
  target: flow.ftgo.gateway.get.restaurant.get-supplier-restaurant-info
  completeness: resolved
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/restaurant/restaurant.py
  symbol: application.routes.restaurant.restaurant.get_supplier_restaurant_info
  line_start: 46
  line_end: 71
  evidence_type: implemented
- type: PARTICIPATES_IN
  target: flow.ftgo.gateway.post.menu.add
  completeness: resolved
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/restaurant/menu.py
  symbol: application.routes.restaurant.menu.add_item
  line_start: 21
  line_end: 40
  evidence_type: implemented
- type: PARTICIPATES_IN
  target: flow.ftgo.gateway.post.menu.get-all-menu-item
  completeness: resolved
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/restaurant/menu.py
  symbol: application.routes.restaurant.menu.get_all_menu_item
  line_start: 109
  line_end: 128
  evidence_type: implemented
- type: PARTICIPATES_IN
  target: flow.ftgo.gateway.post.restaurant.register
  completeness: resolved
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/restaurant/restaurant.py
  symbol: application.routes.restaurant.restaurant.register
  line_start: 22
  line_end: 44
  evidence_type: implemented
- type: PARTICIPATES_IN
  target: flow.ftgo.gateway.put.menu.update
  completeness: resolved
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/restaurant/menu.py
  symbol: application.routes.restaurant.menu.update_item
  line_start: 66
  line_end: 85
  evidence_type: implemented
- type: PARTICIPATES_IN
  target: flow.ftgo.gateway.put.restaurant.update
  completeness: resolved
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/application/routes/restaurant/restaurant.py
  symbol: application.routes.restaurant.restaurant.update_information
  line_start: 115
  line_end: 133
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

This page is approved canonical knowledge. Secret values are redacted at extraction time.

