---
inclusion: always
---
# Bounded Loop Engineering Rules
1. Treat each approved task as a bounded Goal -> Action -> Observation -> Adjustment loop.
2. Load the applicable contract from `loops/` before editing code.
3. Respect allowed repositories, paths, forbidden actions, budgets, and escalation conditions.
4. Run deterministic verification after every meaningful change.
5. Stop only in PASS, ESCALATE, or FAIL.
6. Never expand a service loop into another repository; route cross-service discoveries to the enterprise orchestrator.
7. Record commands, results, changed files, uncertainty, and terminal state in the PR evidence bundle.
