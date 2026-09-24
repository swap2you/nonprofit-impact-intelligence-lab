# Daily runbook

```powershell
.\scripts\windows\Start-ImpactLab.ps1
.\scripts\windows\Status-ImpactLab.ps1
.\scripts\windows\Stop-ImpactLab.ps1
```

| Need | Command |
|---|---|
| Start without opening a browser | `.\scripts\windows\Start-ImpactLab.ps1 -NoBrowser` |
| Start and reseed | `.\scripts\windows\Start-ImpactLab.ps1 -Reseed` |
| Logs | `.runtime\logs\api.log`, `.runtime\logs\api.err.log`, `.runtime\logs\dashboard.log`, `.runtime\logs\dashboard.err.log` |
| Stop API and dashboard only | `.\scripts\windows\Stop-ImpactLab.ps1` |
| Also stop PostgreSQL | `.\scripts\windows\Stop-ImpactLab.ps1 -StopDatabase` |
| Reseed after typing `RESEED` | `.\scripts\windows\Reset-ImpactLabData.ps1` |
| Read-only diagnosis | `.\scripts\windows\Doctor-ImpactLab.ps1` |

URLs: http://127.0.0.1:8501 and http://127.0.0.1:8000/docs.

A second start while both processes are alive prints the URLs and exits. It does not launch another pair.
