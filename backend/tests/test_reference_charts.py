"""
Reference Birth Chart Validation Test Suite.
Cross-validates AstroLogic's Swiss Ephemeris calculation engine against 3 famous published 
reference charts with AAA-rated birth data and published Lahiri Sidereal positions:

1. Jawaharlal Nehru (Nov 14, 1889, 23:03 LMT/IST, Allahabad)
2. Mahatma Gandhi (Oct 2, 1869, 07:12 LMT/IST, Porbandar)
3. Swami Vivekananda (Jan 12, 1863, 06:33 LMT/IST, Kolkata)
"""

import pytest
import swisseph as swe
from modules.kundali.planets import calculate_all_planets
from modules.kundali.houses import calculate_lagna
from shared.veda.nakshatra import calculate_nakshatra
from modules.kundali.dasha import calculate_mahadasha



def arcmin_diff(deg1: float, deg2: float) -> float:
    """Calculate absolute difference between two degrees in arc-minutes."""
    diff = abs(deg1 - deg2) % 360.0
    if diff > 180.0:
        diff = 360.0 - diff
    return round(diff * 60.0, 2)


# ==============================================================================
# REFERENCE CHART 1: Jawaharlal Nehru
# Published Positions (Lahiri Sidereal Ayanamsha):
# ==============================================================================
REF_NEHRU = {
    "Lagna": 112.95,   # Cancer 22°57'
    "Moon": 107.88,    # Cancer 17°53'
    "Sun": 210.26,     # Scorpio 0°16'
    "Mars": 159.98,    # Virgo 9°59'
    "Mercury": 197.14, # Libra 17°08'
    "Jupiter": 255.17, # Sagittarius 15°10'
    "Venus": 187.35,   # Libra 7°21'
    "Saturn": 130.79,  # Leo 10°47'
    "Rahu": 71.44,     # Gemini 11°26'
}


def test_reference_chart_nehru():
    """Validate Jawaharlal Nehru birth chart calculations against published reference."""
    swe.set_sid_mode(swe.SIDM_LAHIRI)
    utc_hour = 23.05 - (81.8463 / 15.0)  # Historical LMT offset pre-1905 IST
    jd = swe.julday(1889, 11, 14, utc_hour)

    planets = calculate_all_planets(jd)
    asc_deg, lagna_sign = calculate_lagna(jd, 25.4358, 81.8463)

    assert lagna_sign == "Karka"  # Cancer Lagna

    for name, ref_lon in REF_NEHRU.items():
        calc_lon = asc_deg if name == "Lagna" else planets[name]
        dev_arcmin = arcmin_diff(calc_lon, ref_lon)
        assert dev_arcmin < 30.0, f"Excessive deviation for {name} in Nehru chart: {dev_arcmin}' arc"

    moon_nak, pada = calculate_nakshatra(planets["Moon"])
    assert moon_nak == "Ashlesha"
    dasha_lord, balance = calculate_mahadasha(planets["Moon"], moon_nak)
    assert dasha_lord == "Mercury"


# ==============================================================================
# REFERENCE CHART 2: Mahatma Gandhi
# Published Positions (Lahiri Sidereal Ayanamsha):
# ==============================================================================
REF_GANDHI = {
    "Lagna": 184.62,   # Libra 4°37'
    "Moon": 117.94,    # Cancer 27°56'
    "Sun": 166.89,     # Virgo 16°53'
    "Mars": 206.37,    # Libra 26°22'
    "Mercury": 191.74, # Libra 11°44'
    "Jupiter": 28.14,  # Aries 28°08'
    "Venus": 204.40,   # Libra 24°24'
    "Saturn": 230.33,  # Scorpio 20°20'
    "Rahu": 103.66,    # Cancer 13°40'
}


def test_reference_chart_gandhi():
    """Validate Mahatma Gandhi birth chart calculations against published reference."""
    swe.set_sid_mode(swe.SIDM_LAHIRI)
    utc_hour = 7.2 - (69.6293 / 15.0)  # Historical LMT offset pre-1905 IST
    jd = swe.julday(1869, 10, 2, utc_hour)

    planets = calculate_all_planets(jd)
    asc_deg, lagna_sign = calculate_lagna(jd, 21.6417, 69.6293)

    assert lagna_sign == "Tula"  # Libra Lagna

    for name, ref_lon in REF_GANDHI.items():
        calc_lon = asc_deg if name == "Lagna" else planets[name]
        dev_arcmin = arcmin_diff(calc_lon, ref_lon)
        assert dev_arcmin < 30.0, f"Excessive deviation for {name} in Gandhi chart: {dev_arcmin}' arc"

    moon_nak, pada = calculate_nakshatra(planets["Moon"])
    assert moon_nak == "Ashlesha"
    dasha_lord, balance = calculate_mahadasha(planets["Moon"], moon_nak)
    assert dasha_lord == "Mercury"


# ==============================================================================
# REFERENCE CHART 3: Swami Vivekananda
# Published Positions (Lahiri Sidereal Ayanamsha):
# ==============================================================================
REF_VIVEKANANDA = {
    "Lagna": 266.03,   # Sagittarius 26°02'
    "Moon": 167.45,    # Virgo 17°27'
    "Sun": 269.42,     # Sagittarius 29°25'
    "Mars": 6.32,      # Aries 6°19'
    "Mercury": 281.77, # Capricorn 11°46'
    "Jupiter": 184.01, # Libra 4°01'
    "Venus": 277.10,   # Capricorn 7°06'
    "Saturn": 163.57,  # Virgo 13°34'
    "Rahu": 233.50,    # Scorpio 23°30'
}


def test_reference_chart_vivekananda():
    """Validate Swami Vivekananda birth chart calculations against published reference."""
    swe.set_sid_mode(swe.SIDM_LAHIRI)
    utc_hour = 6.55 - (88.3639 / 15.0)  # Historical LMT offset pre-1905 IST
    jd = swe.julday(1863, 1, 12, utc_hour)

    planets = calculate_all_planets(jd)
    asc_deg, lagna_sign = calculate_lagna(jd, 22.5726, 88.3639)

    assert lagna_sign == "Dhanu"  # Sagittarius Lagna

    for name, ref_lon in REF_VIVEKANANDA.items():
        calc_lon = asc_deg if name == "Lagna" else planets[name]
        dev_arcmin = arcmin_diff(calc_lon, ref_lon)
        assert dev_arcmin < 30.0, f"Excessive deviation for {name} in Vivekananda chart: {dev_arcmin}' arc"

    moon_nak, pada = calculate_nakshatra(planets["Moon"])
    assert moon_nak == "Hasta"
    dasha_lord, balance = calculate_mahadasha(planets["Moon"], moon_nak)
    assert dasha_lord == "Moon"
