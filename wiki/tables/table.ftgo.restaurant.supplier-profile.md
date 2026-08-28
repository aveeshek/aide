---
id: table.ftgo.restaurant.supplier-profile
kind: Table
type: Table
title: supplier_profile
status: approved
review_status: approved
candidate_of: data-model-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: data-model
service: service.ftgo.restaurant
owner: aide-ftgo-cohort
table_name: supplier_profile
storage_engine: postgresql
persistence_library: sqlalchemy
database: database.ftgo.restaurant-postgres
model_class: models.supplier.Supplier
primary_key:
- id
orm_relationships:
- attribute: menu
  line: 25
  target: '"MenuItem"'
  back_populates: supplier
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/restaurant/src/models/supplier.py
  symbol: models.supplier.Supplier
  line_start: 10
  line_end: 25
  evidence_type: implemented
inbound_relations:
- type: CONTAINS
  source: database.ftgo.restaurant-postgres
  table_name: supplier_profile
  storage_engine: postgresql
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/restaurant/src/models/supplier.py
  symbol: models.supplier.Supplier
  line_start: 10
  line_end: 25
  evidence_type: implemented
- type: READS
  source: service.ftgo.restaurant
  role: read
  target_kind: Table
  persistence_library: sqlalchemy
  call_site_count: 5
  call_sites:
  - operation: select
    resolution: wrapper_argument
    call: DatabaseRepository.fetch_by_query(Supplier, query=query_dict, one_or_none=True)
    repository: ftgo
    commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
    path: backend/microservices/restaurant/src/domain/restaurant.py
    symbol: domain.restaurant.RestaurantDomain.load
    line_start: 53
    line_end: 53
    evidence_type: implemented
  - operation: select
    resolution: wrapper_argument
    call: DatabaseRepository.fetch_by_query(Supplier, query={})
    repository: ftgo
    commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
    path: backend/microservices/restaurant/src/domain/restaurant.py
    symbol: domain.restaurant.RestaurantDomain.load_all
    line_start: 69
    line_end: 69
    evidence_type: implemented
  - operation: select
    resolution: wrapper_argument
    call: 'DatabaseRepository.fetch_by_query(Supplier, query={"owner_user_id": owner_user_id})'
    repository: ftgo
    commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
    path: backend/microservices/restaurant/src/domain/restaurant.py
    symbol: domain.restaurant.RestaurantDomain.register
    line_start: 88
    line_end: 88
    evidence_type: implemented
  - operation: select
    resolution: wrapper_argument
    call: 'DatabaseRepository.update_by_query( Supplier, query={"id": restaurant_id}, update_fields=update_fields,
      )'
    repository: ftgo
    commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
    path: backend/microservices/restaurant/src/domain/restaurant.py
    symbol: domain.restaurant.RestaurantDomain.update_profile_information
    line_start: 139
    line_end: 143
    evidence_type: implemented
  - operation: select
    resolution: wrapper_argument
    call: 'DatabaseRepository.delete_by_query(Supplier, query={"id": self.restaurant_id})'
    repository: ftgo
    commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
    path: backend/microservices/restaurant/src/domain/restaurant.py
    symbol: domain.restaurant.RestaurantDomain.delete_restaurant
    line_start: 153
    line_end: 153
    evidence_type: implemented
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/restaurant/src/domain/restaurant.py
  symbol: domain.restaurant.RestaurantDomain.load
  line_start: 53
  line_end: 53
  evidence_type: implemented
- type: WRITES
  source: service.ftgo.restaurant
  role: write
  target_kind: Table
  persistence_library: asyncpg_client
  call_site_count: 1
  call_sites:
  - operation: add
    resolution: wrapper_argument
    call: DatabaseRepository.insert(new_profile)
    repository: ftgo
    commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
    path: backend/microservices/restaurant/src/domain/restaurant.py
    symbol: domain.restaurant.RestaurantDomain.register
    line_start: 105
    line_end: 105
    evidence_type: implemented
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/restaurant/src/domain/restaurant.py
  symbol: domain.restaurant.RestaurantDomain.register
  line_start: 105
  line_end: 105
  evidence_type: implemented
- type: DEPENDS_ON
  source: table.ftgo.restaurant.menu-item
  foreign_key_column: restaurant_id
  references: supplier_profile.id
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/restaurant/src/models/menu.py
  symbol: models.menu.MenuItem
  line_start: 8
  line_end: 21
  evidence_type: implemented
relations:
- type: CONTAINS
  target: column.ftgo.restaurant.supplier-profile.address
  column_name: address
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/restaurant/src/models/supplier.py
  symbol: models.supplier.Supplier.address
  line_start: 17
  line_end: 17
  evidence_type: implemented
- type: CONTAINS
  target: column.ftgo.restaurant.supplier-profile.address-lat
  column_name: address_lat
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/restaurant/src/models/supplier.py
  symbol: models.supplier.Supplier.address_lat
  line_start: 18
  line_end: 18
  evidence_type: implemented
- type: CONTAINS
  target: column.ftgo.restaurant.supplier-profile.address-lng
  column_name: address_lng
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/restaurant/src/models/supplier.py
  symbol: models.supplier.Supplier.address_lng
  line_start: 19
  line_end: 19
  evidence_type: implemented
- type: CONTAINS
  target: column.ftgo.restaurant.supplier-profile.created-at
  column_name: created_at
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/restaurant/src/models/supplier.py
  symbol: models.supplier.Supplier.created_at
  line_start: 22
  line_end: 22
  evidence_type: implemented
- type: CONTAINS
  target: column.ftgo.restaurant.supplier-profile.id
  column_name: id
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/restaurant/src/models/supplier.py
  symbol: models.supplier.Supplier.id
  line_start: 13
  line_end: 13
  evidence_type: implemented
- type: CONTAINS
  target: column.ftgo.restaurant.supplier-profile.name
  column_name: name
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/restaurant/src/models/supplier.py
  symbol: models.supplier.Supplier.name
  line_start: 15
  line_end: 15
  evidence_type: implemented
- type: CONTAINS
  target: column.ftgo.restaurant.supplier-profile.owner-user-id
  column_name: owner_user_id
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/restaurant/src/models/supplier.py
  symbol: models.supplier.Supplier.owner_user_id
  line_start: 14
  line_end: 14
  evidence_type: implemented
- type: CONTAINS
  target: column.ftgo.restaurant.supplier-profile.postal-code
  column_name: postal_code
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/restaurant/src/models/supplier.py
  symbol: models.supplier.Supplier.postal_code
  line_start: 16
  line_end: 16
  evidence_type: implemented
- type: CONTAINS
  target: column.ftgo.restaurant.supplier-profile.restaurant-licence-id
  column_name: restaurant_licence_id
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/restaurant/src/models/supplier.py
  symbol: models.supplier.Supplier.restaurant_licence_id
  line_start: 20
  line_end: 20
  evidence_type: implemented
- type: CONTAINS
  target: column.ftgo.restaurant.supplier-profile.updated-at
  column_name: updated_at
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/restaurant/src/models/supplier.py
  symbol: models.supplier.Supplier.updated_at
  line_start: 23
  line_end: 23
  evidence_type: implemented
attributes:
  persistence_role: relational_table
  declarative_base: DeclarativeBase
  column_count: 10
---

# supplier_profile

Canonical relational table extracted from an ORM mapping in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Owning service: `service.ftgo.restaurant`
- Database: `database.ftgo.restaurant-postgres`
- Mapped class: `models.supplier.Supplier`
- Persistence library: `sqlalchemy`
- Declared in: `backend/microservices/restaurant/src/models/supplier.py` (lines 10-25)
- Evidence class: `implemented`

## Review notes

This page was promoted to canonical knowledge after review. The physical table name comes from an explicit `__tablename__`; column metadata is read from the mapping and no default value is ever evaluated or emitted.

