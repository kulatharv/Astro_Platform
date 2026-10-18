"""Event timing and Dasha activation engine."""

from .zodiac import SIGNS_SK, SIGN_LORDS


def evaluate_event_trigger(chart: dict, event_type: str) -> dict:
    """
    Evaluate if current Dasha and planetary positions activate a specific life event (marriage, career, etc.).
    """
    dasha_info = chart.get("dasha", {})
    current_md = dasha_info.get("current_mahadasha", "Jupiter")
    lagna = chart.get("basic_details", {}).get("lagna", "Mesha")
    lagna_idx = SIGNS_SK.index(lagna) if lagna in SIGNS_SK else 0

    target_houses = {
        "marriage": [7, 5, 2, 11],
        "career": [10, 6, 11, 1],
        "wealth": [2, 11, 9, 1],
        "foreign": [12, 9, 3],
    }.get(event_type, [1, 5, 9])

    # Check houses ruled by current MD lord
    ruled_houses = []
    for h in range(1, 13):
        sign = SIGNS_SK[(lagna_idx + h - 1) % 12]
        if SIGN_LORDS.get(sign) == current_md:
            ruled_houses.append(h)

    # Check house placement of MD lord
    md_placement = 1
    planets_by_house = chart.get("planets_by_house", {})
    for h_str, p_list in planets_by_house.items():
        for p in p_list:
            if p.get("planet") == current_md:
                try:
                    md_placement = int(h_str)
                except ValueError:
                    md_placement = 1

    is_activated = md_placement in target_houses or any(rh in target_houses for rh in ruled_houses)

    return {
        "event": event_type,
        "mahadasha_lord": current_md,
        "activated": is_activated,
        "active_houses": [md_placement] + ruled_houses,
        "intensity": "High" if is_activated else "Moderate",
    }
