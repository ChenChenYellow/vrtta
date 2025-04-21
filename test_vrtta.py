import sys
import os
import pytest
import json
from vrtta import app

@pytest.fixture
def client():
    """A test client for the app."""
    with app.test_client() as client:
        yield client

def test_home(client):
    response = client.get('/')
    assert response.text == "Hello World"

def test_score(client):
    body = {
    "product_name": "bbb",
    "materials": ["aluminium", "plastic"],
    "weight_grams": 10,
    "transport": "air",
    "packaging": "recyclable"
    }
    response = client.post('/score', content_type="application/json", data=json.dumps(body))
    assert response.status_code == 200
    assert response.json == {
        "product_name": "bbb",
        "rating": "D",
        "suggestions": [
            "Avoid use of plastic",
            "Avoid air transport"
        ],
        "sustainability_score": -0.5
    }
def test_score_when_weight_grams_not_number(client):
    body = {
    "product_name": "bbb",
    "materials": ["aluminium", "plastic"],
    "weight_grams": "10.0.0",
    "transport": "air",
    "packaging": "recyclable"
    }
    response = client.post('/score', content_type="application/json", data=json.dumps(body))
    assert response.status_code == 401
    assert response.text == "weight_grams not int nor float"
