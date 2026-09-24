$ErrorActionPreference = 'Stop'
$script:LabRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
$script:Runtime = Join-Path $LabRoot '.runtime'
$script:LogDir = Join-Path $Runtime 'logs'
$script:PidFile = Join-Path $Runtime 'pids.json'
$script:Python = Join-Path $LabRoot '.venv\Scripts\python.exe'
$script:DatabaseUrl = 'postgresql+psycopg2://impact@localhost:5432/impact_lab'

function Get-LabPython {
    if (Test-Path $script:Python) { return $script:Python }
    $uv = Join-Path $env:USERPROFILE '.local\bin\uv.exe'
    if (-not (Test-Path $uv)) { $uv = (Get-Command uv -ErrorAction SilentlyContinue).Source }
    if (-not $uv) { throw 'uv was not found. Install uv or run Setup-ImpactLab.ps1 after uv is on PATH.' }
    & $uv venv (Join-Path $LabRoot '.venv') --python 3.11
    if (-not (Test-Path $script:Python)) { throw 'Python 3.11 virtual environment was not created.' }
    return $script:Python
}

function Test-DockerEngine {
    docker version --format '{{.Server.Version}}' *> $null
    return $LASTEXITCODE -eq 0
}

function Wait-Postgres {
    param([int]$Attempts = 30)
    for ($i = 0; $i -lt $Attempts; $i++) {
        docker exec nonprofit-impact-intelligence-lab-postgres-1 pg_isready -U impact -d impact_lab *> $null
        if ($LASTEXITCODE -eq 0) { return $true }
        Start-Sleep -Seconds 2
    }
    return $false
}

function Get-ProcessCommandLine {
    param([int]$ProcessId)
    $proc = Get-CimInstance Win32_Process -Filter "ProcessId=$ProcessId" -ErrorAction SilentlyContinue
    if ($proc) { return $proc.CommandLine }
    return $null
}

function Test-LabProcess {
    param([int]$ProcessId, [string]$Expected)
    if ($ProcessId -le 0) { return $false }
    $command = Get-ProcessCommandLine -ProcessId $ProcessId
    if (-not $command) { return $false }
    return ($command -like "*$Expected*") -and ($command -like "*$LabRoot*" -or $command -like '*api.main:app*' -or $command -like '*app/dashboard.py*' -or $command -like '*app\dashboard.py*')
}

function Read-LabPids {
    if (-not (Test-Path $script:PidFile)) { return $null }
    return Get-Content $script:PidFile -Raw | ConvertFrom-Json
}

function Save-LabPids {
    param($Record)
    New-Item -ItemType Directory -Force -Path $script:Runtime | Out-Null
    $Record | ConvertTo-Json | Set-Content -Path $script:PidFile -Encoding utf8
}
