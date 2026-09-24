import streamlit as st, pandas as pd, plotly.express as px, sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from database.schema import engine
from analytics.methods import trend
st.set_page_config(page_title='Impact Intelligence Lab',page_icon='◎',layout='wide')
st.sidebar.markdown('## Impact Intelligence Lab')
st.sidebar.warning('SYNTHETIC DATA ONLY\nIndependent demonstration; not affiliated with or endorsed by buildOn.')
page=st.sidebar.radio('Dashboard area',['Executive Impact Overview','Data Quality Command Center','Donor / Funding Lookup','Country / Program Operations','Migration & Reconciliation','Analytics & Early Warning','Ad-Hoc Query & Export'])
def q(sql): return pd.read_sql_query(sql,engine)
st.caption('Last refreshed: '+pd.Timestamp.utcnow().strftime('%Y-%m-%d %H:%M UTC'))
if page=='Executive Impact Overview':
 st.title('Executive Impact Overview'); e=q('select * from fact_enrollment'); i=q('select * from fact_data_quality_issue'); a,b,c,d=st.columns(4); a.metric('Enrollment records',f'{len(e):,}'); b.metric('Enrolled participants',f'{e.enrolled.sum():,}'); c.metric('Quality issues',f'{len(i):,}'); d.metric('Latest period',q('select max(period_label) x from dim_reporting_period').iloc[0,0]); t=trend(e); st.plotly_chart(px.line(t,x='period_id',y='rolling_3',markers=True,title='3-period rolling enrollment trend'),use_container_width=True); st.info('Diagnostic indicator only: review movement alongside freshness and issue rates; no causal claim is made.')
elif page=='Data Quality Command Center':
 st.title('Data Quality Command Center'); i=q('select * from fact_data_quality_issue'); st.metric('Quality score',f'{max(0,100-len(i)/5760*100):.1f}%'); st.dataframe(i.groupby(['dimension','severity','issue_type']).size().reset_index(name='count'),use_container_width=True); st.dataframe(i.head(100),use_container_width=True)
elif page=='Donor / Funding Lookup':
 st.title('Donor / Funding Program Lookup'); countries=q('select country_code,country_name from dim_country'); programs=q('select program_id,program_name from dim_program'); cc=st.selectbox('Country',['All']+countries.country_code.tolist()); pp=st.selectbox('Program',['All']+programs.program_id.astype(str).tolist()); sql='select c.country_name,p.program_name,sum(e.enrolled) enrolled,avg(o.completion_rate) completion_rate,sum(cast(sub.is_stale as integer)) stale from fact_enrollment e join dim_site s on s.site_id=e.site_id join dim_country c on c.country_code=s.country_code join dim_program p on p.program_id=s.program_id join fact_program_outcomes o on o.record_id=e.record_id join fact_data_submission sub on sub.record_id=e.record_id where 1=1'; sql += '' if cc=='All' else f" and c.country_code='{cc}'"; sql += '' if pp=='All' else f' and p.program_id={int(pp)}'; out=q(sql+' group by c.country_name,p.program_name'); st.dataframe(out,use_container_width=True); st.download_button('Download lookup CSV',out.to_csv(index=False),'funding_lookup.csv')
elif page=='Country / Program Operations':
 st.title('Country / Program Operations'); x=q('select c.country_name,p.program_name,sum(e.enrolled) enrolled,avg(cast(sub.is_complete as integer)) completeness from fact_enrollment e join dim_site s on s.site_id=e.site_id join dim_country c on c.country_code=s.country_code join dim_program p on p.program_id=s.program_id join fact_data_submission sub on sub.record_id=e.record_id group by c.country_name,p.program_name'); st.dataframe(x,use_container_width=True); st.plotly_chart(px.bar(x,x='country_name',y='enrolled',color='program_name',title='Enrollment by country and program'),use_container_width=True)
elif page=='Migration & Reconciliation':
 st.title('Migration & Reconciliation'); x=q('select match_status,count(*) rows from fact_migration_reconciliation group by match_status'); st.plotly_chart(px.pie(x,names='match_status',values='rows',title='Migration readiness'),use_container_width=True); st.dataframe(q("select * from fact_migration_reconciliation where match_status<>'matched'"),use_container_width=True)
elif page=='Analytics & Early Warning':
 st.title('Analytics & Early Warning'); e=q('select period_id,enrolled from fact_enrollment'); t=trend(e); st.plotly_chart(px.line(t,x='period_id',y=['enrolled','rolling_3'],title='Trend and rolling average'),use_container_width=True); st.warning('Diagnostic indicator: sustained movement should be reviewed with data-quality context before operational action.'); st.dataframe(t.tail(10),use_container_width=True)
else:
 st.title('Ad-Hoc Query & Export'); st.write('Safe preset exports for analyst workflows; arbitrary SQL is intentionally not exposed.');
 for kind,sql in [('enrollment','select * from fact_enrollment'),('quality','select * from fact_data_quality_issue'),('migration','select * from fact_migration_reconciliation')]: st.download_button(f'Download {kind} CSV',q(sql).to_csv(index=False),f'{kind}.csv')
