# Operations runbook

## Lifecycle

`Setup-ImpactLab.ps1` prepares the machine-local environment. `Start-ImpactLab.ps1` starts PostgreSQL, seeds when enrollment is below 5,000, and starts the API and dashboard. `Stop-ImpactLab.ps1` stops only those recorded processes. `-StopDatabase` stops the Compose service and keeps the volume.

## Health

| Check | Command or URL |
|---|---|
| Engine | `docker version` |
| PostgreSQL | `pg_isready` inside the Compose container |
| API | http://127.0.0.1:8000/health |
| Dashboard | http://127.0.0.1:8501 |
| Bundle | `.\scripts\windows\Doctor-ImpactLab.ps1` |

## Logs

`.runtime\logs\api.log`, `api.err.log`, `dashboard.log`, and `dashboard.err.log`. `.runtime/` is gitignored.

## Deterministic reset

`Reset-ImpactLabData.ps1` asks you to type `RESEED` unless `-Force` is passed. It refuses to run unless `DATABASE_URL` is the PostgreSQL `impact_lab` database, then reruns the generator and checks that fact volume stays at least 20,000. Every row is synthetic.

## Release verification

Follow [Release Checklist](RELEASE_CHECKLIST.md). CI on `main` must pass the SQLite job and the PostgreSQL job.

## Constraints

No production credentials, no real participant data, and no outbound chat integrations. Trust authentication on PostgreSQL is only for this localhost demo and the ephemeral CI service.
