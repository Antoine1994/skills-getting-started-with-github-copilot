import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert isinstance(data["Chess Club"], dict)

def test_signup_and_unregister():
    email = "testuser@mergington.edu"
    activity = "Art Club"
    # Signup
    response = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert response.status_code == 200
    assert f"Signed up {email}" in response.json()["message"]
    # Already signed up
    response = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert response.status_code == 400
    # Unregister
    response = client.post(f"/activities/{activity}/unregister", params={"email": email})
    assert response.status_code == 200
    assert f"Unregistered {email}" in response.json()["message"]
    # Not registered anymore
    response = client.post(f"/activities/{activity}/unregister", params={"email": email})
    assert response.status_code == 400

def test_signup_activity_not_found():
    response = client.post("/activities/UnknownActivity/signup", params={"email": "a@b.com"})
    assert response.status_code == 404

def test_unregister_activity_not_found():
    response = client.post("/activities/UnknownActivity/unregister", params={"email": "a@b.com"})
    assert response.status_code == 404
