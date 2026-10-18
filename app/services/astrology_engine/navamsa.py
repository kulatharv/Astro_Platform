"""Navamsa (D9) Divisional Chart calculations."""

from .zodiac import SIGNS_SK

# 9 Navamsa parts per sign (3°20' each)
NAVAMSA_START = {
    # Fire signs (Mesha, Simha, Dhanu) start from Mesha (0)
    0: 0, 4: 0, 8: 0,
    # Earth signs (Vrishabha, Kanya, Makara) start from Makara (9)
    1: 9, 5: 9, 9: 9,
    # Air signs (Mithuna, Tula, Kumbha) start from Tula (6)
    2: 6, 6: 6, 10: 6,
    # Water signs (Karka, Vrischika, Meena) start from Karka (3)
    3: 3, 7: 3, 11: 3,
}

PADA_DEG = 30.0 / 9.0  # 3.3333333333333335 degrees


def calculate_navamsa(longitude: float) -> str:
    """
    Calculate the D9 Navamsa sign name for a given absolute longitude degree (0-360).
    """
    norm_deg = longitude % 360.0
    sign_idx = int(norm_deg / 30.0)
    deg_in_sign = norm_deg % 30.0

    pada = int(deg_in_sign / PADA_DEG)
    start_sign = NAVAMSA_START[sign_idx]
    nav_idx = (start_sign + pada) % 12

    return SIGNS_SK[nav_idx]


def calculate_navamsa_sign(longitude: float) -> str:
    """Alias for calculate_navamsa."""
    return calculate_navamsa(longitude)
