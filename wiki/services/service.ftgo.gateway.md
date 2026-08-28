---
id: service.ftgo.gateway
kind: Service
type: Service
title: gateway_service
status: approved
review_status: approved
candidate_of: compose-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: compose
role: application
compose_service: gateway_service
owner: aide-ftgo-cohort
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/docker-compose.yaml
  pointer: /services/gateway_service
  evidence_type: implemented
relations:
- type: DEPENDS_ON
  target: component.ftgo.rabbitmq
  config_key: RABBITMQ_HOST
  referenced_host: rabbitmq
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/docker-compose.yaml
  pointer: /services/gateway_service/environment/RABBITMQ_HOST
  evidence_type: implemented
- type: DEPENDS_ON
  target: component.ftgo.gateway-redis
  config_key: REDIS_HOST
  referenced_host: gateway_redis
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/docker-compose.yaml
  pointer: /services/gateway_service/environment/REDIS_HOST
  evidence_type: implemented
- type: EXPOSES
  target: api.ftgo.gateway
  framework: fastapi
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/main.py
  symbol: main.app
  line_start: 24
  line_end: 28
  evidence_type: implemented
- type: PUBLISHES
  target: event.ftgo.rabbitmq.delivery.rating.create
  role: publisher
  operation: call
  broker_library: rabbitmq_rpc
  mechanism: rpc
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/feedback.py
  symbol: services.feedback.FeedbackService.create_delivery_rating
  line_start: 12
  line_end: 12
  evidence_type: implemented
  call_sites:
  - backend/gateway/src/services/feedback.py:12
  via_wrapper: services.base.Microservice._call_rpc
- type: PUBLISHES
  target: event.ftgo.rabbitmq.delivery.rating.get
  role: publisher
  operation: call
  broker_library: rabbitmq_rpc
  mechanism: rpc
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/feedback.py
  symbol: services.feedback.FeedbackService.get_delivery_rating
  line_start: 20
  line_end: 20
  evidence_type: implemented
  call_sites:
  - backend/gateway/src/services/feedback.py:20
  via_wrapper: services.base.Microservice._call_rpc
- type: PUBLISHES
  target: event.ftgo.rabbitmq.delivery.rating.get-customer-ratings
  role: publisher
  operation: call
  broker_library: rabbitmq_rpc
  mechanism: rpc
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/feedback.py
  symbol: services.feedback.FeedbackService.get_customer_delivery_ratings
  line_start: 24
  line_end: 24
  evidence_type: implemented
  call_sites:
  - backend/gateway/src/services/feedback.py:24
  via_wrapper: services.base.Microservice._call_rpc
- type: PUBLISHES
  target: event.ftgo.rabbitmq.delivery.rating.get-driver-ratings
  role: publisher
  operation: call
  broker_library: rabbitmq_rpc
  mechanism: rpc
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/feedback.py
  symbol: services.feedback.FeedbackService.get_driver_delivery_ratings
  line_start: 28
  line_end: 28
  evidence_type: implemented
  call_sites:
  - backend/gateway/src/services/feedback.py:28
  via_wrapper: services.base.Microservice._call_rpc
- type: PUBLISHES
  target: event.ftgo.rabbitmq.delivery.rating.update
  role: publisher
  operation: call
  broker_library: rabbitmq_rpc
  mechanism: rpc
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/feedback.py
  symbol: services.feedback.FeedbackService.update_delivery_rating
  line_start: 16
  line_end: 16
  evidence_type: implemented
  call_sites:
  - backend/gateway/src/services/feedback.py:16
  via_wrapper: services.base.Microservice._call_rpc
- type: PUBLISHES
  target: event.ftgo.rabbitmq.driver.location.get
  role: publisher
  operation: call
  broker_library: rabbitmq_rpc
  mechanism: rpc
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/location.py
  symbol: services.location.LocationService.get_last_location
  line_start: 27
  line_end: 27
  evidence_type: implemented
  call_sites:
  - backend/gateway/src/services/location.py:27
  via_wrapper: services.base.Microservice._call_rpc
- type: PUBLISHES
  target: event.ftgo.rabbitmq.driver.location.submit
  role: publisher
  operation: call
  broker_library: rabbitmq_rpc
  mechanism: rpc
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/location.py
  symbol: services.location.LocationService.submit_location
  line_start: 11
  line_end: 11
  evidence_type: implemented
  call_sites:
  - backend/gateway/src/services/location.py:11
  via_wrapper: services.base.Microservice._call_rpc
- type: PUBLISHES
  target: event.ftgo.rabbitmq.driver.status.get
  role: publisher
  operation: call
  broker_library: rabbitmq_rpc
  mechanism: rpc
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/location.py
  symbol: services.location.LocationService.get_driver_status
  line_start: 31
  line_end: 31
  evidence_type: implemented
  call_sites:
  - backend/gateway/src/services/location.py:31
  via_wrapper: services.base.Microservice._call_rpc
- type: PUBLISHES
  target: event.ftgo.rabbitmq.driver.status.offline
  role: publisher
  operation: call
  broker_library: rabbitmq_rpc
  mechanism: rpc
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/location.py
  symbol: services.location.LocationService.change_status_offline
  line_start: 19
  line_end: 19
  evidence_type: implemented
  call_sites:
  - backend/gateway/src/services/location.py:19
  via_wrapper: services.base.Microservice._call_rpc
- type: PUBLISHES
  target: event.ftgo.rabbitmq.driver.status.online
  role: publisher
  operation: call
  broker_library: rabbitmq_rpc
  mechanism: rpc
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/location.py
  symbol: services.location.LocationService.change_status_online
  line_start: 15
  line_end: 15
  evidence_type: implemented
  call_sites:
  - backend/gateway/src/services/location.py:15
  via_wrapper: services.base.Microservice._call_rpc
- type: PUBLISHES
  target: event.ftgo.rabbitmq.driver.vehicle.delete
  role: publisher
  operation: call
  broker_library: rabbitmq_rpc
  mechanism: rpc
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/vehicle.py
  symbol: services.vehicle.VehicleService.delete
  line_start: 19
  line_end: 19
  evidence_type: implemented
  call_sites:
  - backend/gateway/src/services/vehicle.py:19
  via_wrapper: services.base.Microservice._call_rpc
- type: PUBLISHES
  target: event.ftgo.rabbitmq.driver.vehicle.get-info
  role: publisher
  operation: call
  broker_library: rabbitmq_rpc
  mechanism: rpc
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/user.py
  symbol: services.user.UserService.get_vehicle_info
  line_start: 75
  line_end: 75
  evidence_type: implemented
  call_sites:
  - backend/gateway/src/services/user.py:75
  - backend/gateway/src/services/vehicle.py:15
  via_wrapper: services.base.Microservice._call_rpc
- type: PUBLISHES
  target: event.ftgo.rabbitmq.driver.vehicle.register
  role: publisher
  operation: call
  broker_library: rabbitmq_rpc
  mechanism: rpc
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/user.py
  symbol: services.user.UserService.register_vehicle
  line_start: 19
  line_end: 19
  evidence_type: implemented
  call_sites:
  - backend/gateway/src/services/user.py:19
  - backend/gateway/src/services/vehicle.py:11
  via_wrapper: services.base.Microservice._call_rpc
- type: PUBLISHES
  target: event.ftgo.rabbitmq.location.drivers.get-nearest
  role: publisher
  operation: call
  broker_library: rabbitmq_rpc
  mechanism: rpc
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/location.py
  symbol: services.location.LocationService.get_nearest_drivers
  line_start: 23
  line_end: 23
  evidence_type: implemented
  call_sites:
  - backend/gateway/src/services/location.py:23
  via_wrapper: services.base.Microservice._call_rpc
- type: PUBLISHES
  target: event.ftgo.rabbitmq.order.create
  role: publisher
  operation: call
  broker_library: rabbitmq_rpc
  mechanism: rpc
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/order.py
  symbol: services.order.OrderService.create_order
  line_start: 15
  line_end: 15
  evidence_type: implemented
  call_sites:
  - backend/gateway/src/services/order.py:15
  via_wrapper: services.base.Microservice._call_rpc
- type: PUBLISHES
  target: event.ftgo.rabbitmq.order.history
  role: publisher
  operation: call
  broker_library: rabbitmq_rpc
  mechanism: rpc
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/order.py
  symbol: services.order.OrderService.get_order_history
  line_start: 11
  line_end: 11
  evidence_type: implemented
  call_sites:
  - backend/gateway/src/services/order.py:11
  via_wrapper: services.base.Microservice._call_rpc
- type: PUBLISHES
  target: event.ftgo.rabbitmq.order.rating.create
  role: publisher
  operation: call
  broker_library: rabbitmq_rpc
  mechanism: rpc
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/feedback.py
  symbol: services.feedback.FeedbackService.create_order_rating
  line_start: 33
  line_end: 33
  evidence_type: implemented
  call_sites:
  - backend/gateway/src/services/feedback.py:33
  via_wrapper: services.base.Microservice._call_rpc
- type: PUBLISHES
  target: event.ftgo.rabbitmq.order.rating.get
  role: publisher
  operation: call
  broker_library: rabbitmq_rpc
  mechanism: rpc
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/feedback.py
  symbol: services.feedback.FeedbackService.get_order_rating
  line_start: 41
  line_end: 41
  evidence_type: implemented
  call_sites:
  - backend/gateway/src/services/feedback.py:41
  via_wrapper: services.base.Microservice._call_rpc
- type: PUBLISHES
  target: event.ftgo.rabbitmq.order.rating.get-customer-ratings
  role: publisher
  operation: call
  broker_library: rabbitmq_rpc
  mechanism: rpc
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/feedback.py
  symbol: services.feedback.FeedbackService.get_customer_order_ratings
  line_start: 45
  line_end: 45
  evidence_type: implemented
  call_sites:
  - backend/gateway/src/services/feedback.py:45
  via_wrapper: services.base.Microservice._call_rpc
- type: PUBLISHES
  target: event.ftgo.rabbitmq.order.rating.get-restaurant-ratings
  role: publisher
  operation: call
  broker_library: rabbitmq_rpc
  mechanism: rpc
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/feedback.py
  symbol: services.feedback.FeedbackService.get_restaurant_order_ratings
  line_start: 49
  line_end: 49
  evidence_type: implemented
  call_sites:
  - backend/gateway/src/services/feedback.py:49
  via_wrapper: services.base.Microservice._call_rpc
- type: PUBLISHES
  target: event.ftgo.rabbitmq.order.rating.update
  role: publisher
  operation: call
  broker_library: rabbitmq_rpc
  mechanism: rpc
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/feedback.py
  symbol: services.feedback.FeedbackService.update_order_rating
  line_start: 37
  line_end: 37
  evidence_type: implemented
  call_sites:
  - backend/gateway/src/services/feedback.py:37
  via_wrapper: services.base.Microservice._call_rpc
- type: PUBLISHES
  target: event.ftgo.rabbitmq.order.restaurant.confirm
  role: publisher
  operation: call
  broker_library: rabbitmq_rpc
  mechanism: rpc
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/order.py
  symbol: services.order.OrderService.restaurant_confirm
  line_start: 23
  line_end: 23
  evidence_type: implemented
  call_sites:
  - backend/gateway/src/services/order.py:23
  via_wrapper: services.base.Microservice._call_rpc
- type: PUBLISHES
  target: event.ftgo.rabbitmq.order.restaurant.reject
  role: publisher
  operation: call
  broker_library: rabbitmq_rpc
  mechanism: rpc
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/order.py
  symbol: services.order.OrderService.restaurant_reject
  line_start: 27
  line_end: 27
  evidence_type: implemented
  call_sites:
  - backend/gateway/src/services/order.py:27
  via_wrapper: services.base.Microservice._call_rpc
- type: PUBLISHES
  target: event.ftgo.rabbitmq.order.update
  role: publisher
  operation: call
  broker_library: rabbitmq_rpc
  mechanism: rpc
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/order.py
  symbol: services.order.OrderService.update_order
  line_start: 19
  line_end: 19
  evidence_type: implemented
  call_sites:
  - backend/gateway/src/services/order.py:19
  via_wrapper: services.base.Microservice._call_rpc
- type: PUBLISHES
  target: event.ftgo.rabbitmq.restaurant.menu.add-item
  role: publisher
  operation: call
  broker_library: rabbitmq_rpc
  mechanism: rpc
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/menu.py
  symbol: services.menu.MenuService.add_item
  line_start: 11
  line_end: 11
  evidence_type: implemented
  call_sites:
  - backend/gateway/src/services/menu.py:11
  via_wrapper: services.base.Microservice._call_rpc
- type: PUBLISHES
  target: event.ftgo.rabbitmq.restaurant.menu.delete-item
  role: publisher
  operation: call
  broker_library: rabbitmq_rpc
  mechanism: rpc
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/menu.py
  symbol: services.menu.MenuService.delete_item
  line_start: 23
  line_end: 23
  evidence_type: implemented
  call_sites:
  - backend/gateway/src/services/menu.py:23
  via_wrapper: services.base.Microservice._call_rpc
- type: PUBLISHES
  target: event.ftgo.rabbitmq.restaurant.menu.get-all-menu-item
  role: publisher
  operation: call
  broker_library: rabbitmq_rpc
  mechanism: rpc
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/menu.py
  symbol: services.menu.MenuService.get_all_menu_item
  line_start: 27
  line_end: 27
  evidence_type: implemented
  call_sites:
  - backend/gateway/src/services/menu.py:27
  via_wrapper: services.base.Microservice._call_rpc
- type: PUBLISHES
  target: event.ftgo.rabbitmq.restaurant.menu.get-item-info
  role: publisher
  operation: call
  broker_library: rabbitmq_rpc
  mechanism: rpc
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/menu.py
  symbol: services.menu.MenuService.get_item_info
  line_start: 15
  line_end: 15
  evidence_type: implemented
  call_sites:
  - backend/gateway/src/services/menu.py:15
  via_wrapper: services.base.Microservice._call_rpc
- type: PUBLISHES
  target: event.ftgo.rabbitmq.restaurant.menu.update-item
  role: publisher
  operation: call
  broker_library: rabbitmq_rpc
  mechanism: rpc
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/menu.py
  symbol: services.menu.MenuService.update_item
  line_start: 19
  line_end: 19
  evidence_type: implemented
  call_sites:
  - backend/gateway/src/services/menu.py:19
  via_wrapper: services.base.Microservice._call_rpc
- type: PUBLISHES
  target: event.ftgo.rabbitmq.restaurant.supplier.delete-restaurant
  role: publisher
  operation: call
  broker_library: rabbitmq_rpc
  mechanism: rpc
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/restaurant.py
  symbol: services.restaurant.RestaurantService.delete_restaurant
  line_start: 31
  line_end: 31
  evidence_type: implemented
  call_sites:
  - backend/gateway/src/services/restaurant.py:31
  via_wrapper: services.base.Microservice._call_rpc
- type: PUBLISHES
  target: event.ftgo.rabbitmq.restaurant.supplier.get-all-restaurant-info
  role: publisher
  operation: call
  broker_library: rabbitmq_rpc
  mechanism: rpc
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/restaurant.py
  symbol: services.restaurant.RestaurantService.get_all_restaurant_info
  line_start: 19
  line_end: 19
  evidence_type: implemented
  call_sites:
  - backend/gateway/src/services/restaurant.py:19
  via_wrapper: services.base.Microservice._call_rpc
- type: PUBLISHES
  target: event.ftgo.rabbitmq.restaurant.supplier.get-restaurant-info
  role: publisher
  operation: call
  broker_library: rabbitmq_rpc
  mechanism: rpc
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/restaurant.py
  symbol: services.restaurant.RestaurantService.get_restaurant_info
  line_start: 15
  line_end: 15
  evidence_type: implemented
  call_sites:
  - backend/gateway/src/services/restaurant.py:15
  via_wrapper: services.base.Microservice._call_rpc
- type: PUBLISHES
  target: event.ftgo.rabbitmq.restaurant.supplier.get-supplier-restaurant-info
  role: publisher
  operation: call
  broker_library: rabbitmq_rpc
  mechanism: rpc
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/restaurant.py
  symbol: services.restaurant.RestaurantService.get_supplier_restaurant_info
  line_start: 23
  line_end: 23
  evidence_type: implemented
  call_sites:
  - backend/gateway/src/services/restaurant.py:23
  via_wrapper: services.base.Microservice._call_rpc
- type: PUBLISHES
  target: event.ftgo.rabbitmq.restaurant.supplier.register
  role: publisher
  operation: call
  broker_library: rabbitmq_rpc
  mechanism: rpc
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/restaurant.py
  symbol: services.restaurant.RestaurantService.register
  line_start: 11
  line_end: 11
  evidence_type: implemented
  call_sites:
  - backend/gateway/src/services/restaurant.py:11
  via_wrapper: services.base.Microservice._call_rpc
- type: PUBLISHES
  target: event.ftgo.rabbitmq.restaurant.supplier.update-information
  role: publisher
  operation: call
  broker_library: rabbitmq_rpc
  mechanism: rpc
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/restaurant.py
  symbol: services.restaurant.RestaurantService.update_information
  line_start: 27
  line_end: 27
  evidence_type: implemented
  call_sites:
  - backend/gateway/src/services/restaurant.py:27
  via_wrapper: services.base.Microservice._call_rpc
- type: PUBLISHES
  target: event.ftgo.rabbitmq.user.address.add-address
  role: publisher
  operation: call
  broker_library: rabbitmq_rpc
  mechanism: rpc
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/user.py
  symbol: services.user.UserService.add_address
  line_start: 15
  line_end: 15
  evidence_type: implemented
  call_sites:
  - backend/gateway/src/services/user.py:15
  via_wrapper: services.base.Microservice._call_rpc
- type: PUBLISHES
  target: event.ftgo.rabbitmq.user.address.delete
  role: publisher
  operation: call
  broker_library: rabbitmq_rpc
  mechanism: rpc
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/user.py
  symbol: services.user.UserService.delete_address
  line_start: 55
  line_end: 55
  evidence_type: implemented
  call_sites:
  - backend/gateway/src/services/user.py:55
  via_wrapper: services.base.Microservice._call_rpc
- type: PUBLISHES
  target: event.ftgo.rabbitmq.user.address.get-address-info
  role: publisher
  operation: call
  broker_library: rabbitmq_rpc
  mechanism: rpc
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/user.py
  symbol: services.user.UserService.get_address_info
  line_start: 63
  line_end: 63
  evidence_type: implemented
  call_sites:
  - backend/gateway/src/services/user.py:63
  via_wrapper: services.base.Microservice._call_rpc
- type: PUBLISHES
  target: event.ftgo.rabbitmq.user.address.get-all-addresses
  role: publisher
  operation: call
  broker_library: rabbitmq_rpc
  mechanism: rpc
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/user.py
  symbol: services.user.UserService.get_all_addresses
  line_start: 67
  line_end: 67
  evidence_type: implemented
  call_sites:
  - backend/gateway/src/services/user.py:67
  via_wrapper: services.base.Microservice._call_rpc
- type: PUBLISHES
  target: event.ftgo.rabbitmq.user.address.get-default-address
  role: publisher
  operation: call
  broker_library: rabbitmq_rpc
  mechanism: rpc
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/user.py
  symbol: services.user.UserService.get_default_address
  line_start: 51
  line_end: 51
  evidence_type: implemented
  call_sites:
  - backend/gateway/src/services/user.py:51
  via_wrapper: services.base.Microservice._call_rpc
- type: PUBLISHES
  target: event.ftgo.rabbitmq.user.address.set-preferred-address
  role: publisher
  operation: call
  broker_library: rabbitmq_rpc
  mechanism: rpc
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/user.py
  symbol: services.user.UserService.set_preferred_address
  line_start: 59
  line_end: 59
  evidence_type: implemented
  call_sites:
  - backend/gateway/src/services/user.py:59
  via_wrapper: services.base.Microservice._call_rpc
- type: PUBLISHES
  target: event.ftgo.rabbitmq.user.address.update-information
  role: publisher
  operation: call
  broker_library: rabbitmq_rpc
  mechanism: rpc
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/user.py
  symbol: services.user.UserService.update_information
  line_start: 71
  line_end: 71
  evidence_type: implemented
  call_sites:
  - backend/gateway/src/services/user.py:71
  via_wrapper: services.base.Microservice._call_rpc
- type: PUBLISHES
  target: event.ftgo.rabbitmq.user.profile.create
  role: publisher
  operation: call
  broker_library: rabbitmq_rpc
  mechanism: rpc
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/user.py
  symbol: services.user.UserService.create_profile
  line_start: 11
  line_end: 11
  evidence_type: implemented
  call_sites:
  - backend/gateway/src/services/user.py:11
  via_wrapper: services.base.Microservice._call_rpc
- type: PUBLISHES
  target: event.ftgo.rabbitmq.user.profile.delete-account
  role: publisher
  operation: call
  broker_library: rabbitmq_rpc
  mechanism: rpc
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/user.py
  symbol: services.user.UserService.delete_account
  line_start: 39
  line_end: 39
  evidence_type: implemented
  call_sites:
  - backend/gateway/src/services/user.py:39
  via_wrapper: services.base.Microservice._call_rpc
- type: PUBLISHES
  target: event.ftgo.rabbitmq.user.profile.get-info
  role: publisher
  operation: call
  broker_library: rabbitmq_rpc
  mechanism: rpc
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/user.py
  symbol: services.user.UserService.get_profile_info
  line_start: 35
  line_end: 35
  evidence_type: implemented
  call_sites:
  - backend/gateway/src/services/user.py:35
  via_wrapper: services.base.Microservice._call_rpc
- type: PUBLISHES
  target: event.ftgo.rabbitmq.user.profile.login
  role: publisher
  operation: call
  broker_library: rabbitmq_rpc
  mechanism: rpc
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/user.py
  symbol: services.user.UserService.login
  line_start: 31
  line_end: 31
  evidence_type: implemented
  call_sites:
  - backend/gateway/src/services/user.py:31
  via_wrapper: services.base.Microservice._call_rpc
- type: PUBLISHES
  target: event.ftgo.rabbitmq.user.profile.logout
  role: publisher
  operation: call
  broker_library: rabbitmq_rpc
  mechanism: rpc
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/user.py
  symbol: services.user.UserService.logout
  line_start: 43
  line_end: 43
  evidence_type: implemented
  call_sites:
  - backend/gateway/src/services/user.py:43
  via_wrapper: services.base.Microservice._call_rpc
- type: PUBLISHES
  target: event.ftgo.rabbitmq.user.profile.resend-auth-code
  role: publisher
  operation: call
  broker_library: rabbitmq_rpc
  mechanism: rpc
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/user.py
  symbol: services.user.UserService.resend_auth_code
  line_start: 23
  line_end: 23
  evidence_type: implemented
  call_sites:
  - backend/gateway/src/services/user.py:23
  via_wrapper: services.base.Microservice._call_rpc
- type: PUBLISHES
  target: event.ftgo.rabbitmq.user.profile.update-profile
  role: publisher
  operation: call
  broker_library: rabbitmq_rpc
  mechanism: rpc
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/user.py
  symbol: services.user.UserService.update_profile
  line_start: 47
  line_end: 47
  evidence_type: implemented
  call_sites:
  - backend/gateway/src/services/user.py:47
  via_wrapper: services.base.Microservice._call_rpc
- type: PUBLISHES
  target: event.ftgo.rabbitmq.user.profile.verify-account
  role: publisher
  operation: call
  broker_library: rabbitmq_rpc
  mechanism: rpc
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: backend/gateway/src/services/user.py
  symbol: services.user.UserService.verify_account
  line_start: 27
  line_end: 27
  evidence_type: implemented
  call_sites:
  - backend/gateway/src/services/user.py:27
  via_wrapper: services.base.Microservice._call_rpc
attributes:
  build_context: ./gateway
  build_dockerfile: Dockerfile
  container_name: gateway_service
  ports:
  - 8000:8000
  networks:
  - backend-network
  - frontend-network
  env_file:
  - ./gateway/.env
  environment:
    ENVIRONMENT: test
    DEBUG: 'true'
    RABBITMQ_USER: rabbitmq_user
    RABBITMQ_PASS: '[redacted]'
    RABBITMQ_VHOST: /
    RABBITMQ_HOST: rabbitmq
    RABBITMQ_PORT: '5672'
    REDIS_HOST: gateway_redis
    REDIS_PORT: '6379'
    REDIS_DB: '0'
    REDIS_PASSWORD: '[redacted]'
    TOKEN_SECRET_KEY: '[redacted]'
    API_PREFIX: /api/v1
    SERVICE_HOST: 0.0.0.0
    SERVICE_PORT: '8000'
---

# gateway_service

Candidate extracted from Docker Compose evidence in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Compose service: `gateway_service`
- Declared in: `backend/docker-compose.yaml`
- YAML pointer: `/services/gateway_service`
- Evidence class: `implemented`

## Runtime dependencies

- `DEPENDS_ON` -> `component.ftgo.rabbitmq` (from `RABBITMQ_HOST=rabbitmq`)
- `DEPENDS_ON` -> `component.ftgo.gateway-redis` (from `REDIS_HOST=gateway_redis`)

## Review notes

This page is a candidate awaiting review. It is not canonical knowledge and secret values are redacted at extraction time.

