# Data dictionary

All keys and names are synthetic. Seed `20260923` reloads every table. Grain below is the generator's grain.

| Table | Purpose | Grain | Primary key | Important fields | Relationships | Caveat |
|---|---|---|---|---|---|---|
| dim_country | Fictional countries | country | country_code | country_name | sites | Codes look like `SYN-A` |
| dim_program | Fictional programs | program | program_id | program_code, program_name | sites, funding | Six programs |
| dim_site | Delivery points | site | site_id | site_code, country_code, program_id | country, program, facts | 240 sites |
| dim_indicator | Indicator labels | indicator | indicator_id | indicator_code, indicator_name | none enforced | Reference list only |
| dim_funding_source | Fictional funders | source | funding_source_id | funding_code, funding_name | allocations | Not real donors |
| dim_reporting_period | Months | period | period_id | period_start, period_label | facts | 24 months from 2024-01 |
| fact_enrollment | Headcount | site-period | record_id | site_id, period_id, enrolled, status | site, period | 5,760 rows |
| fact_program_outcomes | Rates | site-period | record_id | completion_rate, attendance_rate | shares record_id with enrollment | Synthetic rates |
| fact_site_progress | Milestones | site-period | record_id | milestones, progress_pct | site, period | Not a verified outcome |
| fact_funding_allocation | Funding links | allocation | record_id | funding_source_id, program_id, site_id, amount, allocation_status | program; site except record 97 | site_id 999 is an orphan |
| fact_data_submission | Submission flags | site-period | record_id | is_complete, is_stale, submitted_at | site, period | Stale means older than 60 days at generation |
| fact_data_quality_issue | Issue ledger | issue | issue_id | table_name, record_id, dimension, issue_type, severity | record_id in the named table | Includes planted defects |
| fact_data_refresh | Refresh log | refresh event | refresh_id | table_name, refreshed_at, row_count | none | Drives the header timestamp |
| fact_ad_hoc_request | Sample request log | request | request_id | request_type, status | none | Not a workflow engine |
| fact_migration_reconciliation | Key compare | source key | reconciliation_id | source_key, target_key, match_status, difference_reason | target_key resembles a site code | Mostly unresolved on purpose |

The API summary count adds enrollment, outcomes, progress, submissions, funding, quality issues, and migration rows. For this seed that total is 23,745.
