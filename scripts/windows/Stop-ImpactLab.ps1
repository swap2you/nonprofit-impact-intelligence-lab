param([switch]$StopDatabase)
$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot '_LabCommon.ps1')
$record = Read-LabPids
if (-not $record) { Write-Host 'No runtime PID file. Nothing to stop.' }
else {
    foreach ($pair in @(@{ Id = [int]$record.api_pid; Kind = 'uvicorn' }, @{ Id = [int]$record.dashboard_pid; Kind = 'streamlit' })) {
        if (Test-LabProcess -ProcessId $pair.Id -Expected $pair.Kind) {
            Stop-Process -Id $pair.Id -Force
            Write-Host "Stopped $($pair.Kind) PID $($pair.Id)"
        } else {
            Write-Host "Skipped PID $($pair.Id); it is not this project's $($pair.Kind) process."
        }
    }
    Remove-Item $PidFile -ErrorAction SilentlyContinue
}
if ($StopDatabase) {
    Push-Location $LabRoot
    try { docker compose stop } finally { Pop-Location }
    Write-Host 'PostgreSQL container stopped. The volume was kept.'
}
