[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)][string]$Contract,
    [string]$RunId
)
. (Join-Path $PSScriptRoot 'common.ps1')
$root = Get-RepositoryRoot
$python = Get-VenvPython -Root $root
$contractPath = Resolve-Path (Join-Path $root $Contract)
$argsList = @('-m', 'knowledge_plane.loop_contract', $contractPath.Path)
if ($RunId) {
    $manifest = Join-Path $root "generated\loop-runs\$RunId\run.json"
    $argsList += @('--write-run-manifest', $manifest)
}
& $python @argsList
Assert-LastExitCode 'Loop contract validation'
