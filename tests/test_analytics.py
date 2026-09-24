import pandas as pd
from analytics.methods import iqr_flags,trend,diagnostic
def test_iqr_flags_detects_spike(): assert bool(iqr_flags([1,1,1,1,20]).iloc[-1])
def test_trend_and_diagnostic():
 x=trend(pd.DataFrame({'period_id':[1,2,3],'enrolled':[10,8,6]})); assert 'rolling_3' in x and diagnostic(-.2,.3,.01).startswith('Possible reporting')
