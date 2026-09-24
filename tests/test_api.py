from fastapi.testclient import TestClient
from api.main import app
client=TestClient(app)
def test_health(): assert client.get('/health').json()['synthetic'] is True
def test_summary(): assert client.get('/summary').json()['records']>=20000
def test_lookup_supports_postgresql_parameters():
    response=client.get('/lookup',params={'country':'SYN-A','program_id':1})
    assert response.status_code==200
    assert response.json()
def test_migration_reports_all_statuses():
    payload=client.get('/migration').json()
    statuses={row['match_status'] for row in payload['counts']}
    assert {'matched','mismatch','rejected'} <= statuses
    assert payload['total_rows']==120
    assert payload['readiness_score']==10.8

def test_analytics_exposes_bounded_forecast():
    forecast=client.get('/analytics').json()['forecast']
    assert forecast['available'] is True
    assert forecast['lower_bound'] <= forecast['estimate'] <= forecast['upper_bound']
