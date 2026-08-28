---
id: database.ftgo.feedback-mongo
kind: Database
type: Database
title: feedback_mongo
status: approved
review_status: approved
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
relations:
- type: CONTAINS
  target: collection.ftgo.feedback.delivery-ratings
  collection_name: delivery_ratings
  storage_engine: mongodb
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/feedback/src/models/delivery_rating.py
  symbol: models.delivery_rating.DeliveryRating
  line_start: 10
  line_end: 39
  evidence_type: implemented
- type: CONTAINS
  target: collection.ftgo.feedback.order-ratings
  collection_name: order_ratings
  storage_engine: mongodb
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/feedback/src/models/order_rating.py
  symbol: models.order_rating.OrderRating
  line_start: 9
  line_end: 34
  evidence_type: implemented
---

# feedback_mongo

Candidate extracted from Docker Compose evidence in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Compose service: `feedback_mongo`
- Declared in: `backend/infra/mongo/docker-compose.yaml`
- YAML pointer: `/services/feedback_mongo`
- Evidence class: `implemented`

## Review notes

This page is approved canonical knowledge. Secret values are redacted at extraction time.

