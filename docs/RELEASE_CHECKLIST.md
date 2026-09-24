# Release checklist

- [ ] `docker compose config` succeeds
- [ ] PostgreSQL `pg_isready` succeeds
- [ ] `python scripts/generate_data.py` is deterministic for seed `20260923`
- [ ] Fact total is at least 20,000
- [ ] `python -m pytest -q` passes on SQLite
- [ ] The same suite passes with `DATABASE_URL` pointed at PostgreSQL
- [ ] `/health`, `/summary`, `/quality`, `/lookup`, `/analytics`, `/migration`, and a CSV export respond
- [ ] All seven dashboard pages render, including questions and limitations
- [ ] `Start-ImpactLab.ps1 -NoBrowser`, duplicate start, `Status`, `Stop`, `Reset` confirmation, and `Doctor` have been exercised
- [ ] Seven screenshots in `assets/screenshots/` match the running UI
- [ ] Executive PPTX, presentation PDF, user-guide PDF, and technical-runbook PDF open
- [ ] README links and images resolve
- [ ] `00_INBOX`, `.env`, `.venv`, `.runtime`, local databases, and `delivery/` are untracked
- [ ] GitHub default branch is `main` and Actions is green
