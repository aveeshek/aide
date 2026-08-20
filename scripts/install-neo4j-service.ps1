[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$Neo4jHome,
    [Security.SecureString]$InitialPassword,
    [switch]$SkipInitialPassword,
    [switch]$SkipServiceInstall
)

. (Join-Path $PSScriptRoot 'common.ps1')

$identity = [Security.Principal.WindowsIdentity]::GetCurrent()
$principal = New-Object Security.Principal.WindowsPrincipal($identity)
if (-not $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
    throw 'Run this script from an elevated PowerShell window (Run as administrator).'
}

$resolvedHome = (Resolve-Path $Neo4jHome).Path
$neo4jCandidates = @(
    (Join-Path $resolvedHome 'bin\neo4j.bat'),
    (Join-Path $resolvedHome 'bin\neo4j.ps1'),
    (Join-Path $resolvedHome 'bin\neo4j')
)
$adminCandidates = @(
    (Join-Path $resolvedHome 'bin\neo4j-admin.bat'),
    (Join-Path $resolvedHome 'bin\neo4j-admin.ps1'),
    (Join-Path $resolvedHome 'bin\neo4j-admin')
)
$neo4j = $neo4jCandidates | Where-Object { Test-Path $_ -PathType Leaf } | Select-Object -First 1
$neo4jAdmin = $adminCandidates | Where-Object { Test-Path $_ -PathType Leaf } | Select-Object -First 1
if (-not $neo4j -or -not $neo4jAdmin) {
    throw "Neo4j commands were not found below $resolvedHome. Confirm that the Windows ZIP was fully extracted."
}

$javaText = (& cmd.exe /d /c 'java -version 2>&1' | Out-String)
if ($javaText -notmatch 'version "21[\.]') {
    throw "JDK 21 is required for the recommended setup. Detected:`n$javaText"
}

$env:NEO4J_HOME = $resolvedHome
[Environment]::SetEnvironmentVariable('NEO4J_HOME', $resolvedHome, 'Machine')

$confPath = Join-Path $resolvedHome 'conf\neo4j.conf'
if (-not (Test-Path $confPath -PathType Leaf)) {
    throw "neo4j.conf was not found at $confPath."
}
$confText = [System.IO.File]::ReadAllText($confPath)
$managedSettings = [ordered]@{
    'server.default_listen_address' = '127.0.0.1'
    'server.bolt.listen_address' = ':7687'
    'server.http.listen_address' = ':7474'
}
foreach ($entry in $managedSettings.GetEnumerator()) {
    $keyPattern = [regex]::Escape($entry.Key)
    $confText = [regex]::Replace(
        $confText,
        "(?m)^\s*#?\s*$keyPattern\s*=.*(?:\r?\n|$)",
        ''
    )
}
$managedBlock = ($managedSettings.GetEnumerator() | ForEach-Object { "$($_.Key)=$($_.Value)" }) -join [Environment]::NewLine
$confText = $confText.TrimEnd() + [Environment]::NewLine + $managedBlock + [Environment]::NewLine
Write-Utf8NoBom -Path $confPath -Content $confText

if (-not $SkipInitialPassword) {
    if ($null -eq $InitialPassword) {
        $InitialPassword = Read-Host 'Set the initial Neo4j password (only valid before first database start)' -AsSecureString
    }
    $plainPassword = ConvertFrom-SecureStringToPlainText -SecureValue $InitialPassword
    if ($plainPassword.Length -lt 8) {
        throw 'Neo4j requires a password of at least 8 characters by default.'
    }
    & $neo4jAdmin dbms set-initial-password $plainPassword
    Assert-LastExitCode 'Neo4j initial-password configuration'
    $env:NEO4J_PASSWORD = $plainPassword
    [Environment]::SetEnvironmentVariable('NEO4J_PASSWORD', $plainPassword, 'User')
}

if (-not $SkipServiceInstall) {
    & $neo4j windows-service install
    Assert-LastExitCode 'Neo4j Windows-service installation'
    & $neo4j start
    Assert-LastExitCode 'Neo4j service start'
}
else {
    Write-Host 'Service installation skipped. Start manually with: '
    Write-Host "  & '$neo4j' console"
}

$recordPath = Join-Path (Get-RepositoryRoot) 'windows\.installed-neo4j-home.txt'
Write-Utf8NoBom -Path $recordPath -Content ($resolvedHome + [Environment]::NewLine)
Write-Host "Neo4j is configured at $resolvedHome" -ForegroundColor Green
Write-Host 'For production, change the Windows service logon from LocalSystem to a dedicated low-privilege account.' -ForegroundColor Yellow
