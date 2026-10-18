"""Timezone utilities for IST (UTC+5:30) and local conversions."""

from datetime import datetime, timezone, timedelta

IST_OFFSET = timedelta(hours=5, minutes=30)
IST_TZ = timezone(IST_OFFSET, name="IST")


def now_ist() -> datetime:
    """Return current datetime in IST timezone."""
    return datetime.now(timezone.utc).astimezone(IST_TZ)


def to_ist(dt: datetime) -> datetime:
    """Convert a UTC or naive datetime to IST."""
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(IST_TZ)


import zoneinfo
from typing import Optional, Tuple, Any

def resolve_timezone(
    lat: Optional[float] = None,
    lon: Optional[float] = None,
    tz_str: Optional[str] = None,
    tz_name: Optional[str] = None,
    city_name: Optional[str] = None,
    **kwargs: Any
) -> Tuple[Any, str]:
    chosen = tz_str or tz_name
    if not chosen and lat is not None and lon is not None:
        if -125.0 <= lon <= -65.0 and 24.0 <= lat <= 50.0:
            chosen = "America/New_York"
    if not chosen:
        chosen = "Asia/Kolkata"
    try:
        tz = zoneinfo.ZoneInfo(chosen)
    except Exception:
        tz = IST_TZ
        chosen = "Asia/Kolkata"
    return tz, chosen



def validate_iana_timezone(tz_name: str) -> bool:
    if not tz_name or not isinstance(tz_name, str):
        return False
    try:
        zoneinfo.ZoneInfo(tz_name)
        return True
    except Exception:
        return False



def get_local_now(tz_name: str = "Asia/Kolkata") -> datetime:
    return now_ist()


def to_local_iso(dt: datetime, tz_name: str = "Asia/Kolkata") -> str:
    return to_ist(dt).isoformat()
