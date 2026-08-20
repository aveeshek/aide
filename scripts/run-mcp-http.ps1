[CmdletBinding()]
param()

. (Join-Path $PSScriptRoot 'common.ps1')
$root = Get-RepositoryRoot
$python = Get-VenvPython -Root $root
Push-Location $root
try {
    Write-Host 'Starting optional HTTP diagnostics endpoint at http://127.0.0.1:8000/mcp'
    & $python -m knowledge_plane.server --transport streamable-http
}
finally {
    Pop-Location
}
