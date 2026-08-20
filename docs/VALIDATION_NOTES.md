# Validation notes

Updated on 20 August 2026 for the Python 3.12+ compatibility release.

## Python compatibility changes

- `pyproject.toml` now declares `requires-python = ">=3.12"` with no artificial upper minor-version cap.
- Ruff remains targeted at `py312` to preserve syntax compatibility with the minimum supported runtime.
- The Windows installer auto-selects a Python 3.12+ runtime and supports `-PythonVersion` and `-RecreateVenv`.
- The GitHub validation workflow is configured as a Python 3.12 / 3.13 / 3.14 matrix.
- The publish workflow uses Python 3.14 as the latest runtime in that configured qualification matrix.
- The Knowledge Plane package/version metadata is synchronized at `1.0.1`.
- Health output now reports both Knowledge Plane version and Python runtime version.
- Command Prompt guidance now uses double quotes for `.[dev,docs]`.

## Artifact validation performed

- Python source compilation completed successfully under Python 3.13.5 in the artifact environment.
- Focused unit tests passed (`2 passed`).
- Canonical knowledge validation passed (`status: ok`, 9 pages).
- TOML metadata parsed successfully and reports `requires-python = ">=3.12"`.
- YAML/Markdown source structure was retained.
- Both DOCX documents were regenerated/updated and rendered for visual inspection.
- ZIP integrity was checked after packaging.

The artifact environment cannot execute native Windows Service Control Manager, Kiro, or Windows PowerShell installation flows. The configured GitHub CI matrix should be run after import to produce authoritative 3.12/3.13/3.14 runtime evidence. Native Neo4j, MCP, OpenWiki, Graphiti, and Zensical smoke tests must be executed on the target Windows host.
