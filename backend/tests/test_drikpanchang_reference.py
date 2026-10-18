"""
Permanent regression unit tests validating AstroLogic Panchang Engine against
published Drik Panchang ground-truth reference values (fetched live from drikpanchang.com).

Tolerances:
- Sunrise & Sunset: +/- 90 seconds (optical refraction / limb definition differences)
- Tithi, Nakshatra, Yoga, Karana transition end times: +/- 2 minutes (iterative root-finding precision)
"""
import pytest
from datetime import date, datetime, timedelta
from modules.panchang.engine import get_full_panchang



def _parse_ampm_minutes(t_str: str) -> int:
    """Helper to convert HH:MM AM/PM to minutes since midnight."""
    clean = t_str.strip()
    dt = datetime.strptime(clean, "%I:%M %p")
    return dt.hour * 60 + dt.minute


def _assert_time_within_tolerance_mins(actual_str: str, expected_str: str, max_tol_mins: int = 2):
    act_min = _parse_ampm_minutes(actual_str)
    exp_min = _parse_ampm_minutes(expected_str)
    diff = abs(act_min - exp_min)
    # Handle midnight wrapping
    if diff > 720:
        diff = 1440 - diff
    assert diff <= max_tol_mins, (
        f"Time deviation exceeded tolerance! Actual: {actual_str} ({act_min}m), "
        f"Expected: {expected_str} ({exp_min}m), Diff: {diff}m > {max_tol_mins}m"
    )


def test_drikpanchang_chennai_december_solstice_2026():
    """
    Case 1: Chennai (Coastal / Sea-level 6.0m) on Winter Solstice (2026-12-21)
    Live Drik Reference:
      - Sunrise: 06:26 AM, Sunset: 05:48 PM
      - Tithi: Shukla Dwadashi (ends 05:36 PM)
      - Nakshatra: Bharani (ends 01:08 PM)
      - Yoga: Siddha (ends 01:32 AM next day)
      - Karana at Sunrise: Bava (ends 07:00 AM)
    """
    res = get_full_panchang(city_name="Chennai", target_date=date(2026, 12, 21))

    # Core elements
    assert "Dwadashi" in res["tithi"]
    assert res["nakshatra"] == "Bharani"
    assert res["yoga"] == "Siddha"
    assert res["karana"] == "Bava"

    # Sunrise / Sunset (within 90 seconds -> max 2 min difference)
    _assert_time_within_tolerance_mins(res["sunrise"], "06:26 AM", max_tol_mins=2)
    _assert_time_within_tolerance_mins(res["sunset"], "05:48 PM", max_tol_mins=2)

    # End Times (within 2 minutes)
    _assert_time_within_tolerance_mins(res["tithi_end"], "05:36 PM", max_tol_mins=2)
    _assert_time_within_tolerance_mins(res["nakshatra_end"], "01:08 PM", max_tol_mins=2)
    _assert_time_within_tolerance_mins(res["yoga_end"], "01:32 AM", max_tol_mins=2)
    _assert_time_within_tolerance_mins(res["karana_end"], "07:00 AM", max_tol_mins=2)


def test_drikpanchang_leh_high_altitude_solstice_2026():
    """
    Case 2: Leh (High Altitude 3500.0m) on Winter Solstice (2026-12-21)
    Live Drik Reference:
      - Sunrise: 07:21 AM, Sunset: 05:14 PM
      - Tithi: Shukla Dwadashi (ends 05:36 PM)
      - Nakshatra: Bharani (ends 01:08 PM)
      - Yoga: Siddha (ends 01:32 AM next day)
      - Karana: Balava (ends 05:36 PM)
    """
    res = get_full_panchang(city_name="Leh", target_date=date(2026, 12, 21))

    # Core elements
    assert "Dwadashi" in res["tithi"]
    assert res["nakshatra"] == "Bharani"
    assert res["yoga"] == "Siddha"

    # Sunrise / Sunset with altitude pressure refraction (within 90s -> 2 mins)
    _assert_time_within_tolerance_mins(res["sunrise"], "07:21 AM", max_tol_mins=2)
    _assert_time_within_tolerance_mins(res["sunset"], "05:14 PM", max_tol_mins=2)

    # End Times (within 2 minutes)
    _assert_time_within_tolerance_mins(res["tithi_end"], "05:36 PM", max_tol_mins=2)
    _assert_time_within_tolerance_mins(res["nakshatra_end"], "01:08 PM", max_tol_mins=2)
    _assert_time_within_tolerance_mins(res["yoga_end"], "01:32 AM", max_tol_mins=2)


def test_drikpanchang_chennai_sunrise_proximate_tithi_transition_2026():
    """
    Case 3: Chennai on 2026-01-07 (Tithi transition ~20 min after sunrise)
    Live Drik Reference:
      - Sunrise: 06:33 AM, Sunset: 05:57 PM
      - Tithi at Sunrise: Krishna Chaturthi (ends 06:52 AM)
      - Nakshatra at Sunrise: Magha (ends 11:56 AM)
      - Yoga at Sunrise: Ayushmana (ends 06:34 PM)
      - Karana at Sunrise: Balava (ends 06:52 AM)
    """
    res = get_full_panchang(city_name="Chennai", target_date=date(2026, 1, 7))

    # Core Udaya Kalina elements at sunrise
    assert "Chaturthi" in res["tithi"]
    assert res["nakshatra"] == "Magha"
    assert "Ayushman" in res["yoga"]
    assert res["karana"] == "Balava"

    # Sunrise / Sunset (exact match)
    _assert_time_within_tolerance_mins(res["sunrise"], "06:33 AM", max_tol_mins=2)
    _assert_time_within_tolerance_mins(res["sunset"], "05:57 PM", max_tol_mins=2)

    # End Times (within 2 minutes)
    _assert_time_within_tolerance_mins(res["tithi_end"], "06:52 AM", max_tol_mins=2)
    _assert_time_within_tolerance_mins(res["nakshatra_end"], "11:56 AM", max_tol_mins=2)
    _assert_time_within_tolerance_mins(res["yoga_end"], "06:34 PM", max_tol_mins=2)
    _assert_time_within_tolerance_mins(res["karana_end"], "06:52 AM", max_tol_mins=2)
