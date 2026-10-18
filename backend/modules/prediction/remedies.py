"""
Remedies and Timing Windows for Life Domain Analysis.
"""

from datetime import datetime
from modules.prediction.scoring import _dasha_activates, _transit_influence, _ordinal, RASHI, RASHI_EN

PLANET_REMEDIES = {
    "Sun":     dict(gem="Ruby",mantra="Om Suryaya Namah (108×)",fast="Sunday",donate="Wheat, jaggery, copper"),
    "Moon":    dict(gem="Pearl",mantra="Om Chandraya Namah (108×)",fast="Monday",donate="Rice, white items, milk"),
    "Mars":    dict(gem="Red Coral",mantra="Om Mangalaya Namah (108×)",fast="Tuesday",donate="Red lentils, copper"),
    "Mercury": dict(gem="Emerald",mantra="Om Budhaya Namah (108×)",fast="Wednesday",donate="Green gram, green cloth"),
    "Jupiter": dict(gem="Yellow Sapphire",mantra="Om Gurave Namah (108×)",fast="Thursday",donate="Yellow items, gold, turmeric"),
    "Venus":   dict(gem="Diamond / White Sapphire",mantra="Om Shukraya Namah (108×)",fast="Friday",donate="White items, perfume, silver"),
    "Saturn":  dict(gem="Blue Sapphire",mantra="Om Shanicharaya Namah (108×)",fast="Saturday",donate="Sesame, iron, black items"),
    "Rahu":    dict(gem="Hessonite (Gomed)",mantra="Om Rahave Namah (108×)",fast="Saturday",donate="Coconut, blue items"),
    "Ketu":    dict(gem="Cat's Eye (Lehsunia)",mantra="Om Ketave Namah (108×)",fast="Tuesday",donate="Multi-colored items, sesame"),
}

DOMAIN_RITUALS = {
    "marriage":    "Offer Swayamvara Parvati puja. Worship Katyayani Devi on Navratri.",
    "career":      "Chant Gayatri Mantra at sunrise. Worship Lord Surya on Sundays.",
    "wealth":      "Perform Lakshmi puja on Fridays with lotus flowers.",
    "health":      "Recite Maha Mrityunjaya Mantra 108× daily. Worship Lord Dhanvantari.",
    "children":    "Santana Gopala mantra. Worship Lord Krishna on Ashtami.",
    "education":   "Saraswati puja on Panchami. Keep books clean and respected.",
    "property":    "Vastu puja before any property purchase. Worship Bhumi Devi.",
    "challenges":  "Hanuman Chalisa on Tuesdays and Saturdays. Navagraha homa.",
    "travel":      "Worship Lord Ganesha before journey. Offer prayers at Kaal Bhairav temple.",
    "spirituality":"Daily Sandhyavandanam. Guru sewa and meditation at Brahma Muhurat.",
}


def _build_remedies(ctx: dict, weak_planets: list, domain: str) -> dict:
    """Build remedy recommendations for a domain based on weak planets."""
    remedies = []
    for p in weak_planets[:2]:
        r = PLANET_REMEDIES.get(p, {})
        if r:
            remedies.append({
                "planet":  p,
                "gem":     r["gem"],
                "mantra":  r["mantra"],
                "fast":    r["fast"],
                "donate":  r["donate"],
            })
    return {
        "planet_remedies": remedies,
        "ritual":          DOMAIN_RITUALS.get(domain, "Perform Navagraha homa for all-round benefit."),
    }


def _timing_windows(ctx: dict, key_houses: list, event_name: str) -> dict:
    currently_active = _dasha_activates(ctx, key_houses)
    transit_score    = _transit_influence(ctx, key_houses, ["Jupiter","Venus"])

    jup_house = ctx["transit_map"].get("Jupiter",{}).get("house",1)
    jup_to_key = [(h - jup_house) % 12 for h in key_houses]
    jup_years  = min(jup_to_key) if jup_to_key else 12

    if currently_active and transit_score > 0:
        window = "Current Dasha & transit alignment active"
        confidence = "High"
        icon = "🟢"
    elif currently_active:
        window = "Active Dasha period — supportive phase underway"
        confidence = "Moderate"
        icon = "🟡"
    elif jup_years <= 2:
        window = "Upcoming Jupiter transit phase"
        confidence = "Moderate"
        icon = "🟡"
    else:
        window = "Subsequent Dasha & transit cycle"
        confidence = "Reflective"
        icon = "🔵"

    sat_house = ctx["transit_map"].get("Saturn",{}).get("house",1)
    sat_to_key = min([(h - sat_house) % 12 for h in key_houses], default=12)
    if sat_to_key <= 1:
        challenge = "Saturn's current transit traditionally indicates a phase of consolidation and patience"
    elif sat_to_key <= 3:
        challenge = "Saturn's approaching transit suggests planning with extra diligence"
    else:
        challenge = "No significant Saturn transit pressure on this area"

    return {
        "best_window":        f"{icon} {window}",
        "alignment_strength": confidence,
        "challenge":          challenge,
        "dasha_active":       currently_active,
        "jupiter_years":      jup_years,
    }


_timing = _timing_windows


def _house_lord_str(ctx: dict, house: int) -> str:
    lord = ctx["house_lords"][house]
    pdata = ctx["planet_map"].get(lord, {})
    return f"{lord} in {_ordinal(pdata.get('house', 1))}H ({pdata.get('strength', 'Neutral')})"
