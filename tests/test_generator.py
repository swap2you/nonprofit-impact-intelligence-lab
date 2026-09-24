import os,sys
sys.path.insert(0,os.path.dirname(os.path.dirname(__file__)))
from database.schema import engine
import pandas as pd
def test_fact_volume_and_seed():
 n=pd.read_sql_query('select count(*) n from fact_enrollment',engine).iloc[0,0]; assert n>=5000
 assert pd.read_sql_query('select count(*) n from fact_data_quality_issue',engine).iloc[0,0]>0
def test_quality_dimensions_and_severities():
    rows=pd.read_sql_query('select distinct dimension,severity from fact_data_quality_issue',engine)
    assert {'completeness','validity','consistency','uniqueness','timeliness','freshness'} <= set(rows.dimension)
    assert {'Low','Medium','High'} <= set(rows.severity)

def test_relationship_integrity():
    x=pd.read_sql_query('select count(*) n from fact_enrollment e join dim_site s on s.site_id=e.site_id join dim_reporting_period p on p.period_id=e.period_id',engine)
    assert x.iloc[0,0]>0
