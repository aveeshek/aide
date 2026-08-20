[CmdletBinding()]
param()
. (Join-Path $PSScriptRoot 'common.ps1')
$root = Get-RepositoryRoot
$zensical = Join-Path $root '.venv\Scripts\zensical.exe'
if (-not (Test-Path $zensical -PathType Leaf)) { throw "Zensical not found at $zensical. Run install-native-windows.ps1." }
Push-Location $root
try {
    & (Join-Path $root '.venv\Scripts\python.exe') scripts\build_docs_tree.py
    Assert-LastExitCode 'Zensical source-tree preparation'
    & $zensical build
    Assert-LastExitCode 'Static documentation build'
    Write-Host "Static documentation built at $(Join-Path $root 'site')" -ForegroundColor Green
}
finally { Pop-Location }
