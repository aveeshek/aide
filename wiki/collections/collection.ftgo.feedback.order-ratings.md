---
id: collection.ftgo.feedback.order-ratings
kind: Collection
type: Collection
title: order_ratings
status: approved
review_status: approved
candidate_of: data-model-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: data-model
service: service.ftgo.feedback
owner: aide-ftgo-cohort
collection_name: order_ratings
storage_engine: mongodb
persistence_library: beanie
database: database.ftgo.feedback-mongo
schema: schema.ftgo.feedback.persistence.models.order-rating.orderrating
model_class: models.order_rating.OrderRating
declared_indexes:
- order_rating_order_id_index
- order_rating_customer_id_index
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/feedback/src/models/order_rating.py
  symbol: models.order_rating.OrderRating
  line_start: 9
  line_end: 34
  evidence_type: implemented
inbound_relations:
- type: CONTAINS
  source: database.ftgo.feedback-mongo
  collection_name: order_ratings
  storage_engine: mongodb
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/feedback/src/models/order_rating.py
  symbol: models.order_rating.OrderRating
  line_start: 9
  line_end: 34
  evidence_type: implemented
- type: READS
  source: service.ftgo.feedback
  role: read
  target_kind: Collection
  persistence_library: beanie
  call_site_count: 2
  call_sites:
  - operation: find_all
    resolution: direct_model_reference
    call: OrderRatingModel.find_all(customer_id=customer_id)
    repository: ftgo
    commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
    path: backend/microservices/feedback/src/domain/order_rating.py
    symbol: domain.order_rating.OrderRatingHandler.get_customer_order_ratings
    line_start: 57
    line_end: 57
    evidence_type: implemented
  - operation: find_all
    resolution: direct_model_reference
    call: OrderRatingModel.find_all(restaurant_id=restaurant_id)
    repository: ftgo
    commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
    path: backend/microservices/feedback/src/domain/order_rating.py
    symbol: domain.order_rating.OrderRatingHandler.get_restaurant_order_ratings
    line_start: 67
    line_end: 67
    evidence_type: implemented
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/feedback/src/domain/order_rating.py
  symbol: domain.order_rating.OrderRatingHandler.get_customer_order_ratings
  line_start: 57
  line_end: 57
  evidence_type: implemented
relations:
- type: USES_SCHEMA
  target: schema.ftgo.feedback.persistence.models.order-rating.orderrating
  model_class: models.order_rating.OrderRating
  persistence_role: document_model
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/feedback/src/models/order_rating.py
  symbol: models.order_rating.OrderRating
  line_start: 9
  line_end: 34
  evidence_type: implemented
attributes:
  persistence_role: document_model
  storage_engine: mongodb
  document_base: Document
---

# order_ratings

Canonical MongoDB collection extracted from an explicit ODM collection name in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Owning service: `service.ftgo.feedback`
- Database: `database.ftgo.feedback-mongo`
- Document schema: `schema.ftgo.feedback.persistence.models.order-rating.orderrating`
- Model class: `models.order_rating.OrderRating`
- Persistence library: `beanie`
- Declared in: `backend/microservices/feedback/src/models/order_rating.py` (lines 9-34)
- Evidence class: `implemented`

## Review notes

This page was promoted to canonical knowledge after review. The collection name comes from an explicit ODM `Settings` declaration; the document model itself is the linked `Schema`, and no `Column` entity is created for a document field.

