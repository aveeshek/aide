---
id: schema.ftgo.feedback.persistence.models.order-rating.orderrating
kind: Schema
type: Schema
title: OrderRating
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
collection: order_ratings
model_class: models.order_rating.OrderRating
fields:
- name: created_at
  annotation: datetime
  has_default: true
  line: 15
- name: customer_id
  annotation: str
  required: true
  has_default: true
  indexed: true
  line: 11
- name: feedback
  annotation: Optional[str]
  required: false
  has_default: true
  line: 13
- name: order_id
  annotation: str
  required: true
  has_default: true
  indexed: true
  line: 10
- name: rating
  annotation: int
  required: true
  has_default: true
  line: 12
- name: updated_at
  annotation: datetime
  has_default: true
  line: 16
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
- type: USES_SCHEMA
  source: collection.ftgo.feedback.order-ratings
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
  field_count: 6
  settings_declared: true
---

# OrderRating

Candidate persistent document model extracted from an ODM declaration in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Owning service: `service.ftgo.feedback`
- Database: `database.ftgo.feedback-mongo`
- Collection: `order_ratings`
- Persistence library: `beanie`
- Declared in: `backend/microservices/feedback/src/models/order_rating.py` (lines 9-34)
- Evidence class: `implemented`

## Ontology note

The ontology has no `Collection` kind, so this document model is recorded as a `Schema` with `persistence_role: document_model` and the collection name kept as an attribute. See `ontology_gaps` in the extraction report.

## Review notes

This page is a candidate awaiting review. Fields are recorded as declared source text and no default is evaluated.

