---
id: schema.ftgo.feedback.persistence.models.delivery-rating.deliveryrating
kind: Schema
type: Schema
title: DeliveryRating
status: candidate
review_status: pending
candidate_of: data-model-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: data-model
service: service.ftgo.feedback
owner: aide-ftgo-cohort
persistence_role: document_model
storage_engine: mongodb
persistence_library: beanie
database: database.ftgo.feedback-mongo
collection: delivery_ratings
model_class: models.delivery_rating.DeliveryRating
fields:
- name: created_at
  annotation: datetime
  has_default: true
  line: 18
- name: customer_id
  annotation: str
  required: true
  has_default: true
  indexed: true
  line: 13
- name: delivery_id
  annotation: str
  required: true
  has_default: true
  indexed: true
  line: 11
- name: driver_id
  annotation: Optional[str]
  required: false
  has_default: true
  indexed: true
  line: 14
- name: feedback
  annotation: Optional[str]
  required: false
  has_default: true
  line: 16
- name: order_id
  annotation: str
  required: true
  has_default: true
  indexed: true
  line: 12
- name: rating
  annotation: int
  required: true
  has_default: true
  line: 15
- name: updated_at
  annotation: datetime
  has_default: true
  line: 19
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
- type: USES_SCHEMA
  source: collection.ftgo.feedback.delivery-ratings
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
  field_count: 8
  settings_declared: true
---

# DeliveryRating

Candidate persistent document model extracted from an ODM declaration in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Owning service: `service.ftgo.feedback`
- Database: `database.ftgo.feedback-mongo`
- Collection: `delivery_ratings`
- Persistence library: `beanie`
- Declared in: `backend/microservices/feedback/src/models/delivery_rating.py` (lines 10-39)
- Evidence class: `implemented`

## Ontology note

The ontology has no `Collection` kind, so this document model is recorded as a `Schema` with `persistence_role: document_model` and the collection name kept as an attribute. See `ontology_gaps` in the extraction report.

## Review notes

This page is a candidate awaiting review. Fields are recorded as declared source text and no default is evaluated.

