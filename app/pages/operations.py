import sys
from pathlib import Path

import plotly.express as px
import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from app.queries import query
from app.ui import apply_chart, kpi_row, page_footer, page_intro, section, show_chart

page_intro(
    "Compare synthetic operational performance across countries and programs: enrollment, submission completeness, and timeliness.",
    [
        "Which country and program combinations contribute the most enrollment?",
        "Where is submission completeness or timeliness weaker?",
        "Where should an operator drill in next?",
    ],
)
frame = query(
    """
    select c.country_name, p.program_name,
           sum(e.enrolled) enrolled,
           avg(case when sub.is_complete then 1.0 else 0.0 end) completeness,
           avg(case when sub.is_stale then 1.0 else 0.0 end) stale_rate
    from fact_enrollment e
    join dim_site s on s.site_id=e.site_id
    join dim_country c on c.country_code=s.country_code
    join dim_program p on p.program_id=s.program_id
    join fact_data_submission sub on sub.record_id=e.record_id
    group by c.country_name, p.program_name
    """
)
country = st.selectbox("Country", ["All"] + sorted(frame.country_name.unique()))
program = st.selectbox("Program", ["All"] + sorted(frame.program_name.unique()))
view = frame
if country != "All":
    view = view[view.country_name == country]
if program != "All":
    view = view[view.program_name == program]
kpi_row(
    [
        ("Combinations", f"{len(view):,}", None),
        ("Enrollment", f"{int(view.enrolled.sum()) if len(view) else 0:,}", None),
        ("Mean completeness", f"{float(view.completeness.mean()):.0%}" if len(view) else "n/a", None),
        ("Mean stale rate", f"{float(view.stale_rate.mean()):.0%}" if len(view) else "n/a", None),
    ]
)
section("Enrollment by country and program")
show_chart(apply_chart(px.bar(view, x="country_name", y="enrolled", color="program_name"), "Enrollment contribution"))
section("Contribution table", "Sort by completeness or stale rate to find the first drill-down.")
shown = view.copy()
shown["completeness"] = shown["completeness"].map(lambda v: f"{v:.0%}")
shown["stale_rate"] = shown["stale_rate"].map(lambda v: f"{v:.0%}")
st.dataframe(shown, width="stretch", hide_index=True)
page_footer(
    "Each row is a country-program rollup of site enrollment and submission flags.",
    "Look first at combinations with high enrollment and a weak completeness or elevated stale rate. Those are the operational review queue.",
    "Comparisons are synthetic and evenly generated. They do not prove that one country outperforms another.",
    "Pick the weakest completeness row, then open Donor / Funding Lookup with that country and program.",
)
