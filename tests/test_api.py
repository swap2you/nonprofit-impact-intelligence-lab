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
    statuses={row['match_status'] for row in client.get('/migration').json()}
    assert {'matched','mismatch','rejected'} <= statuses
