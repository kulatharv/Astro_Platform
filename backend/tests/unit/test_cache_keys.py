"""Unit tests for cache key generation and input hash determinism."""

import pytest
from shared.cache.keys import compute_input_hash, chart_cache_key
from modules.kundali.schemas import KundaliRequest


def test_deterministic_input_hash():
    req1 = {"year": 1995, "month": 5, "day": 15, "hour": 14, "minute": 30, "city": "Pune"}
    req2 = KundaliRequest(year=1995, month=5, day=15, hour=14, minute=30, city="Pune")

    hash1 = compute_input_hash(req1)
    hash2 = compute_input_hash(req2)

    assert hash1 == hash2
    assert len(hash1) == 64


def test_different_inputs_produce_different_hashes():
    base = {"year": 1995, "month": 5, "day": 15, "hour": 14, "minute": 30, "city": "Pune"}

    hash_base = compute_input_hash(base)
    hash_tz = compute_input_hash({**base, "timezone": "America/New_York"})
    hash_ayanamsa = compute_input_hash({**base, "ayanamsa": "Raman"})
    hash_min = compute_input_hash({**base, "minute": 31})

    assert hash_base != hash_tz
    assert hash_base != hash_ayanamsa
    assert hash_base != hash_min


def test_cache_key_formatting():
    input_hash = "abc123hash"
    key = chart_cache_key(input_hash, engine_version="2.0.0")
    assert key == "chart:2.0.0:abc123hash"
