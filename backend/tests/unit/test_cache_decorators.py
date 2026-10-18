"""Unit tests for @cached_chart decorator."""

import pytest
from unittest.mock import MagicMock, patch
from shared.cache.decorators import cached_chart
from shared.cache.redis_client import CacheService


class DummyService:
    def __init__(self):
        self.call_count = 0

    @cached_chart(ttl=3600)
    def compute_chart(self, req: dict) -> dict:
        self.call_count += 1
        return {"lagna": "Karka", "computed": True}


def test_cached_chart_hit_and_miss():
    CacheService.clear()
    service = DummyService()
    req = {"year": 1995, "month": 5, "day": 15, "hour": 14, "minute": 30, "city": "Pune"}

    # First call -> miss -> call_count = 1
    res1 = service.compute_chart(req)
    assert res1["lagna"] == "Karka"
    assert service.call_count == 1

    # Second call -> hit -> call_count remains 1
    res2 = service.compute_chart(req)
    assert res2["lagna"] == "Karka"
    assert service.call_count == 1


def test_cached_chart_fail_open_on_cache_error():
    CacheService.clear()
    service = DummyService()
    req = {"year": 1995, "month": 5, "day": 15, "hour": 14, "minute": 30, "city": "Pune"}

    with patch.object(CacheService, "get", side_effect=RuntimeError("Redis connection lost")):
        res = service.compute_chart(req)
        assert res["lagna"] == "Karka"
