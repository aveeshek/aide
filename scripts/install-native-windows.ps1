[CmdletBinding()]
param(
    # Empty means auto-select: preferred `python` on PATH, then `py -3`.
    # Supply 3.12 / 3.13 / 3.14 / etc. to force a registered py-launcher runtime.
    [string]$PythonVersion = '',
    [switch]$RecreateVenv,
    [switch]$SkipOpenWiki,
    [switch]$SkipTests,
    [Security.SecureString]$Neo4jPassword
)

. (Join-Path $PSScriptRoot 'common.ps1')

$root = Get-RepositoryRoot
Write-Host "Installing the knowledge plane natively in $root" -ForegroundColor Cyan

if (-not [Environment]::Is64BitOperatingSystem) {
    throw 'A 64-bit Windows operating system is required.'
}

$required = @('git', 'java')
if (-not $SkipOpenWiki) {
    $required += @('node', 'npm')
}
$missing = @($required | Where-Object { -not (Test-CommandAvailable $_) })
if ($missing.Count -gt 0) {
    throw "Missing required commands: $($missing -join ', '). Install the prerequisites listed in the installation guide, open a new PowerShell window, and rerun this script."
}

# Select a Python interpreter. Python 3.12 is the minimum, not a pinned runtime.
# An explicit -PythonVersion uses the Windows py launcher. Otherwise prefer the
# user's PATH-selected `python`, then fall back to the latest Python 3 known to `py`.
$pythonCommand = $null
$pythonPrefixArgs = @()
$pythonDescription = $null

if (-not [string]::IsNullOrWhiteSpace($PythonVersion)) {
    if (-not (Test-CommandAvailable 'py')) {
        throw "The Windows Python launcher 'py' is required when -PythonVersion is supplied."
    }
    $pythonCommand = 'py'
    $pythonPrefixArgs = @("-$PythonVersion")
    $pythonDescription = "py -$PythonVersion"
}
elseif (Test-CommandAvailable 'python') {
    $pathPython = ((& python -c "import platform; print(platform.python_version())") | Out-String).Trim()
    Assert-LastExitCode 'PATH Python version check'
    $pathCompatible = (& python -c "import sys; raise SystemExit(0 if sys.version_info >= (3,12) else 3)")
    $pathExitCode = $LASTEXITCODE
    if ($pathExitCode -eq 0) {
        $pythonCommand = 'python'
        $pythonDescription = 'python from PATH'
    }
    elseif ($pathExitCode -eq 3 -and (Test-CommandAvailable 'py')) {
        Write-Warning "PATH Python $pathPython is below 3.12; falling back to py -3."
        $pythonCommand = 'py'
        $pythonPrefixArgs = @('-3')
        $pythonDescription = 'py -3'
    }
    else {
        throw "Python 3.12 or later is required. Detected PATH Python $pathPython and no compatible fallback was available."
    }
}
elseif (Test-CommandAvailable 'py') {
    $pythonCommand = 'py'
    $pythonPrefixArgs = @('-3')
    $pythonDescription = 'py -3'
}
else {
    throw 'Python 3.12 or later is required. Neither python nor the Windows py launcher was found.'
}

$selectedPython = ((& $pythonCommand @pythonPrefixArgs -c "import platform,sys; print(platform.python_version()); raise SystemExit(0 if sys.version_info >= (3,12) else 3)") | Out-String).Trim()
if ($LASTEXITCODE -eq 3) {
    throw "Python 3.12 or later is required. Detected Python $selectedPython using $pythonDescription."
}
Assert-LastExitCode "Python compatibility check ($pythonDescription)"
Write-Host "Using $pythonDescription -> Python $selectedPython" -ForegroundColor Green

if (-not $SkipOpenWiki) {
    $nodeVersion = (& node --version).Trim().TrimStart('v')
    Assert-LastExitCode 'Node.js version check'
    $nodeMajor = [int]($nodeVersion.Split('.')[0])
    if ($nodeMajor -lt 22) {
        throw "OpenWiki requires Node.js 22 or later. Detected $nodeVersion."
    }
}

$javaText = (& cmd.exe /d /c 'java -version 2>&1' | Out-String)
if ($javaText -notmatch 'version "21[\.]') {
    throw "JDK 21 is required for the recommended Neo4j setup. Detected:`n$javaText"
}

if (-not (Test-CommandAvailable 'kiro-cli')) {
    Write-Warning 'kiro-cli was not found. The Kiro IDE can still use this repository; install Kiro CLI for the full workflow.'
}

$venv = Join-Path $root '.venv'
if ($RecreateVenv -and (Test-Path $venv)) {
    Write-Host "Removing existing virtual environment $venv" -ForegroundColor Yellow
    Remove-Item -Recurse -Force $venv
}

if (-not (Test-Path $venv)) {
    & $pythonCommand @pythonPrefixArgs -m venv $venv
    Assert-LastExitCode 'Virtual environment creation'
}

$python = Get-VenvPython -Root $root
$venvPython = ((& $python -c "import platform,sys; print(platform.python_version()); raise SystemExit(0 if sys.version_info >= (3,12) else 3)") | Out-String).Trim()
if ($LASTEXITCODE -eq 3) {
    throw "The existing repository virtual environment uses Python $venvPython, which is below the minimum 3.12. Rerun with -RecreateVenv."
}
Assert-LastExitCode 'Repository virtual environment compatibility check'
Write-Host "Repository .venv uses Python $venvPython" -ForegroundColor Green

if ($venvPython -ne $selectedPython -and $RecreateVenv -eq $false) {
    Write-Warning "An existing .venv is being reused (Python $venvPython) while the selected interpreter is Python $selectedPython. Use -RecreateVenv to rebuild it on the selected runtime."
}

& $python -m pip install --upgrade pip setuptools wheel
Assert-LastExitCode 'pip bootstrap'
& $python -m pip install -e "${root}[dev,docs]"
Assert-LastExitCode 'Knowledge-plane dependency installation'

if (-not $SkipOpenWiki) {
    if (-not (Test-CommandAvailable 'openwiki')) {
        & npm install --global openwiki
        Assert-LastExitCode 'OpenWiki installation'
    }
    else {
        Write-Host 'OpenWiki is already available.'
    }
}

$envPath = Join-Path $root '.env'
if (-not (Test-Path $envPath)) {
    Copy-Item (Join-Path $root '.env.example') $envPath
}

if ($null -eq $Neo4jPassword) {
    $Neo4jPassword = Read-Host 'Enter the Neo4j password used during native Neo4j installation' -AsSecureString
}
$plainPassword = ConvertFrom-SecureStringToPlainText -SecureValue $Neo4jPassword
if ($plainPassword.Length -lt 8) {
    throw 'Neo4j requires a password of at least 8 characters by default.'
}

$envText = [System.IO.File]::ReadAllText($envPath)
if ($envText -match '(?m)^NEO4J_PASSWORD=.*$') {
    $envText = [regex]::Replace(
        $envText,
        '(?m)^NEO4J_PASSWORD=.*$',
        [Text.RegularExpressions.MatchEvaluator]{ param($match) 'NEO4J_PASSWORD=' + $plainPassword }
    )
}
else {
    $envText = $envText.TrimEnd() + [Environment]::NewLine + 'NEO4J_PASSWORD=' + $plainPassword + [Environment]::NewLine
}
Write-Utf8NoBom -Path $envPath -Content $envText
$env:NEO4J_PASSWORD = $plainPassword
[Environment]::SetEnvironmentVariable('NEO4J_PASSWORD', $plainPassword, 'User')

& (Join-Path $PSScriptRoot 'configure-kiro.ps1')

Push-Location $root
try {
    & $python -m knowledge_plane.validate
    Assert-LastExitCode 'Canonical knowledge validation'
    if (-not $SkipTests) {
        & $python -m pytest -q
        Assert-LastExitCode 'Unit tests'
    }
}
finally {
    Pop-Location
}

Write-Host ''
Write-Host 'Native application installation completed.' -ForegroundColor Green
Write-Host "Knowledge Plane Python: $venvPython"
Write-Host 'Next:'
Write-Host '  1. Confirm the native Neo4j 5.26 LTS service is running.'
Write-Host '  2. Run scripts\healthcheck.ps1.'
Write-Host '  3. Run scripts\ingest.ps1 -Graphiti off.'
Write-Host '  4. Open this repository in Kiro and refresh MCP servers.'
