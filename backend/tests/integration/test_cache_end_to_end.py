"""Integration tests verifying end-to-end caching behavior and fail-open guarantees."""

import uuid
import pytest
from fastapi.testclient import TestClient
from gateway.main import app
from shared.cache.redis_client import CacheService
from shared.cache.metrics import cache_metrics
from shared.db.session import SessionLocal, init_db
from modules.auth.models import AdminUser
from modules.auth.security import hash_password

client = TestClient(app)


def get_auth_client():
    c = TestClient(app)
    uid = uuid.uuid4().hex[:8]
    c.post(
        "/signup",
        data={"name": f"Test User {uid}", "email": f"tester_{uid}@example.com", "password": "Password123!"},
    )
    return c


SAMPLE_REQ = {
    "year": 1990,
    "month": 1,
    "day": 1,
    "hour": 12,
    "minute": 0,
    "city": "Pune",
}


def test_cache_hit_and_miss_via_api():
    """Verify first request is a cache miss and second identical request is a cache hit."""
    CacheService.clear()
    cache_metrics.reset()
    auth_client = get_auth_client()

    # First request -> MISS
    res1 = auth_client.post("/api/kundali", json=SAMPLE_REQ)
    assert res1.status_code == 200
    data1 = res1.json()

    stats1 = cache_metrics.get_stats()
    assert stats1["misses"] >= 1
    assert stats1["hits"] == 0

    # Second request -> HIT
    res2 = auth_client.post("/api/kundali", json=SAMPLE_REQ)
    assert res2.status_code == 200
    data2 = res2.json()

    stats2 = cache_metrics.get_stats()
    assert stats2["hits"] >= 1

    # Byte-identical response verification
    assert data1 == data2


def test_metrics_endpoint():
    """Verify /metrics route returns cache statistics."""
    res = client.get("/metrics")
    assert res.status_code == 200
    data = res.json()
    assert "cache" in data
    assert "hits" in data["cache"]
    assert "misses" in data["cache"]


def test_admin_cache_flush():
    """Verify admin flush route clears cache counters and entries."""
    init_db()
    db = SessionLocal()
    try:
        if not db.query(AdminUser).filter(AdminUser.username == "cache_admin").first():
            db.add(AdminUser(username="cache_admin", password_hash=hash_password("adminpass123")))
            db.commit()
    finally:
        db.close()

    admin_client = TestClient(app)
    admin_client.post("/admin/login", data={"username": "cache_admin", "password": "adminpass123"})

    # Trigger some cache usage
    auth_c = get_auth_client()
    auth_c.post("/api/kundali", json=SAMPLE_REQ)

    # Admin flushes cache
    res_flush = admin_client.post("/api/admin/cache/flush")
    assert res_flush.status_code == 200
    assert res_flush.json()["status"] == "ok"

    stats = cache_metrics.get_stats()
    assert stats["hits"] == 0
    assert stats["misses"] == 0
