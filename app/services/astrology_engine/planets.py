"""Swiss Ephemeris precision planetary calculations."""

import swisseph as swe

PLANETS_MAP = {
    "Sun": swe.SUN,
    "Moon": swe.MOON,
    "Mars": swe.MARS,
    "Mercury": swe.MERCURY,
    "Jupiter": swe.JUPITER,
    "Venus": swe.VENUS,
    "Saturn": swe.SATURN,
    "Rahu": swe.MEAN_NODE,
    "Ketu": swe.MEAN_NODE,
}


def calculate_all_planets(jd: float) -> dict[str, float]:
    """
    Calculate Sidereal (Lahiri) longitudes for all 9 Vedic planets.
    Returns: dict mapping planet name -> longitude degree (0-360).
    """
    swe.set_sid_mode(swe.SIDM_LAHIRI)
    flags = swe.FLG_SWIEPH | swe.FLG_SIDEREAL | swe.FLG_SPEED

    positions = {}
    rahu_lon = 0.0

    for name, code in PLANETS_MAP.items():
        if name == "Ketu":
            continue
        result = swe.calc_ut(jd, code, flags)
        lon = result[0][0] % 360.0
        positions[name] = lon
        if name == "Rahu":
            rahu_lon = lon

    # Ketu is exactly 180 degrees from Rahu
    positions["Ketu"] = (rahu_lon + 180.0) % 360.0

    return positions


def calculate_planets_with_speed(jd: float) -> list[dict]:
    """
    Calculate detailed planetary positions including speed, sign, degree, and retrograde status.
    """
    swe.set_sid_mode(swe.SIDM_LAHIRI)
    flags = swe.FLG_SWIEPH | swe.FLG_SIDEREAL | swe.FLG_SPEED

    planet_list = [
        ("Sun", swe.SUN),
        ("Moon", swe.MOON),
        ("Mars", swe.MARS),
        ("Mercury", swe.MERCURY),
        ("Jupiter", swe.JUPITER),
        ("Venus", swe.VENUS),
        ("Saturn", swe.SATURN),
        ("Rahu", swe.MEAN_NODE),
    ]

    results = []
    rahu_raw = 0.0

    for name, code in planet_list:
        data = swe.calc_ut(jd, code, flags)
        lon = data[0][0] % 360.0
        speed = data[0][3]

        if name == "Rahu":
            rahu_raw = lon

        results.append({
            "name": name,
            "longitude": lon,
            "speed": speed,
            "retrograde": speed < 0 or name in ("Rahu", "Ketu"),
        })

    # Add Ketu
    ketu_lon = (rahu_raw + 180.0) % 360.0
    results.append({
        "name": "Ketu",
        "longitude": ketu_lon,
        "speed": -0.05,
        "retrograde": True,
    })

    return results
