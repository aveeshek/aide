[CmdletBinding()]
param([switch]$Interactive)

. (Join-Path $PSScriptRoot 'common.ps1')
if (-not (Test-CommandAvailable 'openwiki')) {
    throw 'OpenWiki is not installed. Run: npm install --global openwiki'
}
$root = Get-RepositoryRoot
Push-Location $root
try {
    if ($Interactive) {
        & openwiki --update
    }
    else {
        & openwiki code --update --print
    }
    Assert-LastExitCode 'OpenWiki update'
}
finally {
    Pop-Location
}
