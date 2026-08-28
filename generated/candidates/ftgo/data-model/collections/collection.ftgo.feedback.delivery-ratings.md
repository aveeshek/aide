---
id: collection.ftgo.feedback.delivery-ratings
kind: Collection
type: Collection
title: delivery_ratings
status: candidate
review_status: pending
candidate_of: data-model-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: data-model
service: service.ftgo.feedback
owner: aide-ftgo-cohort
collection_name: delivery_ratings
storage_engine: mongodb
persistence_library: beanie
database: database.ftgo.feedback-mongo
schema: schema.ftgo.feedback.persistence.models.delivery-rating.deliveryrating
model_class: models.delivery_rating.DeliveryRating
declared_indexes:
- delivery_rating_delivery_id_index
- delivery_rating_order_id_index
- delivery_rating_customer_id_index
- delivery_rating_driver_id_index
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/feedback/src/models/delivery_rating.py
  symbol: models.delivery_rating.DeliveryRating
  line_start: 10
  line_end: 39
  evidence_type: implemented
inbound_relations:
- type: CONTAINS
  source: database.ftgo.feedback-mongo
  collection_name: delivery_ratings
  storage_engine: mongodb
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/feedback/src/models/delivery_rating.py
  symbol: models.delivery_rating.DeliveryRating
  line_start: 10
  line_end: 39
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
    call: DeliveryRatingModel.find_all(customer_id=customer_id)
    repository: ftgo
    commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
    path: backend/microservices/feedback/src/domain/delivery_rating.py
    symbol: domain.delivery_rating.DeliveryRatingHandler.get_customer_delivery_ratings
    line_start: 51
    line_end: 51
    evidence_type: implemented
  - operation: find_all
    resolution: direct_model_reference
    call: DeliveryRatingModel.find_all(driver_id=driver_id)
    repository: ftgo
    commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
    path: backend/microservices/feedback/src/domain/delivery_rating.py
    symbol: domain.delivery_rating.DeliveryRatingHandler.get_driver_delivery_ratings
    line_start: 61
    line_end: 61
    evidence_type: implemented
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/feedback/src/domain/delivery_rating.py
  symbol: domain.delivery_rating.DeliveryRatingHandler.get_customer_delivery_ratings
  line_start: 51
  line_end: 51
  evidence_type: implemented
relations:
- type: USES_SCHEMA
  target: schema.ftgo.feedback.persistence.models.delivery-rating.deliveryrating
  model_class: models.delivery_rating.DeliveryRating
  persistence_role: document_model
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/feedback/src/models/delivery_rating.py
  symbol: models.delivery_rating.DeliveryRating
  line_start: 10
  line_end: 39
  evidence_type: implemented
attributes:
  persistence_role: document_model
  storage_engine: mongodb
  document_base: Document
---

# delivery_ratings

Candidate MongoDB collection extracted from an explicit ODM collection name in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Owning service: `service.ftgo.feedback`
- Database: `database.ftgo.feedback-mongo`
- Document schema: `schema.ftgo.feedback.persistence.models.delivery-rating.deliveryrating`
- Model class: `models.delivery_rating.DeliveryRating`
- Persistence library: `beanie`
- Declared in: `backend/microservices/feedback/src/models/delivery_rating.py` (lines 10-39)
- Evidence class: `implemented`

## Review notes

This page is a candidate awaiting review. The collection name comes from an explicit ODM `Settings` declaration; the document model itself is the linked `Schema`, and no `Column` entity is created for a document field.

