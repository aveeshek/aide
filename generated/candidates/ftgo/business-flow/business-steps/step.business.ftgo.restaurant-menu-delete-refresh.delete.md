---
id: step.business.ftgo.restaurant-menu-delete-refresh.delete
kind: FlowStep
type: FlowStep
title: 'Restaurant menu item delete and refresh: DELETE /menu/delete'
status: candidate
review_status: pending
candidate_of: business-flow-extraction
repository: ftgo
commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
evidence_type: implemented
extractor: business-flow
owner: aide-ftgo-cohort
layer: business
role: user_flow_reference
business_flow: business-flow.ftgo.ui.restaurant-menu-delete-refresh
position: 1
user_flow: flow.ftgo.gateway.delete.menu.delete
http_method: DELETE
path: /menu/delete
trigger: conditional
evidence_mechanism:
- template_binding
- helper_call
- conditional_branch
condition:
- confirm('آیا از حذف این محصول اطمینان دارید؟')
source_refs:
- repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: ui/src/components/SupplierMainPage.vue
  symbol: SupplierMainPage.deleteItem
  line_start: 189
  line_end: 192
  evidence_type: implemented
relations:
- type: DERIVED_FROM
  target: flow.ftgo.gateway.delete.menu.delete
  evidence_mechanism:
  - template_binding
  - helper_call
  - conditional_branch
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: ui/src/components/SupplierMainPage.vue
  symbol: SupplierMainPage.deleteItem
  line_start: 189
  line_end: 192
  evidence_type: implemented
- type: PRECEDES
  target: step.business.ftgo.restaurant-menu-delete-refresh.get-all-menu-item
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
  source: business-flow.ftgo.ui.restaurant-menu-delete-refresh
  position: 1
  layer: business
  repository: ftgo
  commit: 52b1fd1b5d808e32b7925e890f560445a8460e7a
  path: ui/src/components/SupplierMainPage.vue
  symbol: SupplierMainPage.deleteItem
  line_start: 189
  line_end: 192
  evidence_type: implemented
attributes:
  layer: business
  role: user_flow_reference
  position: 1
  trigger: conditional
  http_method: DELETE
  path: /menu/delete
  evidence_mechanism:
  - template_binding
  - helper_call
  - conditional_branch
  actor: restaurant_admin
  condition:
  - confirm('آیا از حذف این محصول اطمینان دارید؟')
  condition_evidence:
  - condition: confirm('آیا از حذف این محصول اطمینان دارید؟')
    kind: confirmation_guard
---

# Restaurant menu item delete and refresh: DELETE /menu/delete

Candidate business step referencing an approved Pass-5 UserFlow, extracted from reachability evidence in `ftgo` at commit `52b1fd1b5d808e32b7925e890f560445a8460e7a`.

- Layer: `business`
- Role: `user_flow_reference`
- Business flow: `business-flow.ftgo.ui.restaurant-menu-delete-refresh` (position 1)
- References user flow: `flow.ftgo.gateway.delete.menu.delete`
- Trigger: `conditional`
- Evidence mechanism: `template_binding`, `helper_call`, `conditional_branch`
- Declared in: `ui/src/components/SupplierMainPage.vue` (lines 189-192)
- Evidence class: `implemented`

## Guards

- `confirm('آیا از حذف این محصول اطمینان دارید؟')` (`confirmation_guard`)

## Review notes

This page is a candidate awaiting review. It carries no endpoint, event or persistence detail of its own: that evidence already lives on the referenced UserFlow page and is not duplicated here.

