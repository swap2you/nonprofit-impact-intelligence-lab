import io
import sys
from pathlib import Path

import pandas as pd
import streamlit as st
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from app.queries import table
from app.ui import page_footer, page_intro, section

PRESETS = [
    ("enrollment", "fact_enrollment", "Site-period enrollment facts."),
    ("outcomes", "fact_program_outcomes", "Completion and attendance rates aligned to enrollment records."),
    ("quality", "fact_data_quality_issue", "Issue ledger with dimension, severity, and affected record."),
    ("funding", "fact_funding_allocation", "Synthetic funding linkage, including known incomplete rows."),
    ("migration", "fact_migration_reconciliation", "Matched, mismatched, and rejected migration keys."),
]


def to_pdf(frame: pd.DataFrame, title: str) -> bytes:
    buffer = io.BytesIO()
    preview = frame.head(18).astype(str)
    data = [list(preview.columns)] + preview.values.tolist()
    story = [
        Paragraph(title),
        Spacer(1, 8),
        Paragraph("Synthetic demonstration extract. Diagnostic use only."),
        Spacer(1, 8),
        Table(
            data,
            repeatRows=1,
            style=TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1b2636")),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                    ("GRID", (0, 0), (-1, -1), 0.25, colors.grey),
                    ("FONTSIZE", (0, 0), (-1, -1), 7),
                ]
            ),
        ),
    ]
    SimpleDocTemplate(buffer, pagesize=letter).build(story)
    return buffer.getvalue()


def to_xlsx(frame: pd.DataFrame) -> bytes:
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        frame.to_excel(writer, index=False)
    return buffer.getvalue()


page_intro(
    "Download preset synthetic datasets. There is no arbitrary SQL editor; every extract is a named, documented table.",
    [
        "Which datasets can an analyst export?",
        "How many rows does each preset contain?",
        "Which file format should be used for a review note?",
    ],
)
st.caption("Formats: CSV for analysis, XLSX for a workbook, PDF for a short preview extract. See docs/USER_GUIDE.md.")
for key, source, description in PRESETS:
    frame = table(source)
    with st.container(border=True):
        section(key.replace("_", " ").title(), description)
        st.markdown(f"**{len(frame):,} rows** from `{source}`.")
        csv_col, xlsx_col, pdf_col = st.columns(3)
        with csv_col:
            st.download_button("CSV", frame.to_csv(index=False), f"{key}.csv", key=f"{key}-csv", icon=":material/download:")
        with xlsx_col:
            st.download_button("XLSX", to_xlsx(frame), f"{key}.xlsx", key=f"{key}-xlsx", icon=":material/download:")
        with pdf_col:
            st.download_button("PDF preview", to_pdf(frame, key), f"{key}.pdf", key=f"{key}-pdf", icon=":material/download:")
page_footer(
    "Exports are the same relational tables the API and dashboard read. PDF files include a short preview, not every row.",
    "Use CSV or XLSX when you need the full preset. Use the PDF preview only as a readable attachment.",
    "Exports do not add new metrics, and they cannot be used to query tables outside this list.",
    "Choose the preset that matches the page you just reviewed, then attach the file to the investigation note.",
)
