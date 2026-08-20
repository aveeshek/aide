[CmdletBinding()]
param(
    [switch]$RemoveVirtualEnvironment,
    [switch]$RemoveUserSecrets,
    [switch]$RemoveScheduledTasks
)

. (Join-Path $PSScriptRoot 'common.ps1')
$root = Get-RepositoryRoot

if ($RemoveScheduledTasks) {
    Get-ScheduledTask -TaskName 'BOS-KnowledgePlane-*' -ErrorAction SilentlyContinue |
        Unregister-ScheduledTask -Confirm:$false
}
if ($RemoveVirtualEnvironment) {
    Remove-Item (Join-Path $root '.venv') -Recurse -Force -ErrorAction SilentlyContinue
}
if ($RemoveUserSecrets) {
    [Environment]::SetEnvironmentVariable('NEO4J_PASSWORD', $null, 'User')
    [Environment]::SetEnvironmentVariable('OPENAI_API_KEY', $null, 'User')
    [Environment]::SetEnvironmentVariable('OPENAI_BASE_URL', $null, 'User')
}
Remove-Item (Join-Path $root '.kiro\settings\mcp.json') -Force -ErrorAction SilentlyContinue
Write-Host 'Knowledge-plane application cleanup completed. Neo4j is not removed by this script.'
