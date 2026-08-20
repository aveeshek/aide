# BOS AIDE Knowledge-Centric Loop Engineering

## Architecture and Detailed Design

**Subtitle:** Graph-Governed Spec-Driven Development for Single- and Multi-Microservice Delivery  
**Version:** 1.0.1  
**Date:** 20 August 2026  
**Deployment baseline:** Native Windows 11 x64

---

## 1. Executive summary

BOS AIDE Knowledge-Centric Loop Engineering combines three disciplines:

1. **Spec-Driven Development** defines the destination: requirements, design, tasks, acceptance criteria, and traceability.
2. **Loop Engineering** executes bounded Goal -> Action -> Observation -> Adjustment cycles until deterministic evidence produces PASS, a decision requires ESCALATE, or limits produce FAIL.
3. **Graph Engineering** provides connected enterprise context: services, repositories, APIs, events, schemas, data, user flows, tests, ADRs, owners, deployments, incidents, and provenance.

A multi-service change does not use one unrestricted global coding loop. It starts with one enterprise specification and graph-derived impact context, derives one local specification per affected service, and executes separate service, contract, integration, and E2E loops.

The Knowledge Plane is Markdown-first:

- Git-backed `wiki/` pages are governed artifacts.
- Neo4j is the exact typed relationship index.
- Graphiti adds temporal and semantic context.
- OpenWiki compiles user-readable documentation.
- Kiro retrieves bounded context through indexed resources and a custom MCP server.
- Only reviewed and merged outcomes become canonical learning.

---

## 2. Architecture principles

1. Kiro proposes; deterministic gates and human-governed delivery systems decide.
2. Markdown is durable; the graph is rebuildable.
3. Deterministic extraction precedes LLM synthesis.
4. Declared, contracted, implemented, and observed evidence remain distinct.
5. Context is assembled for the task, not dumped wholesale.
6. Loops have explicit scope, gates, budgets, escalation, and terminal states.
7. The enterprise orchestrator coordinates and routes; it does not edit all repositories freely.
8. OpenWiki and temporal memory are derived and lower trust.
9. Learning is merge-gated.
10. The exact graph remains usable when Graphiti or an LLM provider is unavailable.

---

## 3. Goals and non-goals

### Goals

- Support new and legacy systems from one repository to enterprise service graphs.
- Keep knowledge predominantly in Markdown.
- Give Kiro exact contract and schema evidence.
- Provide graph-based impact analysis and failure routing.
- Bound agent execution and cost.
- Preserve provenance and history.
- Generate readable documentation without weakening authority.
- Run natively on Windows without containers.

### Non-goals

- Fine-tune a model on every source change.
- Replace Git, CI, Jira, architecture review, or CODEOWNERS.
- Allow Kiro to deploy directly to production.
- Treat OpenWiki, Graphiti, or Mem0 as canonical truth.
- Add a separate vector platform before scale measurements justify it.

---

## 4. Operating model

### Single microservice

```text
Feature Spec -> task loop -> service loop -> deterministic gates -> PR -> approved learning
```

### Multiple microservices

```text
Enterprise Spec -> graph impact/context -> bounded service-local specs
-> service loops -> contract loop -> integration loop -> E2E loop
-> coordinated PRs -> approved learning
```

---

## 5. System context

```mermaid
flowchart TB
    U[Product owner, architect, developer, tester]
    K[Kiro IDE / CLI]
    M[Knowledge-Plane MCP]
    W[Canonical Markdown wiki]
    N[Neo4j exact graph]
    G[Graphiti temporal graph]
    R[Application repositories]
    D[Jira, Git, CI, test and artifact systems]
    O[OpenWiki]
    Z[Zensical portal]
    H[CODEOWNERS and reviewers]
    U --> K
    K --> M
    M --> W
    M --> N
    M --> G
    K --> R
    K --> D
    R --> D
    D --> H
    H --> W
    W --> N
    W --> G
    W --> O
    O --> Z
    W --> Z
```

---

## 6. Layered reference architecture

```mermaid
flowchart TB
    subgraph X[Experience and specification]
        K[Kiro IDE / CLI]
        S[Feature Specs and Quick Spec]
        A[Custom agents and steering]
    end
    subgraph C[Context and loop orchestration]
        E[Enterprise E2E orchestrator]
        L[Service-loop agents]
        CT[Contract loop]
        ET[Integration and E2E loops]
        B[Knowledge Context Broker / MCP]
    end
    subgraph P[Knowledge and graph plane]
        MD[Canonical Git Markdown]
        NG[Neo4j exact graph]
        GT[Graphiti temporal context]
        OW[OpenWiki derived docs]
        OB[Obsidian authoring]
    end
    subgraph Q[Evidence and authority]
        BU[Build and static checks]
        TE[Unit, component, contract and E2E tests]
        SE[Security and SBOM gates]
        PR[PR, CI, CODEOWNERS and review]
    end
    K --> S
    S --> E
    E --> B
    B --> MD
    B --> NG
    B --> GT
    E --> L
    L --> CT
    CT --> ET
    L --> BU
    L --> TE
    CT --> TE
    ET --> TE
    BU --> PR
    TE --> PR
    SE --> PR
    PR --> MD
    MD --> NG
    MD --> GT
    MD --> OW
    OB --> MD
```

---

## 7. Final component stack

| Capability | Choice | Architectural role |
|---|---|---|
| Specification | Kiro Feature Specs | Requirements, design, tasks and acceptance traceability |
| Loop orchestration | Kiro agents + YAML contracts + CI | Bounded execution and deterministic termination |
| Canonical knowledge | Git Markdown + YAML | Governed, human-readable knowledge |
| Exact graph | Neo4j 5.26 LTS | Typed traversal and deterministic provenance |
| Temporal graph | Graphiti | Changing facts, episodes and hybrid retrieval |
| Context interface | Custom MCP server | Policy boundary between Kiro and knowledge systems |
| Documentation | OpenWiki + Zensical | Derived explanations and Mermaid portal |
| Authoring | Obsidian | Human navigation and editing |
| Authority | Git/Jira/CI/CODEOWNERS | Acceptance and publication control |

---

## 8. Loop state model

```mermaid
stateDiagram-v2
    [*] --> Ready
    Ready --> ContextReady: approved spec, graph context, loop contract
    ContextReady --> Act: select smallest task
    Act --> Verify: change code and tests
    Verify --> Observe: collect deterministic evidence
    Observe --> Pass: all required gates pass
    Observe --> Adjust: fixable within scope and budget
    Adjust --> Act
    Observe --> Escalate: ambiguity, policy, contract or new dependency
    Observe --> Fail: non-recoverable or budget exhausted
    Pass --> EvidenceBundle
    Escalate --> EvidenceBundle
    Fail --> EvidenceBundle
    EvidenceBundle --> [*]
```

Every loop contract defines goal, allowed repositories and paths, forbidden actions, escalation conditions, verification gates, budgets, and exactly three terminal states.

---

## 9. Single-service sequence

```mermaid
sequenceDiagram
    autonumber
    actor D as Developer / architect
    participant K as Kiro service-loop agent
    participant M as Knowledge-Plane MCP
    participant R as Service repository
    participant G as Deterministic gates
    participant P as CI / PR reviewer
    D->>K: Approve requirements, design and tasks
    K->>M: resolve_task_context(story, service)
    M-->>K: bounded context, provenance and contradictions
    K->>R: create scoped branch or worktree
    loop Configured maximum iterations
        K->>R: implement smallest pending task and tests
        K->>G: compile, lint, test and scan
        G-->>K: structured evidence
        alt required gates pass
            K->>K: mark task PASS
        else fixable within scope and budget
            K->>K: diagnose and adjust
        else decision or cross-service dependency
            K->>K: terminate ESCALATE
        else budget exhausted
            K->>K: terminate FAIL
        end
    end
    K->>P: PR with traceability and evidence bundle
    P-->>D: authoritative review decision
```

---

## 10. Multi-service nested loops

```mermaid
flowchart TD
    ST[Enterprise story] --> ES[Enterprise E2E spec]
    ES --> GI[Graph impact analysis]
    GI --> CP[Bounded E2E context pack]
    CP --> SA[Service A local spec]
    CP --> SB[Service B local spec]
    CP --> SN[Service N local spec]
    SA --> LA[Service A loop]
    SB --> LB[Service B loop]
    SN --> LN[Service N loop]
    LA --> CG[Contract compatibility loop]
    LB --> CG
    LN --> CG
    CG -->|PASS| IG[Integration loop]
    CG -->|failure| FR[Graph-based failure routing]
    IG -->|PASS| EG[E2E business-flow loop]
    IG -->|failure| FR
    EG -->|failure| FR
    FR --> LA
    FR --> LB
    FR --> LN
    EG -->|PASS| PR[Coordinated pull requests]
    PR --> AU[CI, CODEOWNERS and human approval]
    AU --> KL[Approved knowledge learning]
```

---

## 11. Enterprise orchestration sequence

```mermaid
sequenceDiagram
    autonumber
    actor O as Product / architecture owner
    participant E as Enterprise E2E orchestrator
    participant K as Knowledge-Plane MCP
    participant S as Service-loop agents
    participant C as Contract test system
    participant T as E2E test system
    participant R as CI / CODEOWNERS
    O->>E: Approve enterprise requirements and constraints
    E->>K: resolve context and analyze impact
    K-->>E: services, contracts, owners, tests, drift and provenance
    E->>E: build service-impact, contract, rollout and rollback plans
    par Derive bounded service specs
        E->>S: Service A spec and loop contract
        E->>S: Service B spec and loop contract
        E->>S: Service N spec and loop contract
    end
    S-->>E: PASS, ESCALATE or FAIL with evidence
    E->>C: run compatibility checks when service loops pass
    C-->>E: compatibility matrix and evidence
    E->>T: run integration and E2E flows
    T-->>E: flow evidence and failure path
    E->>R: coordinated PR dependency map and bundles
    R-->>O: authoritative merge decision
```

---

## 12. Graph Engineering lifecycle

Graph Engineering comprises:

1. Ontology engineering.
2. Deterministic extraction.
3. Entity resolution.
4. Relationship and provenance validation.
5. Context retrieval and impact analysis.
6. Graph evolution after approved delivery.

It is not merely loading Markdown into Neo4j.

```mermaid
flowchart LR
    S[HLD, LLD, ADR, contracts, schemas, code, tests, IaC] --> D[Deterministic parsers]
    S --> L[LLM-assisted semantic compiler]
    D --> C[Candidate canonical Markdown]
    L --> C
    C --> V[Schema, provenance and contradiction validation]
    V --> P[Knowledge pull request]
    P --> R[CI, CODEOWNERS and human review]
    R -->|approved| W[Approved wiki]
    R -->|rejected| X[Correct or retain as non-authoritative evidence]
    W --> N[Neo4j exact graph]
    W --> G[Graphiti enrichment]
    W --> O[OpenWiki generation]
    O --> Z[Documentation PR and Zensical portal]
```

---

## 13. Context assembly

```mermaid
sequenceDiagram
    autonumber
    participant K as Kiro
    participant B as Context Broker / MCP
    participant W as Canonical Markdown index
    participant N as Neo4j exact graph
    participant G as Graphiti temporal graph
    participant O as Operations registers
    K->>B: resolve_task_context(story, targets, token budget)
    B->>W: retrieve approved pages
    W-->>B: pages and source references
    B->>N: traverse typed relationships
    N-->>B: services, contracts, data, tests, owners and ADRs
    B->>G: temporal search when enabled
    G-->>B: episodes and changing facts
    B->>O: contradictions and staleness
    O-->>B: unresolved warnings
    B->>B: trust rank, deduplicate and budget
    B-->>K: bounded context pack with provenance and uncertainty
```

Context packs are disposable views, not canonical knowledge.

---

## 14. Context-pack model

```text
generated/context-packs/<story-id>/
|-- objective.md
|-- acceptance-criteria.md
|-- affected-services.md
|-- user-flow.md
|-- current-contracts.md
|-- data-impact.md
|-- code-entry-points.md
|-- relevant-adrs.md
|-- existing-tests.md
|-- dependency-order.md
|-- rollout-and-rollback.md
|-- contradictions.md
`-- provenance.md
```

---

## 15. Core ontology

```mermaid
classDiagram
    class EnterpriseProject
    class BusinessCapability
    class UserFlow
    class FlowStep
    class Requirement
    class AcceptanceCriterion
    class Service
    class Repository
    class CodeSymbol
    class API
    class Endpoint
    class Event
    class Schema
    class Database
    class Table
    class ADR
    class Test
    class Owner
    class Deployment
    EnterpriseProject --> BusinessCapability : CONTAINS
    BusinessCapability --> UserFlow : REALIZED_BY
    UserFlow --> FlowStep : CONTAINS
    FlowStep --> Service : PARTICIPATES_IN
    Requirement --> AcceptanceCriterion : CONTAINS
    Service --> Repository : IMPLEMENTED_IN
    Repository --> CodeSymbol : CONTAINS
    Service --> API : EXPOSES
    API --> Endpoint : CONTAINS
    Service --> Event : PUBLISHES_OR_CONSUMES
    Event --> Schema : USES_SCHEMA
    Service --> Table : READS_OR_WRITES
    Database --> Table : CONTAINS
    Service --> ADR : GOVERNED_BY
    AcceptanceCriterion --> Test : VALIDATED_BY
    Owner --> Service : OWNS
    Service --> Deployment : DEPLOYED_AS
```

Every fact should preserve source, commit, location or pointer, evidence class, confidence, review status, validity interval, last verification, extractor, and access scope.

---

## 16. Contract change sequence

```mermaid
sequenceDiagram
    autonumber
    participant E as Enterprise orchestrator
    participant P as Producer service loop
    participant G as Knowledge graph
    participant C as Consumer service loops
    participant T as Contract gate
    participant D as Deployment authority
    E->>G: identify producer, consumers, schemas and rollout constraints
    G-->>E: current edges, owners, versions and tests
    E->>P: approved producer-local spec
    E->>C: approved consumer-local specs
    P-->>E: producer evidence
    C-->>E: consumer evidence
    E->>T: validate schemas and consumer compatibility
    T-->>E: compatibility matrix
    alt backward compatible
        E->>D: approved rollout sequence and feature flags
    else breaking change required
        E->>E: terminate ESCALATE for migration/version decision
    end
```

---

## 17. Self-learning model

Self-learning means evidence-driven improvement of knowledge and procedure, not unsupervised rewriting of architectural truth.

```mermaid
stateDiagram-v2
    [*] --> Observed
    Observed --> Candidate: extraction or delivery outcome
    Candidate --> Validated: schema, provenance and target checks
    Candidate --> Rejected: invalid or unsupported
    Validated --> Reviewed: pull request opened
    Reviewed --> Approved: CI, CODEOWNERS and human approval
    Reviewed --> Rejected: corrections required
    Approved --> Published: protected merge and ingestion
    Published --> Superseded: newer approved fact
    Published --> Deprecated: intentionally retired
    Superseded --> [*]
    Deprecated --> [*]
    Rejected --> [*]
```

| Learning domain | Examples | Rule |
|---|---|---|
| Semantic knowledge | APIs, schemas, dependencies, ownership | Source-backed PR required |
| Episodic memory | Attempt, incident, task discussion | Advisory and retention-controlled |
| Procedural knowledge | Testing or migration convention | Promote to steering after reviewed evidence |
| Retrieval learning | Query misses and accepted context | Improve ranking, not canonical facts |

---

## 18. Trust and security boundaries

```mermaid
flowchart TB
    subgraph A[Authoritative control plane]
        J[Jira and approved story]
        R[Protected Git branches]
        C[CI and deterministic gates]
        H[CODEOWNERS and reviewers]
    end
    subgraph K[Governed knowledge]
        W[Approved canonical Markdown]
        N[Neo4j exact graph]
    end
    subgraph D[Derived and advisory]
        G[Graphiti episodes]
        O[OpenWiki documentation]
        P[Context packs]
        M[Optional personalized memory]
    end
    subgraph E[Agent execution]
        I[Kiro]
        B[Policy-enforcing MCP]
        X[Candidate changes]
    end
    A --> K
    K --> D
    K --> B
    D --> B
    B --> I
    I --> X
    X --> A
```

The transition from candidate changes to authority always crosses validation and human review.

---

## 19. Windows native deployment

```mermaid
flowchart LR
    subgraph W[Windows 11 x64]
        K[Kiro IDE / CLI]
        P[Python 3.12+ virtual environment]
        M[FastMCP stdio server]
        N[Neo4j 5.26 Windows service]
        O[OpenWiki Node.js CLI]
        Z[Zensical Python CLI]
        B[Obsidian]
        F[Git-backed filesystem]
        T[Task Scheduler / CI agent]
    end
    K -->|child process| M
    M --> P
    M -->|Bolt| N
    M --> F
    O --> F
    Z --> F
    B --> F
    T --> O
    T --> Z
    T --> P
```

---

## 20. MCP design

Read tools:

```text
health
list_knowledge_pages
read_knowledge_page
get_entity
search_knowledge
trace_dependencies
analyze_change_impact
resolve_task_context
list_contradictions
```

Controlled write tool:

```text
propose_knowledge_delta
```

The write tool may create a candidate only under `generated/candidates/`. It cannot write to `wiki/`, merge a branch, or publish graph facts.

---

## 21. OpenWiki architecture

```text
Approved wiki and source evidence
    -> OpenWiki generation
    -> openwiki/ derived Markdown
    -> documentation PR
    -> review
    -> Zensical portal
```

OpenWiki pages may orient a reader or agent. Exact code, contract, and schema decisions must rely on canonical and source evidence.

---

## 22. Failure routing

| Failure | Required response |
|---|---|
| Local build/test failure | Continue local loop within scope and budget |
| New service dependency | Terminate ESCALATE and update enterprise impact |
| Contract incompatibility | Route to contract loop and owners |
| E2E failure with graph path | Route to responsible service or edge loop |
| Unknown failure owner | ESCALATE and create a knowledge-gap candidate |
| Graphiti provider unavailable | Continue with Markdown and exact Neo4j graph |
| Neo4j unavailable | Stop graph-dependent planning; do not invent impact |
| Contradictory current facts | Surface both with provenance |
| OpenWiki hallucination | Reject derived documentation |
| Loop budget exhausted | Terminate FAIL or ESCALATE; never continue indefinitely |

---

## 23. Observability and evaluation

Collect:

- MCP request count, latency, errors, and tool use.
- Neo4j query latency and result size.
- Graphiti provider cost, latency, and failures.
- Ingestion duration, nodes, edges, contradictions, and staleness.
- Loop iterations, elapsed time, terminal state, gates, files, and credits.
- OpenWiki changed pages and PR acceptance.

Measure:

| Metric | Purpose |
|---|---|
| Context precision and recall | Useful context without missing critical facts |
| Provenance coverage | Claims with resolvable evidence |
| Contract hallucination rate | Invented endpoint/event/field/table references |
| Impact-analysis accuracy | Correct affected services and consumers |
| Loop convergence | PASS rate and iterations |
| Escalation quality | Correct owner, evidence, and decision request |
| Knowledge-delta acceptance | Candidate learning approved after review |
| Delivery outcome | CI, defects, rollback, and lead-time results |

---

## 24. Scalability

### Small service
Use local Kiro specs, bounded loops, direct Markdown indexing, and optionally a lightweight graph.

### Six to seven services
Use the complete design: enterprise spec, Neo4j, Graphiti, MCP, service loops, contract loop, E2E loop, OpenWiki, and merge-gated learning.

### Large legacy estate
Add Tree-sitter/SCIP-style code intelligence, incremental ingestion, repository federation, access-control propagation, and stronger evidence-class separation.

### Enterprise federation
Use globally unique IDs and a shared ontology while allowing domain-owned knowledge repositories and graph groups.

---

## 25. Architecture decisions

### ADR-001 - Git Markdown is canonical
Graphs are rebuildable; publication uses ordinary PR governance.

### ADR-002 - Exact and temporal graphs coexist
Neo4j stores deterministic facts; Graphiti supplies temporal and semantic context.

### ADR-003 - Custom MCP policy facade
Kiro receives task-oriented tools, not unrestricted Cypher or graph administration.

### ADR-004 - Multi-service work uses nested loops
The enterprise orchestrator coordinates bounded service, contract, integration, and E2E loops.

### ADR-005 - OpenWiki is derived
Generated documentation cannot override canonical knowledge.

### ADR-006 - Native Windows baseline
Neo4j runs as a service; Python and Node tools run natively without containers.

### ADR-007 - Zensical for new portals
Use a current Mermaid-capable documentation generator while preserving Markdown portability.

---

## 26. Delivery roadmap

1. Standardize Kiro Feature Specs and deterministic local loops.
2. Normalize canonical Markdown and build the exact Neo4j graph.
3. Add graph-backed impact and bounded service-local specs.
4. Add contract, integration, and E2E loops.
5. Enable Graphiti with an approved provider.
6. Add OpenWiki and the Zensical portal.
7. Add access-control propagation, evaluation, and federation.

---

## 27. Architecture acceptance criteria

- [ ] Exact graph rebuilds from approved Markdown.
- [ ] Every published graph fact has provenance and review status.
- [ ] Single-service loops enforce repository, path, gate, and budget scope.
- [ ] Multi-service changes have one enterprise spec and one local spec per affected service.
- [ ] Contract and E2E loops pass before coordinated merge.
- [ ] Kiro cannot silently expand a service loop into another repository.
- [ ] Exact retrieval works during Graphiti/provider degradation.
- [ ] OpenWiki cannot overwrite canonical knowledge.
- [ ] Candidate learning cannot bypass CI and review.
- [ ] The developer topology runs natively on Windows.

---

## 28. Summary

> The specification defines the destination.  
> The graph identifies the connected route and evidence.  
> Bounded loops implement, observe, adjust, and prove the journey.  
> Deterministic gates and humans decide what is accepted and learned.

---

## 29. Primary references

- Kiro Feature Specs: https://kiro.dev/docs/specs/feature-specs/
- Kiro MCP: https://kiro.dev/docs/mcp/
- Kiro custom agents: https://kiro.dev/docs/cli/custom-agents/configuration-reference/
- Neo4j Windows installation: https://neo4j.com/docs/operations-manual/current/installation/windows/
- Graphiti: https://github.com/getzep/graphiti
- MCP Python SDK: https://github.com/modelcontextprotocol/python-sdk
- OpenWiki: https://github.com/langchain-ai/openwiki
- Zensical: https://zensical.org/docs/get-started/
