"""Future planetary transit forecast engine."""

import swisseph as swe
from datetime import datetime, timedelta
from typing import Dict, Any, List
from shared.veda.zodiac import degree_to_sign, SIGNS
from modules.kundali.houses import assign_house
from shared.cache.redis_client import CacheService
from shared.cache.keys import compute_input_hash

PLANET_CODES = {
    "Jupiter": swe.JUPITER,
    "Saturn": swe.SATURN,
    "Rahu": swe.TRUE_NODE,
}


def compute_transit_aspects(planet: str, house_from_lagna: int) -> List[int]:
    """Compute houses aspected by a transit planet using classical Parashari rules."""
    aspects = [(house_from_lagna + 6) % 12 or 12]  # 7th aspect for all planets

    if planet == "Jupiter":
        aspects.append((house_from_lagna + 4) % 12 or 12)  # 5th aspect
        aspects.append((house_from_lagna + 8) % 12 or 12)  # 9th aspect
    elif planet == "Saturn":
        aspects.append((house_from_lagna + 2) % 12 or 12)  # 3rd aspect
        aspects.append((house_from_lagna + 9) % 12 or 12)  # 10th aspect
    elif planet in ("Mars",):
        aspects.append((house_from_lagna + 3) % 12 or 12)  # 4th aspect
        aspects.append((house_from_lagna + 7) % 12 or 12)  # 8th aspect

    return sorted(list(set(aspects)))


def is_sade_sati_active(saturn_sign: str, natal_moon_sign: str) -> Dict[str, Any]:
    """Determine Sade Sati status and phase given transit Saturn sign and natal Moon sign."""
    if saturn_sign not in SIGNS or natal_moon_sign not in SIGNS:
        return {"active": False, "phase": "None"}

    moon_idx = SIGNS.index(natal_moon_sign)
    saturn_idx = SIGNS.index(saturn_sign)

    diff = (saturn_idx - moon_idx) % 12

    if diff == 11:
        return {"active": True, "phase": "Rising (12th from Moon)"}
    elif diff == 0:
        return {"active": True, "phase": "Peak (over Moon)"}
    elif diff == 1:
        return {"active": True, "phase": "Setting (2nd from Moon)"}

    return {"active": False, "phase": "None"}


def compute_ingress_windows(chart: dict, planet: str, start_date: datetime, num_years: int = 15) -> List[dict]:
    """Compute planetary sign ingress windows with 1-month granularity over a date range."""
    lagna = chart.get("basic_details", {}).get("lagna", "Mesha")
    swe.set_sid_mode(swe.SIDM_LAHIRI)
    flags = swe.FLG_SWIEPH | swe.FLG_SIDEREAL

    code = PLANET_CODES.get(planet, swe.JUPITER)

    windows = []
    current_window = None

    total_months = num_years * 12
    for m in range(total_months):
        # Sample on 1st of each month
        dt = start_date + timedelta(days=m * 30.4375)
        jd = swe.julday(dt.year, dt.month, dt.day, 0.0)

        raw_pos = swe.calc_ut(jd, code, flags)[0][0]
        if planet == "Ketu":
            raw_pos = (raw_pos + 180.0) % 360.0
        else:
            raw_pos = raw_pos % 360.0

        sign, _ = degree_to_sign(raw_pos)
        house = assign_house(sign, lagna)
        aspects = compute_transit_aspects(planet, house)

        if not current_window:
            current_window = {
                "planet": planet,
                "sign": sign,
                "house": house,
                "aspects": aspects,
                "start": dt.strftime("%Y-%m-%d"),
                "end": dt.strftime("%Y-%m-%d"),
            }
        elif current_window["sign"] == sign:
            current_window["end"] = dt.strftime("%Y-%m-%d")
        else:
            windows.append(current_window)
            current_window = {
                "planet": planet,
                "sign": sign,
                "house": house,
                "aspects": aspects,
                "start": dt.strftime("%Y-%m-%d"),
                "end": dt.strftime("%Y-%m-%d"),
            }

    if current_window:
        windows.append(current_window)

    return windows


def compute_transit_forecast(chart: dict, start_date: datetime | None = None, num_years: int = 15) -> Dict[str, Any]:
    """
    Compute structured 15-year Gochara transit forecast with 90-day caching.
    """
    start_dt = start_date or datetime.utcnow()
    input_hash = compute_input_hash(chart)
    as_of_ym = start_dt.strftime("%Y-%m")
    cache_key = f"transit_forecast:{input_hash}:{as_of_ym}:{num_years}"

    cached = CacheService.get(cache_key)
    if cached:
        return cached

    jup_windows = compute_ingress_windows(chart, "Jupiter", start_dt, num_years)
    sat_windows = compute_ingress_windows(chart, "Saturn", start_dt, num_years)
    rahu_windows = compute_ingress_windows(chart, "Rahu", start_dt, num_years)

    natal_moon = chart.get("basic_details", {}).get("moon_sign", "Mesha")

    # Sade sati timeline
    sade_sati_windows = []
    for w in sat_windows:
        ss_info = is_sade_sati_active(w["sign"], natal_moon)
        if ss_info["active"]:
            sade_sati_windows.append({
                "start": w["start"],
                "end": w["end"],
                "saturn_sign": w["sign"],
                "phase": ss_info["phase"],
            })

    forecast = {
        "as_of": start_dt.strftime("%Y-%m-%d"),
        "num_years": num_years,
        "jupiter_ingress": jup_windows,
        "saturn_ingress": sat_windows,
        "rahu_ingress": rahu_windows,
        "sade_sati_windows": sade_sati_windows,
    }

    CacheService.set(cache_key, forecast, ttl=7776000)  # 90 days
    return forecast
