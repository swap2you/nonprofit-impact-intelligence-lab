# Architecture

The system follows Generator -> quality validation -> curated relational store -> API -> dashboard/reporting. SQLite is the zero-config fallback; PostgreSQL is provided via Docker Compose. The API is stateless and reads an explicit database path from `DATABASE_URL`.

```mermaid
flowchart TB
 gen[Deterministic generator] --> raw[Relational tables]
 raw --> q[Quality rules]
 q --> issues[fact_data_quality_issue]
 raw --> api[FastAPI]
 api --> dash[Streamlit]
 api --> exports[CSV XLSX PDF]
```

Operational guardrails: synthetic banner, UTC timestamps, safe preset queries, no arbitrary SQL endpoint, no outbound integrations.
