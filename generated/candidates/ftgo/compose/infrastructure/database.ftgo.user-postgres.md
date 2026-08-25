---
id: database.ftgo.user-postgres
kind: Database
type: Database
title: user_postgres
status: candidate
review_status: pending
candidate_of: compose-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: compose
role: infrastructure
compose_service: user_postgres
engine: postgresql
network_aliases:
- user_postgres
owner: aide-ftgo-cohort
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/infra/postgres/docker-compose.yaml
  pointer: /services/user_postgres
  evidence_type: implemented
attributes:
  image: postgres:16.3
  container_name: user_postgres
  hostname: user_postgres
  ports:
  - 5438:5432
  networks:
  - backend-network
  volumes:
  - user_postgres_data:/var/lib/postgresql/data
  environment:
    POSTGRES_USER: user_user
    POSTGRES_PASSWORD: '[redacted]'
    POSTGRES_DB: user_database
---

# user_postgres

Candidate extracted from Docker Compose evidence in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Compose service: `user_postgres`
- Declared in: `backend/infra/postgres/docker-compose.yaml`
- YAML pointer: `/services/user_postgres`
- Evidence class: `implemented`

## Review notes

This page is a candidate awaiting review. It is not canonical knowledge and secret values are redacted at extraction time.
