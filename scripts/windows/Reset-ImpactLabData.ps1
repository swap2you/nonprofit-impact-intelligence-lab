param([switch]$Force)
$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot '_LabCommon.ps1')
if (-not $Force) {
    Write-Host 'This reseeds the local synthetic demo database only.'
    $answer = Read-Host 'Type RESEED to continue'
    if ($answer -ne 'RESEED') { throw 'Reset cancelled.' }
}
if (-not (Wait-Postgres -Attempts 5)) { throw 'Project PostgreSQL is not accepting connections.' }
$env:DATABASE_URL = $DatabaseUrl
$python = Get-LabPython
& $python -c "import os; url=os.environ['DATABASE_URL']; assert 'impact_lab' in url and url.startswith('postgresql'), url"
if ($LASTEXITCODE -ne 0) { throw 'Refusing to reseed because DATABASE_URL is not the project demo database.' }
& $python (Join-Path $LabRoot 'scripts\generate_data.py')
if ($LASTEXITCODE -ne 0) { throw 'Seed failed.' }
& $python -c "import pandas as pd; from sqlalchemy import text; from database.schema import engine; n=int(pd.read_sql_query(text('select count(*) n from fact_enrollment'), engine).iloc[0,0]); total=sum(int(pd.read_sql_query(text('select count(*) n from '+t), engine).iloc[0,0]) for t in ['fact_enrollment','fact_program_outcomes','fact_site_progress','fact_data_submission','fact_funding_allocation','fact_data_quality_issue','fact_migration_reconciliation']); print(n, total); assert n>=5000 and total>=20000"
if ($LASTEXITCODE -ne 0) { throw 'Record-count verification failed.' }
Write-Host 'Reseed complete. All rows are synthetic.'
