---
id: knowledge.home
kind: Index
type: Index
title: Approved Engineering Knowledge
status: approved
review_status: approved
owner: architecture-governance
last_verified_at: 2026-07-22
source_refs:
  - repository: engineering-knowledge-plane
    commit: starter-kit
    path: wiki/index.md
    evidence_type: declared
relations:
  - type: CONTAINS
    target: service.order
  - type: CONTAINS
    target: api.order.v2
  - type: CONTAINS
    target: flow.place-order
---

# Approved Engineering Knowledge

This directory contains the canonical, reviewable knowledge used by Kiro and the knowledge-plane MCP server.

## Entry points

- [Order Service](services/order-service.md)
- [Order API v2](apis/order-api-v2.md)
- [Place Order user flow](user-flows/place-order.md)

Generated documentation is published separately under `openwiki/` and is not authoritative.
