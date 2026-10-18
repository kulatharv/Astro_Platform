"""Sun Combustion (Asta) Detection Engine (Pure Shared Library)."""

COMBUSTION_RANGES = {
    "Mercury": 14.0,  # 12.0 if retrograde
    "Venus": 10.0,    # 8.0 if retrograde
    "Mars": 17.0,
    "Jupiter": 11.0,
    "Saturn": 15.0,
}


def is_combust(name: str, pdata: dict, sun_data: dict) -> bool:
    """
    Check if a planet is combust (Asta) — within proximity to the Sun.
    """
    if name in ("Sun", "Rahu", "Ketu"):
        return False
    if not pdata or not sun_data:
        return False

    sun_lon = float(sun_data.get("longitude", sun_data.get("lon", 0)))
    p_lon = float(pdata.get("longitude", pdata.get("lon", 0)))

    if sun_lon == 0 and p_lon == 0:
        # Fallback to house check if longitudes missing
        sun_h = sun_data.get("house", 0)
        p_h = pdata.get("house", 0)
        return sun_h > 0 and sun_h == p_h and name in ("Mercury", "Venus")

    diff = abs(sun_lon - p_lon) % 360
    if diff > 180:
        diff = 360 - diff

    max_orb = COMBUSTION_RANGES.get(name, 12.0)
    if pdata.get("retrograde") and name in ("Mercury", "Venus"):
        max_orb -= 2.0

    return diff <= max_orb
