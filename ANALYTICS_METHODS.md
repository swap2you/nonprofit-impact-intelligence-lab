# Analytics methods

- Rolling trends: 3-period rolling mean by reporting period.
- Period-over-period: `(current-prior)/prior`, guarded for zero denominators.
- Anomaly detection: IQR fences on monthly site metrics.
- Missingness: submission completeness by period.
- Forecast: linear trend on the last six observations with a wide uncertainty band; only shown when at least four points exist.
- Diagnostics: rule-based associations such as metric drop + stale submissions = likely reporting delay, spike + duplicates = likely data-quality issue, and sustained movement + healthy quality = operational signal requiring review.

These are diagnostic indicators, not causal claims.
