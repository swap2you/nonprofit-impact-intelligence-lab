import os,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle
from reportlab.lib import colors
from database.schema import engine
OUT=Path(__file__).resolve().parents[1]/'assets'/'sample_outputs'; OUT.mkdir(parents=True,exist_ok=True)
def pdf(name,title,df):
 doc=SimpleDocTemplate(str(OUT/name),pagesize=letter); data=[list(df.columns)]+df.head(18).astype(str).values.tolist(); story=[Paragraph(title),Spacer(1,12),Paragraph('Synthetic demonstration; diagnostic summary only.'),Spacer(1,12),Table(data,repeatRows=1,style=TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#17324d')),('TEXTCOLOR',(0,0),(-1,0),colors.white),('GRID',(0,0),(-1,-1),.25,colors.grey),('FONTSIZE',(0,0),(-1,-1),7)]))]; doc.build(story)
def main():
 e=pd.read_sql_query('select * from fact_enrollment',engine); i=pd.read_sql_query('select dimension,severity,issue_type,count(*) issue_count from fact_data_quality_issue group by dimension,severity,issue_type',engine); f=pd.read_sql_query('select * from fact_funding_allocation',engine); m=pd.read_sql_query('select match_status,count(*) rows from fact_migration_reconciliation group by match_status',engine)
 for n,t,d in [('executive_impact_snapshot.pdf','Executive Impact Snapshot',e.groupby('period_id',as_index=False).enrolled.sum()),('data_quality_summary.pdf','Data Quality Summary',i),('funding_program_brief.pdf','Funding / Program Brief',f),('migration_reconciliation_summary.pdf','Migration Reconciliation Summary',m)]: pdf(n,t,d)
 e.to_csv(OUT/'enrollment_sample.csv',index=False); f.to_excel(OUT/'funding_program_brief.xlsx',index=False)
 print([str(x) for x in OUT.iterdir()])
if __name__=='__main__': main()
