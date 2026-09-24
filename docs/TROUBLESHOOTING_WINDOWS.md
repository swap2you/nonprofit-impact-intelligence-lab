# Windows troubleshooting

Format: **Symptom → Likely cause → Diagnostic → Safe repair → Validation**

## Broken Python launcher

**Symptom.** `py -3.11` reports that the system cannot find the file specified.

**Likely cause.** The `py` launcher is stale or points at a removed install.

**Diagnostic.** `Get-Command py` and `uv python list`.

**Safe repair.** Use `uv` to create `.venv` with Python 3.11. `Setup-ImpactLab.ps1` does this. Do not repair unrelated global Python installs.

**Validation.** `.\.venv\Scripts\python.exe --version` prints 3.11.

## PowerShell activation blocked

**Symptom.** Running a script returns an execution-policy error.

**Likely cause.** The current user policy is Restricted.

**Diagnostic.** `Get-ExecutionPolicy -List`.

**Safe repair.** `Set-ExecutionPolicy -Scope Process Bypass` in that terminal only.

**Validation.** `.\scripts\windows\Doctor-ImpactLab.ps1` runs.

## Hermes Git shim

**Symptom.** `BUG (fork bomb)` from a path ending in `hermes\git\bin\git.exe`.

**Likely cause.** A Hermes Git shim is ahead of Git for Windows on `PATH`.

**Diagnostic.** `where.exe git`.

**Safe repair.** Put `C:\Program Files\Git\cmd\git.exe` first. Do not delete Hermes as the first step.

**Validation.** `where.exe git` lists Git for Windows first, and `git --version` returns.

## GitHub authentication

**Symptom.** `git push` asks for credentials or fails.

**Likely cause.** Git Credential Manager has no stored GitHub login.

**Diagnostic.** `git credential-manager --version` or `where.exe git-credential-manager`.

**Safe repair.** Sign in through Git Credential Manager. Do not paste tokens into files or docs.

**Validation.** `git ls-remote origin` succeeds.

## Docker and WSL

**Symptom.** `docker version` has a client and no server, or Compose cannot start.

**Likely cause.** Docker Desktop is stopped, or WSL2 is not available.

**Diagnostic.** `wsl --version`, `wsl --status`, `docker version`, `docker info`, `docker compose version`, `docker run --rm hello-world`.

**Safe repair.** Start Docker Desktop and wait until the engine is running. Confirm the Virtual Machine Platform and WSL features only if those commands show they are missing. Do not unregister WSL or factory-reset Docker as the first fix.

**Validation.** `docker compose config` from the repo succeeds and `docker compose up -d` starts PostgreSQL.

## Port already in use

**Symptom.** API, Streamlit, or PostgreSQL exits because 8000, 8501, or 5432 is taken.

**Likely cause.** A previous lab process, or another local service.

**Diagnostic.** `Get-NetTCPConnection -LocalPort 5432,8000,8501 -State Listen` and `.\scripts\windows\Status-ImpactLab.ps1`.

**Safe repair.** `.\scripts\windows\Stop-ImpactLab.ps1`. If the listener is not this project, stop that specific process. Do not stop every Python process.

**Validation.** Status shows the expected listeners only after start.

## PostgreSQL unhealthy

**Symptom.** Start fails while waiting for PostgreSQL, or `pg_isready` fails.

**Likely cause.** The container is new, crashed, or Compose is not the owner of an older container.

**Diagnostic.** `docker compose ps` and `docker compose logs postgres`.

**Safe repair.** `docker compose up -d` from the repo. If a nameless leftover container blocks the name, remove that container only after confirming it uses the `nonprofit-impact-intelligence-lab_pgdata` volume, then compose up again. Do not delete the volume.

**Validation.** `docker exec nonprofit-impact-intelligence-lab-postgres-1 pg_isready -U impact -d impact_lab`.

## Dashboard has no rows

**Symptom.** Pages load and metrics are zero or queries fail.

**Likely cause.** `DATABASE_URL` points at an empty database, or seed did not run.

**Diagnostic.** Status output and `.runtime\logs\dashboard.err.log`.

**Safe repair.** `.\scripts\windows\Start-ImpactLab.ps1 -Reseed`, or `Reset-ImpactLabData.ps1` after typing `RESEED`.

**Validation.** Enrollment count is at least 5,000.

## API unavailable

**Symptom.** http://127.0.0.1:8000/health does not answer.

**Likely cause.** Uvicorn exited, or port 8000 is busy.

**Diagnostic.** `.\scripts\windows\Status-ImpactLab.ps1` and the tail of `.runtime\logs\api.err.log`.

**Safe repair.** Stop the lab, free port 8000 if a foreign process owns it, then start again.

**Validation.** `/health` returns `{"status":"ok","synthetic":true}`.
