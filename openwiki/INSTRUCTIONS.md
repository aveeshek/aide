# OpenWiki repository brief

Generate and maintain user-readable documentation for this engineering knowledge-plane repository.

## Authoritative input

Use these sources, in this order:

1. `wiki/` - approved canonical knowledge
2. `ontology/` - allowed entity and relationship vocabulary
3. `manifests/` - repository, ownership, and source-path metadata
4. `operations/` - explicit contradictions and staleness reports

Treat `generated/`, `.site-docs/`, `site/`, and existing prose in `openwiki/` as derived output, not as independent evidence.

## Required generated views

Maintain concise, interlinked Markdown for:

- executive architecture overview
- service catalog and ownership map
- E2E user-flow narratives
- API, event, and schema maps
- dependency and impact-analysis guides
- ADR and constraint summaries
- test and quality-gate traceability
- glossary
- known contradictions and stale knowledge

## Governance rules

- Never edit `wiki/`, `ontology/`, or `manifests/`.
- Never claim that generated documentation is authoritative.
- Preserve canonical IDs in each page.
- Link claims back to canonical Markdown pages and reproduce source references when available.
- Surface contradictions instead of resolving them silently.
- Do not invent endpoints, fields, events, tables, owners, or code symbols.
- Prefer Mermaid diagrams for architecture and flows.
- Keep each page useful to both engineers and non-engineering stakeholders.
- Add a generated-content notice to every top-level generated page.

## Loop and graph documentation

Also maintain reviewed explanations of:

- the single-service task and service loops
- enterprise graph impact and context assembly
- bounded service-local specifications
- producer-consumer contract loops
- integration and E2E verification loops
- PASS, ESCALATE, and FAIL termination evidence
- the approved knowledge-learning lifecycle
