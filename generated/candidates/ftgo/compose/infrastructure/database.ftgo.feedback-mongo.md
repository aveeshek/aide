---
id: database.ftgo.feedback-mongo
kind: Database
type: Database
title: feedback_mongo
status: candidate
review_status: pending
candidate_of: compose-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: compose
role: infrastructure
compose_service: feedback_mongo
engine: mongodb
network_aliases:
- feedback_mongo
owner: aide-ftgo-cohort
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/infra/mongo/docker-compose.yaml
  pointer: /services/feedback_mongo
  evidence_type: implemented
attributes:
  image: mongo:latest
  container_name: feedback_mongo
  restart: unless-stopped
  ports:
  - 7018:27017
  networks:
  - backend-network
  volumes:
  - feedback_mongo_data:/data/db
  environment:
    MONGO_INITDB_ROOT_USERNAME: feedback_user
    MONGO_INITDB_ROOT_PASSWORD: '[redacted]'
    MONGO_INITDB_DATABASE: feedback_database
---

# feedback_mongo

Candidate extracted from Docker Compose evidence in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Compose service: `feedback_mongo`
- Declared in: `backend/infra/mongo/docker-compose.yaml`
- YAML pointer: `/services/feedback_mongo`
- Evidence class: `implemented`

## Review notes

This page is a candidate awaiting review. It is not canonical knowledge and secret values are redacted at extraction time.
