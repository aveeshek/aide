---
id: business-flow.ftgo.ui.driver-active-location-refresh
kind: BusinessFlow
type: BusinessFlow
title: Driver active location refresh
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
entry_component: ui/src/components/DeliveryMainPage.vue
entry_handler: startRefresh
actor: driver
actor_resolution: role_branch_navigation_region
user_flows:
- flow.ftgo.gateway.get.status.get
- flow.ftgo.gateway.post.location.submit
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: ui/src/components/DeliveryMainPage.vue
  symbol: DeliveryMainPage.fetchDriverOnlineStatus
  line_start: 132
  line_end: 136
  evidence_type: implemented
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: ui/src/components/DeliveryMainPage.vue
  symbol: DeliveryMainPage.submitLocation
  line_start: 177
  line_end: 181
  evidence_type: implemented
relations:
- type: CONTAINS
  target: step.business.ftgo.driver-active-location-refresh.get
  position: 1
  layer: business
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: ui/src/components/DeliveryMainPage.vue
  symbol: DeliveryMainPage.fetchDriverOnlineStatus
  line_start: 132
  line_end: 136
  evidence_type: implemented
- type: CONTAINS
  target: step.business.ftgo.driver-active-location-refresh.submit
  position: 2
  layer: business
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: ui/src/components/DeliveryMainPage.vue
  symbol: DeliveryMainPage.submitLocation
  line_start: 177
  line_end: 181
  evidence_type: implemented
attributes:
  surface: ui
  step_count: 2
  user_flow_count: 2
  entry_component: ui/src/components/DeliveryMainPage.vue
  entry_handler: startRefresh
  entry_trigger: lifecycle
  actor_resolution: role_branch_navigation_region
  actor: driver
---

# Driver active location refresh

Candidate business journey composed from approved Pass-5 UserFlow pages using reachability evidence in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Surface: `ui`
- Entry: `ui/src/components/DeliveryMainPage.vue` handler `startRefresh`
- Completeness: `resolved`
- Actor: `driver` (`role_branch_navigation_region`)
- Evidence class: `implemented`

## Ordered user flows

1. `flow.ftgo.gateway.get.status.get` `automatic` via `step.business.ftgo.driver-active-location-refresh.get`
2. `flow.ftgo.gateway.post.location.submit` `conditional` via `step.business.ftgo.driver-active-location-refresh.submit`

## Review notes

This page is a candidate awaiting review. It adds no technical detail: every step is a reference to an existing approved UserFlow, and every ordering edge carries the reachability evidence that established it.

