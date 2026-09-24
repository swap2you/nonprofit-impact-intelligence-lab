"""Capture the seven dashboard pages from the running local app."""
from pathlib import Path

from playwright.sync_api import sync_playwright

OUT = Path(__file__).resolve().parents[1] / "assets" / "screenshots"
PAGES = [
    ("Executive Impact Overview", "01-executive-impact-overview.png"),
    ("Data Quality Command Center", "02-data-quality-command-center.png"),
    ("Donor / Funding Lookup", "03-donor-funding-lookup.png"),
    ("Country / Program Operations", "04-country-program-operations.png"),
    ("Migration & Reconciliation", "05-migration-reconciliation.png"),
    ("Analytics & Early Warning", "06-analytics-early-warning.png"),
    ("Ad-Hoc Query & Export", "07-ad-hoc-query-export.png"),
]


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        page = browser.new_page(viewport={"width": 1600, "height": 1000})
        page.goto("http://127.0.0.1:8501", wait_until="networkidle", timeout=60000)
        page.get_by_text("SYNTHETIC DEMO").first.wait_for(timeout=60000)
        for title, filename in PAGES:
            page.get_by_role("link", name=title).click()
            page.get_by_text("Questions this page answers").wait_for(timeout=60000)
            page.locator(".js-plotly-plot").first.wait_for(timeout=15000, state="visible") if title not in {"Donor / Funding Lookup", "Ad-Hoc Query & Export"} else None
            page.wait_for_timeout(800)
            page.screenshot(path=str(OUT / filename), full_page=True)
            print(OUT / filename)
        browser.close()


if __name__ == "__main__":
    main()
