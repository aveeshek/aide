---
id: business-flow.ftgo.ui.customer-login-restaurant-browse
kind: BusinessFlow
type: BusinessFlow
title: Customer login and restaurant browsing
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
actor: customer
actor_resolution: role_branch
user_flows:
- flow.ftgo.gateway.post.auth.login
- flow.ftgo.gateway.get.restaurant.get-all-restaurant-info
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
  path: ui/src/components/CustomerMainPage.vue
  symbol: CustomerMainPage.fetchRestaurants
  line_start: 86
  line_end: 91
  evidence_type: implemented
relations:
- type: CONTAINS
  target: step.business.ftgo.customer-login-restaurant-browse.get-all-restaurant-info
  position: 2
  layer: business
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: ui/src/components/CustomerMainPage.vue
  symbol: CustomerMainPage.fetchRestaurants
  line_start: 86
  line_end: 91
  evidence_type: implemented
- type: CONTAINS
  target: step.business.ftgo.customer-login-restaurant-browse.login
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
  step_count: 2
  user_flow_count: 2
  entry_component: ui/src/components/SignInComp.vue
  entry_handler: signin
  entry_trigger: user_action
  actor_resolution: role_branch
  actor: customer
  branch_selector:
    this.userRole: customer
---

# Customer login and restaurant browsing

Candidate business journey composed from approved Pass-5 UserFlow pages using reachability evidence in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Surface: `ui`
- Entry: `ui/src/components/SignInComp.vue` handler `signin`
- Completeness: `resolved`
- Actor: `customer` (`role_branch`)
- Evidence class: `implemented`

## Ordered user flows

1. `flow.ftgo.gateway.post.auth.login` `user_action` via `step.business.ftgo.customer-login-restaurant-browse.login`
2. `flow.ftgo.gateway.get.restaurant.get-all-restaurant-info` `automatic` via `step.business.ftgo.customer-login-restaurant-browse.get-all-restaurant-info`

## Review notes

This page is a candidate awaiting review. It adds no technical detail: every step is a reference to an existing approved UserFlow, and every ordering edge carries the reachability evidence that established it.

