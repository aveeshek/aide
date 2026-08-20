[CmdletBinding()]
param()

. (Join-Path $PSScriptRoot 'common.ps1')
if (-not (Test-CommandAvailable 'openwiki')) {
    throw 'OpenWiki is not installed. Run: npm install --global openwiki'
}
$root = Get-RepositoryRoot
Push-Location $root
try {
    & openwiki --init
    Assert-LastExitCode 'OpenWiki initialization'
}
finally {
    Pop-Location
}
