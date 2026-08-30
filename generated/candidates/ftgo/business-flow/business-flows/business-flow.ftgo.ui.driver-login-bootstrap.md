---
id: business-flow.ftgo.ui.driver-login-bootstrap
kind: BusinessFlow
type: BusinessFlow
title: Driver login bootstrap
status: candidate
review_status: pending
candidate_of: business-flow-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: business-flow
owner: aide-ftgo-cohort
surface: ui
completeness: resolved
entry_component: ui/src/components/SignInComp.vue
entry_handler: signin
actor: driver
actor_resolution: role_branch
user_flows:
- flow.ftgo.gateway.post.auth.login
- flow.ftgo.gateway.get.vehicle.get-info
- flow.ftgo.gateway.get.status.get
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: ui/src/components/SignInComp.vue
  symbol: SignInComp.signin
  line_start: 86
  line_end: 86
  evidence_type: implemented
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: ui/src/components/SignInComp.vue
  symbol: SignInComp.fetchAndStoreVehicleInfo
  line_start: 157
  line_end: 161
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
  target: step.business.ftgo.driver-login-bootstrap.get
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
  target: step.business.ftgo.driver-login-bootstrap.get-info
  position: 2
  layer: business
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: ui/src/components/SignInComp.vue
  symbol: SignInComp.fetchAndStoreVehicleInfo
  line_start: 157
  line_end: 161
  evidence_type: implemented
- type: CONTAINS
  target: step.business.ftgo.driver-login-bootstrap.login
  position: 1
  layer: business
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: ui/src/components/SignInComp.vue
  symbol: SignInComp.signin
  line_start: 86
  line_end: 86
  evidence_type: implemented
attributes:
  surface: ui
  step_count: 3
  user_flow_count: 3
  entry_component: ui/src/components/SignInComp.vue
  entry_handler: signin
  entry_trigger: user_action
  actor_resolution: role_branch
  actor: driver
  branch_selector:
    this.userRole: driver
  terminated_because: 'no ordering evidence between flow.ftgo.gateway.get.status.get and flow.ftgo.gateway.get.status.get:
    the preceding operation is neither awaited nor chained through a resolved promise'
---

# Driver login bootstrap

Candidate business journey composed from approved Pass-5 UserFlow pages using reachability evidence in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Surface: `ui`
- Entry: `ui/src/components/SignInComp.vue` handler `signin`
- Completeness: `resolved`
- Actor: `driver` (`role_branch`)
- Evidence class: `implemented`

## Ordered user flows

1. `flow.ftgo.gateway.post.auth.login` `user_action` via `step.business.ftgo.driver-login-bootstrap.login`
2. `flow.ftgo.gateway.get.vehicle.get-info` `automatic` via `step.business.ftgo.driver-login-bootstrap.get-info`
3. `flow.ftgo.gateway.get.status.get` `automatic` via `step.business.ftgo.driver-login-bootstrap.get`

## Where the journey stops

The composition ends here because source does not carry it further:

- no ordering evidence between flow.ftgo.gateway.get.status.get and flow.ftgo.gateway.get.status.get: the preceding operation is neither awaited nor chained through a resolved promise

## Review notes

This page is a candidate awaiting review. It adds no technical detail: every step is a reference to an existing approved UserFlow, and every ordering edge carries the reachability evidence that established it.

