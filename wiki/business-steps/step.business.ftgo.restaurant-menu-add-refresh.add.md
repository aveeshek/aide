---
id: step.business.ftgo.restaurant-menu-add-refresh.add
kind: FlowStep
type: FlowStep
title: 'Restaurant menu item add and refresh: POST /menu/add'
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
business_flow: business-flow.ftgo.ui.restaurant-menu-add-refresh
position: 1
user_flow: flow.ftgo.gateway.post.menu.add
http_method: POST
path: /menu/add
trigger: user_action
evidence_mechanism:
- template_binding
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: ui/src/components/SupplierMainPage.vue
  symbol: SupplierMainPage.addFood
  line_start: 148
  line_end: 152
  evidence_type: implemented
relations:
- type: DERIVED_FROM
  target: flow.ftgo.gateway.post.menu.add
  evidence_mechanism:
  - template_binding
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: ui/src/components/SupplierMainPage.vue
  symbol: SupplierMainPage.addFood
  line_start: 148
  line_end: 152
  evidence_type: implemented
- type: PRECEDES
  target: step.business.ftgo.restaurant-menu-add-refresh.get-all-menu-item
  evidence_mechanism:
  - await_sequence
  - helper_call
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: ui/src/components/SupplierMainPage.vue
  symbol: SupplierMainPage.fetchMenu
  line_start: 131
  line_end: 137
  evidence_type: implemented
inbound_relations:
- type: CONTAINS
  source: business-flow.ftgo.ui.restaurant-menu-add-refresh
  position: 1
  layer: business
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: ui/src/components/SupplierMainPage.vue
  symbol: SupplierMainPage.addFood
  line_start: 148
  line_end: 152
  evidence_type: implemented
attributes:
  layer: business
  role: user_flow_reference
  position: 1
  trigger: user_action
  http_method: POST
  path: /menu/add
  evidence_mechanism:
  - template_binding
  actor: restaurant_admin
---

# Restaurant menu item add and refresh: POST /menu/add

Canonical business step referencing an approved Pass-5 UserFlow, extracted from reachability evidence in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Layer: `business`
- Role: `user_flow_reference`
- Business flow: `business-flow.ftgo.ui.restaurant-menu-add-refresh` (position 1)
- References user flow: `flow.ftgo.gateway.post.menu.add`
- Trigger: `user_action`
- Evidence mechanism: `template_binding`
- Declared in: `ui/src/components/SupplierMainPage.vue` (lines 148-152)
- Evidence class: `implemented`

## Review notes

This approved canonical page records a source-backed business journey. It carries no endpoint, event or persistence detail of its own: that evidence already lives on the referenced UserFlow page and is not duplicated here.

