---
id: collection.ftgo.order.orders
kind: Collection
type: Collection
title: orders
status: approved
review_status: approved
candidate_of: data-model-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: data-model
service: service.ftgo.order
owner: aide-ftgo-cohort
collection_name: orders
storage_engine: mongodb
persistence_library: beanie
database: database.ftgo.order-mongo
schema: schema.ftgo.order.persistence.models.order.order
model_class: models.order.Order
declared_indexes:
- order_customer_id_index
- order_restaurant_id_index
- order_created_at_index
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/order/src/models/order.py
  symbol: models.order.Order
  line_start: 11
  line_end: 40
  evidence_type: implemented
inbound_relations:
- type: CONTAINS
  source: database.ftgo.order-mongo
  collection_name: orders
  storage_engine: mongodb
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/order/src/models/order.py
  symbol: models.order.Order
  line_start: 11
  line_end: 40
  evidence_type: implemented
- type: WRITES
  source: service.ftgo.order
  role: write
  target_kind: Collection
  persistence_library: beanie
  call_site_count: 3
  call_sites:
  - operation: insert
    resolution: class_attribute
    call: self.document.insert()
    repository: ftgo
    commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
    path: backend/microservices/order/src/domain/entities/order.py
    symbol: domain.entities.order.Order.save
    line_start: 46
    line_end: 46
    evidence_type: implemented
  - operation: save
    resolution: class_attribute
    call: self.document.save()
    repository: ftgo
    commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
    path: backend/microservices/order/src/domain/entities/order.py
    symbol: domain.entities.order.Order.calculate_total
    line_start: 73
    line_end: 73
    evidence_type: implemented
  - operation: save
    resolution: class_attribute
    call: self.document.save()
    repository: ftgo
    commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
    path: backend/microservices/order/src/domain/entities/order.py
    symbol: domain.entities.order.Order.change_status
    line_start: 94
    line_end: 94
    evidence_type: implemented
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/order/src/domain/entities/order.py
  symbol: domain.entities.order.Order.save
  line_start: 46
  line_end: 46
  evidence_type: implemented
relations:
- type: USES_SCHEMA
  target: schema.ftgo.order.persistence.models.order.order
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
---

# orders

Canonical MongoDB collection extracted from an explicit ODM collection name in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Owning service: `service.ftgo.order`
- Database: `database.ftgo.order-mongo`
- Document schema: `schema.ftgo.order.persistence.models.order.order`
- Model class: `models.order.Order`
- Persistence library: `beanie`
- Declared in: `backend/microservices/order/src/models/order.py` (lines 11-40)
- Evidence class: `implemented`

## Review notes

This page was promoted to canonical knowledge after review. The collection name comes from an explicit ODM `Settings` declaration; the document model itself is the linked `Schema`, and no `Column` entity is created for a document field.

