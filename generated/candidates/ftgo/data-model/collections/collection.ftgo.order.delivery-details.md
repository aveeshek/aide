---
id: collection.ftgo.order.delivery-details
kind: Collection
type: Collection
title: delivery_details
status: candidate
review_status: pending
candidate_of: data-model-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: data-model
service: service.ftgo.order
owner: aide-ftgo-cohort
collection_name: delivery_details
storage_engine: mongodb
persistence_library: beanie
database: database.ftgo.order-mongo
schema: schema.ftgo.order.persistence.models.delivery-detail.deliverydetail
model_class: models.delivery_detail.DeliveryDetail
declared_indexes:
- delivery_detail_delivery_status_index
- delivery_detail_order_id_index
- delivery_detail_driver_id_index
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/order/src/models/delivery_detail.py
  symbol: models.delivery_detail.DeliveryDetail
  line_start: 11
  line_end: 38
  evidence_type: implemented
inbound_relations:
- type: CONTAINS
  source: database.ftgo.order-mongo
  collection_name: delivery_details
  storage_engine: mongodb
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/order/src/models/delivery_detail.py
  symbol: models.delivery_detail.DeliveryDetail
  line_start: 11
  line_end: 38
  evidence_type: implemented
- type: WRITES
  source: service.ftgo.order
  role: write
  target_kind: Collection
  persistence_library: beanie
  call_site_count: 2
  call_sites:
  - operation: insert
    resolution: class_attribute
    call: self.document.insert()
    repository: ftgo
    commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
    path: backend/microservices/order/src/domain/entities/delivery.py
    symbol: domain.entities.delivery.Delivery.save
    line_start: 43
    line_end: 43
    evidence_type: implemented
  - operation: save
    resolution: class_attribute
    call: self.document.save()
    repository: ftgo
    commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
    path: backend/microservices/order/src/domain/entities/delivery.py
    symbol: domain.entities.delivery.Delivery.update_status
    line_start: 55
    line_end: 55
    evidence_type: implemented
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/order/src/domain/entities/delivery.py
  symbol: domain.entities.delivery.Delivery.save
  line_start: 43
  line_end: 43
  evidence_type: implemented
relations:
- type: USES_SCHEMA
  target: schema.ftgo.order.persistence.models.delivery-detail.deliverydetail
  model_class: models.delivery_detail.DeliveryDetail
  persistence_role: document_model
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/order/src/models/delivery_detail.py
  symbol: models.delivery_detail.DeliveryDetail
  line_start: 11
  line_end: 38
  evidence_type: implemented
attributes:
  persistence_role: document_model
  storage_engine: mongodb
  document_base: Document
---

# delivery_details

Candidate MongoDB collection extracted from an explicit ODM collection name in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Owning service: `service.ftgo.order`
- Database: `database.ftgo.order-mongo`
- Document schema: `schema.ftgo.order.persistence.models.delivery-detail.deliverydetail`
- Model class: `models.delivery_detail.DeliveryDetail`
- Persistence library: `beanie`
- Declared in: `backend/microservices/order/src/models/delivery_detail.py` (lines 11-38)
- Evidence class: `implemented`

## Review notes

This page is a candidate awaiting review. The collection name comes from an explicit ODM `Settings` declaration; the document model itself is the linked `Schema`, and no `Column` entity is created for a document field.

