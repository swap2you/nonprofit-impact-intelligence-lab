# Architecture

Streamlit and FastAPI read one relational database. The generator is the only writer in this demo.

```mermaid
flowchart LR
  gen[Deterministic generator] --> db[(SQLite or PostgreSQL)]
  db --> api[FastAPI]
  db --> dash[Streamlit dashboard]
  api --> exports[CSV exports]
  dash --> files[CSV XLSX PDF presets]
```

```mermaid
flowchart TB
  subgraph windows [Windows scripts]
    start[Start-ImpactLab.ps1]
  end
  start --> compose[Docker Compose PostgreSQL 16]
  start --> api[Uvicorn 127.0.0.1:8000]
  start --> dash[Streamlit 127.0.0.1:8501]
  compose --> db[(impact_lab)]
  api --> db
  dash --> db
```

| Component | Port | Notes |
|---|---|---|
| PostgreSQL | 5432 | localhost only, trust auth for this demo |
| FastAPI | 8000 | stateless reads |
| Streamlit | 8501 | seven pages, preset exports |

SQLite remains the zero-config path when `DATABASE_URL` is unset. There is no arbitrary SQL endpoint.
