# Python Compatibility Policy

## Policy

BOS AIDE Knowledge Plane requires **Python 3.12 or later**.

- Minimum supported version: Python 3.12.
- Package metadata: `requires-python = ">=3.12"`.
- Configured CI qualification minors: Python 3.12, 3.13, and 3.14.
- Newer Python 3.x versions are allowed by package metadata and should be added to the validation matrix when qualified.
- Ruff remains `target-version = "py312"` so source syntax stays compatible with the minimum supported runtime.

## Windows interpreter selection

The native installer follows this order when `-PythonVersion` is not supplied:

1. Use `python` from `PATH` if available and Python 3.12 or later.
2. Otherwise use `py -3` from the Windows Python launcher.
3. Reject any runtime older than Python 3.12.

To force a registered interpreter:

```powershell
.\scripts\install-native-windows.ps1 -PythonVersion 3.14
```

To recreate an existing repository-local `.venv` with that runtime:

```powershell
.\scripts\install-native-windows.ps1 -PythonVersion 3.14 -RecreateVenv
```

Useful discovery commands:

```powershell
python --version
py -0p
```

## Manual virtual environment creation

PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip setuptools wheel
python -m pip install -e ".[dev,docs]"
```

Command Prompt:

```cmd
python -m venv .venv
.venv\Scripts\activate.bat
python -m pip install --upgrade pip setuptools wheel
python -m pip install -e ".[dev,docs]"
```

Use double quotes around `.[dev,docs]` in Command Prompt. Single quotes are passed literally by `cmd.exe`.
