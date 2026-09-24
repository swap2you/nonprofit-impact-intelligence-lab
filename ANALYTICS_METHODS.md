# Analytics methods

- Rolling trends: 3-period rolling mean by reporting period.
- Period-over-period: `(current-prior)/prior`, guarded for zero denominators.
- Anomaly detection: IQR fences on monthly site metrics.
- Missingness: submission completeness by period.
- Forecast: if at least four period observations exist, fit ordinary least squares to the last six period means (or fewer when only four or five exist), project one period ahead, and report a non-negative estimate plus a bounded interval using 1.96 residual standard deviations with a 5% minimum margin. This is an illustrative diagnostic forecast, not a causal model, commitment, or guarantee; API `/analytics` and the dashboard expose the estimate and bounds.
- Diagnostics: rule-based associations such as metric drop + stale submissions = possible reporting delay, spike + duplicates = possible data-quality issue, and sustained movement + healthy quality = operational signal requiring review.

These are diagnostic indicators, not causal claims.
