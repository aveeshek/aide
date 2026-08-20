[CmdletBinding()]
param(
    [string]$DailyAt = '02:00',
    [switch]$Replace
)

. (Join-Path $PSScriptRoot 'common.ps1')
$root = Get-RepositoryRoot
$pwsh = (Get-Process -Id $PID).Path
$taskPrefix = 'BOS-KnowledgePlane'
$time = [DateTime]::ParseExact($DailyAt, 'HH:mm', $null)
$trigger = New-ScheduledTaskTrigger -Daily -At $time
$settings = New-ScheduledTaskSettingsSet -StartWhenAvailable -ExecutionTimeLimit (New-TimeSpan -Hours 2)

$jobs = @(
    @{ Name = "$taskPrefix-OpenWiki"; Script = 'openwiki-update.ps1'; Args = '' },
    @{ Name = "$taskPrefix-Ingest"; Script = 'ingest.ps1'; Args = '-Graphiti auto' },
    @{ Name = "$taskPrefix-Docs"; Script = 'build-docs.ps1'; Args = '' }
)

foreach ($job in $jobs) {
    $scriptPath = Join-Path $root "scripts\$($job.Script)"
    $arguments = "-NoProfile -ExecutionPolicy RemoteSigned -File `"$scriptPath`" $($job.Args)"
    $action = New-ScheduledTaskAction -Execute $pwsh -Argument $arguments -WorkingDirectory $root
    if ($Replace -and (Get-ScheduledTask -TaskName $job.Name -ErrorAction SilentlyContinue)) {
        Unregister-ScheduledTask -TaskName $job.Name -Confirm:$false
    }
    Register-ScheduledTask -TaskName $job.Name -Action $action -Trigger $trigger -Settings $settings -Description 'BOS engineering knowledge-plane maintenance' | Out-Null
    Write-Host "Registered $($job.Name)"
}
