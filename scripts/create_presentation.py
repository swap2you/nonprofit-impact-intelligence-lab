from pptx import Presentation
from pptx.util import Inches,Pt
from pptx.dml.color import RGBColor
from pathlib import Path
out=Path(__file__).resolve().parents[1]/'assets'/'Nonprofit_Impact_Intelligence_Lab.pptx'; out.parent.mkdir(parents=True,exist_ok=True)
slides=[('Problem','Nonprofit reporting is fragmented, late, and difficult to explain.'),('Synthetic data model','8 fictional countries | 6 programs | 240 sites | 24 periods | 23,745 fact records'),('Architecture','Generator → quality engine → relational store → FastAPI → Streamlit → exports'),('Data quality','Completeness, validity, consistency, uniqueness, timeliness, referential integrity, freshness'),('Executive dashboard','Enrollment, outcomes, freshness, quality score, risks, latest period'),('Funding lookup','Safe filters by synthetic funding source, program, site, and country'),('Analytics / early warning','Rolling trends, IQR flags, missingness, bounded forecast, diagnostic indicators'),('Migration / reconciliation','Matched, mismatched, rejected rows with readiness context'),('Extension model','Planned / Extensible: Teams, Slack, WhatsApp, Telegram, Discord; not implemented'),('Limitations / next steps','Synthetic only; add auth, governance, configurable rules, and PostgreSQL tests for production') ]
r=Presentation(); r.slide_width=Inches(13.333); r.slide_height=Inches(7.5)
for title,body in slides:
 s=r.slides.add_slide(r.slide_layouts[6]); bg=s.background.fill; bg.solid(); bg.fore_color.rgb=RGBColor(12,27,43)
 tb=s.shapes.add_textbox(Inches(1),Inches(1.2),Inches(11),Inches(1)).text_frame; p=tb.paragraphs[0]; p.text=title; p.font.size=Pt(34); p.font.bold=True; p.font.color.rgb=RGBColor(64,196,190)
 b=s.shapes.add_textbox(Inches(1),Inches(2.5),Inches(11),Inches(2)).text_frame; p=b.paragraphs[0]; p.text=body; p.font.size=Pt(24); p.font.color.rgb=RGBColor(240,244,248)
 f=s.shapes.add_textbox(Inches(1),Inches(6.8),Inches(11),Inches(.3)).text_frame.paragraphs[0]; f.text='Independent synthetic demonstration • no confidential data'; f.font.size=Pt(10); f.font.color.rgb=RGBColor(170,185,200)
r.save(out); print(out)
