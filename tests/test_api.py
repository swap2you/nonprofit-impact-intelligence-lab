from fastapi.testclient import TestClient
from api.main import app
def test_health(): assert TestClient(app).get('/health').json()['synthetic'] is True
def test_summary(): assert TestClient(app).get('/summary').json()['records']>=20000
