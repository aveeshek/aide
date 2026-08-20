---
inclusion: always
---

# Engineering Knowledge Rules

Before creating a design or changing code:

1. Call `resolve_task_context` with the story and any known service or API IDs.
2. Use current approved facts unless the task explicitly requests historical state.
3. Treat code, contracts, schemas, Jira, deployment records, and CI as authoritative evidence.
4. Treat approved HLD, LLD, ADR, NFR, policy, and canonical `wiki/` pages as governed context.
5. Treat `openwiki/`, Graphiti episodes, and any personalized memory as derived or advisory.
6. Surface contradictions instead of silently choosing one source.
7. Never invent an endpoint, event, field, table, configuration key, owner, or code symbol.
8. Cite canonical page paths, source repositories, commits, pointers, or symbols for architectural claims.
9. Produce the smallest E2E design and task set that covers all affected services and tests.
10. After implementation, call `propose_knowledge_delta` only when approved knowledge must change.
11. A candidate delta requires validation, a pull request, CI, CODEOWNER review, and protected-branch merge.
