import io,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import pandas as pd
from fastapi import FastAPI
from fastapi.responses import StreamingResponse,HTMLResponse
from sqlalchemy import text
from database.schema import engine
from analytics.methods import trend,diagnostic
app=FastAPI(title='Nonprofit Impact Intelligence Lab API',version='1.0')
def q(sql,params=None): return pd.read_sql_query(text(sql),engine,params=params)
@app.get('/health')
def health(): return {'status':'ok','synthetic':True}
@app.get('/summary')
def summary():
 e=q('select * from fact_enrollment'); i=q('select * from fact_data_quality_issue'); s=q('select * from fact_data_submission')
 tables=['fact_enrollment','fact_program_outcomes','fact_site_progress','fact_data_submission','fact_funding_allocation','fact_data_quality_issue','fact_migration_reconciliation']
 return {'records':int(sum(len(q('select * from '+t)) for t in tables)),'enrollment':int(e.enrolled.sum()),'countries':int(q('select count(*) n from dim_country').iloc[0,0]),'programs':int(q('select count(*) n from dim_program').iloc[0,0]),'sites':int(q('select count(*) n from dim_site').iloc[0,0]),'quality_score':round(max(0,100-len(i)/max(len(s),1)*100),1),'issues':len(i),'latest_period':q('select max(period_label) x from dim_reporting_period').iloc[0,0]}
@app.get('/quality')
def quality(): return q('select dimension,severity,issue_type,count(*) as issue_count from fact_data_quality_issue group by dimension,severity,issue_type order by issue_count desc').to_dict('records')
@app.get('/lookup')
def lookup(country=None,program_id=None):
 sql="select s.site_code,c.country_name,p.program_name,sum(e.enrolled) enrolled,avg(o.completion_rate) completion_rate,sum(cast(sub.is_stale as integer)) stale_submissions from fact_enrollment e join dim_site s on s.site_id=e.site_id join dim_country c on c.country_code=s.country_code join dim_program p on p.program_id=s.program_id join fact_program_outcomes o on o.record_id=e.record_id join fact_data_submission sub on sub.record_id=e.record_id where 1=1"
 params={}
 if country: sql+=' and c.country_code=:country'; params['country']=country
 if program_id is not None: sql+=' and p.program_id=:program_id'; params['program_id']=program_id
 return q(sql+' group by s.site_code,c.country_name,p.program_name',params).to_dict('records')
@app.get('/analytics')
def analytics():
 t=trend(q('select period_id,enrolled from fact_enrollment')); ch=float(t['pct_change'].iloc[-1]) if len(t) else 0.0; stale=float(q('select avg(cast(is_stale as integer)) x from fact_data_submission').iloc[0,0]); rows=[{'period_id':int(r.period_id),'enrolled':float(r.enrolled),'rolling_3':float(r.rolling_3),'pct_change':float(r.pct_change)} for r in t.itertuples()]; return {'trend':rows,'diagnostic':diagnostic(ch,stale,.03),'stale_rate':stale}
@app.get('/migration')
def migration(): return q('select match_status,count(*) as rows from fact_migration_reconciliation group by match_status').to_dict('records')
@app.get('/export/{kind}.csv')
def export_csv(kind):
 sql={'quality':'select * from fact_data_quality_issue','migration':'select * from fact_migration_reconciliation'}.get(kind,'select * from fact_enrollment'); b=io.BytesIO(); b.write(q(sql).to_csv(index=False).encode()); b.seek(0); return StreamingResponse(b,media_type='text/csv',headers={'Content-Disposition':'attachment; filename='+kind+'.csv'})
@app.get('/')
def root(): return HTMLResponse('<h1>Nonprofit Impact Intelligence Lab API</h1><a href="/docs">OpenAPI docs</a>')
