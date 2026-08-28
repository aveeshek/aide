---
id: schema.ftgo.order.persistence.models.order-item.orderitem
kind: Schema
type: Schema
title: OrderItem
status: candidate
review_status: pending
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
collection: order_items
model_class: models.order_item.OrderItem
fields:
- name: created_at
  annotation: datetime
  has_default: true
  line: 17
- name: item_price
  annotation: float
  required: true
  has_default: true
  line: 13
- name: menu_item_id
  annotation: str
  required: true
  has_default: false
  line: 11
- name: order_id
  annotation: str
  required: true
  has_default: false
  line: 10
- name: quantity
  annotation: int
  required: true
  has_default: true
  line: 12
- name: special_instructions
  annotation: Optional[str]
  has_default: true
  line: 15
- name: subtotal
  annotation: float
  required: true
  has_default: true
  line: 14
- name: updated_at
  annotation: datetime
  has_default: true
  line: 18
declared_indexes:
- order_item_order_id_index
- order_item_menu_item_id_index
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/order/src/models/order_item.py
  symbol: models.order_item.OrderItem
  line_start: 9
  line_end: 36
  evidence_type: implemented
inbound_relations:
- type: USES_SCHEMA
  source: collection.ftgo.order.order-items
  model_class: models.order_item.OrderItem
  persistence_role: document_model
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/order/src/models/order_item.py
  symbol: models.order_item.OrderItem
  line_start: 9
  line_end: 36
  evidence_type: implemented
attributes:
  persistence_role: document_model
  storage_engine: mongodb
  document_base: Document
  field_count: 8
  settings_declared: true
---

# OrderItem

Candidate persistent document model extracted from an ODM declaration in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Owning service: `service.ftgo.order`
- Database: `database.ftgo.order-mongo`
- Collection: `order_items`
- Persistence library: `beanie`
- Declared in: `backend/microservices/order/src/models/order_item.py` (lines 9-36)
- Evidence class: `implemented`

## Ontology note

The ontology has no `Collection` kind, so this document model is recorded as a `Schema` with `persistence_role: document_model` and the collection name kept as an attribute. See `ontology_gaps` in the extraction report.

## Review notes

This page is a candidate awaiting review. Fields are recorded as declared source text and no default is evaluated.

