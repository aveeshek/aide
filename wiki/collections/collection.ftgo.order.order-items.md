---
id: collection.ftgo.order.order-items
kind: Collection
type: Collection
title: order_items
status: approved
review_status: approved
candidate_of: data-model-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: data-model
service: service.ftgo.order
owner: aide-ftgo-cohort
collection_name: order_items
storage_engine: mongodb
persistence_library: beanie
database: database.ftgo.order-mongo
schema: schema.ftgo.order.persistence.models.order-item.orderitem
model_class: models.order_item.OrderItem
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
- type: CONTAINS
  source: database.ftgo.order-mongo
  collection_name: order_items
  storage_engine: mongodb
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/order/src/models/order_item.py
  symbol: models.order_item.OrderItem
  line_start: 9
  line_end: 36
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
    path: backend/microservices/order/src/domain/entities/order_item.py
    symbol: domain.entities.order_item.OrderItem.save
    line_start: 42
    line_end: 42
    evidence_type: implemented
  - operation: save
    resolution: class_attribute
    call: self.document.save()
    repository: ftgo
    commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
    path: backend/microservices/order/src/domain/entities/order_item.py
    symbol: domain.entities.order_item.OrderItem.update_quantity
    line_start: 52
    line_end: 52
    evidence_type: implemented
  - operation: save
    resolution: class_attribute
    call: self.document.save()
    repository: ftgo
    commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
    path: backend/microservices/order/src/domain/entities/order_item.py
    symbol: domain.entities.order_item.OrderItem.update_item_price
    line_start: 62
    line_end: 62
    evidence_type: implemented
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/order/src/domain/entities/order_item.py
  symbol: domain.entities.order_item.OrderItem.save
  line_start: 42
  line_end: 42
  evidence_type: implemented
relations:
- type: USES_SCHEMA
  target: schema.ftgo.order.persistence.models.order-item.orderitem
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
---

# order_items

Canonical MongoDB collection extracted from an explicit ODM collection name in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Owning service: `service.ftgo.order`
- Database: `database.ftgo.order-mongo`
- Document schema: `schema.ftgo.order.persistence.models.order-item.orderitem`
- Model class: `models.order_item.OrderItem`
- Persistence library: `beanie`
- Declared in: `backend/microservices/order/src/models/order_item.py` (lines 9-36)
- Evidence class: `implemented`

## Review notes

This page was promoted to canonical knowledge after review. The collection name comes from an explicit ODM `Settings` declaration; the document model itself is the linked `Schema`, and no `Column` entity is created for a document field.

