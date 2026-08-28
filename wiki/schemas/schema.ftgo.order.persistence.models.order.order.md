---
id: schema.ftgo.order.persistence.models.order.order
kind: Schema
type: Schema
title: Order
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
collection: orders
model_class: models.order.Order
fields:
- name: created_at
  annotation: datetime
  has_default: true
  line: 20
- name: customer_id
  annotation: str
  required: true
  has_default: false
  line: 12
- name: order_items
  annotation: List[Link[OrderItem]]
  has_default: true
  references:
  - OrderItem
  line: 16
- name: payment_id
  annotation: Optional[str]
  has_default: true
  line: 18
- name: restaurant_id
  annotation: str
  required: true
  has_default: false
  line: 13
- name: special_instructions
  annotation: Optional[str]
  has_default: true
  line: 19
- name: status
  annotation: OrderStatus
  required: true
  has_default: false
  line: 15
- name: status_history
  annotation: Optional[List[Link[OrderStatus]]]
  has_default: true
  references:
  - OrderStatus
  line: 17
- name: total_amount
  annotation: float
  required: true
  has_default: true
  line: 14
- name: updated_at
  annotation: datetime
  has_default: true
  line: 21
declared_indexes:
- order_customer_id_index
- order_restaurant_id_index
- order_created_at_index
document_references:
- models.order_item.OrderItem
- models.order_status.OrderStatus
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/order/src/models/order.py
  symbol: models.order.Order
  line_start: 11
  line_end: 40
  evidence_type: implemented
inbound_relations:
- type: USES_SCHEMA
  source: collection.ftgo.order.orders
  model_class: models.order.Order
  persistence_role: document_model
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/order/src/models/order.py
  symbol: models.order.Order
  line_start: 11
  line_end: 40
  evidence_type: implemented
attributes:
  persistence_role: document_model
  storage_engine: mongodb
  document_base: Document
  field_count: 10
  settings_declared: true
---

# Order

Canonical persistent document model extracted from an ODM declaration in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Owning service: `service.ftgo.order`
- Database: `database.ftgo.order-mongo`
- Collection: `orders`
- Persistence library: `beanie`
- Declared in: `backend/microservices/order/src/models/order.py` (lines 11-40)
- Evidence class: `implemented`

## Ontology note

The document model is represented as a `Schema` and linked from its first-class MongoDB `Collection` entity through `USES_SCHEMA`. The `Collection` represents physical persistence, while this `Schema` represents document structure.

## Review notes

This page was promoted to canonical knowledge after review. Fields are recorded as declared source text and no default is evaluated.

