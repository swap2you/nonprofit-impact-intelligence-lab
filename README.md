# Nonprofit Impact Intelligence Lab

An independent, synthetic demonstration of nonprofit impact-data quality, reporting, funding lookup, migration reconciliation, and explainable analytics.

> This project is an independent synthetic demonstration of nonprofit impact-data quality, reporting, donor/funding lookup, and analytics patterns. It is not affiliated with or endorsed by buildOn and contains no buildOn confidential data.

## What is implemented

| Area | Status |
|---|---|
| Synthetic interconnected dataset (20,000+) | Implemented |
| FastAPI API and exports | Implemented |
| Streamlit dashboard (7 pages) | Implemented |
| Data-quality dimensions and issue drill-down | Implemented |
| Trend, IQR anomaly, diagnostic indicators | Implemented |
| PDF/CSV/XLSX reports | Implemented |
| PostgreSQL Docker environment | Implemented; SQLite fallback is default |
| Teams/Slack/WhatsApp/Telegram/Discord | Planned / Extensible; not connected |

## Quick start

```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
pip install -r requirements.txt
# PostgreSQL-backed validation (Docker Desktop required)
docker compose up -d
$env:DATABASE_URL='postgresql+psycopg2://impact:impact_demo_only@localhost:5432/impact_lab'
python scripts/generate_data.py
python -m pytest -q
uvicorn api.main:app --reload
# in another terminal
streamlit run app/dashboard.py
```

API: http://localhost:8000/docs  | Dashboard: http://localhost:8501

SQLite remains available for zero-config development by omitting `DATABASE_URL`; final validation exercises PostgreSQL through the Compose stack.

## Architecture

```mermaid
flowchart LR
 A[Synthetic generator] --> B[(Staging SQLite/PostgreSQL)]
 B --> C[Quality engine]
 C --> D[(Curated facts + issues)]
 D --> E[FastAPI] --> F[Streamlit dashboard]
 D --> G[CSV/XLSX/PDF exports]
```

## Dashboard gallery

Screenshots are in `assets/screenshots/` and are generated from the running app.

## Data and methods

Eight fictional countries, six programs, 48 sites, 24 monthly periods, synthetic funding sources, and deliberately injected defects are generated deterministically. See [DATA_MODEL.md](DATA_MODEL.md), [DATA_QUALITY_RULES.md](DATA_QUALITY_RULES.md), and [ANALYTICS_METHODS.md](ANALYTICS_METHODS.md).

Analytics are diagnostic indicators, not causal conclusions. Forecasts are intentionally bounded and should not be treated as commitments.

## Privacy and limitations

No real people, donors, school names, contact details, or confidential records are used. The application is a local portfolio demonstration, not a production control system. See [SECURITY_PRIVACY.md](SECURITY_PRIVACY.md).

## Demo

See [DEMO_SCRIPT_7_MIN.md](DEMO_SCRIPT_7_MIN.md) and [DEMO_SCRIPT_15_MIN.md](DEMO_SCRIPT_15_MIN.md).
