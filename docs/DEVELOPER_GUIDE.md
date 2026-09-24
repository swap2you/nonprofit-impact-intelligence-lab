# Developer guide

## Environment

Python 3.11 in `.venv`, created by `uv`. Dependencies are `requirements.txt`. `DATABASE_URL` selects the engine in `database/schema.py` at import time. Unset, it uses `sqlite:///./impact_lab.db`. The demo URL is `postgresql+psycopg2://impact@localhost:5432/impact_lab`.

## Schema and generator

`database/schema.py` defines dimensions and facts. `scripts/generate_data.py` deletes and reloads them with seed `20260923`. For that seed the generator reports 5,760 enrollment, outcome, progress, and submission rows, 488 quality issues, and a combined fact total of 23,745.

## API

`api/main.py`: `/health`, `/summary`, `/quality`, `/lookup`, `/analytics`, `/migration`, `/export/{kind}.csv`.

## Dashboard

`app/dashboard.py` is the shell: navigation, synthetic badge, backend, health, and refresh time. Pages live in `app/pages/`. Shared queries are `app/queries.py`. Shared layout helpers are `app/ui.py`. Theme tokens are `.streamlit/config.toml`.

Prefer `width="stretch"` over `use_container_width`. Cache table reads with the helpers in `app/queries.py`.

## Adding a metric

Compute it from an existing table in the page, label it as a diagnostic indicator, and add an API test if the API should return it.

## Analytics

`analytics/methods.py` holds `trend`, `iqr_flags`, `diagnostic`, and `bounded_forecast`. Keep forecast language illustrative.

## Tests and CI

`python -m pytest -q` covers generator rules, analytics edges, API contracts, and a headless render of all seven pages. GitHub Actions runs that suite on SQLite and then on PostgreSQL 16.

## Exports and artifacts

Page exports use CSV, openpyxl, and reportlab. `reports/generate_reports.py` writes sample files under `assets/sample_outputs/`. `scripts/create_presentation.py` rebuilds the executive deck. `scripts/build_guides.py` rebuilds the guide PDFs.
