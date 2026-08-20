# BOS AIDE Graph-Governed Spec-Driven Loop Engineering

A Windows-native starter kit combining Kiro Spec-Driven Development, bounded Loop Engineering, Graph Engineering, a Markdown-first Knowledge Plane, OpenWiki, and Zensical.

No Docker, Docker Compose, Podman, WSL, or Kubernetes is required.

## Python compatibility

- Minimum supported runtime: **Python 3.12**.
- Default behavior: use the preferred installed Python 3.12+ runtime; the installer falls back to `py -3`.
- CI qualification matrix is configured for **3.12, 3.13, and 3.14**.
- `pyproject.toml` intentionally uses `requires-python = ">=3.12"`; Ruff remains `py312` so source syntax stays compatible with the minimum runtime.
- To force a registered version: `.\scripts\install-native-windows.ps1 -PythonVersion 3.14`.
- To rebuild `.venv` on a selected version: add `-RecreateVenv`.

Check available interpreters with `python --version` and `py -0p`.

## Operating model

```text
Single service:
Feature Spec -> task/service loop -> deterministic gates -> PR -> approved learning

Multiple services:
Enterprise Spec -> graph context -> service-local specs -> service loops
-> contract loop -> integration loop -> E2E loop -> coordinated review
```

The enterprise orchestrator coordinates and routes. It is not an unrestricted global coding agent.

## Documents

- `docs/BOS_AIDE_Loop_Graph_Windows_Installation_Guide.md`
- `docs/BOS_AIDE_Loop_Graph_Architecture.md`
- `docs/PYTHON_COMPATIBILITY.md`
- `docs/VALIDATION_NOTES.md`

## Install

```powershell
# Elevated PowerShell for Neo4j
.\scripts\install-neo4j-service.ps1 `
  -Neo4jHome 'C:\BOS\Neo4j\neo4j-community-5.26.x'

# Standard PowerShell for the application
.\scripts\install-native-windows.ps1
.\scripts\healthcheck.ps1
.\scripts\validate.ps1
.\scripts\ingest.ps1 -Graphiti off
```

For manual installation from **Command Prompt (`cmd.exe`)**, use double quotes around extras: `python -m pip install -e ".[dev,docs]"`.

## Validate a loop contract

```powershell
.\scripts\validate-loop.ps1 `
  -Contract 'loops\service-loop.yaml' `
  -RunId 'STORY-123-service-a'
```

## Documentation

```powershell
.\scripts\openwiki-init.ps1
.\scripts\openwiki-update.ps1
.\scripts\serve-docs.ps1
```

OpenWiki writes derived documentation under `openwiki/`. Zensical publishes canonical and generated content as separate trust levels.

## Authority

Kiro proposes. Build, test, security, CI, Jira, Git, CODEOWNERS, and human reviewers decide. Canonical knowledge enters `wiki/` only after a reviewed merge.
