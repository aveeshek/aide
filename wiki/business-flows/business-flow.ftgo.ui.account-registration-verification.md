---
id: business-flow.ftgo.ui.account-registration-verification
kind: BusinessFlow
type: BusinessFlow
title: Account registration and verification
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
entry_component: ui/src/components/SignUpComp.vue
entry_handler: signup
actors:
- customer
- driver
- restaurant_admin
actor_resolution: parameterized_by_user_selected_role
user_flows:
- flow.ftgo.gateway.post.auth.register
- flow.ftgo.gateway.post.auth.verify
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: ui/src/components/SignUpComp.vue
  symbol: SignUpComp.signup
  line_start: 113
  line_end: 113
  evidence_type: implemented
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: ui/src/components/VerifyAccountPage.vue
  symbol: VerifyAccountPage.verify
  line_start: 75
  line_end: 75
  evidence_type: implemented
relations:
- type: CONTAINS
  target: step.business.ftgo.account-registration-verification.register
  position: 1
  layer: business
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: ui/src/components/SignUpComp.vue
  symbol: SignUpComp.signup
  line_start: 113
  line_end: 113
  evidence_type: implemented
- type: CONTAINS
  target: step.business.ftgo.account-registration-verification.verify
  position: 2
  layer: business
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: ui/src/components/VerifyAccountPage.vue
  symbol: VerifyAccountPage.verify
  line_start: 75
  line_end: 75
  evidence_type: implemented
attributes:
  surface: ui
  step_count: 2
  user_flow_count: 2
  entry_component: ui/src/components/SignUpComp.vue
  entry_handler: signup
  entry_trigger: user_action
  actor_resolution: parameterized_by_user_selected_role
  actors:
  - customer
  - driver
  - restaurant_admin
  terminated_because: route 'SignIn' offers only the user action 'signin', which consumes no state this
    journey wrote; arriving on the page does not prove a further request
---

# Account registration and verification

Canonical business journey composed from approved Pass-5 UserFlow pages using reachability evidence in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Surface: `ui`
- Entry: `ui/src/components/SignUpComp.vue` handler `signup`
- Completeness: `resolved`
- Actor: `customer, driver, restaurant_admin` (`parameterized_by_user_selected_role`)
- Evidence class: `implemented`

## Ordered user flows

1. `flow.ftgo.gateway.post.auth.register` `user_action` via `step.business.ftgo.account-registration-verification.register`
2. `flow.ftgo.gateway.post.auth.verify` `user_action` via `step.business.ftgo.account-registration-verification.verify`

## Where the journey stops

The composition ends here because source does not carry it further:

- route 'SignIn' offers only the user action 'signin', which consumes no state this journey wrote; arriving on the page does not prove a further request

## Review notes

This approved canonical page records a source-backed business journey. It adds no technical detail: every step is a reference to an existing approved UserFlow, and every ordering edge carries the reachability evidence that established it.

