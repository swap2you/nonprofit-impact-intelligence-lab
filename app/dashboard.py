import sys
from pathlib import Path

import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.queries import backend_name, data_health, quality_score, table
from app.ui import latest_refresh, sidebar_help, status_header

st.set_page_config(
    page_title="Nonprofit Impact Intelligence Lab",
    page_icon=":material/insights:",
    layout="wide",
    initial_sidebar_state="expanded",
)

pages = st.navigation(
    [
        st.Page(ROOT / "app" / "pages" / "executive.py", title="Executive Impact Overview", icon=":material/dashboard:", default=True),
        st.Page(ROOT / "app" / "pages" / "quality.py", title="Data Quality Command Center", icon=":material/fact_check:"),
        st.Page(ROOT / "app" / "pages" / "funding.py", title="Donor / Funding Lookup", icon=":material/volunteer_activism:"),
        st.Page(ROOT / "app" / "pages" / "operations.py", title="Country / Program Operations", icon=":material/public:"),
        st.Page(ROOT / "app" / "pages" / "migration.py", title="Migration & Reconciliation", icon=":material/sync_alt:"),
        st.Page(ROOT / "app" / "pages" / "analytics.py", title="Analytics & Early Warning", icon=":material/monitoring:"),
        st.Page(ROOT / "app" / "pages" / "exports.py", title="Ad-Hoc Query & Export", icon=":material/download:"),
    ],
    position="sidebar",
)

with st.sidebar:
    sidebar_help()

issues = table("fact_data_quality_issue")
submissions = table("fact_data_submission")
score = quality_score(len(issues), len(submissions))
stale_rate = float(submissions["is_stale"].mean()) if len(submissions) else 0.0
status_header(backend_name(), data_health(score, stale_rate), latest_refresh(table("fact_data_refresh")))
pages.run()
