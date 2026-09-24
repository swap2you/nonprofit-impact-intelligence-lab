# Data quality rules

Dimensions: completeness, validity, consistency, uniqueness, timeliness, referential integrity, freshness. Rules deliberately identify missing enrollment values, duplicate record keys, late submissions, stale periods, code inconsistencies, orphan-like links, funding gaps, and migration mismatches. Severity is Critical/High/Medium/Low.

The deterministic generator includes a referential-integrity scenario: funding allocation record 97 points to site_id 999, which is absent from dim_site. The issue ledger records the affected source record, and the Data Quality Command Center surfaces it under `referential_integrity / orphan_site_reference` for drill-down.

The score is a transparent weighted count of passed checks; it is not a certification.

PostgreSQL Compose uses trust authentication only for the isolated local demonstration and ephemeral CI service. It is not appropriate for production; production deployments require authenticated, network-restricted database configuration.
