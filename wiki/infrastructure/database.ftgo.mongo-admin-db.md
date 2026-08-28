---
id: database.ftgo.mongo-admin-db
kind: Database
type: Database
title: mongo_admin_db
status: approved
review_status: approved
candidate_of: compose-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: compose
role: infrastructure
compose_service: mongo_admin_db
engine: mongodb
network_aliases:
- mongo_admin_db
owner: aide-ftgo-cohort
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/infra/admin/docker-compose.yaml
  pointer: /services/mongo_admin_db
  evidence_type: implemented
attributes:
  image: mongo
  container_name: mongo_admin_db
  restart: always
  ports:
  - 27017:27017
  networks:
  - backend-network
  volumes:
  - mongo_admin_db_data:/data/db
  environment:
    MONGO_INITDB_ROOT_USERNAME: admin_user
    MONGO_INITDB_ROOT_PASSWORD: '[redacted]'
---

# mongo_admin_db

Candidate extracted from Docker Compose evidence in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Compose service: `mongo_admin_db`
- Declared in: `backend/infra/admin/docker-compose.yaml`
- YAML pointer: `/services/mongo_admin_db`
- Evidence class: `implemented`

## Review notes

This page is approved canonical knowledge. Secret values are redacted at extraction time.

