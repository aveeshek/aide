[CmdletBinding()]
param(
    [ValidateSet('true', 'false')]
    [string]$EnableGraphiti = 'false'
)

. (Join-Path $PSScriptRoot 'common.ps1')

$root = Get-RepositoryRoot
$python = Get-VenvPython -Root $root
$settingsDir = Join-Path $root '.kiro\settings'
New-Item -ItemType Directory -Path $settingsDir -Force | Out-Null
$configPath = Join-Path $settingsDir 'mcp.json'

$server = [ordered]@{
    command = $python
    args = @('-m', 'knowledge_plane.server', '--transport', 'stdio')
    env = [ordered]@{
        KNOWLEDGE_ROOT = $root
        NEO4J_URI = 'bolt://localhost:7687'
        NEO4J_USER = 'neo4j'
        NEO4J_PASSWORD = '${NEO4J_PASSWORD}'
        NEO4J_DATABASE = 'neo4j'
        GRAPH_GROUP_ID = 'engineering-knowledge'
        ENABLE_GRAPHITI = $EnableGraphiti
        OPENAI_API_KEY = '${OPENAI_API_KEY}'
        OPENAI_BASE_URL = '${OPENAI_BASE_URL}'
        GRAPHITI_TELEMETRY_ENABLED = 'false'
        MCP_TRANSPORT = 'stdio'
        PYTHONUTF8 = '1'
        PYTHONUNBUFFERED = '1'
    }
    disabled = $false
    autoApprove = @(
        'health',
        'list_knowledge_pages',
        'read_knowledge_page',
        'get_entity',
        'search_knowledge',
        'trace_dependencies',
        'analyze_change_impact',
        'resolve_task_context',
        'list_contradictions'
    )
    disabledTools = @()
}

$config = [ordered]@{
    mcpServers = [ordered]@{
        'engineering-knowledge-plane' = $server
    }
}

$json = $config | ConvertTo-Json -Depth 12
Write-Utf8NoBom -Path $configPath -Content ($json + [Environment]::NewLine)
Write-Host "Created Kiro workspace MCP configuration: $configPath" -ForegroundColor Green
Write-Host 'Restart Kiro or refresh the MCP server list after changing this file.'
