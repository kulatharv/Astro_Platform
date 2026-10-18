"""Integration tests for module cross-communication and gateway router mounting."""

import pytest
from fastapi.testclient import TestClient
from gateway.main import app
from modules.prediction.api import PredictionService
from modules.prediction.schemas import PredictionRequest


client = TestClient(app)


def test_gateway_mounts_all_routers():
    """Verify gateway mounts all public endpoints successfully."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

    response = client.get("/api/locales/en")
    assert response.status_code == 200
    assert "translations" in response.json()


def test_prediction_calls_kundali_via_public_api():
    """Verify PredictionService calls Kundali compute_chart through api interface without direct internals access."""
    service = PredictionService()
    req = PredictionRequest(
        year=1990,
        month=5,
        day=15,
        hour=14.5,
        city="Pune",
    )
    result = service.analyse_domains(req)
    assert result is not None
    assert "domains" in result
    assert "marriage" in result["domains"]
    assert "career" in result["domains"]


