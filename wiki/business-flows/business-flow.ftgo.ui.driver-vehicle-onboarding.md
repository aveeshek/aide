---
id: business-flow.ftgo.ui.driver-vehicle-onboarding
kind: BusinessFlow
type: BusinessFlow
title: Driver vehicle onboarding
status: approved
review_status: approved
candidate_of: business-flow-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: business-flow
owner: aide-ftgo-cohort
surface: ui
completeness: resolved
entry_component: ui/src/components/RegisterVehiclePage.vue
entry_handler: registerVehicle
actor: driver
actor_resolution: role_branch_navigation_region
user_flows:
- flow.ftgo.gateway.post.vehicle.register
- flow.ftgo.gateway.get.vehicle.get-info
- flow.ftgo.gateway.get.status.get
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: ui/src/components/RegisterVehiclePage.vue
  symbol: RegisterVehiclePage.registerVehicle
  line_start: 84
  line_end: 88
  evidence_type: implemented
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: ui/src/components/RegisterVehiclePage.vue
  symbol: RegisterVehiclePage.fetchAndStoreVehicleInfo
  line_start: 111
  line_end: 115
  evidence_type: implemented
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: ui/src/components/DeliveryMainPage.vue
  symbol: DeliveryMainPage.fetchDriverOnlineStatus
  line_start: 132
  line_end: 136
  evidence_type: implemented
relations:
- type: CONTAINS
  target: step.business.ftgo.driver-vehicle-onboarding.get
  position: 3
  layer: business
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: ui/src/components/DeliveryMainPage.vue
  symbol: DeliveryMainPage.fetchDriverOnlineStatus
  line_start: 132
  line_end: 136
  evidence_type: implemented
- type: CONTAINS
  target: step.business.ftgo.driver-vehicle-onboarding.get-info
  position: 2
  layer: business
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: ui/src/components/RegisterVehiclePage.vue
  symbol: RegisterVehiclePage.fetchAndStoreVehicleInfo
  line_start: 111
  line_end: 115
  evidence_type: implemented
- type: CONTAINS
  target: step.business.ftgo.driver-vehicle-onboarding.register
  position: 1
  layer: business
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: ui/src/components/RegisterVehiclePage.vue
  symbol: RegisterVehiclePage.registerVehicle
  line_start: 84
  line_end: 88
  evidence_type: implemented
attributes:
  surface: ui
  step_count: 3
  user_flow_count: 3
  entry_component: ui/src/components/RegisterVehiclePage.vue
  entry_handler: registerVehicle
  entry_trigger: user_action
  actor_resolution: role_branch_navigation_region
  actor: driver
  terminated_because: 'no ordering evidence between flow.ftgo.gateway.get.status.get and flow.ftgo.gateway.get.status.get:
    the preceding operation is neither awaited nor chained through a resolved promise'
---

# Driver vehicle onboarding

Canonical business journey composed from approved Pass-5 UserFlow pages using reachability evidence in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Surface: `ui`
- Entry: `ui/src/components/RegisterVehiclePage.vue` handler `registerVehicle`
- Completeness: `resolved`
- Actor: `driver` (`role_branch_navigation_region`)
- Evidence class: `implemented`

## Ordered user flows

1. `flow.ftgo.gateway.post.vehicle.register` `user_action` via `step.business.ftgo.driver-vehicle-onboarding.register`
2. `flow.ftgo.gateway.get.vehicle.get-info` `automatic` via `step.business.ftgo.driver-vehicle-onboarding.get-info`
3. `flow.ftgo.gateway.get.status.get` `automatic` via `step.business.ftgo.driver-vehicle-onboarding.get`

## Where the journey stops

The composition ends here because source does not carry it further:

- no ordering evidence between flow.ftgo.gateway.get.status.get and flow.ftgo.gateway.get.status.get: the preceding operation is neither awaited nor chained through a resolved promise

## Review notes

This approved canonical page records a source-backed business journey. It adds no technical detail: every step is a reference to an existing approved UserFlow, and every ordering edge carries the reachability evidence that established it.

