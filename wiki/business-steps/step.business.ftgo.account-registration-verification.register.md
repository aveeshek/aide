---
id: step.business.ftgo.account-registration-verification.register
kind: FlowStep
type: FlowStep
title: 'Account registration and verification: POST /auth/register'
status: approved
review_status: approved
candidate_of: business-flow-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: business-flow
owner: aide-ftgo-cohort
layer: business
role: user_flow_reference
business_flow: business-flow.ftgo.ui.account-registration-verification
position: 1
user_flow: flow.ftgo.gateway.post.auth.register
http_method: POST
path: /auth/register
trigger: user_action
evidence_mechanism:
- template_binding
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: ui/src/components/SignUpComp.vue
  symbol: SignUpComp.signup
  line_start: 113
  line_end: 113
  evidence_type: implemented
relations:
- type: DERIVED_FROM
  target: flow.ftgo.gateway.post.auth.register
  evidence_mechanism:
  - template_binding
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: ui/src/components/SignUpComp.vue
  symbol: SignUpComp.signup
  line_start: 113
  line_end: 113
  evidence_type: implemented
- type: PRECEDES
  target: step.business.ftgo.account-registration-verification.verify
  evidence_mechanism:
  - route_navigation
  - vuex_dependency
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: ui/src/components/VerifyAccountPage.vue
  symbol: VerifyAccountPage.verify
  line_start: 75
  line_end: 75
  evidence_type: implemented
inbound_relations:
- type: CONTAINS
  source: business-flow.ftgo.ui.account-registration-verification
  position: 1
  layer: business
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: ui/src/components/SignUpComp.vue
  symbol: SignUpComp.signup
  line_start: 113
  line_end: 113
  evidence_type: implemented
attributes:
  layer: business
  role: user_flow_reference
  position: 1
  trigger: user_action
  http_method: POST
  path: /auth/register
  evidence_mechanism:
  - template_binding
  actors:
  - customer
  - driver
  - restaurant_admin
---

# Account registration and verification: POST /auth/register

Canonical business step referencing an approved Pass-5 UserFlow, extracted from reachability evidence in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Layer: `business`
- Role: `user_flow_reference`
- Business flow: `business-flow.ftgo.ui.account-registration-verification` (position 1)
- References user flow: `flow.ftgo.gateway.post.auth.register`
- Trigger: `user_action`
- Evidence mechanism: `template_binding`
- Declared in: `ui/src/components/SignUpComp.vue` (lines 113-113)
- Evidence class: `implemented`

## Review notes

This approved canonical page records a source-backed business journey. It carries no endpoint, event or persistence detail of its own: that evidence already lives on the referenced UserFlow page and is not duplicated here.

