import os,sys
sys.path.insert(0,os.path.dirname(os.path.dirname(__file__)))
from database.schema import engine
import pandas as pd
def test_fact_volume_and_seed():
 n=pd.read_sql_query('select count(*) n from fact_enrollment',engine).iloc[0,0]; assert n>=5000
 assert pd.read_sql_query('select count(*) n from fact_data_quality_issue',engine).iloc[0,0]>0
def test_quality_dimensions_and_severities():
    rows=pd.read_sql_query('select distinct dimension,severity from fact_data_quality_issue',engine)
    assert {'completeness','validity','consistency','uniqueness','timeliness','freshness','referential_integrity'} <= set(rows.dimension)
    assert {'Low','Medium','High'} <= set(rows.severity)

def test_referential_integrity_issue_is_a_real_orphan():
    row=pd.read_sql_query("select * from fact_funding_allocation where record_id=97",engine).iloc[0]
    assert pd.read_sql_query(f"select count(*) n from dim_site where site_id={int(row.site_id)}",engine).iloc[0,0] == 0
    issue=pd.read_sql_query("select * from fact_data_quality_issue where dimension='referential_integrity' and record_id=97",engine)
    assert len(issue)==1 and issue.iloc[0].issue_type=='orphan_site_reference'
