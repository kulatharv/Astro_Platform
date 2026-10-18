"""Unit tests for cache envelope serialization and deserialization."""

import pytest
from shared.cache.envelope import serialize_chart, deserialize_chart


def test_envelope_roundtrip_byte_identical():
    chart_payload = {
        "lagna": "Karka",
        "lagna_degree": "15° 30'",
        "planets": [{"name": "Sun", "sign": "Simha", "degree": 12.5}],
        "scores": {"strength": 88},
    }

    serialized = serialize_chart(chart_payload, engine_version="2.0.0")
    assert isinstance(serialized, bytes)
    assert b"2.0.0" in serialized
    assert b"cached_at" in serialized

    deserialized = deserialize_chart(serialized)
    assert deserialized == chart_payload


def test_deserialize_fallback():
    raw_payload = {"lagna": "Mesha"}
    serialized_raw = b'{"lagna": "Mesha"}'
    
    res = deserialize_chart(serialized_raw)
    assert res == raw_payload
