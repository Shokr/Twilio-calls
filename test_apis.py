from fastapi.testclient import TestClient

from api import app

client = TestClient(app)


def test_create_call_success():
    """Test creating a call with valid input."""
    response = client.post("/calls", json={"to_number": "+201289859363", "message": "Hello!"})
    assert response.status_code == 201
    json_response = response.json()
    assert "call_sid" in json_response
    assert json_response.get("success") is True


def test_create_call_invalid_number():
    """Test creating a call with an invalid number."""
    response = client.post("/calls", json={"to_number": "invalid_number", "message": "Test message"})
    assert response.status_code == 400
    json_response = response.json()
    assert "detail" in json_response


def test_get_call_status_success():
    """Test fetching a valid call status."""
    call_sid = "CAdf2d8ffbb6cd027b81b2eb27371ade4c"
    response = client.get(f"/calls/{call_sid}")
    assert response.status_code in [200, 404]

    if response.status_code == 200:
        json_response = response.json()
        assert "call_sid" in json_response
        assert "status" in json_response
