# Idempotent first-time setup for the Impact Intelligence Lab.
$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot '_LabCommon.ps1')

Write-Host "Impact Lab setup"
Write-Host "Repo: $LabRoot"
if ($PSVersionTable.PSVersion.Major -lt 5) { throw 'PowerShell 5 or newer is required.' }

if (-not (Get-Command docker -ErrorAction SilentlyContinue)) { throw 'Docker CLI was not found. Install Docker Desktop and reopen the terminal.' }
if (-not (Test-DockerEngine)) { throw 'Docker Engine is not reachable. Start Docker Desktop and wait until it reports running.' }
docker compose version | Out-Host

$uv = Join-Path $env:USERPROFILE '.local\bin\uv.exe'
if (-not (Test-Path $uv)) {
    $cmd = Get-Command uv -ErrorAction SilentlyContinue
    if ($cmd) { $uv = $cmd.Source }
}
if (-not $uv) { throw 'uv was not found. Install uv for the current user. Do not rely on py -3.11.' }

& $uv venv (Join-Path $LabRoot '.venv') --python 3.11
& $uv pip install -r (Join-Path $LabRoot 'requirements.txt') --python (Join-Path $LabRoot '.venv\Scripts\python.exe')
New-Item -ItemType Directory -Force -Path $LogDir | Out-Null
Push-Location $LabRoot
try { docker compose config | Out-Null } finally { Pop-Location }
if ($LASTEXITCODE -ne 0) { throw 'docker compose config failed.' }

Write-Host ""
Write-Host "Setup complete. Next command:"
Write-Host "  .\scripts\windows\Start-ImpactLab.ps1"
