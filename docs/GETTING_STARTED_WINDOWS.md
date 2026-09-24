# Getting started on Windows

## Prerequisites

- Windows 10 or 11 with PowerShell
- Docker Desktop, using the WSL2 backend
- Git for Windows (`C:\Program Files\Git\cmd\git.exe` first on `PATH`)
- [uv](https://docs.astral.sh/uv/) for the current user, typically `%USERPROFILE%\.local\bin\uv.exe`

Do not use `py -3.11` for this repo. On this machine that launcher can report that the file is missing. Setup creates `.venv` with Python 3.11 through `uv`.

## First-time setup

From the repository root:

```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\scripts\windows\Setup-ImpactLab.ps1
.\scripts\windows\Start-ImpactLab.ps1
```

`Setup-ImpactLab.ps1` checks Docker, creates `.venv`, installs `requirements.txt`, creates `.runtime\logs`, and validates `docker compose config`. It does not change global Python settings.

## Expected URLs

| Surface | URL |
|---|---|
| Dashboard | http://127.0.0.1:8501 |
| API health | http://127.0.0.1:8000/health |
| API docs | http://127.0.0.1:8000/docs |
| PostgreSQL | `127.0.0.1:5432`, database `impact_lab`, user `impact` |

## Verify

```powershell
.\scripts\windows\Status-ImpactLab.ps1
.\scripts\windows\Doctor-ImpactLab.ps1
```

The dashboard badge should read `SYNTHETIC DEMO` and `PostgreSQL`. Enrollment facts should be 5,760 and the seven-fact total should be 23,745 for seed `20260923`.
