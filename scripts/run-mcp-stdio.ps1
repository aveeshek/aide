[CmdletBinding()]
param()

. (Join-Path $PSScriptRoot 'common.ps1')
$root = Get-RepositoryRoot
$python = Get-VenvPython -Root $root
Push-Location $root
try {
    & $python -m knowledge_plane.server --transport stdio
}
finally {
    Pop-Location
}
