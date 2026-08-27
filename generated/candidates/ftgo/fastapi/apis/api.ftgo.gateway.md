---
id: api.ftgo.gateway
kind: API
type: API
title: Food Delivery Server
status: candidate
review_status: pending
candidate_of: fastapi-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: fastapi
service: service.ftgo.gateway
owner: aide-ftgo-cohort
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/main.py
  symbol: main.app
  line_start: 24
  line_end: 28
  evidence_type: implemented
inbound_relations:
- type: EXPOSES
  source: service.ftgo.gateway
  framework: fastapi
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/main.py
  symbol: main.app
  line_start: 24
  line_end: 28
  evidence_type: implemented
relations:
- type: CONTAINS
  target: endpoint.ftgo.gateway.delete.address.delete
  method: DELETE
  path: backend/gateway/src/application/routes/customer/address.py
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  symbol: application.routes.customer.address.delete_address
  line_start: 66
  line_end: 85
  evidence_type: implemented
- type: CONTAINS
  target: endpoint.ftgo.gateway.delete.menu.delete
  method: DELETE
  path: backend/gateway/src/application/routes/restaurant/menu.py
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  symbol: application.routes.restaurant.menu.delete_item
  line_start: 88
  line_end: 107
  evidence_type: implemented
- type: CONTAINS
  target: endpoint.ftgo.gateway.delete.profile.delete
  method: DELETE
  path: backend/gateway/src/application/routes/account/profile.py
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  symbol: application.routes.account.profile.delete_account
  line_start: 65
  line_end: 81
  evidence_type: implemented
- type: CONTAINS
  target: endpoint.ftgo.gateway.delete.restaurant.delete
  method: DELETE
  path: backend/gateway/src/application/routes/restaurant/restaurant.py
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  symbol: application.routes.restaurant.restaurant.delete_restaurant
  line_start: 93
  line_end: 112
  evidence_type: implemented
- type: CONTAINS
  target: endpoint.ftgo.gateway.delete.vehicle.delete
  method: DELETE
  path: backend/gateway/src/application/routes/driver/vehicle.py
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  symbol: application.routes.driver.vehicle.delete
  line_start: 63
  line_end: 83
  evidence_type: implemented
- type: CONTAINS
  target: endpoint.ftgo.gateway.get.address.get-all-info
  method: GET
  path: backend/gateway/src/application/routes/customer/address.py
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  symbol: application.routes.customer.address.get_all_addresses
  line_start: 22
  line_end: 39
  evidence_type: implemented
- type: CONTAINS
  target: endpoint.ftgo.gateway.get.feedback.delivery.rating.customer
  method: GET
  path: backend/gateway/src/application/routes/order/feedback.py
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  symbol: application.routes.order.feedback.get_customer_delivery_ratings
  line_start: 89
  line_end: 107
  evidence_type: implemented
- type: CONTAINS
  target: endpoint.ftgo.gateway.get.feedback.delivery.rating.driver
  method: GET
  path: backend/gateway/src/application/routes/order/feedback.py
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  symbol: application.routes.order.feedback.get_driver_delivery_ratings
  line_start: 109
  line_end: 127
  evidence_type: implemented
- type: CONTAINS
  target: endpoint.ftgo.gateway.get.feedback.delivery.rating.get
  method: GET
  path: backend/gateway/src/application/routes/order/feedback.py
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  symbol: application.routes.order.feedback.get_delivery_rating
  line_start: 70
  line_end: 87
  evidence_type: implemented
- type: CONTAINS
  target: endpoint.ftgo.gateway.get.feedback.order.rating.customer
  method: GET
  path: backend/gateway/src/application/routes/order/feedback.py
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  symbol: application.routes.order.feedback.get_customer_order_ratings
  line_start: 191
  line_end: 209
  evidence_type: implemented
- type: CONTAINS
  target: endpoint.ftgo.gateway.get.feedback.order.rating.get
  method: GET
  path: backend/gateway/src/application/routes/order/feedback.py
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  symbol: application.routes.order.feedback.get_order_rating
  line_start: 171
  line_end: 189
  evidence_type: implemented
- type: CONTAINS
  target: endpoint.ftgo.gateway.get.feedback.order.rating.restaurant
  method: GET
  path: backend/gateway/src/application/routes/order/feedback.py
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  symbol: application.routes.order.feedback.get_restaurant_order_ratings
  line_start: 211
  line_end: 229
  evidence_type: implemented
- type: CONTAINS
  target: endpoint.ftgo.gateway.get.location.get
  method: GET
  path: backend/gateway/src/application/routes/driver/location.py
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  symbol: application.routes.driver.location.get_location
  line_start: 41
  line_end: 62
  evidence_type: implemented
- type: CONTAINS
  target: endpoint.ftgo.gateway.get.menu.get-info
  method: GET
  path: backend/gateway/src/application/routes/restaurant/menu.py
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  symbol: application.routes.restaurant.menu.get_info
  line_start: 43
  line_end: 63
  evidence_type: implemented
- type: CONTAINS
  target: endpoint.ftgo.gateway.get.profile.user-info
  method: GET
  path: backend/gateway/src/application/routes/account/profile.py
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  symbol: application.routes.account.profile.get_info
  line_start: 39
  line_end: 63
  evidence_type: implemented
- type: CONTAINS
  target: endpoint.ftgo.gateway.get.restaurant.get-all-restaurant-info
  method: GET
  path: backend/gateway/src/application/routes/restaurant/restaurant.py
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  symbol: application.routes.restaurant.restaurant.get_all_restaurant_info
  line_start: 74
  line_end: 91
  evidence_type: implemented
- type: CONTAINS
  target: endpoint.ftgo.gateway.get.restaurant.get-supplier-restaurant-info
  method: GET
  path: backend/gateway/src/application/routes/restaurant/restaurant.py
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  symbol: application.routes.restaurant.restaurant.get_supplier_restaurant_info
  line_start: 46
  line_end: 71
  evidence_type: implemented
- type: CONTAINS
  target: endpoint.ftgo.gateway.get.status.get
  method: GET
  path: backend/gateway/src/application/routes/driver/online_status.py
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  symbol: application.routes.driver.online_status.get_status
  line_start: 50
  line_end: 66
  evidence_type: implemented
- type: CONTAINS
  target: endpoint.ftgo.gateway.get.vehicle.get-info
  method: GET
  path: backend/gateway/src/application/routes/driver/vehicle.py
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  symbol: application.routes.driver.vehicle.get_info
  line_start: 42
  line_end: 60
  evidence_type: implemented
- type: CONTAINS
  target: endpoint.ftgo.gateway.post.address.add
  method: POST
  path: backend/gateway/src/application/routes/customer/address.py
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  symbol: application.routes.customer.address.add_address
  line_start: 42
  line_end: 63
  evidence_type: implemented
- type: CONTAINS
  target: endpoint.ftgo.gateway.post.address.set-preferred
  method: POST
  path: backend/gateway/src/application/routes/customer/address.py
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  symbol: application.routes.customer.address.set_address_preferency
  line_start: 88
  line_end: 110
  evidence_type: implemented
- type: CONTAINS
  target: endpoint.ftgo.gateway.post.auth.login
  method: POST
  path: backend/gateway/src/application/routes/auth/registration.py
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  symbol: application.routes.auth.registration.login
  line_start: 78
  line_end: 100
  evidence_type: implemented
- type: CONTAINS
  target: endpoint.ftgo.gateway.post.auth.register
  method: POST
  path: backend/gateway/src/application/routes/auth/registration.py
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  symbol: application.routes.auth.registration.register
  line_start: 21
  line_end: 40
  evidence_type: implemented
- type: CONTAINS
  target: endpoint.ftgo.gateway.post.auth.resend-code
  method: POST
  path: backend/gateway/src/application/routes/auth/registration.py
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  symbol: application.routes.auth.registration.resend_auth_code
  line_start: 60
  line_end: 76
  evidence_type: implemented
- type: CONTAINS
  target: endpoint.ftgo.gateway.post.auth.verify
  method: POST
  path: backend/gateway/src/application/routes/auth/registration.py
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  symbol: application.routes.auth.registration.verify_account
  line_start: 42
  line_end: 58
  evidence_type: implemented
- type: CONTAINS
  target: endpoint.ftgo.gateway.post.feedback.delivery.rating.create
  method: POST
  path: backend/gateway/src/application/routes/order/feedback.py
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  symbol: application.routes.order.feedback.create_delivery_rating
  line_start: 30
  line_end: 48
  evidence_type: implemented
- type: CONTAINS
  target: endpoint.ftgo.gateway.post.feedback.order.rating.create
  method: POST
  path: backend/gateway/src/application/routes/order/feedback.py
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  symbol: application.routes.order.feedback.create_order_rating
  line_start: 131
  line_end: 149
  evidence_type: implemented
- type: CONTAINS
  target: endpoint.ftgo.gateway.post.location.submit
  method: POST
  path: backend/gateway/src/application/routes/driver/location.py
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  symbol: application.routes.driver.location.submit_location
  line_start: 16
  line_end: 38
  evidence_type: implemented
- type: CONTAINS
  target: endpoint.ftgo.gateway.post.menu.add
  method: POST
  path: backend/gateway/src/application/routes/restaurant/menu.py
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  symbol: application.routes.restaurant.menu.add_item
  line_start: 21
  line_end: 40
  evidence_type: implemented
- type: CONTAINS
  target: endpoint.ftgo.gateway.post.menu.get-all-menu-item
  method: POST
  path: backend/gateway/src/application/routes/restaurant/menu.py
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  symbol: application.routes.restaurant.menu.get_all_menu_item
  line_start: 109
  line_end: 128
  evidence_type: implemented
- type: CONTAINS
  target: endpoint.ftgo.gateway.post.order.confirm
  method: POST
  path: backend/gateway/src/application/routes/order/order.py
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  symbol: application.routes.order.order.restaurant_confirm
  line_start: 96
  line_end: 118
  evidence_type: implemented
- type: CONTAINS
  target: endpoint.ftgo.gateway.post.order.create
  method: POST
  path: backend/gateway/src/application/routes/order/order.py
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  symbol: application.routes.order.order.create_order
  line_start: 44
  line_end: 67
  evidence_type: implemented
- type: CONTAINS
  target: endpoint.ftgo.gateway.post.order.history
  method: POST
  path: backend/gateway/src/application/routes/order/order.py
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  symbol: application.routes.order.order.get_order_history
  line_start: 19
  line_end: 40
  evidence_type: implemented
- type: CONTAINS
  target: endpoint.ftgo.gateway.post.order.reject
  method: POST
  path: backend/gateway/src/application/routes/order/order.py
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  symbol: application.routes.order.order.restaurant_reject
  line_start: 121
  line_end: 143
  evidence_type: implemented
- type: CONTAINS
  target: endpoint.ftgo.gateway.post.order.update
  method: POST
  path: backend/gateway/src/application/routes/order/order.py
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  symbol: application.routes.order.order.update_order
  line_start: 70
  line_end: 93
  evidence_type: implemented
- type: CONTAINS
  target: endpoint.ftgo.gateway.post.profile.logout
  method: POST
  path: backend/gateway/src/application/routes/account/profile.py
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  symbol: application.routes.account.profile.logout
  line_start: 21
  line_end: 37
  evidence_type: implemented
- type: CONTAINS
  target: endpoint.ftgo.gateway.post.restaurant.register
  method: POST
  path: backend/gateway/src/application/routes/restaurant/restaurant.py
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  symbol: application.routes.restaurant.restaurant.register
  line_start: 22
  line_end: 44
  evidence_type: implemented
- type: CONTAINS
  target: endpoint.ftgo.gateway.post.status.offline
  method: POST
  path: backend/gateway/src/application/routes/driver/online_status.py
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  symbol: application.routes.driver.online_status.change_status_offline
  line_start: 42
  line_end: 48
  evidence_type: implemented
- type: CONTAINS
  target: endpoint.ftgo.gateway.post.status.online
  method: POST
  path: backend/gateway/src/application/routes/driver/online_status.py
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  symbol: application.routes.driver.online_status.change_status_online
  line_start: 34
  line_end: 40
  evidence_type: implemented
- type: CONTAINS
  target: endpoint.ftgo.gateway.post.vehicle.register
  method: POST
  path: backend/gateway/src/application/routes/driver/vehicle.py
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  symbol: application.routes.driver.vehicle.register
  line_start: 17
  line_end: 39
  evidence_type: implemented
- type: CONTAINS
  target: endpoint.ftgo.gateway.put.feedback.delivery.rating.update
  method: PUT
  path: backend/gateway/src/application/routes/order/feedback.py
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  symbol: application.routes.order.feedback.update_delivery_rating
  line_start: 50
  line_end: 68
  evidence_type: implemented
- type: CONTAINS
  target: endpoint.ftgo.gateway.put.feedback.order.rating.update
  method: PUT
  path: backend/gateway/src/application/routes/order/feedback.py
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  symbol: application.routes.order.feedback.update_order_rating
  line_start: 151
  line_end: 169
  evidence_type: implemented
- type: CONTAINS
  target: endpoint.ftgo.gateway.put.menu.update
  method: PUT
  path: backend/gateway/src/application/routes/restaurant/menu.py
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  symbol: application.routes.restaurant.menu.update_item
  line_start: 66
  line_end: 85
  evidence_type: implemented
- type: CONTAINS
  target: endpoint.ftgo.gateway.put.profile.update
  method: PUT
  path: backend/gateway/src/application/routes/account/profile.py
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  symbol: application.routes.account.profile.update_profile
  line_start: 85
  line_end: 106
  evidence_type: implemented
- type: CONTAINS
  target: endpoint.ftgo.gateway.put.restaurant.update
  method: PUT
  path: backend/gateway/src/application/routes/restaurant/restaurant.py
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  symbol: application.routes.restaurant.restaurant.update_information
  line_start: 115
  line_end: 133
  evidence_type: implemented
attributes:
  framework: fastapi
  application_count: 1
  router_count: 11
  endpoint_count: 45
  endpoints_with_partial_paths: 45
  application_symbol: main.app
  application_title: Food Delivery Server
---

# Food Delivery Server

Candidate FastAPI surface extracted from Python source in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Owning service: `service.ftgo.gateway`
- Declared in: `backend/gateway/src/main.py`
- Symbol: `main.app`
- Evidence class: `implemented`

## Endpoints

- `CONTAINS` -> `endpoint.ftgo.gateway.delete.address.delete`
- `CONTAINS` -> `endpoint.ftgo.gateway.delete.menu.delete`
- `CONTAINS` -> `endpoint.ftgo.gateway.delete.profile.delete`
- `CONTAINS` -> `endpoint.ftgo.gateway.delete.restaurant.delete`
- `CONTAINS` -> `endpoint.ftgo.gateway.delete.vehicle.delete`
- `CONTAINS` -> `endpoint.ftgo.gateway.get.address.get-all-info`
- `CONTAINS` -> `endpoint.ftgo.gateway.get.feedback.delivery.rating.customer`
- `CONTAINS` -> `endpoint.ftgo.gateway.get.feedback.delivery.rating.driver`
- `CONTAINS` -> `endpoint.ftgo.gateway.get.feedback.delivery.rating.get`
- `CONTAINS` -> `endpoint.ftgo.gateway.get.feedback.order.rating.customer`
- `CONTAINS` -> `endpoint.ftgo.gateway.get.feedback.order.rating.get`
- `CONTAINS` -> `endpoint.ftgo.gateway.get.feedback.order.rating.restaurant`
- `CONTAINS` -> `endpoint.ftgo.gateway.get.location.get`
- `CONTAINS` -> `endpoint.ftgo.gateway.get.menu.get-info`
- `CONTAINS` -> `endpoint.ftgo.gateway.get.profile.user-info`
- `CONTAINS` -> `endpoint.ftgo.gateway.get.restaurant.get-all-restaurant-info`
- `CONTAINS` -> `endpoint.ftgo.gateway.get.restaurant.get-supplier-restaurant-info`
- `CONTAINS` -> `endpoint.ftgo.gateway.get.status.get`
- `CONTAINS` -> `endpoint.ftgo.gateway.get.vehicle.get-info`
- `CONTAINS` -> `endpoint.ftgo.gateway.post.address.add`
- `CONTAINS` -> `endpoint.ftgo.gateway.post.address.set-preferred`
- `CONTAINS` -> `endpoint.ftgo.gateway.post.auth.login`
- `CONTAINS` -> `endpoint.ftgo.gateway.post.auth.register`
- `CONTAINS` -> `endpoint.ftgo.gateway.post.auth.resend-code`
- `CONTAINS` -> `endpoint.ftgo.gateway.post.auth.verify`
- `CONTAINS` -> `endpoint.ftgo.gateway.post.feedback.delivery.rating.create`
- `CONTAINS` -> `endpoint.ftgo.gateway.post.feedback.order.rating.create`
- `CONTAINS` -> `endpoint.ftgo.gateway.post.location.submit`
- `CONTAINS` -> `endpoint.ftgo.gateway.post.menu.add`
- `CONTAINS` -> `endpoint.ftgo.gateway.post.menu.get-all-menu-item`
- `CONTAINS` -> `endpoint.ftgo.gateway.post.order.confirm`
- `CONTAINS` -> `endpoint.ftgo.gateway.post.order.create`
- `CONTAINS` -> `endpoint.ftgo.gateway.post.order.history`
- `CONTAINS` -> `endpoint.ftgo.gateway.post.order.reject`
- `CONTAINS` -> `endpoint.ftgo.gateway.post.order.update`
- `CONTAINS` -> `endpoint.ftgo.gateway.post.profile.logout`
- `CONTAINS` -> `endpoint.ftgo.gateway.post.restaurant.register`
- `CONTAINS` -> `endpoint.ftgo.gateway.post.status.offline`
- `CONTAINS` -> `endpoint.ftgo.gateway.post.status.online`
- `CONTAINS` -> `endpoint.ftgo.gateway.post.vehicle.register`
- `CONTAINS` -> `endpoint.ftgo.gateway.put.feedback.delivery.rating.update`
- `CONTAINS` -> `endpoint.ftgo.gateway.put.feedback.order.rating.update`
- `CONTAINS` -> `endpoint.ftgo.gateway.put.menu.update`
- `CONTAINS` -> `endpoint.ftgo.gateway.put.profile.update`
- `CONTAINS` -> `endpoint.ftgo.gateway.put.restaurant.update`

## Review notes

This page is a candidate awaiting review. It is not canonical knowledge. Paths come from statically resolvable decorators and router prefixes only.

