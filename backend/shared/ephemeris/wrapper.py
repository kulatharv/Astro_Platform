"""Thin wrapper over pyswisseph (Swiss Ephemeris) for planetary math."""

import swisseph as swe

# Set Lahiri Ayanamsa by default
swe.set_ephe_path('.')
swe.set_sid_mode(swe.SIDM_LAHIRI)


def calc_ut(julian_day: float, body: int, flags: int = swe.FLG_SIDEREAL) -> tuple:
    """Calculate sidereal longitude and speed for a celestial body."""
    return swe.calc_ut(julian_day, body, flags)


def get_ayanamsa_ut(julian_day: float) -> float:
    """Return Lahiri ayanamsa value for a given Julian Day."""
    return swe.get_ayanamsa_ut(julian_day)


def julday(year: int, month: int, day: int, hour: float) -> float:
    """Convert UT date and decimal hour to Julian Day number."""
    return swe.julday(year, month, day, hour)


def houses(julian_day: float, lat: float, lon: float, hsys: bytes = b'E') -> tuple:
    """Calculate house cusps and Ascendant/MC (Equal system b'E' or Placidus b'P')."""
    return swe.houses(julian_day, lat, lon, hsys)
