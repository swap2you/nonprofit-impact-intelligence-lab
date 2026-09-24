import pandas as pd, numpy as np
def iqr_flags(values):
 s=pd.Series(values).dropna(); q1,q3=s.quantile(.25),s.quantile(.75); i=q3-q1
 return (s<q1-1.5*i)|(s>q3+1.5*i)
def trend(df,value='enrolled'):
 x=df.groupby('period_id',as_index=False)[value].mean().sort_values('period_id'); x['rolling_3']=x[value].rolling(3,min_periods=1).mean(); x['pct_change']=x[value].pct_change().replace([np.inf,-np.inf],np.nan).fillna(0); return x
def diagnostic(change,stale_rate,duplicate_rate):
 if change < -.1 and stale_rate > .15: return 'Possible reporting delay: metric drop coincides with stale submissions; requires analyst review.'
 if change > .2 and duplicate_rate > .02: return 'Possible data-quality issue: spike coincides with duplicate increase; requires analyst review.'
 if abs(change) > .1 and stale_rate < .05: return 'Diagnostic indicator: movement with healthy freshness; operational signal requiring review.'
 return 'No dominant diagnostic indicator; inspect contributing sites and periods.'
