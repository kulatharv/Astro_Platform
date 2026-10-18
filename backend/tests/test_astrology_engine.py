"""Unit tests for Pure Astrology Calculation Engine."""

import pytest
from modules.kundali.planets import calculate_all_planets
from modules.kundali.houses import calculate_lagna
from shared.veda.nakshatra import calculate_nakshatra
from modules.kundali.varga import calculate_navamsa
from modules.kundali.dasha import calculate_mahadasha, generate_dasha_timeline, generate_antardasha
from shared.veda.yogas import calculate_yogas
from shared.veda.doshas import calculate_doshas
from modules.kundali.engine import calculate_kundali
from modules.kundali.varga import generate_full_chart

from modules.panchang.engine import calculate_panchang_for_datetime, get_full_panchang
from modules.horoscope.engine import generate_horoscope, generate_all_horoscopes
from modules.prediction.engine import analyse_all_domains
from modules.kundali.cities import get_city
from shared.veda.zodiac import degree_to_sign, to_dms



def test_zodiac_and_dms():
    sign, deg = degree_to_sign(45.5)
    assert sign == "Vrishabha"
    assert round(deg, 1) == 15.5

    dms_str = to_dms(15.5)
    assert "15° 30'" in dms_str


def test_nakshatra_calculation():
    # 0 degrees is Ashwini Pada 1
    nak, pada = calculate_nakshatra(0.0)
    assert nak == "Ashwini"
    assert pada == 1

    # 15 degrees is Bharani Pada 1
    nak2, pada2 = calculate_nakshatra(15.0)
    assert nak2 == "Bharani"
    assert pada2 == 1


def test_navamsa_calculation():
    # 0 deg (Mesha) Navamsa is Mesha
    nav = calculate_navamsa(0.0)
    assert nav == "Mesha"


def test_planet_calculation():
    # Test for fixed Julian Day
    jd = 2451545.0  # Jan 1, 2000 12:00 UTC
    planets = calculate_all_planets(jd)

    assert "Sun" in planets
    assert "Moon" in planets
    assert "Mars" in planets
    assert "Jupiter" in planets
    assert "Rahu" in planets
    assert "Ketu" in planets
    assert len(planets) == 9

    # Check Ketu is 180 degrees from Rahu
    diff = abs(planets["Ketu"] - planets["Rahu"]) % 360.0
    assert abs(diff - 180.0) < 0.001


def test_lagna_calculation():
    jd = 2451545.0
    asc_deg, lagna_sign = calculate_lagna(jd, 18.5204, 73.8567)
    assert 0.0 <= asc_deg < 360.0
    assert isinstance(lagna_sign, str)


def test_dasha_calculation():
    moon_lon = 10.0  # Ashwini -> Ketu Dasha
    nak = "Ashwini"
    lord, balance = calculate_mahadasha(moon_lon, nak)
    assert lord == "Ketu"
    assert balance > 0.0

    timeline = generate_dasha_timeline(lord, balance)
    assert len(timeline) >= 9
    assert timeline[0]["lord"] == "Ketu"

    antardashas = generate_antardasha("Jupiter")
    assert len(antardashas) == 9
    assert antardashas[0]["lord"] == "Jupiter"


def test_kundali_orchestrator():
    # Year: 1995, Month: 5, Day: 15, Hour: 14, Minute: 30, City: Pune
    res = calculate_kundali(1995, 5, 15, 14, 30, 18.5204, 73.8567)

    assert "lagna" in res
    assert "planets" in res
    assert len(res["planets"]) == 9
    assert "houses" in res
    assert "d9_houses" in res
    assert "scores" in res
    assert "yogas" in res
    assert "doshas" in res
    assert "tithi_name" in res
    assert "nakshatra" in res


def test_panchang_engine():
    panchang = get_full_panchang("Pune")
    assert panchang["city"] == "Pune"
    assert "tithi" in panchang
    assert "nakshatra" in panchang
    assert "yoga" in panchang
    assert "karana" in panchang
    assert "sunrise" in panchang
    assert "rahu_kaal" in panchang


def test_horoscope_engine():
    horoscope = generate_horoscope("aries")
    assert horoscope["sign"] == "Aries"
    assert "scores" in horoscope
    assert "lucky_number" in horoscope
    assert "mantra" in horoscope

    all_horoscopes = generate_all_horoscopes()
    assert len(all_horoscopes) == 12
    assert "leo" in all_horoscopes


def test_life_domains_analysis():
    chart = calculate_kundali(1998, 8, 20, 10, 15, 18.5204, 73.8567)
    domains = analyse_all_domains(chart)

    assert "domains" in domains
    d_map = domains["domains"]
    
    # Priority: Children / Progeny
    assert "children" in d_map
    assert "domain" in d_map["children"]
    assert 0 <= d_map["children"]["score"] <= 100

    # Remaining 9 domains
    assert "marriage" in d_map
    assert "career" in d_map
    assert "wealth" in d_map
    assert "health" in d_map
    assert "education" in d_map
    assert "property" in d_map
    assert "challenges" in d_map
    assert "travel" in d_map
    assert "spirituality" in d_map

    # Ensure all 10 domains are present
    assert len(d_map) == 10


def test_full_chart_generator():
    chart = generate_full_chart(1992, 11, 4, 8.5, 18.5204, 73.8567)
    assert "basic_details" in chart
    assert "planets_by_house" in chart
    assert "marriage_prediction" in chart
    assert "career_prediction" in chart


def test_festival_engine():
    from datetime import datetime
    from modules.panchang.festival import (
        get_today_festivals,
        get_upcoming_festivals,
        get_day_festivals,
    )


    # 1. Today's festivals
    today_fests = get_today_festivals()
    assert isinstance(today_fests, list)
    assert len(today_fests) >= 1
    assert "name" in today_fests[0]
    assert today_fests[0]["is_today"] is True

    # 2. Upcoming festivals (next 60 days)
    upcoming = get_upcoming_festivals(limit=14)
    assert len(upcoming) >= 1
    festival_names = [f["name"] for f in upcoming]

    # Verify no false cross-month contaminations
    # Maha Shivaratri is in Magha/Phalguna (March) -> should NOT be in Autumn
    assert "Maha Shivaratri" not in festival_names

    # 3. Check specific known astronomical date: Sharad Navratri on Oct 11, 2026
    dt_navratri = datetime(2026, 10, 11)
    fests_navratri = get_day_festivals(dt_navratri)
    assert any("Navratri" in f["name"] for f in fests_navratri)

    # 4. Check Diwali on Nov 8, 2026
    dt_diwali = datetime(2026, 11, 8)
    fests_diwali = get_day_festivals(dt_diwali)
    assert any("Diwali" in f["name"] for f in fests_diwali)

