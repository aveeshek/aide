---
id: database.ftgo.order-mongo
kind: Database
type: Database
title: order_mongo
status: approved
review_status: approved
candidate_of: compose-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: compose
role: infrastructure
compose_service: order_mongo
engine: mongodb
network_aliases:
- order_mongo
owner: aide-ftgo-cohort
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/infra/mongo/docker-compose.yaml
  pointer: /services/order_mongo
  evidence_type: implemented
attributes:
  image: mongo:latest
  container_name: order_mongo
  restart: unless-stopped
  ports:
  - 7017:27017
  networks:
  - backend-network
  volumes:
  - order_mongo_data:/data/db
  environment:
    MONGO_INITDB_ROOT_USERNAME: order_user
    MONGO_INITDB_ROOT_PASSWORD: '[redacted]'
    MONGO_INITDB_DATABASE: order_database
relations:
- type: CONTAINS
  target: collection.ftgo.order.delivery-details
  collection_name: delivery_details
  storage_engine: mongodb
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/order/src/models/delivery_detail.py
  symbol: models.delivery_detail.DeliveryDetail
  line_start: 11
  line_end: 38
  evidence_type: implemented
- type: CONTAINS
  target: collection.ftgo.order.order-items
  collection_name: order_items
  storage_engine: mongodb
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/order/src/models/order_item.py
  symbol: models.order_item.OrderItem
  line_start: 9
  line_end: 36
  evidence_type: implemented
- type: CONTAINS
  target: collection.ftgo.order.order-status
  collection_name: order_status
  storage_engine: mongodb
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/order/src/models/order_status.py
  symbol: models.order_status.OrderStatus
  line_start: 9
  line_end: 34
  evidence_type: implemented
- type: CONTAINS
  target: collection.ftgo.order.orders
  collection_name: orders
  storage_engine: mongodb
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/order/src/models/order.py
  symbol: models.order.Order
  line_start: 11
  line_end: 40
  evidence_type: implemented
---

# order_mongo

Candidate extracted from Docker Compose evidence in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Compose service: `order_mongo`
- Declared in: `backend/infra/mongo/docker-compose.yaml`
- YAML pointer: `/services/order_mongo`
- Evidence class: `implemented`

## Review notes

This page is approved canonical knowledge. Secret values are redacted at extraction time.

