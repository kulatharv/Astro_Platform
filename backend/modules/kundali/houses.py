"""Lagna (Ascendant) and house calculation engine."""

import swisseph as swe
from shared.veda.zodiac import SIGNS_SK, degree_to_sign


def calculate_lagna(jd: float, latitude: float = 18.5204, longitude: float = 73.8567) -> tuple[float, str]:
    """
    Calculate Lagna (Ascendant) longitude and sign name.
    Returns: (lagna_degree_360, lagna_sign_name).
    """
    swe.set_sid_mode(swe.SIDM_LAHIRI)
    flags = swe.FLG_SWIEPH | swe.FLG_SIDEREAL

    cusps, ascmc = swe.houses_ex(
        jd,
        latitude,
        longitude,
        b'W',  # Whole sign
        flags,
    )

    asc_degree = ascmc[0] % 360.0
    sign, _ = degree_to_sign(asc_degree)

    return asc_degree, sign


def assign_house(planet_sign: str, lagna_sign: str) -> int:
    """
    Determine the house number (1-12) of a planet using the Vedic Whole Sign system.
    """
    lagna_index = SIGNS_SK.index(lagna_sign) if lagna_sign in SIGNS_SK else 0
    planet_index = SIGNS_SK.index(planet_sign) if planet_sign in SIGNS_SK else 0

    return ((planet_index - lagna_index) % 12) + 1


def assign_bhava_house(jd: float, latitude: float, longitude: float, planet_longitude: float) -> int:
    """
    Calculate Placidus / Sripati Bhava Chalit house (1-12) for a given planet longitude.
    """
    swe.set_sid_mode(swe.SIDM_LAHIRI)
    flags = swe.FLG_SWIEPH | swe.FLG_SIDEREAL

    cusps, ascmc = swe.houses_ex(
        jd,
        latitude,
        longitude,
        b'P',  # Placidus / Bhava
        flags,
    )

    cusp_list = list(cusps)
    if len(cusp_list) == 13:
        cusp_list = cusp_list[1:]

    if len(cusp_list) != 12:
        return 1

    pl = planet_longitude % 360.0

    for i in range(12):
        start = cusp_list[i] % 360.0
        end = cusp_list[(i + 1) % 12] % 360.0

        if start < end:
            if start <= pl < end:
                return i + 1
        else:  # Wraps around 360/0
            if pl >= start or pl < end:
                return i + 1

    return 1
