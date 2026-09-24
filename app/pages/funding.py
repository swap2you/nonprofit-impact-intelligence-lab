import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from app.queries import query, table
from app.ui import callout, kpi_row, page_footer, page_intro, section

page_intro(
    "A filtered briefing of synthetic country, program, enrollment, completion, freshness, and funding linkage. This is a diagnostic demo view, not a donor-ready certification.",
    [
        "What enrollment and completion does a selected country or program show?",
        "How fresh is the underlying submission, and where are known gaps?",
        "Which funding rows are linked, incomplete, or orphaned?",
    ],
)
countries = table("dim_country")
programs = table("dim_program")
country = st.selectbox("Country", ["All"] + countries.country_code.tolist(), format_func=lambda code: "All countries" if code == "All" else f"{code} — {countries.set_index('country_code').loc[code, 'country_name']}")
program = st.selectbox("Program", ["All"] + programs.program_id.astype(str).tolist(), format_func=lambda pid: "All programs" if pid == "All" else programs.set_index("program_id").loc[int(pid), "program_name"])
sql = """
select c.country_name, p.program_name,
       sum(e.enrolled) enrolled,
       avg(o.completion_rate) completion_rate,
       sum(case when sub.is_stale then 1 else 0 end) stale,
       sum(case when sub.is_complete then 0 else 1 end) incomplete
from fact_enrollment e
join dim_site s on s.site_id=e.site_id
join dim_country c on c.country_code=s.country_code
join dim_program p on p.program_id=s.program_id
join fact_program_outcomes o on o.record_id=e.record_id
join fact_data_submission sub on sub.record_id=e.record_id
where 1=1
"""
params = {}
if country != "All":
    sql += " and c.country_code=:country"
    params["country"] = country
if program != "All":
    sql += " and p.program_id=:program_id"
    params["program_id"] = int(program)
import json
out = query(sql + " group by c.country_name, p.program_name", json.dumps(params))
funds = table("fact_funding_allocation")
if program != "All":
    funds = funds[funds.program_id == int(program)]
linked = int((funds.allocation_status == "linked").sum())
incomplete = int((funds.allocation_status != "linked").sum())
orphan = int((funds.site_id == 999).sum())
kpi_row(
    [
        ("Enrollment", f"{int(out.enrolled.sum()) if len(out) else 0:,}", None),
        ("Mean completion", f"{float(out.completion_rate.mean()):.0%}" if len(out) else "n/a", None),
        ("Stale submissions", f"{int(out.stale.sum()) if len(out) else 0:,}", None),
        ("Incomplete submissions", f"{int(out.incomplete.sum()) if len(out) else 0:,}", None),
        ("Linked funding rows", f"{linked:,}", f"{incomplete} incomplete", "off"),
        ("Orphan site references", f"{orphan:,}", "Requires review" if orphan else "None in filter", "off"),
    ]
)
callout("info", "Synthetic scenario label: figures are generated, not a live donor portfolio. Treat gaps as diagnostic indicators.")
section("Country and program summary")
st.dataframe(out, width="stretch", hide_index=True)
section("Funding linkage", "Incomplete status and site_id 999 are known synthetic defects.")
st.dataframe(funds, width="stretch", hide_index=True)
st.download_button("Download lookup CSV", out.to_csv(index=False), "funding_lookup.csv", icon=":material/download:")
page_footer(
    "Filters follow the same country and program parameters as the lookup API. Funding rows are included so linkage gaps stay visible.",
    "Use enrollment and completion together with stale and incomplete counts. A strong completion rate with stale submissions still requires review.",
    "This page does not prove donor attribution, grant compliance, or that a briefing is ready for an external audience.",
    "If orphan references or incomplete allocations are present, open Data Quality and export the filtered CSV for the review note.",
)
