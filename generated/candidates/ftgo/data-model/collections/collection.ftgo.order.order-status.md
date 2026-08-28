---
id: collection.ftgo.order.order-status
kind: Collection
type: Collection
title: order_status
status: candidate
review_status: pending
candidate_of: data-model-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: data-model
service: service.ftgo.order
owner: aide-ftgo-cohort
collection_name: order_status
storage_engine: mongodb
persistence_library: beanie
database: database.ftgo.order-mongo
schema: schema.ftgo.order.persistence.models.order-status.orderstatus
model_class: models.order_status.OrderStatus
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
- type: CONTAINS
  source: database.ftgo.order-mongo
  collection_name: order_status
  storage_engine: mongodb
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/order/src/models/order_status.py
  symbol: models.order_status.OrderStatus
  line_start: 9
  line_end: 34
  evidence_type: implemented
- type: WRITES
  source: service.ftgo.order
  role: write
  target_kind: Collection
  persistence_library: beanie
  call_site_count: 1
  call_sites:
  - operation: insert
    resolution: class_attribute
    call: self.document.insert()
    repository: ftgo
    commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
    path: backend/microservices/order/src/domain/entities/order_status.py
    symbol: domain.entities.order_status.OrderStatus.save
    line_start: 40
    line_end: 40
    evidence_type: implemented
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/order/src/domain/entities/order_status.py
  symbol: domain.entities.order_status.OrderStatus.save
  line_start: 40
  line_end: 40
  evidence_type: implemented
relations:
- type: USES_SCHEMA
  target: schema.ftgo.order.persistence.models.order-status.orderstatus
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
---

# order_status

Candidate MongoDB collection extracted from an explicit ODM collection name in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Owning service: `service.ftgo.order`
- Database: `database.ftgo.order-mongo`
- Document schema: `schema.ftgo.order.persistence.models.order-status.orderstatus`
- Model class: `models.order_status.OrderStatus`
- Persistence library: `beanie`
- Declared in: `backend/microservices/order/src/models/order_status.py` (lines 9-34)
- Evidence class: `implemented`

## Review notes

This page is a candidate awaiting review. The collection name comes from an explicit ODM `Settings` declaration; the document model itself is the linked `Schema`, and no `Column` entity is created for a document field.

