import pandas as pd
from analytics.methods import iqr_flags,trend,diagnostic,bounded_forecast
def test_iqr_flags_detects_spike(): assert bool(iqr_flags([1,1,1,1,20]).iloc[-1])
def test_trend_and_diagnostic():
 x=trend(pd.DataFrame({'period_id':[1,2,3],'enrolled':[10,8,6]})); assert 'rolling_3' in x and diagnostic(-.2,.3,.01).startswith('Possible reporting')
def test_bounded_forecast_returns_interval_and_requires_minimum():
 x=bounded_forecast(pd.DataFrame({'period_id':[1,2,3,4,5,6],'enrolled':[10,12,14,16,18,20]}))
 assert x['available'] and x['lower_bound'] <= x['estimate'] <= x['upper_bound'] and x['observations']==6
 assert bounded_forecast(pd.DataFrame({'period_id':[1,2,3],'enrolled':[10,12,14]}))['available'] is False
