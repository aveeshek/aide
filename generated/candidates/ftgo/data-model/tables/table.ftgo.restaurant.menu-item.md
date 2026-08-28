---
id: table.ftgo.restaurant.menu-item
kind: Table
type: Table
title: menu_item
status: candidate
review_status: pending
candidate_of: data-model-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: data-model
service: service.ftgo.restaurant
owner: aide-ftgo-cohort
table_name: menu_item
storage_engine: postgresql
persistence_library: sqlalchemy
database: database.ftgo.restaurant-postgres
model_class: models.menu.MenuItem
primary_key:
- item_id
foreign_keys:
- column: restaurant_id
  references: supplier_profile.id
orm_relationships:
- attribute: supplier
  line: 21
  target: '"Supplier"'
  back_populates: menu
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/restaurant/src/models/menu.py
  symbol: models.menu.MenuItem
  line_start: 8
  line_end: 21
  evidence_type: implemented
inbound_relations:
- type: CONTAINS
  source: database.ftgo.restaurant-postgres
  table_name: menu_item
  storage_engine: postgresql
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/restaurant/src/models/menu.py
  symbol: models.menu.MenuItem
  line_start: 8
  line_end: 21
  evidence_type: implemented
- type: READS
  source: service.ftgo.restaurant
  role: read
  target_kind: Table
  persistence_library: sqlalchemy
  call_site_count: 4
  call_sites:
  - operation: select
    resolution: wrapper_argument
    call: 'DatabaseRepository.fetch_by_query(MenuItem, query={"item_id": item_id}, one_or_none=True)'
    repository: ftgo
    commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
    path: backend/microservices/restaurant/src/domain/menu.py
    symbol: domain.menu.MenuDomain.load
    line_start: 67
    line_end: 67
    evidence_type: implemented
  - operation: select
    resolution: wrapper_argument
    call: 'DatabaseRepository.update_by_query( MenuItem, query={"item_id": item_id}, update_fields=update_fields,
      )'
    repository: ftgo
    commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
    path: backend/microservices/restaurant/src/domain/menu.py
    symbol: domain.menu.MenuDomain.update_item
    line_start: 95
    line_end: 99
    evidence_type: implemented
  - operation: select
    resolution: wrapper_argument
    call: 'DatabaseRepository.delete_by_query(MenuItem, query={"item_id": item_id})'
    repository: ftgo
    commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
    path: backend/microservices/restaurant/src/domain/menu.py
    symbol: domain.menu.MenuDomain.delete_item
    line_start: 113
    line_end: 113
    evidence_type: implemented
  - operation: select
    resolution: wrapper_argument
    call: 'DatabaseRepository.fetch_by_query(MenuItem, query={"restaurant_id": self.restaurant_id})'
    repository: ftgo
    commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
    path: backend/microservices/restaurant/src/domain/restaurant.py
    symbol: domain.restaurant.RestaurantDomain.load_all_menu_item
    line_start: 205
    line_end: 205
    evidence_type: implemented
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/restaurant/src/domain/menu.py
  symbol: domain.menu.MenuDomain.load
  line_start: 67
  line_end: 67
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
    call: DatabaseRepository.insert(new_item)
    repository: ftgo
    commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
    path: backend/microservices/restaurant/src/domain/menu.py
    symbol: domain.menu.MenuDomain.add_item
    line_start: 50
    line_end: 50
    evidence_type: implemented
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/restaurant/src/domain/menu.py
  symbol: domain.menu.MenuDomain.add_item
  line_start: 50
  line_end: 50
  evidence_type: implemented
relations:
- type: CONTAINS
  target: column.ftgo.restaurant.menu-item.count
  column_name: count
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/restaurant/src/models/menu.py
  symbol: models.menu.MenuItem.count
  line_start: 15
  line_end: 15
  evidence_type: implemented
- type: CONTAINS
  target: column.ftgo.restaurant.menu-item.created-at
  column_name: created_at
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/restaurant/src/models/menu.py
  symbol: models.menu.MenuItem.created_at
  line_start: 18
  line_end: 18
  evidence_type: implemented
- type: CONTAINS
  target: column.ftgo.restaurant.menu-item.description
  column_name: description
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/restaurant/src/models/menu.py
  symbol: models.menu.MenuItem.description
  line_start: 16
  line_end: 16
  evidence_type: implemented
- type: CONTAINS
  target: column.ftgo.restaurant.menu-item.item-id
  column_name: item_id
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/restaurant/src/models/menu.py
  symbol: models.menu.MenuItem.item_id
  line_start: 11
  line_end: 11
  evidence_type: implemented
- type: CONTAINS
  target: column.ftgo.restaurant.menu-item.name
  column_name: name
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/restaurant/src/models/menu.py
  symbol: models.menu.MenuItem.name
  line_start: 13
  line_end: 13
  evidence_type: implemented
- type: CONTAINS
  target: column.ftgo.restaurant.menu-item.price
  column_name: price
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/restaurant/src/models/menu.py
  symbol: models.menu.MenuItem.price
  line_start: 14
  line_end: 14
  evidence_type: implemented
- type: CONTAINS
  target: column.ftgo.restaurant.menu-item.restaurant-id
  column_name: restaurant_id
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/restaurant/src/models/menu.py
  symbol: models.menu.MenuItem.restaurant_id
  line_start: 12
  line_end: 12
  evidence_type: implemented
- type: CONTAINS
  target: column.ftgo.restaurant.menu-item.updated-at
  column_name: updated_at
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/restaurant/src/models/menu.py
  symbol: models.menu.MenuItem.updated_at
  line_start: 19
  line_end: 19
  evidence_type: implemented
- type: DEPENDS_ON
  target: table.ftgo.restaurant.supplier-profile
  foreign_key_column: restaurant_id
  references: supplier_profile.id
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/microservices/restaurant/src/models/menu.py
  symbol: models.menu.MenuItem
  line_start: 8
  line_end: 21
  evidence_type: implemented
attributes:
  persistence_role: relational_table
  declarative_base: DeclarativeBase
  column_count: 8
---

# menu_item

Candidate relational table extracted from an ORM mapping in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Owning service: `service.ftgo.restaurant`
- Database: `database.ftgo.restaurant-postgres`
- Mapped class: `models.menu.MenuItem`
- Persistence library: `sqlalchemy`
- Declared in: `backend/microservices/restaurant/src/models/menu.py` (lines 8-21)
- Evidence class: `implemented`

## Review notes

This page is a candidate awaiting review. The physical table name comes from an explicit `__tablename__`; column metadata is read from the mapping and no default value is ever evaluated or emitted.

