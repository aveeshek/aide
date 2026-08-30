---
id: business-flow.ftgo.ui.restaurant-menu-update-refresh
kind: BusinessFlow
type: BusinessFlow
title: Restaurant menu item update and refresh
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
entry_component: ui/src/components/SupplierMainPage.vue
entry_handler: updateFood
actor: restaurant_admin
actor_resolution: role_branch_navigation_region
user_flows:
- flow.ftgo.gateway.put.menu.update
- flow.ftgo.gateway.post.menu.get-all-menu-item
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: ui/src/components/SupplierMainPage.vue
  symbol: SupplierMainPage.updateFood
  line_start: 163
  line_end: 167
  evidence_type: implemented
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: ui/src/components/SupplierMainPage.vue
  symbol: SupplierMainPage.fetchMenu
  line_start: 131
  line_end: 137
  evidence_type: implemented
relations:
- type: CONTAINS
  target: step.business.ftgo.restaurant-menu-update-refresh.get-all-menu-item
  position: 2
  layer: business
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: ui/src/components/SupplierMainPage.vue
  symbol: SupplierMainPage.fetchMenu
  line_start: 131
  line_end: 137
  evidence_type: implemented
- type: CONTAINS
  target: step.business.ftgo.restaurant-menu-update-refresh.update
  position: 1
  layer: business
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: ui/src/components/SupplierMainPage.vue
  symbol: SupplierMainPage.updateFood
  line_start: 163
  line_end: 167
  evidence_type: implemented
attributes:
  surface: ui
  step_count: 2
  user_flow_count: 2
  entry_component: ui/src/components/SupplierMainPage.vue
  entry_handler: updateFood
  entry_trigger: user_action
  actor_resolution: role_branch_navigation_region
  actor: restaurant_admin
---

# Restaurant menu item update and refresh

Candidate business journey composed from approved Pass-5 UserFlow pages using reachability evidence in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Surface: `ui`
- Entry: `ui/src/components/SupplierMainPage.vue` handler `updateFood`
- Completeness: `resolved`
- Actor: `restaurant_admin` (`role_branch_navigation_region`)
- Evidence class: `implemented`

## Ordered user flows

1. `flow.ftgo.gateway.put.menu.update` `user_action` via `step.business.ftgo.restaurant-menu-update-refresh.update`
2. `flow.ftgo.gateway.post.menu.get-all-menu-item` `conditional` via `step.business.ftgo.restaurant-menu-update-refresh.get-all-menu-item`

## Review notes

This page is a candidate awaiting review. It adds no technical detail: every step is a reference to an existing approved UserFlow, and every ordering edge carries the reachability evidence that established it.

