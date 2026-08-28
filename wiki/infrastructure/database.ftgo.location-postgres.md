---
id: database.ftgo.location-postgres
kind: Database
type: Database
title: location_postgres
status: approved
review_status: approved
candidate_of: compose-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: compose
role: infrastructure
compose_service: location_postgres
engine: postgresql
network_aliases:
- location_postgres
owner: aide-ftgo-cohort
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/infra/postgres/docker-compose.yaml
  pointer: /services/location_postgres
  evidence_type: implemented
attributes:
  image: postgres:16.3
  container_name: location_postgres
  hostname: location_postgres
  ports:
  - 5439:5432
  networks:
  - backend-network
  volumes:
  - location_postgres_data:/var/lib/postgresql/data
  environment:
    POSTGRES_USER: location_user
    POSTGRES_PASSWORD: '[redacted]'
    POSTGRES_DB: location_database
relations:
- type: CONTAINS
  target: table.ftgo.location.driver-location
  table_name: driver_location
  storage_engine: postgresql
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/location/src/data_access/models/driver_location.py
  symbol: data_access.models.driver_location.DriverLocation
  line_start: 11
  line_end: 49
  evidence_type: implemented
---

# location_postgres

Candidate extracted from Docker Compose evidence in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Compose service: `location_postgres`
- Declared in: `backend/infra/postgres/docker-compose.yaml`
- YAML pointer: `/services/location_postgres`
- Evidence class: `implemented`

## Review notes

This page is approved canonical knowledge. Secret values are redacted at extraction time.

