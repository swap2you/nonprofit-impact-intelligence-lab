# Dashboard guide

Every page shows its purpose, the questions it answers, and a footer for interpretation, limitations, and the next action. Data is synthetic.

## 1. Executive Impact Overview

- Audience: executives and reviewers.
- Purpose: situational awareness for the latest cycle.
- Questions: scale, latest period, enrollment movement, and which quality signals need review.
- Metrics: enrollment records, enrolled participants, mean completion, quality score, stale submissions, latest period.
- Chart: three-period rolling enrollment.
- First look: quality score and high-severity count, then the trend.
- Alert meaning: the diagnostic sentence is a possible contributor, not a cause.
- Next action: open Data Quality.
- Limitation: does not prove effectiveness.
- Screenshot: `assets/screenshots/01-executive-impact-overview.png`

## 2. Data Quality Command Center

- Audience: data stewards and analysts.
- Purpose: prioritize issues.
- Metrics: quality score and High / Medium / Low counts, plus referential-integrity issues.
- Charts: counts by dimension and by severity. Severity labels include words, not color alone.
- Filters: severity pills and dimension multiselect.
- Dimensions: completeness, validity, consistency, uniqueness, timeliness, freshness, referential integrity.
- Alert meaning: High means review first. The orphan funding row (`record_id` 97, `site_id` 999) is a real missing site in this dataset.
- Next action: investigate those rows, then reseed only when a clean baseline is required.
- Screenshot: `assets/screenshots/02-data-quality-command-center.png`

## 3. Donor / Funding Lookup

- Audience: fundraising and program-development reviewers.
- Purpose: a filtered briefing. It is a diagnostic demo, not a donor-ready certification.
- Filters: country and program.
- Metrics: enrollment, completion, stale and incomplete submissions, linked versus incomplete funding, orphan site references.
- Export: CSV of the filtered summary.
- Alert meaning: incomplete or orphan funding requires review.
- Next action: open Data Quality if an orphan reference is present.
- Screenshot: `assets/screenshots/03-donor-funding-lookup.png`

## 4. Country / Program Operations

- Audience: program operations.
- Purpose: compare enrollment, completeness, and stale rate.
- Filters: country and program.
- Chart: enrollment contribution.
- First look: high enrollment with weak completeness.
- Next action: open Funding Lookup for that pair.
- Limitation: countries are fictional and not a performance ranking.
- Screenshot: `assets/screenshots/04-country-program-operations.png`

## 5. Migration & Reconciliation

- Audience: migration leads.
- Purpose: matched, mismatch, and rejected keys.
- Metric: readiness = matched / all rows. The synthetic set is about 10.8% by design.
- Alert meaning: a low score means unresolved keys remain. It does not mean the application failed.
- Next action: review mismatch and rejected rows and their difference reasons.
- Screenshot: `assets/screenshots/05-migration-reconciliation.png`

## 6. Analytics & Early Warning

- Audience: analysts.
- Purpose: trend, rolling mean, IQR markers, and a one-period bounded forecast.
- Forecast: OLS on recent period means, with a residual band and a minimum margin. The point is inside the band.
- Alert meaning: a marker plus a stale-rate note is a possible contributor to investigate, not a cause.
- Next action: compare the same periods in Data Quality and Country Operations.
- Screenshot: `assets/screenshots/06-analytics-early-warning.png`

## 7. Ad-Hoc Query & Export

- Audience: analysts who need a file.
- Purpose: preset extracts only. There is no SQL editor.
- Datasets: enrollment, outcomes, quality, funding, migration, with row counts.
- Formats: CSV, XLSX, and a short PDF preview.
- Next action: export the dataset that matches the page under review.
- Screenshot: `assets/screenshots/07-ad-hoc-query-export.png`
