[CmdletBinding()]
param()

. (Join-Path $PSScriptRoot 'common.ps1')

$root = Get-RepositoryRoot
$python = Get-VenvPython -Root $root

$bolt = Test-NetConnection -ComputerName '127.0.0.1' -Port 7687 -WarningAction SilentlyContinue
if (-not $bolt.TcpTestSucceeded) {
    throw 'Neo4j Bolt is not reachable on 127.0.0.1:7687. Start the Neo4j Windows service.'
}

Push-Location $root
try {
    & $python scripts\healthcheck.py
    Assert-LastExitCode 'Knowledge-plane health check'
}
finally {
    Pop-Location
}
