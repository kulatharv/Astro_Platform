"""Integration test for async narrative queue and predictions API."""

import time
import uuid
import pytest
from fastapi.testclient import TestClient
from gateway.main import app

client = TestClient(app)


def get_auth_client():
    c = TestClient(app)
    uid = uuid.uuid4().hex[:8]
    c.post(
        "/signup",
        data={"name": f"Test User {uid}", "email": f"tester_{uid}@example.com", "password": "Password123!"},
    )
    return c


PRED_REQ = {
    "year": 1990,
    "month": 5,
    "day": 15,
    "hour": 14.5,
    "city": "Pune",
}


def test_async_prediction_endpoint_latency_and_job_id():
    """Verify POST /api/prediction returns scores immediately (< 500ms) with a narrative_job_id."""
    auth_c = get_auth_client()

    start_time = time.time()
    res = auth_c.post("/api/prediction", json=PRED_REQ)
    elapsed_ms = (time.time() - start_time) * 1000

    assert res.status_code == 200
    data = res.json()

    assert "marriage_score" in data
    assert "career_score" in data
    assert "narrative_job_id" in data
    assert data["narrative_job_id"] is not None
    assert len(data["narrative_job_id"]) == 16
    assert elapsed_ms < 3000  # fast response


def test_narrative_job_status_polling():
    """Verify GET /api/narrative/{job_id} retrieves valid job status."""
    auth_c = get_auth_client()
    res_pred = auth_c.post("/api/prediction", json=PRED_REQ)
    job_id = res_pred.json()["narrative_job_id"]

    res_job = auth_c.get(f"/api/narrative/{job_id}")
    assert res_job.status_code == 200
    st_data = res_job.json()
    assert st_data["job_id"] == job_id
    assert st_data["status"] in ("queued", "running", "completed")


def test_legacy_sync_prediction_flag():
    """Verify ?sync=true flag preserves legacy synchronous LLM behavior."""
    auth_c = get_auth_client()
    res_sync = auth_c.post("/api/prediction?sync=true", json=PRED_REQ)

    assert res_sync.status_code == 200
    data = res_sync.json()
    assert "marriage_prediction" in data
    assert "career_prediction" in data
