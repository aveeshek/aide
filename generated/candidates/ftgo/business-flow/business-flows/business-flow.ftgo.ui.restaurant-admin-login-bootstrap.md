---
id: business-flow.ftgo.ui.restaurant-admin-login-bootstrap
kind: BusinessFlow
type: BusinessFlow
title: Restaurant admin login bootstrap
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
actor: restaurant_admin
actor_resolution: role_branch
user_flows:
- flow.ftgo.gateway.post.auth.login
- flow.ftgo.gateway.get.restaurant.get-supplier-restaurant-info
- flow.ftgo.gateway.post.menu.get-all-menu-item
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
  symbol: SignInComp.fetchAndStoreRestaurantInfo
  line_start: 140
  line_end: 144
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
  target: step.business.ftgo.restaurant-admin-login-bootstrap.get-all-menu-item
  position: 3
  layer: business
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: ui/src/components/SupplierMainPage.vue
  symbol: SupplierMainPage.fetchMenu
  line_start: 131
  line_end: 137
  evidence_type: implemented
- type: CONTAINS
  target: step.business.ftgo.restaurant-admin-login-bootstrap.get-supplier-restaurant-info
  position: 2
  layer: business
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: ui/src/components/SignInComp.vue
  symbol: SignInComp.fetchAndStoreRestaurantInfo
  line_start: 140
  line_end: 144
  evidence_type: implemented
- type: CONTAINS
  target: step.business.ftgo.restaurant-admin-login-bootstrap.login
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
  actor: restaurant_admin
  branch_selector:
    this.userRole: restaurant_admin
---

# Restaurant admin login bootstrap

Candidate business journey composed from approved Pass-5 UserFlow pages using reachability evidence in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Surface: `ui`
- Entry: `ui/src/components/SignInComp.vue` handler `signin`
- Completeness: `resolved`
- Actor: `restaurant_admin` (`role_branch`)
- Evidence class: `implemented`

## Ordered user flows

1. `flow.ftgo.gateway.post.auth.login` `user_action` via `step.business.ftgo.restaurant-admin-login-bootstrap.login`
2. `flow.ftgo.gateway.get.restaurant.get-supplier-restaurant-info` `automatic` via `step.business.ftgo.restaurant-admin-login-bootstrap.get-supplier-restaurant-info`
3. `flow.ftgo.gateway.post.menu.get-all-menu-item` `conditional` via `step.business.ftgo.restaurant-admin-login-bootstrap.get-all-menu-item`

## Review notes

This page is a candidate awaiting review. It adds no technical detail: every step is a reference to an existing approved UserFlow, and every ordering edge carries the reachability evidence that established it.

