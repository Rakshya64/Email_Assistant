import pytest
from app import app

@pytest.fixture
def client():
    """Fixture to set up a test client for the Flask app."""
    app.testing = True
    with app.test_client() as client:
        yield client

def test_index_route(client):
    """Test the index route ("/")."""
    response = client.get("/")
    assert response.status_code == 200
    assert b"<html>" in response.data

def test_generate_email_route_success(client, monkeypatch):
    """Test the /generate-email route with valid input."""

    # Mock the `generate_email` function
    def mock_generate_email(recipient, message, tone):
        return f"Generated email for {recipient} with tone {tone}."

    # Use monkeypatch to override the `generate_email` function
    monkeypatch.setattr("api.gemini_api.generate_email", mock_generate_email)

    # Test data
    test_data = {
        "to": "test@example.com",
        "message": "Hello!",
        "tone": "friendly"
    }

    response = client.post("/generate-email", json=test_data)
    assert response.status_code == 200

    data = response.get_json()
    assert "email" in data
    assert "Generated email for test@example.com with tone friendly." == data["email"]

def test_generate_email_route_missing_fields(client):
    """Test the /generate-email route with missing fields."""
    test_data = {"to": "test@example.com"}  # Missing 'message' and 'tone'

    response = client.post("/generate-email", json=test_data)
    assert response.status_code == 400
    assert "error" in response.get_json()

def test_generate_email_route_no_json(client):
    """Test the /generate-email route with no JSON input."""
    response = client.post("/generate-email")
    assert response.status_code == 400
    assert "error" in response.get_json()
