param(
    [switch]$NoBrowser,
    [switch]$Reseed
)
$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot '_LabCommon.ps1')

$existing = Read-LabPids
if ($existing -and (Test-LabProcess -ProcessId ([int]$existing.api_pid) -Expected 'uvicorn') -and (Test-LabProcess -ProcessId ([int]$existing.dashboard_pid) -Expected 'streamlit')) {
    Write-Host "Impact Lab is already running."
    Write-Host "API:       http://127.0.0.1:8000/docs"
    Write-Host "Dashboard: http://127.0.0.1:8501"
    exit 0
}

$python = Get-LabPython
if (-not (Test-DockerEngine)) { throw 'Docker Engine is not reachable. Start Docker Desktop, then rerun Start-ImpactLab.ps1.' }
Push-Location $LabRoot
try { docker compose up -d } finally { Pop-Location }
if (-not (Wait-Postgres)) { throw 'PostgreSQL did not become ready. Run .\scripts\windows\Doctor-ImpactLab.ps1' }

$env:DATABASE_URL = $DatabaseUrl
$seeded = 0
try {
    $seededText = & $python -c "import pandas as pd; from sqlalchemy import text; from database.schema import engine; print(int(pd.read_sql_query(text('select count(*) n from fact_enrollment'), engine).iloc[0,0]))"
    if ($LASTEXITCODE -eq 0) { $seeded = [int]$seededText }
} catch { $seeded = 0 }
if ($Reseed -or $seeded -lt 5000) {
    Write-Host "Seeding synthetic data..."
    & $python (Join-Path $LabRoot 'scripts\generate_data.py')
    if ($LASTEXITCODE -ne 0) { throw 'Deterministic seed failed.' }
}

New-Item -ItemType Directory -Force -Path $LogDir | Out-Null
$apiLog = Join-Path $LogDir 'api.log'
$dashLog = Join-Path $LogDir 'dashboard.log'
$api = Start-Process -FilePath $python -ArgumentList '-m','uvicorn','api.main:app','--host','127.0.0.1','--port','8000' -WorkingDirectory $LabRoot -RedirectStandardOutput $apiLog -RedirectStandardError (Join-Path $LogDir 'api.err.log') -PassThru -WindowStyle Hidden
$dash = Start-Process -FilePath $python -ArgumentList '-m','streamlit','run','app/dashboard.py','--server.address','127.0.0.1','--server.port','8501' -WorkingDirectory $LabRoot -RedirectStandardOutput $dashLog -RedirectStandardError (Join-Path $LogDir 'dashboard.err.log') -PassThru -WindowStyle Hidden
Save-LabPids @{ api_pid = $api.Id; dashboard_pid = $dash.Id; started_at = (Get-Date).ToString('o') }

function Wait-Url($Url) {
    for ($i = 0; $i -lt 30; $i++) {
        try {
            $response = Invoke-WebRequest -Uri $Url -UseBasicParsing -TimeoutSec 3
            if ($response.StatusCode -ge 200) { return $true }
        } catch { Start-Sleep -Seconds 1 }
    }
    return $false
}
if (-not (Wait-Url 'http://127.0.0.1:8000/health')) { throw "API did not become healthy. See $apiLog" }
if (-not (Wait-Url 'http://127.0.0.1:8501')) { throw "Dashboard did not become healthy. See $dashLog" }
Write-Host "API:       http://127.0.0.1:8000/docs"
Write-Host "Dashboard: http://127.0.0.1:8501"
if (-not $NoBrowser) { Start-Process 'http://127.0.0.1:8501' }
