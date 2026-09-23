import random, os, sqlite3, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from datetime import date, datetime, timedelta
from database.schema import engine, metadata, create_schema
from sqlalchemy import insert
SEED=int(os.getenv("SYNTHETIC_SEED","20260923")); rng=random.Random(SEED)
def gen():
 create_schema(); conn=engine.connect(); trans=conn.begin();
 # clear for repeatability
 for t in reversed(metadata.sorted_tables): conn.execute(t.delete())
 countries=[(i,f"SYN-{chr(65+i)}",f"Synthetic Country {chr(65+i)}") for i in range(8)]
 programs=[(i,f"PRG-{i+1:02d}",n) for i,n in enumerate(["Learning Access","Community Health","Youth Leadership","Digital Inclusion","Climate Resilience","School Progress"])]
 conn.execute(metadata.tables['dim_country'].insert(),[dict(country_id=a,country_code=b,country_name=c) for a,b,c in countries])
 conn.execute(metadata.tables['dim_program'].insert(),[dict(program_id=a,program_code=b,program_name=c) for a,b,c in programs])
 sites=[]
 for i in range(240): sites.append(dict(site_id=i+1,site_code=f"SITE-{i+1:03d}",country_code=countries[i%8][1],program_id=programs[i%6][0]))
 conn.execute(metadata.tables['dim_site'].insert(),sites)
 conn.execute(metadata.tables['dim_indicator'].insert(),[dict(indicator_id=i+1,indicator_code=f"IND-{i+1:02d}",indicator_name=n) for i,n in enumerate(['Enrollment','Attendance','Completion','Milestones'])])
 conn.execute(metadata.tables['dim_funding_source'].insert(),[dict(funding_source_id=i+1,funding_code=f"FND-{i+1:03d}",funding_name=f"Synthetic Funding Source {i+1}") for i in range(12)])
 periods=[]
 for i in range(24):
  y=2024+i//12; m=i%12+1; periods.append(dict(period_id=i+1,period_start=date(y,m,1),period_label=f"{y}-{m:02d}"))
 conn.execute(metadata.tables['dim_reporting_period'].insert(),periods)
 now=datetime.utcnow(); enroll=[]; outcomes=[]; progress=[]; subs=[]; issues=[]; rid=1
 for s in sites:
  base=80+rng.randint(0,150)
  for p in periods:
   idx=p['period_id']; spike=3.8 if (s['site_id']==7 and idx==18) else (0.45 if (s['site_id']==12 and idx in (14,15)) else 1)
   val=max(0,int(base*(1+0.015*idx)*spike+rng.gauss(0,8)))
   updated=now-timedelta(days=rng.randint(0,55))
   if s['site_id']==3 and idx in (20,21): updated=now-timedelta(days=120)
   enroll.append(dict(record_id=rid,site_id=s['site_id'],period_id=idx,enrolled=val,updated_at=updated,status='reported' if val else 'missing'))
   outcomes.append(dict(record_id=rid,site_id=s['site_id'],period_id=idx,completion_rate=round(min(1,max(.2,.55+rng.random()*.35)),3),attendance_rate=round(min(1,max(.3,.7+rng.random()*.25)),3),updated_at=updated))
   progress.append(dict(record_id=rid,site_id=s['site_id'],period_id=idx,milestones=rng.randint(0,5),progress_pct=round(min(100,idx/24*100+rng.random()*8),1)))
   complete=not (idx%11==0 or (s['site_id']==9 and idx in (10,11)))
   subs.append(dict(record_id=rid,site_id=s['site_id'],period_id=idx,submitted_at=updated,is_complete=complete,is_stale=(now-updated).days>60))
   if not complete: issues.append(dict(issue_id=len(issues)+1,table_name='fact_data_submission',record_id=rid,dimension='completeness',issue_type='missing_monthly_submission',severity='High',description='Submission is incomplete for reporting period',detected_at=now))
   if (s['site_id']==7 and idx==18): issues.append(dict(issue_id=len(issues)+1,table_name='fact_enrollment',record_id=rid,dimension='validity',issue_type='unexpected_spike',severity='High',description='Enrollment is outside IQR fence',detected_at=now))
   if (s['site_id']==3 and idx in (20,21)): issues.append(dict(issue_id=len(issues)+1,table_name='fact_enrollment',record_id=rid,dimension='freshness',issue_type='stale_record',severity='Medium',description='Record has not refreshed within threshold',detected_at=now))
   rid+=1
 for name,rows in [('fact_enrollment',enroll),('fact_program_outcomes',outcomes),('fact_site_progress',progress),('fact_data_submission',subs)]: conn.execute(metadata.tables[name].insert(),rows)
 funds=[]
 for i in range(1,97): funds.append(dict(record_id=i,funding_source_id=(i%12)+1,program_id=(i%6),site_id=(i%240)+1,amount=round(rng.uniform(10000,95000),2),allocation_status='linked' if i%13 else 'incomplete'))
 conn.execute(metadata.tables['fact_funding_allocation'].insert(),funds)
 for i in range(1,25): conn.execute(metadata.tables['fact_data_refresh'].insert(),dict(refresh_id=i,table_name='fact_enrollment',refreshed_at=now-timedelta(hours=i),row_count=len(enroll)))
 for i in range(1,13): conn.execute(metadata.tables['fact_ad_hoc_request'].insert(),dict(request_id=i,request_type='funding_lookup' if i%2 else 'quality_extract',requested_at=now-timedelta(days=i),status='complete'))
 mig=[]
 for i in range(1,121): mig.append(dict(reconciliation_id=i,entity_type='site',source_key=f"SRC-{i:03d}",target_key=f"SITE-{((i-1)%48)+1:03d}",match_status='matched' if i%9 else ('mismatch' if i%3 else 'rejected'),difference_reason='' if i%9 else 'Code or measure differs'))
 conn.execute(metadata.tables['fact_migration_reconciliation'].insert(),mig)
 conn.execute(metadata.tables['fact_data_quality_issue'].insert(),issues)
 trans.commit(); conn.close()
 return {'enrollment':len(enroll),'outcomes':len(outcomes),'progress':len(progress),'submissions':len(subs),'issues':len(issues),'total':len(enroll)+len(outcomes)+len(progress)+len(subs)+len(funds)+len(issues)+len(mig)}
if __name__=='__main__': print(gen())
