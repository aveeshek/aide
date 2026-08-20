# Engineering Knowledge Schema

This repository follows a controlled, LLM-wiki-style compilation model: immutable or reviewed sources are transformed into interlinked Markdown concept pages. The Markdown pages are the governed artifact; databases and indexes are rebuildable.

## Required frontmatter

Every canonical concept under `wiki/`, except directory index pages explicitly marked `type: Index`, must contain:

```yaml
---
id: service.order
kind: Service
type: Service
title: Order Service
status: approved
review_status: approved
owner: team-commerce
last_verified_at: 2026-07-22
source_refs:
  - repository: order-service
    commit: 0123456789abcdef
    path: docs/hld/order-service.md
    lines: "41-96"
    evidence_type: declared
relations:
  - type: EXPOSES
    target: api.order.v2
---
```

`type` is included for Open Knowledge Format compatibility. `kind` is the engineering ontology field. For canonical pages, keep both values identical.

## Evidence classes

- `declared`: HLD, LLD, ADR, runbook, or approved design states the fact.
- `contracted`: OpenAPI, AsyncAPI, protobuf, GraphQL, DDL, or schema states the fact.
- `implemented`: source code, configuration, migration, or infrastructure implements the fact.
- `observed`: traces, logs, runtime inventory, deployment records, or incidents show the fact.

Do not silently collapse conflicting evidence classes. Record the conflict under `operations/contradictions.md` and expose it to Kiro.

## Status model

`candidate -> validated -> reviewed -> approved -> superseded | deprecated`

Only `approved` pages may be treated as current architectural truth. Generated OpenWiki pages are always derived even when their content was produced from approved material.

## Relationship rules

- Relationship types must exist in `ontology/relationship-types.yaml`.
- Targets must resolve to a canonical page ID.
- Relationships are directional unless the relationship definition says otherwise.
- Every relationship inherits the source page's provenance; add relation-level evidence when it differs.

## Source-of-truth rule

For delivery decisions use this precedence:

1. Code, contracts, schema, issue tracking, deployment records, and CI evidence
2. Approved HLD, LLD, ADR, NFR, policy, and runbook content
3. Canonical compounding Markdown wiki
4. OpenWiki-generated synthesis
5. Temporal episodes and personalized memory
6. General model knowledge
