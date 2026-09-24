# User guide

This is a local synthetic demonstration of nonprofit impact reporting. It is not a live donor system, and it is not affiliated with or endorsed by buildOn.

## What it is

A dashboard and API over a deterministic dataset: 8 fictional countries, 6 programs, 240 sites, and 24 months. Some defects are planted so quality and migration pages have something real to show.

## What it is not

It does not prove program effectiveness, donor return, or that a migration succeeded. Forecasts are diagnostic ranges, not commitments.

## Navigation

Use the sidebar:

1. Executive Impact Overview
2. Data Quality Command Center
3. Donor / Funding Lookup
4. Country / Program Operations
5. Migration & Reconciliation
6. Analytics & Early Warning
7. Ad-Hoc Query & Export

The header shows a synthetic-data badge, the database backend, data health, and the last refresh time.

## A useful path

1. Read the executive quality score and stale-submission count.
2. Open Data Quality and filter to High.
3. Note the referential-integrity row for funding record 97.
4. Filter Funding Lookup or Country Operations to the same program.
5. Treat Analytics markers as items to investigate.
6. Export a preset CSV, XLSX, or PDF preview from Ad-Hoc Query & Export.

## Interpretation

Wording on the pages is intentional: diagnostic indicator, possible contributor, investigate, requires review, synthetic scenario. A red or amber badge names the condition in text as well.

Screenshots of the seven pages are in `assets/screenshots/` and in the [Dashboard Guide](DASHBOARD_GUIDE.md).
