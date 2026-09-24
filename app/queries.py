"""Cached reads against the synthetic impact database."""
import json
import os

import pandas as pd
import streamlit as st
from sqlalchemy import text

from database.schema import engine


def backend_name() -> str:
    url = os.getenv("DATABASE_URL", "sqlite:///./impact_lab.db")
    return "PostgreSQL" if url.startswith("postgres") else "SQLite"


@st.cache_data(ttl=120, show_spinner=False)
def query(sql: str, params_json: str = "") -> pd.DataFrame:
    params = json.loads(params_json) if params_json else None
    return pd.read_sql_query(text(sql), engine, params=params)


def table(name: str) -> pd.DataFrame:
    allowed = {
        "fact_enrollment",
        "fact_program_outcomes",
        "fact_site_progress",
        "fact_funding_allocation",
        "fact_data_submission",
        "fact_data_quality_issue",
        "fact_data_refresh",
        "fact_migration_reconciliation",
        "dim_country",
        "dim_program",
        "dim_site",
        "dim_reporting_period",
        "dim_funding_source",
    }
    if name not in allowed:
        raise ValueError(f"Unsupported table: {name}")
    return query(f"select * from {name}")


def quality_score(issues: int, submissions: int) -> float:
    return round(max(0, 100 - issues / max(submissions, 1) * 100), 1)


def data_health(score: float, stale_rate: float) -> str:
    if score < 70 or stale_rate > 0.25:
        return "Needs review"
    if score < 90 or stale_rate > 0.1:
        return "Watch"
    return "Healthy"
