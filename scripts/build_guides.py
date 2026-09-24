"""Render the public user guide and technical runbook PDFs."""
from pathlib import Path

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Image, PageBreak, Paragraph, SimpleDocTemplate, Spacer

ROOT = Path(__file__).resolve().parents[1]
GUIDES = ROOT / "assets" / "guides"
SHOTS = ROOT / "assets" / "screenshots"


def styles():
    base = getSampleStyleSheet()
    body = ParagraphStyle("Body", parent=base["Normal"], fontName="Times-Roman", fontSize=11, leading=15, textColor="#1b2636", spaceAfter=8)
    title = ParagraphStyle("Title2", parent=base["Title"], fontName="Times-Bold", fontSize=22, textColor="#101820", spaceAfter=12)
    h = ParagraphStyle("H", parent=base["Heading2"], fontName="Times-Bold", fontSize=14, textColor="#3d348b", spaceBefore=10, spaceAfter=6)
    return title, h, body


def markdown_flow(path: Path, story, title_style, heading_style, body_style):
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line:
            story.append(Spacer(1, 6))
            continue
        if line.startswith("# "):
            story.append(Paragraph(line[2:], title_style))
        elif line.startswith("## "):
            story.append(Paragraph(line[3:], heading_style))
        elif line.startswith("### "):
            story.append(Paragraph(line[4:], heading_style))
        else:
            safe = line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            story.append(Paragraph(safe, body_style))


def build_user_guide():
    title, heading, body = styles()
    story = []
    markdown_flow(ROOT / "docs" / "USER_GUIDE.md", story, title, heading, body)
    captions = [
        ("01-executive-impact-overview.png", "Executive Impact Overview"),
        ("02-data-quality-command-center.png", "Data Quality Command Center"),
        ("03-donor-funding-lookup.png", "Donor / Funding Lookup"),
        ("04-country-program-operations.png", "Country / Program Operations"),
        ("05-migration-reconciliation.png", "Migration and Reconciliation"),
        ("06-analytics-early-warning.png", "Analytics and Early Warning"),
        ("07-ad-hoc-query-export.png", "Ad-Hoc Query and Export"),
    ]
    for filename, caption in captions:
        story.append(PageBreak())
        story.append(Paragraph(caption, heading))
        story.append(Image(str(SHOTS / filename), width=7.2 * inch, height=4.2 * inch))
        story.append(Paragraph("Screenshot from the running synthetic dashboard.", body))
    out = GUIDES / "Nonprofit_Impact_Intelligence_Lab_User_Guide.pdf"
    SimpleDocTemplate(str(out), pagesize=letter, title="Nonprofit Impact Intelligence Lab User Guide").build(story)
    return out


def build_runbook():
    title, heading, body = styles()
    story = [Paragraph("Technical runbook", title), Paragraph("Synthetic local demonstration. Windows operations, health, and release checks.", body)]
    for name in [
        "GETTING_STARTED_WINDOWS.md",
        "DAILY_RUNBOOK.md",
        "OPERATIONS_RUNBOOK.md",
        "TROUBLESHOOTING_WINDOWS.md",
        "ARCHITECTURE.md",
    ]:
        story.append(PageBreak())
        markdown_flow(ROOT / "docs" / name, story, title, heading, body)
    out = GUIDES / "Nonprofit_Impact_Intelligence_Lab_Technical_Runbook.pdf"
    SimpleDocTemplate(str(out), pagesize=letter, title="Nonprofit Impact Intelligence Lab Technical Runbook").build(story)
    return out


if __name__ == "__main__":
    GUIDES.mkdir(parents=True, exist_ok=True)
    print(build_user_guide())
    print(build_runbook())
