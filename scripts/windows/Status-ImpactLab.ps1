$ErrorActionPreference = 'Continue'
. (Join-Path $PSScriptRoot '_LabCommon.ps1')
Write-Host 'Impact Lab status'
Write-Host ("Docker Engine: " + $(if (Test-DockerEngine) { 'up' } else { 'down' }))
docker compose -f (Join-Path $LabRoot 'compose.yaml') ps
$record = Read-LabPids
function Show-Http($Name, $Url, $PidValue, $Kind) {
    $alive = $false
    if ($record) { $alive = Test-LabProcess -ProcessId ([int]$PidValue) -Expected $Kind }
    $code = 'down'
    try { $code = [int](Invoke-WebRequest -Uri $Url -UseBasicParsing -TimeoutSec 3).StatusCode } catch { $code = 'down' }
    Write-Host ("{0}: pid={1} process={2} http={3}" -f $Name, $PidValue, $alive, $code)
    if ($code -eq 'down') {
        $log = Join-Path $LogDir ($(if ($Kind -eq 'uvicorn') { 'api.log' } else { 'dashboard.log' }))
        if (Test-Path $log) { Get-Content $log -Tail 8 | ForEach-Object { Write-Host "  $_" } }
    }
}
$apiPid = if ($record) { $record.api_pid } else { 0 }
$dashPid = if ($record) { $record.dashboard_pid } else { 0 }
Show-Http 'API' 'http://127.0.0.1:8000/health' $apiPid 'uvicorn'
Show-Http 'Dashboard' 'http://127.0.0.1:8501' $dashPid 'streamlit'
Write-Host "Backend URL: $DatabaseUrl"
Write-Host 'API docs: http://127.0.0.1:8000/docs'
Write-Host 'Dashboard: http://127.0.0.1:8501'
Write-Host "Logs: $LogDir"
Write-Host "PIDs: $PidFile"
