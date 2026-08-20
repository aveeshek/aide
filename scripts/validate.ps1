[CmdletBinding()]
param([switch]$SkipTests)

. (Join-Path $PSScriptRoot 'common.ps1')
$root = Get-RepositoryRoot
$python = Get-VenvPython -Root $root

Push-Location $root
try {
    & $python -m knowledge_plane.validate
    Assert-LastExitCode 'Canonical knowledge validation'
    & $python -m ruff check src tests
    Assert-LastExitCode 'Python lint'
    if (-not $SkipTests) {
        & $python -m pytest -q
        Assert-LastExitCode 'Unit tests'
    }
}
finally {
    Pop-Location
}
