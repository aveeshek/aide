# BOS AIDE Windows Native Starter Kit 1.0.1

Release date: 20 August 2026

## Python compatibility fix

This release changes the runtime policy from a Python 3.12 pin/range to **Python 3.12 or later**.

### Changed

- `pyproject.toml`: `requires-python = ">=3.12"`.
- Package version synchronized to `1.0.1` in both `pyproject.toml` and `knowledge_plane.__version__`.
- Windows installer auto-selects a compatible runtime and rejects Python older than 3.12.
- `-PythonVersion <minor>` can force a Windows `py` launcher version.
- `-RecreateVenv` can rebuild the repository-local `.venv` on the selected runtime.
- Existing `.venv` runtime is validated before reuse.
- CI validation matrix configured for Python 3.12, 3.13, and 3.14.
- Publish workflow moved to Python 3.14 as the latest configured qualification runtime.
- Ruff remains `py312` intentionally so source syntax stays compatible with the minimum runtime.
- Manual install examples use double quotes around `.[dev,docs]`, which works in both PowerShell and Command Prompt.
- MCP/health output now reports Knowledge Plane and Python runtime versions.
- Installation and architecture Markdown/DOCX documentation updated for Python 3.12+.

## Recommended Windows use

Use the preferred Python on PATH:

```cmd
python --version
python -m venv .venv
.venv\Scripts\activate.bat
python -m pip install --upgrade pip setuptools wheel
python -m pip install -e ".[dev,docs]"
```

Or let the PowerShell installer select a compatible runtime:

```powershell
.\scripts\install-native-windows.ps1
```

Force Python 3.14 and rebuild an existing repository-local environment:

```powershell
.\scripts\install-native-windows.ps1 -PythonVersion 3.14 -RecreateVenv
```
