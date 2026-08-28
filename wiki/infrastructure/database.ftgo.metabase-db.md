---
id: database.ftgo.metabase-db
kind: Database
type: Database
title: metabase_db
status: approved
review_status: approved
candidate_of: compose-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: compose
role: infrastructure
compose_service: metabase_db
engine: postgresql
network_aliases:
- metabase_db
owner: aide-ftgo-cohort
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/infra/admin/docker-compose.yaml
  pointer: /services/metabase_db
  evidence_type: implemented
attributes:
  image: postgres:16.3
  container_name: metabase_db
  hostname: metabase_db
  ports:
  - 5858:5432
  networks:
  - backend-network
  volumes:
  - metabase_db_data:/var/lib/postgresql/data
  environment:
    POSTGRES_DB: metabase_db
    POSTGRES_USER: metabase_user
    POSTGRES_PASSWORD: '[redacted]'
---

# metabase_db

Candidate extracted from Docker Compose evidence in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Compose service: `metabase_db`
- Declared in: `backend/infra/admin/docker-compose.yaml`
- YAML pointer: `/services/metabase_db`
- Evidence class: `implemented`

## Review notes

This page is approved canonical knowledge. Secret values are redacted at extraction time.

