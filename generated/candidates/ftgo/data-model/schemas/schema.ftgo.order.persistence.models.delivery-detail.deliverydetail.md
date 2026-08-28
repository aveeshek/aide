---
id: schema.ftgo.order.persistence.models.delivery-detail.deliverydetail
kind: Schema
type: Schema
title: DeliveryDetail
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
collection: delivery_details
model_class: models.delivery_detail.DeliveryDetail
fields:
- name: created_at
  annotation: datetime
  has_default: true
  line: 18
- name: delivery_status
  annotation: str
  required: true
  has_default: true
  line: 14
- name: destination_address_id
  annotation: str
  required: true
  has_default: false
  line: 16
- name: driver_id
  annotation: str
  required: true
  has_default: false
  line: 13
- name: order_id
  annotation: str
  required: true
  has_default: false
  line: 12
- name: source_address_id
  annotation: str
  required: true
  has_default: false
  line: 15
- name: updated_at
  annotation: datetime
  has_default: true
  line: 19
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
- type: USES_SCHEMA
  source: collection.ftgo.order.delivery-details
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
  field_count: 7
  settings_declared: true
---

# DeliveryDetail

Candidate persistent document model extracted from an ODM declaration in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Owning service: `service.ftgo.order`
- Database: `database.ftgo.order-mongo`
- Collection: `delivery_details`
- Persistence library: `beanie`
- Declared in: `backend/microservices/order/src/models/delivery_detail.py` (lines 11-38)
- Evidence class: `implemented`

## Ontology note

The ontology has no `Collection` kind, so this document model is recorded as a `Schema` with `persistence_role: document_model` and the collection name kept as an attribute. See `ontology_gaps` in the extraction report.

## Review notes

This page is a candidate awaiting review. Fields are recorded as declared source text and no default is evaluated.

