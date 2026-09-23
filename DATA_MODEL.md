# Data model

Dimensions: country, program, site, indicator, funding source, reporting period. Facts: enrollment, outcomes, site progress, funding allocation, submissions, quality issues, refreshes, ad-hoc requests, migration reconciliation.

```mermaid
erDiagram
 dim_country ||--o{ dim_site : contains
 dim_program ||--o{ dim_site : serves
 dim_site ||--o{ fact_enrollment : records
 dim_site ||--o{ fact_program_outcomes : reports
 dim_site ||--o{ fact_site_progress : tracks
 dim_funding_source ||--o{ fact_funding_allocation : funds
 dim_reporting_period ||--o{ fact_enrollment : scopes
 dim_reporting_period ||--o{ fact_program_outcomes : scopes
 dim_reporting_period ||--o{ fact_data_submission : scopes
```

All identifiers are synthetic. The generator uses seed 20260923 and produces reproducible rows.
