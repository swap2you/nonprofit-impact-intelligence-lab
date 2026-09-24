"""Headless smoke coverage for the seven dashboard pages."""
from pathlib import Path

from streamlit.testing.v1 import AppTest

ROOT = Path(__file__).resolve().parents[1]

PAGES = [
    "pages/executive.py",
    "pages/quality.py",
    "pages/funding.py",
    "pages/operations.py",
    "pages/migration.py",
    "pages/analytics.py",
    "pages/exports.py",
]


def test_dashboard_pages_render():
    app = AppTest.from_file(ROOT / "app" / "dashboard.py", default_timeout=90)
    app.run()
    assert not app.exception
    for page in PAGES:
        app.switch_page(page)
        app.run()
        assert not app.exception
        text = " ".join(getattr(item, "value", "") or "" for item in app.markdown)
        assert "Questions this page answers" in text
        assert "Limitations" in text
