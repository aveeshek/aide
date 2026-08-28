---
id: database.ftgo.restaurant-postgres
kind: Database
type: Database
title: restaurant_postgres
status: approved
review_status: approved
candidate_of: compose-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: compose
role: infrastructure
compose_service: restaurant_postgres
engine: postgresql
network_aliases:
- restaurant_postgres
owner: aide-ftgo-cohort
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/infra/postgres/docker-compose.yaml
  pointer: /services/restaurant_postgres
  evidence_type: implemented
attributes:
  image: postgres:16.3
  container_name: restaurant_postgres
  hostname: restaurant_postgres
  ports:
  - 5440:5432
  networks:
  - backend-network
  volumes:
  - restaurant_postgres_data:/var/lib/postgresql/data
  environment:
    POSTGRES_USER: restaurant_user
    POSTGRES_PASSWORD: '[redacted]'
    POSTGRES_DB: restaurant_database
relations:
- type: CONTAINS
  target: table.ftgo.restaurant.menu-item
  table_name: menu_item
  storage_engine: postgresql
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/restaurant/src/models/menu.py
  symbol: models.menu.MenuItem
  line_start: 8
  line_end: 21
  evidence_type: implemented
- type: CONTAINS
  target: table.ftgo.restaurant.supplier-profile
  table_name: supplier_profile
  storage_engine: postgresql
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/restaurant/src/models/supplier.py
  symbol: models.supplier.Supplier
  line_start: 10
  line_end: 25
  evidence_type: implemented
---

# restaurant_postgres

Candidate extracted from Docker Compose evidence in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Compose service: `restaurant_postgres`
- Declared in: `backend/infra/postgres/docker-compose.yaml`
- YAML pointer: `/services/restaurant_postgres`
- Evidence class: `implemented`

## Review notes

This page is approved canonical knowledge. Secret values are redacted at extraction time.

