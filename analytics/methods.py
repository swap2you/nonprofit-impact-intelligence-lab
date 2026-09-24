import pandas as pd, numpy as np
def iqr_flags(values):
 s=pd.Series(values).dropna(); q1,q3=s.quantile(.25),s.quantile(.75); i=q3-q1
 return (s<q1-1.5*i)|(s>q3+1.5*i)
def trend(df,value='enrolled'):
 x=df.groupby('period_id',as_index=False)[value].mean().sort_values('period_id'); x['rolling_3']=x[value].rolling(3,min_periods=1).mean(); x['pct_change']=x[value].pct_change().replace([np.inf,-np.inf],np.nan).fillna(0); return x
def bounded_forecast(df,value='enrolled',recent=6,min_observations=4):
    """Illustrative one-period OLS trend with a 95% residual uncertainty band."""
    x=df.groupby('period_id',as_index=False)[value].mean().dropna().sort_values('period_id').tail(recent)
    if len(x)<min_observations: return {'available':False,'reason':f'Requires at least {min_observations} observations.'}
    xs=x['period_id'].to_numpy(dtype=float); ys=x[value].to_numpy(dtype=float)
    slope,intercept=np.polyfit(xs,ys,1); next_period=int(xs[-1]+1); estimate=float(intercept+slope*next_period)
    residuals=ys-(intercept+slope*xs); residual_std=float(np.std(residuals,ddof=1)) if len(residuals)>1 else 0.0
    margin=max(1.96*residual_std,abs(estimate)*0.05,1.0)
    return {'available':True,'forecast_period_id':next_period,'estimate':round(max(0,estimate),2),'lower_bound':round(max(0,estimate-margin),2),'upper_bound':round(max(0,estimate+margin),2),'observations':len(x),'method':'OLS linear trend on last six observations; 95% residual band with 5% minimum margin','label':'Illustrative diagnostic forecast; requires analyst review.'}
def diagnostic(change,stale_rate,duplicate_rate):
 if change < -.1 and stale_rate > .15: return 'Possible reporting delay: metric drop coincides with stale submissions; requires analyst review.'
 if change > .2 and duplicate_rate > .02: return 'Possible data-quality issue: spike coincides with duplicate increase; requires analyst review.'
 if abs(change) > .1 and stale_rate < .05: return 'Diagnostic indicator: movement with healthy freshness; operational signal requiring review.'
 return 'No dominant diagnostic indicator; inspect contributing sites and periods.'
