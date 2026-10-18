"""Real-time planetary transits engine."""

import swisseph as swe
from shared.veda.zodiac import degree_to_sign
from modules.kundali.houses import assign_house


def calculate_transits(chart: dict, current_year: int, current_month: int, current_day: int) -> dict:
    """Calculate current transit positions of planets relative to natal Lagna."""
    lagna = chart.get("basic_details", {}).get("lagna", "Mesha")
    swe.set_sid_mode(swe.SIDM_LAHIRI)
    jd = swe.julday(current_year, current_month, current_day, 0.0)

    planets = {
        "Sun": swe.SUN,
        "Moon": swe.MOON,
        "Mars": swe.MARS,
        "Mercury": swe.MERCURY,
        "Jupiter": swe.JUPITER,
        "Venus": swe.VENUS,
        "Saturn": swe.SATURN,
        "Rahu": swe.TRUE_NODE,
    }

    transit_data = {}
    flags = swe.FLG_SWIEPH | swe.FLG_SIDEREAL

    for name, code in planets.items():
        pos = swe.calc_ut(jd, code, flags)[0][0] % 360.0
        sign, _ = degree_to_sign(pos)
        house = assign_house(sign, lagna)

        transit_data[name] = {
            "sign": sign,
            "house_from_lagna": house,
            "degree": round(pos % 30.0, 2),
        }

    # Add Ketu
    rahu_pos = (transit_data["Rahu"]["degree"] + 180.0) % 360.0
    ketu_sign, _ = degree_to_sign((swe.calc_ut(jd, swe.TRUE_NODE, flags)[0][0] + 180.0) % 360.0)
    transit_data["Ketu"] = {
        "sign": ketu_sign,
        "house_from_lagna": assign_house(ketu_sign, lagna),
        "degree": round(rahu_pos % 30.0, 2),
    }

    return transit_data
