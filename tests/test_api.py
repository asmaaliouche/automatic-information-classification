from fastapi.testclient import TestClient

from api.main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    # The message depends on whether the model is loaded or not
    assert "status" in response.json()

def test_predict_invalid_data():
    # Sending incomplete data
    response = client.post("/predict", json={"age": 30})
    assert response.status_code == 422 # Unprocessable Entity (Pydantic validation error)

# Note: test_predict_success would require the model to be generated first.
