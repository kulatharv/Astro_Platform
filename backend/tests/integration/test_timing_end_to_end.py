"""Integration tests for Phase 5 concrete timing windows and Dasha-Gochara fusion."""

import pytest
from fastapi.testclient import TestClient
from gateway.main import app
from modules.kundali.api import KundaliService, KundaliRequest
from modules.prediction.timing import compute_timing

client = TestClient(app)
kundali_service = KundaliService()

SAMPLE_REQ = {
    "year": 1990,
    "month": 5,
    "day": 15,
    "hour": 14,
    "minute": 30,
    "city": "Pune",
}


def test_timing_windows_generation():
    k_req = KundaliRequest(**SAMPLE_REQ)
    chart = kundali_service.compute_chart(k_req)

    res = compute_timing(chart, "marriage")
    assert "timing_windows" in res
    assert "peak_window" in res
    assert len(res["timing_windows"]) > 0

    first_window = res["timing_windows"][0]
    assert "start" in first_window
    assert "end" in first_window
    assert "score" in first_window
    assert "confidence" in first_window
    assert "mahadasha" in first_window
    assert "antardasha" in first_window
    assert "pratyantardasha" in first_window
    assert "drivers" in first_window
    assert "transit_notes" in first_window


import uuid


def get_auth_client():
    c = TestClient(app)
    uid = uuid.uuid4().hex[:8]
    c.post(
        "/signup",
        data={"name": f"Test User {uid}", "email": f"tester_{uid}@example.com", "password": "Password123!"},
    )
    return c


def test_standalone_timing_endpoint():
    auth_c = get_auth_client()
    res = auth_c.post("/api/prediction/timing/career", json=SAMPLE_REQ)
    assert res.status_code == 200
    data = res.json()
    assert "timing_windows" in data
    assert "peak_window" in data
    assert data["timing_engine"] == "1.0.0"
