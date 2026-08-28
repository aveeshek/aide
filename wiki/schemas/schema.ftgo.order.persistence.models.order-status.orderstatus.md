---
id: schema.ftgo.order.persistence.models.order-status.orderstatus
kind: Schema
type: Schema
title: OrderStatus
status: approved
review_status: approved
candidate_of: data-model-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: data-model
service: service.ftgo.order
owner: aide-ftgo-cohort
persistence_role: document_model
storage_engine: mongodb
persistence_library: beanie
database: database.ftgo.order-mongo
collection: order_status
model_class: models.order_status.OrderStatus
fields:
- name: changed_by
  annotation: Optional[str]
  has_default: true
  line: 12
- name: comments
  annotation: Optional[str]
  has_default: true
  line: 13
- name: created_at
  annotation: datetime
  has_default: true
  line: 15
- name: order_id
  annotation: str
  required: true
  has_default: false
  line: 10
- name: status
  annotation: str
  required: true
  has_default: true
  line: 11
- name: updated_at
  annotation: datetime
  has_default: true
  line: 16
declared_indexes:
- order_status_order_id_index
- order_status_status_index
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/order/src/models/order_status.py
  symbol: models.order_status.OrderStatus
  line_start: 9
  line_end: 34
  evidence_type: implemented
inbound_relations:
- type: USES_SCHEMA
  source: collection.ftgo.order.order-status
  model_class: models.order_status.OrderStatus
  persistence_role: document_model
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/order/src/models/order_status.py
  symbol: models.order_status.OrderStatus
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

# OrderStatus

Canonical persistent document model extracted from an ODM declaration in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Owning service: `service.ftgo.order`
- Database: `database.ftgo.order-mongo`
- Collection: `order_status`
- Persistence library: `beanie`
- Declared in: `backend/microservices/order/src/models/order_status.py` (lines 9-34)
- Evidence class: `implemented`

## Ontology note

The document model is represented as a `Schema` and linked from its first-class MongoDB `Collection` entity through `USES_SCHEMA`. The `Collection` represents physical persistence, while this `Schema` represents document structure.

## Review notes

This page was promoted to canonical knowledge after review. Fields are recorded as declared source text and no default is evaluated.

