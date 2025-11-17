
import json
from flask_app import app

def test_health():
    client = app.test_client()
    res = client.get('/')
    assert res.status_code == 200
