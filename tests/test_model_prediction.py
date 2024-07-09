import pytest
from fastapi.testclient import TestClient

@pytest.fixture(scope="module")
def client():
    import sys
    import os
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

    from fastapi import FastAPI
    from model_prediction import app as main_app  # Assuming your FastAPI app file is named `5_model_prediction.py`

    client = TestClient(main_app)
    return client   

def test_predict_sales(client):
    payload = {
        "month": 1,
        "day_of_week": 1,
        "product_category_name": "electronics"
    }
    response = client.post("/", json=payload)
    assert response.status_code == 200
    assert "predicted_sales_count" in response.json()
