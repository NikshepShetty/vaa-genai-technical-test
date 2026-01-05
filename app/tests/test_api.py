"""
FastAPI test file
Run from repo root: pytest
"""

from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_root_endpoint_running():
    """ Test to check if root endpoint returns correct status code (200)."""
    response = client.get('/')
    assert response.status_code == 200

def test_health_endpoint_running():
    """ Test to check if health endpoint returns correct status code (200)."""
    response = client.get('/health')
    assert response.status_code == 200

def test_help_assistant_valid_return_200():
    """ Test to check if correct status code (200) and valid response format is returned"""
    response = client.post('/help-assistant', json={
        "query": "What is the customer support number?"
    })
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert "sources" in data
    assert "confidence" in data
    assert isinstance(data["sources"], list)
    assert isinstance(data["answer"], str)
    assert data["confidence"] is None or isinstance(data["confidence"], float)

def test_help_assistant_prompt_only_working():
    """ Test to check if query only returns correct status code (200)."""
    response = client.post('/help-assistant', json={
        "query": "What is the customer support number?",
    })
    assert response.status_code == 200

def test_help_assistant_valid_category_working():
    """ Test to check if query and valid category returns correct status code (200)."""
    response = client.post('/help-assistant', json={
        "query": "What is the customer support number?",
        "category": "contact"
    })
    assert response.status_code == 200

def test_help_assistant_category_normalisation_working():
    """ Test to check if category normalisation (strip/lower) returns correct status code (200)."""
    response = client.post('/help-assistant', json={
        "query": "What is the customer support number?",
        "category": "  CONTACT  "
    })
    assert response.status_code == 200

def test_help_assistant_invalid_category_422():
    """ Test to check if query and invalid category returns correct status code (422)."""
    response = client.post('/help-assistant', json={
        "query": "What is the customer support number?",
        "category": "invalid_category"
    })
    assert response.status_code == 422

def test_help_assistant_missing_query_422():
    """ Test to check if missing query field returns correct status code (422)."""
    response = client.post('/help-assistant', json={
        "category": "contact"
    })
    assert response.status_code == 422

def test_help_assistant_empty_query_422():
    """ Test to check if empty query value returns correct status code (422)."""
    response = client.post('/help-assistant', json={
        "query": ""
    })
    assert response.status_code == 422

def test_help_assistant_invalid_body_422():
    """ Test to check if invalid JSON body returns correct status code (422)."""
    response = client.post('/help-assistant', data="not-json")
    assert response.status_code == 422


def test_help_assistant_non_string_query_422():
    """ Test to check if non string query value returns correct status code (422)."""
    response = client.post('/help-assistant', json={
        "query": 12345
    })
    assert response.status_code == 422


def test_help_assistant_non_string_category_422():
    """ Test to check if non string category value returns correct status code (422)."""
    response = client.post('/help-assistant', json={
        "query": "What is the customer support number?",
        "category": ["contact"]
    })
    assert response.status_code == 422