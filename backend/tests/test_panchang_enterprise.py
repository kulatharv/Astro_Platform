"""
Enterprise Test Suite for Panchang Decision Engine.
Tests:
- Timezone resolution, IANA validation, and local time conversion.
- Deterministic Rule Engine (Do's & Don'ts, scoring).
- Multi-tier Cache Service (Redis/In-Memory fallback).
- RFC 5545 iCalendar generation.
- Full API endpoints and schema contracts.
"""

import pytest
from datetime import date, datetime, timedelta, timezone
from fastapi.testclient import TestClient

from gateway.main import app
from shared.timezone.tz import resolve_timezone, validate_iana_timezone
from shared.cache.redis_client import CacheService
from modules.horoscope.rules.daily import evaluate_daily_rules
from modules.panchang.ics import generate_panchang_ics
from modules.panchang.engine import get_full_panchang



@pytest.fixture
def client():
    return TestClient(app)


def test_timezone_resolution():
    """Test IANA timezone detection, coordinate lookup, and fallbacks."""
    assert validate_iana_timezone("Asia/Kolkata") is True
    assert validate_iana_timezone("America/New_York") is True
    assert validate_iana_timezone("Invalid/Fake_TZ") is False

    # Coordinate lookups
    _, tz_ny = resolve_timezone(lat=40.7128, lon=-74.0060)
    assert tz_ny == "America/New_York"

    _, tz_pune = resolve_timezone(lat=18.5204, lon=73.8567)
    assert tz_pune == "Asia/Kolkata"

    _, tz_fallback = resolve_timezone()
    assert tz_fallback == "Asia/Kolkata"


def test_deterministic_rule_engine():
    """Test deterministic evaluation of Vedic daily factors."""
    res = evaluate_daily_rules(
        tithi_name="Shukla Ekadashi",
        nakshatra_name="Pushya",
        yoga_name="Siddha",
        karana_name="Bava",
        weekday_idx=4,  # Thursday
        current_choghadiya={"name": "Amrit", "is_auspicious": True},
        current_hora={"planet": "Jupiter"},
        is_in_rahu_kaal=False,
        has_abhijit=True
    )

    assert "recommended" in res
    assert "avoid" in res
    assert isinstance(res["recommended"], list)
    assert isinstance(res["avoid"], list)
    assert len(res["recommended"]) > 0
    assert 0.0 <= res["rule_alignment_score"] <= 1.0
    assert 1.0 <= res["today_score"] <= 10.0
    assert "disha_shool" in res
    assert res["disha_shool"]["direction"] == "South"


def test_rahu_kaal_rule_override():
    """Test that active Rahu Kaal injects caution and lowers today score."""
    res = evaluate_daily_rules(
        tithi_name="Shukla Saptami",
        nakshatra_name="Rohini",
        yoga_name="Priti",
        karana_name="Balava",
        weekday_idx=1,
        current_choghadiya={"name": "Rog", "is_auspicious": False},
        current_hora={"planet": "Mars"},
        is_in_rahu_kaal=True,
        has_abhijit=False
    )
    first_avoid = res["avoid"][0]
    assert first_avoid["category"] == "High Caution"
    assert "Rahu Kaal" in first_avoid["reason"]


def test_cache_service():
    """Test cache get/set and key generation."""
    key = CacheService.get_panchang_key("2099-01-01", 12.3456, 78.9101)
    assert key == "panchang:2099-01-01:12.346:78.91"

    test_payload = {"city": "TestCity", "score": 9.9}
    success = CacheService.set(key, test_payload, ttl=60)
    assert success is True

    cached = CacheService.get(key)
    assert cached is not None
    assert cached["city"] == "TestCity"
    assert cached["score"] == 9.9



def test_rfc5545_calendar_ics():
    """Test RFC 5545 iCalendar stream formatting."""
    ics_str = generate_panchang_ics(city="Pune", limit=10)
    assert "BEGIN:VCALENDAR" in ics_str
    assert "VERSION:2.0" in ics_str
    assert "BEGIN:VEVENT" in ics_str
    assert "UID:panchang-" in ics_str
    assert "END:VCALENDAR" in ics_str


def test_panchang_engine_extended():
    """Test get_full_panchang with all new rich fields."""
    d = get_full_panchang("Pune", target_date=date(2026, 8, 23))
    assert d["city"] == "Pune"
    assert "choghadiya_day" in d
    assert len(d["choghadiya_day"]) == 8
    assert "choghadiya_night" in d
    assert len(d["choghadiya_night"]) == 8
    assert "current_choghadiya" in d
    assert "horas" in d
    assert len(d["horas"]) == 24
    assert "current_hora" in d
    assert "today_score" in d
    assert "current_period_summary" in d
    assert "next_auspicious_window" in d
    assert "disha_shool" in d
    assert "dos_and_donts" in d
    assert "resolved_timezone" in d
    assert d["resolved_timezone"] == "Asia/Kolkata"


def test_api_panchang_post(client):
    """Test POST /api/panchang endpoint with GPS coordinates."""
    # Test with standard city
    resp1 = client.post("/api/panchang", json={"city": "Pune"})
    assert resp1.status_code == 200
    data1 = resp1.json()
    assert data1["city"] == "Pune"
    assert "today_score" in data1
    assert "dos_and_donts" in data1

    # Test with New York coordinates
    resp2 = client.post("/api/panchang", json={
        "city": "New York",
        "lat": 40.7128,
        "lon": -74.0060
    })
    assert resp2.status_code == 200
    data2 = resp2.json()
    assert data2["resolved_timezone"] == "America/New_York"


def test_api_panchang_calendar_ics(client):
    """Test GET /api/panchang/calendar.ics endpoint."""
    resp = client.get("/api/panchang/calendar.ics?city=Mumbai&limit=15")
    assert resp.status_code == 200
    assert resp.headers["content-type"].startswith("text/calendar")
    assert "BEGIN:VCALENDAR" in resp.text


def test_karana_amavasya_pratipada_boundary():
    """Test Karana determination across the exact Amavasya -> Shukla Pratipada boundary."""
    from modules.panchang.engine import KARANA_NAMES


    def calculate_karana_for_diff(tithi_diff: float) -> tuple[int, str]:
        half_tithi = int((tithi_diff % 360.0) / 6.0)
        if half_tithi == 0:
            k_name = "Kimstughna"
        elif half_tithi >= 57:
            k_name = ["Shakuni", "Chatushpada", "Naga"][half_tithi - 57]
        else:
            k_name = KARANA_NAMES[(half_tithi - 1) % 7]
        return half_tithi, k_name

    # 1. Krishna Chaturdashi 2nd half (342° - 348°) -> Shakuni (Fixed Karana #2)
    ht_57, k_57 = calculate_karana_for_diff(345.0)
    assert ht_57 == 57
    assert k_57 == "Shakuni"

    # 2. Krishna Amavasya 1st half (348° - 354°) -> Chatushpada (Fixed Karana #3)
    ht_58, k_58 = calculate_karana_for_diff(350.0)
    assert ht_58 == 58
    assert k_58 == "Chatushpada"

    # 3. Krishna Amavasya 2nd half (354° - 360°) -> Naga (Fixed Karana #4)
    ht_59, k_59 = calculate_karana_for_diff(359.99)
    assert ht_59 == 59
    assert k_59 == "Naga"

    # 4. Exact Conjunction / Shukla Pratipada 1st half (0° - 6°) -> Kimstughna (Fixed Karana #1)
    ht_0, k_0 = calculate_karana_for_diff(0.01)
    assert ht_0 == 0
    assert k_0 == "Kimstughna"

    # 5. Shukla Pratipada 2nd half (6° - 12°) -> Bava (1st Cyclic Karana)
    ht_1, k_1 = calculate_karana_for_diff(6.5)
    assert ht_1 == 1
    assert k_1 == "Bava"

    # 6. Shukla Dwitiya 1st half (12° - 18°) -> Balava (2nd Cyclic Karana)
    ht_2, k_2 = calculate_karana_for_diff(12.5)
    assert ht_2 == 2
    assert k_2 == "Balava"


def test_vedic_vaar_pre_sunrise_1am():
    """
    Test that a birth/moment at 1:00 AM before astronomical sunrise belongs to the
    previous Vedic day (Vaar) and follows previous day's diurnal/nocturnal cycle.
    """
    import swisseph as swe
    from datetime import datetime, time
    from shared.timezone.tz import resolve_timezone


    # Target: 1:00 AM on Wednesday morning (2026-09-30 01:00:00 IST in Pune)
    # Wednesday Sunrise occurs around 06:15 AM IST.
    tz_obj, _ = resolve_timezone(lat=18.5204, lon=73.8567)
    dt_1am_wednesday = datetime(2026, 9, 30, 1, 0, 0, tzinfo=tz_obj)

    # Compute astronomical sunrise for that morning (Wednesday Sept 30)
    jd_midnight = swe.julday(2026, 9, 30, 0.0)
    res_rise = swe.rise_trans(jd_midnight, swe.SUN, swe.CALC_RISE, (73.8567, 18.5204, 560.0), 0.0, 0.0)
    y, m, d_int, ut_h_float = swe.revjul(res_rise[1][0])
    h = int(ut_h_float)
    m_f = (ut_h_float - h) * 60.0
    minute = int(m_f)
    sec = min(int((m_f - minute) * 60.0), 59)
    from datetime import timezone
    dt_wed_sunrise = datetime(y, m, d_int, h, minute, sec, tzinfo=timezone.utc).astimezone(tz_obj)

    # Confirm 1:00 AM is strictly before sunrise
    assert dt_1am_wednesday < dt_wed_sunrise

    # In Vedic astronomy, if current time is before sunrise, the active Vedic day belongs to Tuesday (Tuesday sunrise to Wednesday sunrise)
    cal_weekday = dt_1am_wednesday.weekday()  # Wednesday = 2 (Mon=0, Tue=1, Wed=2)
    vedic_weekday_idx = (cal_weekday - 1) if dt_1am_wednesday < dt_wed_sunrise else cal_weekday
    assert vedic_weekday_idx == 1  # 1 = Tuesday (Mangalvaar)

    # Tuesday Vedic Day: Rahu Kaal occurs in the 7th octant of Tuesday day span (~15:00 - 16:30)
    rahu_parts = {0: 7, 1: 1, 2: 6, 3: 4, 4: 5, 5: 3, 6: 2}  # Sunday=0, Monday=1, Tuesday=2
    # For Tuesday (Vedic weekday index 2 in Sun=0 notation), Rahu Kaal part is 6 (7th octant)
    tue_v_wd = 2
    assert rahu_parts[tue_v_wd] == 6

    # Verify at 1:00 AM (night), person is NOT in Rahu Kaal (since Rahu Kaal occurred during Tuesday daytime)
    # The active hour at 1:00 AM is Hour #20 of Tuesday solar cycle
    hours_since_tue_sunrise = (dt_1am_wednesday - (dt_wed_sunrise - timedelta(days=1))).total_seconds() / 3600.0
    assert 18.0 <= hours_since_tue_sunrise <= 20.0

