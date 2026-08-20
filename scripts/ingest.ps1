[CmdletBinding()]
param(
    [ValidateSet('auto', 'on', 'off')]
    [string]$Graphiti = 'auto'
)

. (Join-Path $PSScriptRoot 'common.ps1')
$root = Get-RepositoryRoot
$python = Get-VenvPython -Root $root

Push-Location $root
try {
    & $python -m knowledge_plane.ingest --graphiti $Graphiti
    Assert-LastExitCode 'Knowledge ingestion'
}
finally {
    Pop-Location
}
