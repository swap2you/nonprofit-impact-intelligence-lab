# Onboarding guide

Plan about 30 minutes.

## What the demo solves

Nonprofit impact figures often arrive late, incomplete, and hard to reconcile across sites, programs, and funding records. This lab is a local synthetic system that shows data quality, lookup, migration reconciliation, and bounded analytics in one place.

## Layout

| Path | Role |
|---|---|
| `scripts/generate_data.py` | Deterministic synthetic generator, seed `20260923` |
| `database/schema.py` | SQLAlchemy tables and engine |
| `analytics/methods.py` | Trend, IQR flags, diagnostics, bounded forecast |
| `api/main.py` | FastAPI |
| `app/dashboard.py` | Streamlit shell |
| `app/pages/` | Seven dashboard pages |
| `scripts/windows/` | Setup, start, stop, status, reset, doctor |
| `tests/` | Generator, analytics, API, dashboard smoke |
| `.github/workflows/ci.yml` | SQLite then PostgreSQL pytest |

## Architecture

Generator writes relational tables. Quality issues are rows in `fact_data_quality_issue`. FastAPI and Streamlit both read `DATABASE_URL`. SQLite is the default file `impact_lab.db`. PostgreSQL is the Docker demo.

## Walkthrough

1. Run `Setup-ImpactLab.ps1` and `Start-ImpactLab.ps1`.
2. Open the seven pages. Read the questions and the limitations footer on each.
3. Call `/health`, `/summary`, `/quality`, `/lookup`, `/analytics`, `/migration`, and `/export/quality.csv`.
4. Run `python -m pytest -q` with and without `DATABASE_URL`.
5. Change a page in `app/pages/`, keep queries parameterized, and rerun pytest.

## Common change

Add a metric in the page, not in a new service. If the number needs an API, add a field in `api/main.py` and a test in `tests/test_api.py`.
