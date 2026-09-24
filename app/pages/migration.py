import sys
from pathlib import Path

import plotly.express as px
import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from app.queries import table
from app.ui import apply_chart, callout, kpi_row, page_footer, page_intro, section, show_chart

page_intro(
    "Assess whether synthetic source keys are matched, mismatched, or rejected before a migration would be treated as ready.",
    [
        "What share of reconciliation rows are matched?",
        "How many mismatches and rejections remain unresolved?",
        "Why can readiness be low even when the demo is working?",
    ],
)
rows = table("fact_migration_reconciliation")
counts = rows.groupby("match_status").size()
total = int(counts.sum())
matched = int(counts.get("matched", 0))
mismatch = int(counts.get("mismatch", 0))
rejected = int(counts.get("rejected", 0))
readiness = matched / max(total, 1) * 100
kpi_row(
    [
        ("Migration readiness", f"{readiness:.1f}%", "Matched rows / all rows"),
        ("Matched", f"{matched:,}", None),
        ("Mismatch", f"{mismatch:,}", "Requires review"),
        ("Rejected", f"{rejected:,}", "Requires review"),
    ]
)
callout(
    "warning",
    "Readiness is intentionally low. The generator plants mismatches and rejections so this page can show an unresolved migration, not a successful cutover.",
)
section("Match distribution")
summary = counts.reset_index(name="rows")
show_chart(apply_chart(px.bar(summary, x="match_status", y="rows", color="match_status"), "Reconciliation status"))
section("Unresolved items")
open_rows = rows[rows.match_status != "matched"]
st.dataframe(open_rows, width="stretch", hide_index=True)
page_footer(
    "Readiness uses the same matched / total ratio as the migration API. Status labels are matched, mismatch, and rejected.",
    "A low score means unresolved keys remain. It is a diagnostic indicator of migration readiness in this synthetic scenario.",
    "This does not prove that a real system migration succeeded or failed. Poor synthetic data is planted on purpose.",
    "Review mismatch and rejected rows, record the difference reason, and only then discuss whether a reload is warranted.",
)
