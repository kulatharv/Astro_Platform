"""
Shared Pure Vedic Astrology Calculation Library (shared.veda).
Stateless, pure mathematical and astrological calculations — zero DB, zero Redis, zero side effects.
"""

from .zodiac import SIGNS_SK, SIGNS_EN, SIGN_LORDS, degree_to_sign, to_dms
from .nakshatra import NAKSHATRAS, NAKSHATRA_LORDS, calculate_nakshatra, get_nakshatra_lord
from .aspects import calculate_vedic_aspects
from .strength import EXALTATION, DEBILITATION, OWN_SIGNS, FRIENDLY_SIGNS, planet_strength_label, calculate_weighted_strength
from .doshas import evaluate_mangal_dosha, evaluate_pitru_dosha, calculate_doshas
from .yogas import calculate_yogas, detect_advanced_yogas
from .dignity import PLANET_FRIENDS, MOOLATRIKONA, PLANET_ENEMIES, get_naisargika_dignity, get_positional_strength
from .combustion import COMBUSTION_RANGES, is_combust
from .neech_bhanga import is_neech_bhanga
from .constants import PUBLIC_PATH_PREFIXES, USER_ROLE, ADMIN_ROLE, ZODIAC_SIGNS, RASHI_NAMES

__all__ = [
    "SIGNS_SK", "SIGNS_EN", "SIGN_LORDS", "degree_to_sign", "to_dms",
    "NAKSHATRAS", "NAKSHATRA_LORDS", "calculate_nakshatra", "get_nakshatra_lord",
    "calculate_vedic_aspects", "EXALTATION", "DEBILITATION", "OWN_SIGNS", "FRIENDLY_SIGNS",
    "planet_strength_label", "calculate_weighted_strength",
    "evaluate_mangal_dosha", "evaluate_pitru_dosha", "calculate_doshas",
    "calculate_yogas", "detect_advanced_yogas",
    "PLANET_FRIENDS", "MOOLATRIKONA", "PLANET_ENEMIES", "get_naisargika_dignity", "get_positional_strength",
    "COMBUSTION_RANGES", "is_combust", "is_neech_bhanga",
    "PUBLIC_PATH_PREFIXES", "USER_ROLE", "ADMIN_ROLE", "ZODIAC_SIGNS", "RASHI_NAMES"
]
