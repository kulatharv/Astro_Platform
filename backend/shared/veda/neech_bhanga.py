"""Neech Bhanga (Debilitation Cancellation) Engine (Pure Shared Library)."""

from .strength import DEBILITATION
from .zodiac import SIGN_LORDS

NEECH_BHANGA_EXALT_LORDS = {
    "Sun": "Venus",       # Venus rules Tula (Sun's exaltation sign in Mesha ruled by Mars, but exaltation lord for sign)
    "Moon": "Mars",       # Mars rules Makara (Moon exaltation in Vrishabha)
    "Mars": "Moon",       # Moon rules Karka
    "Mercury": "Mercury", # Mercury rules Kanya
    "Jupiter": "Moon",    # Moon rules Karka
    "Venus": "Jupiter",   # Jupiter rules Meena
    "Saturn": "Venus",    # Venus rules Tula
}


def is_neech_bhanga(name: str, sign: str, planet_map: dict) -> bool:
    """
    True if the planet's debilitation is cancelled according to classical rules:
    1. The debilitated planet is Retrograde
    2. Lord of debilitation sign is in Kendra from Lagna or Moon
    3. Exaltation lord of the sign is in Kendra from Lagna or Moon
    """
    if DEBILITATION.get(name) != sign:
        return False

    # Condition 1: Retrograde
    if planet_map.get(name, {}).get("retrograde"):
        return True

    moon_h = planet_map.get("Moon", {}).get("house", 0)

    def is_kendra(h: int) -> bool:
        if h in (1, 4, 7, 10):
            return True
        if moon_h > 0 and ((h - moon_h) % 12 + 1) in (1, 4, 7, 10):
            return True
        return False

    # Condition 2: Dispositor in Kendra from Lagna or Moon
    dispositor = SIGN_LORDS.get(sign)
    if dispositor:
        disp_house = planet_map.get(dispositor, {}).get("house", 0)
        if is_kendra(disp_house):
            return True

    # Condition 3: Exaltation lord in Kendra from Lagna or Moon
    exalt_lord = NEECH_BHANGA_EXALT_LORDS.get(name)
    if exalt_lord:
        el_house = planet_map.get(exalt_lord, {}).get("house", 0)
        if is_kendra(el_house):
            return True

    return False
