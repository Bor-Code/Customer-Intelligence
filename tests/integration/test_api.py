from unittest.mock import MagicMock

import pandas as pd
import pytest
from fastapi.testclient import TestClient
from typing import Generator

from ci.api.main import app, models

client = TestClient(app)

@pytest.fixture(autouse=True)
def mock_models() -> Generator[None, None, None]:
    mock_churn = MagicMock()
    mock_churn.predict.return_value = [1, 0]

    mock_basket = MagicMock()
    mock_basket.predict.return_value = pd.DataFrame(
        {"antecedents": ["A"], "consequents": ["B"], "confidence": [0.8]}
    )

    models["churn"] = mock_churn
    models["basket"] = mock_basket
    yield
    models.clear()

def test_predict_churn_success() -> None:
    response = client.post(
        "/predict/churn", json={"features": [{"Recency": 10, "Frequency": 5, "Monetary": 100}]}
    )
    assert response.status_code == 200
    assert response.json()["predictions"] == [1, 0]

def test_predict_model_not_found() -> None:
    response = client.post("/predict/unknown_model", json={"features": []})
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]

def test_predict_basket_error() -> None:
    response = client.post("/predict/basket", json={"features": []})
    assert response.status_code == 400
    assert "Use /rules/basket" in response.json()["detail"]

def test_get_basket_rules() -> None:
    response = client.get("/rules/basket")
    assert response.status_code == 200
    data = response.json()
    assert "rules" in data
    assert len(data["rules"]) == 1
    assert data["rules"][0]["confidence"] == 0.8
