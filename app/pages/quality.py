import sys
from pathlib import Path

import plotly.express as px
import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from app.queries import quality_score, table
from app.ui import apply_chart, kpi_row, page_footer, page_intro, section, severity_label, show_chart

DIMENSIONS = {
    "completeness": "A required submission or value is missing.",
    "validity": "A value falls outside an expected fence, such as an enrollment spike.",
    "consistency": "Related keys or measures do not reconcile.",
    "uniqueness": "A source key appears more than once.",
    "timeliness": "A submission arrived after the reporting cutoff.",
    "freshness": "A record has not refreshed within the threshold.",
    "referential_integrity": "A fact points at a dimension key that does not exist.",
}

page_intro(
    "Prioritize synthetic data issues by severity and quality dimension so an analyst can decide what to investigate first.",
    [
        "What is the current quality score, and how many issues sit in each severity?",
        "Which dimensions and issue types account for the backlog?",
        "Which records, including the orphan funding reference, need review?",
    ],
)
issues = table("fact_data_quality_issue").copy()
submissions = table("fact_data_submission")
issues["severity_label"] = issues["severity"].map(severity_label)
score = quality_score(len(issues), len(submissions))
by_sev = issues.groupby("severity").size()
kpi_row(
    [
        ("Quality score", f"{score:.1f}%", "Passed-check style ratio, not a certification", "off"),
        ("High — review first", f"{int(by_sev.get('High', 0)):,}", None),
        ("Medium — review", f"{int(by_sev.get('Medium', 0)):,}", None),
        ("Low — monitor", f"{int(by_sev.get('Low', 0)):,}", None),
        ("Referential-integrity issues", f"{int((issues.dimension == 'referential_integrity').sum()):,}", None),
    ]
)
section("Filters")
severities = st.pills("Severity", ["All", "High", "Medium", "Low"], default="All")
dimensions = st.multiselect("Dimension", sorted(issues.dimension.unique()), placeholder="All dimensions")
view = issues
if severities and severities != "All":
    view = view[view.severity == severities]
if dimensions:
    view = view[view.dimension.isin(dimensions)]
grouped = view.groupby(["dimension", "severity_label", "issue_type"]).size().reset_index(name="count")
left, right = st.columns(2)
with left:
    section("Issues by dimension")
    dim_counts = view.groupby("dimension").size().reset_index(name="count")
    show_chart(apply_chart(px.bar(dim_counts, x="dimension", y="count"), "Issue count by dimension"))
with right:
    section("Issues by severity")
    sev_counts = view.groupby("severity_label").size().reset_index(name="count")
    show_chart(apply_chart(px.bar(sev_counts, x="severity_label", y="count"), "Issue count by severity"))
section("Top issue types", "Counts include the severity label so meaning does not depend on color alone.")
st.dataframe(grouped.sort_values("count", ascending=False), width="stretch", hide_index=True)
section("Quality dimensions")
for name, meaning in DIMENSIONS.items():
    st.markdown(f"**{name.replace('_', ' ').title()}.** {meaning}")
section("Affected records", "Most recent detected issues in the filtered set.")
st.dataframe(view.sort_values("detected_at", ascending=False).head(100), width="stretch", hide_index=True)
page_footer(
    "The command center reads fact_data_quality_issue, including the intentional orphan funding allocation (record 97, site_id 999).",
    "Start with High — review first, then referential integrity and validity. Medium and Low still need an owner, but they are not the first queue.",
    "The score is a transparent ratio of issues to submissions. It does not certify data as fit for a real donor report.",
    "Assign the high-severity and orphan-reference rows for investigation, then recheck this page after a reseed.",
)
