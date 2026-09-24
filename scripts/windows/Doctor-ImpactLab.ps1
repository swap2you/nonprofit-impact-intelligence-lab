$ErrorActionPreference = 'Continue'
. (Join-Path $PSScriptRoot '_LabCommon.ps1')
$rows = @()
function Add-Check($Name, $Level, $Detail, $Next) {
    $script:rows += [pscustomobject]@{ Check = $Name; Level = $Level; Detail = $Detail; Next = $Next }
}
$git = (where.exe git | Select-Object -First 1)
if ($git -eq 'C:\Program Files\Git\cmd\git.exe') { Add-Check 'git' 'PASS' $git 'None' }
elseif ($git -like '*hermes*') { Add-Check 'git' 'FAIL' $git 'Put Git for Windows ahead of the Hermes git shim on PATH.' }
else { Add-Check 'git' 'WARN' "$git" 'Prefer C:\Program Files\Git\cmd\git.exe as the first git.' }
git --version | Out-Null
git credential-manager --version *> $null
if ($LASTEXITCODE -eq 0) { Add-Check 'gcm' 'PASS' 'Git Credential Manager responds' 'None' }
else { Add-Check 'gcm' 'WARN' 'Git Credential Manager did not respond' 'Use Git Credential Manager. Do not store tokens in files.' }
wsl --version *> $null
if ($LASTEXITCODE -eq 0) { Add-Check 'wsl' 'PASS' 'wsl --version succeeded' 'None' } else { Add-Check 'wsl' 'WARN' 'wsl --version failed' 'Confirm WSL2 and the virtual machine platform feature before changing Docker settings.' }
if (Test-DockerEngine) { Add-Check 'docker' 'PASS' 'engine reachable' 'None' } else { Add-Check 'docker' 'FAIL' 'engine unreachable' 'Start Docker Desktop and rerun Doctor. Do not factory-reset WSL first.' }
docker compose version *> $null
if ($LASTEXITCODE -eq 0) { Add-Check 'compose' 'PASS' 'compose available' 'None' } else { Add-Check 'compose' 'FAIL' 'compose missing' 'Install the Docker Compose v2 plugin via Docker Desktop.' }
foreach ($port in 5432, 8000, 8501) {
    $listen = Get-NetTCPConnection -LocalPort $port -State Listen -ErrorAction SilentlyContinue
    if ($listen) { Add-Check "port $port" 'PASS' 'listening' 'None' } else { Add-Check "port $port" 'WARN' 'not listening' "Start the lab if you expect port $port." }
}
if (Test-Path $Python) {
    $ver = & $Python --version 2>&1
    if ($ver -like '*3.11*') { Add-Check 'venv' 'PASS' $ver 'None' } else { Add-Check 'venv' 'WARN' $ver 'Recreate .venv with uv and Python 3.11.' }
    & $Python -c "import fastapi,streamlit,pandas,plotly,sqlalchemy,psycopg2,pytest,reportlab,openpyxl,pptx" 2>$null
    if ($LASTEXITCODE -eq 0) { Add-Check 'packages' 'PASS' 'imports succeeded' 'None' } else { Add-Check 'packages' 'FAIL' 'import failed' 'Run .\scripts\windows\Setup-ImpactLab.ps1' }
} else { Add-Check 'venv' 'FAIL' 'missing' 'Run .\scripts\windows\Setup-ImpactLab.ps1' }
docker exec nonprofit-impact-intelligence-lab-postgres-1 pg_isready -U impact -d impact_lab *> $null
if ($LASTEXITCODE -eq 0) { Add-Check 'postgres' 'PASS' 'accepting connections' 'None' } else { Add-Check 'postgres' 'FAIL' 'not ready' 'Run .\scripts\windows\Start-ImpactLab.ps1 and inspect docker compose logs.' }
try { $health = Invoke-RestMethod http://127.0.0.1:8000/health -TimeoutSec 3; Add-Check 'api' 'PASS' $health.status 'None' } catch { Add-Check 'api' 'WARN' 'health endpoint down' 'See .runtime\logs\api.log' }
try { Invoke-WebRequest http://127.0.0.1:8501 -UseBasicParsing -TimeoutSec 3 | Out-Null; Add-Check 'dashboard' 'PASS' 'http 200' 'None' } catch { Add-Check 'dashboard' 'WARN' 'dashboard down' 'See .runtime\logs\dashboard.log' }
$rows | Format-Table -AutoSize
$fail = @($rows | Where-Object Level -eq 'FAIL').Count
if ($fail -gt 0) { exit 1 }
