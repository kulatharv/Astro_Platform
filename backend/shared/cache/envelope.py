"""Envelope serialization for cached chart responses."""

import json
from datetime import datetime, timezone
from typing import Any
from pydantic import BaseModel
from shared.timezone.tz import now_ist


class CacheEnvelope(BaseModel):
    engine_version: str
    cached_at: str
    payload: dict[str, Any]


def serialize_chart(resp: dict[str, Any] | BaseModel, engine_version: str = "2.0.0") -> bytes:
    """
    Serialize chart response object into JSON bytes with metadata envelope.
    """
    if isinstance(resp, BaseModel):
        payload = resp.model_dump()
    else:
        payload = dict(resp)

    envelope = CacheEnvelope(
        engine_version=engine_version,
        cached_at=now_ist().isoformat(),
        payload=payload,
    )
    return envelope.model_dump_json().encode("utf-8")


def deserialize_chart(data: bytes | str) -> dict[str, Any]:
    """
    Deserialize JSON bytes back into pure payload dict, stripping envelope metadata.
    """
    if isinstance(data, bytes):
        raw_str = data.decode("utf-8")
    else:
        raw_str = data

    parsed = json.loads(raw_str)
    if isinstance(parsed, dict) and "payload" in parsed and "engine_version" in parsed:
        return parsed["payload"]
    
    # Fallback if raw payload was stored directly
    return parsed
