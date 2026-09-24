import sys
from pathlib import Path

import plotly.express as px
import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from analytics.methods import diagnostic, trend
from app.queries import quality_score, query, table
from app.ui import apply_chart, callout, kpi_row, page_footer, page_intro, section, show_chart

page_intro(
    "Executive situational awareness for the latest synthetic reporting cycle: scale, freshness, quality, and where attention is warranted.",
    [
        "How large is the current synthetic portfolio, and what is the latest period?",
        "Is enrollment moving, and does that movement coincide with stale reporting?",
        "Which quality signals should a leader ask an analyst to review first?",
    ],
)
enrollment = table("fact_enrollment")
issues = table("fact_data_quality_issue")
submissions = table("fact_data_submission")
outcomes = table("fact_program_outcomes")
latest = query("select max(period_label) x from dim_reporting_period").iloc[0, 0]
score = quality_score(len(issues), len(submissions))
stale = int(submissions["is_stale"].sum())
high = int((issues["severity"] == "High").sum())
completion = float(outcomes["completion_rate"].mean())
series = trend(enrollment)
change = float(series["pct_change"].iloc[-1]) if len(series) else 0.0
stale_rate = float(submissions["is_stale"].mean()) if len(submissions) else 0.0
kpi_row(
    [
        ("Enrollment records", f"{len(enrollment):,}", None),
        ("Enrolled participants", f"{int(enrollment.enrolled.sum()):,}", f"{change:+.1%} vs prior period"),
        ("Mean completion", f"{completion:.0%}", None),
        ("Quality score", f"{score:.1f}%", f"{high} high-severity issues", "off"),
        ("Stale submissions", f"{stale:,}", None),
        ("Latest period", str(latest), None),
    ]
)
section("Enrollment trend", "Three-period rolling mean of period-average enrollment. A diagnostic view, not a target.")
show_chart(apply_chart(px.line(series, x="period_id", y="rolling_3", markers=True), "3-period rolling enrollment"))
left, right = st.columns(2)
with left:
    section("What changed?")
    callout("info", diagnostic(change, stale_rate, 0.03))
with right:
    section("Attention panel")
    callout("warning" if high else "success", f"{high} high-severity quality issues and {stale:,} stale submissions require review before any briefing.")
    st.caption("Look here first: quality score, high-severity count, then the rolling trend.")
page_footer(
    "This page summarizes synthetic enrollment, outcomes, submission freshness, and the quality ledger for leadership review.",
    "Read the quality score beside the stale-submission count. A movement in enrollment is a diagnostic indicator until an analyst checks freshness and issue rates.",
    "This synthetic demonstration does not prove program effectiveness, donor results, or a causal link between operations and outcomes.",
    "Open Data Quality Command Center and review high-severity issues before using any figure in a briefing.",
)
