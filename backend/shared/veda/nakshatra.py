"""Nakshatra and Pada calculation utilities (Pure Shared Library)."""

NAKSHATRAS = [
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra",
    "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni",
    "Uttara Phalguni", "Hasta", "Chitra", "Swati", "Vishakha",
    "Anuradha", "Jyeshtha", "Mula", "Purva Ashadha", "Uttara Ashadha",
    "Shravana", "Dhanishta", "Shatabhisha", "Purva Bhadrapada",
    "Uttara Bhadrapada", "Revati"
]

NAKSHATRA_LORDS = [
    "Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury",
    "Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury",
    "Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury"
]

NAKSHATRA_SIZE = 360.0 / 27.0  # 13.333333333333334 degrees
PADA_SIZE = NAKSHATRA_SIZE / 4.0  # 3.3333333333333335 degrees


def calculate_nakshatra(degree: float) -> tuple[str, int]:
    """Calculate the Nakshatra name and Pada number (1-4) for a given longitude degree."""
    norm_deg = degree % 360.0
    nak_index = int(norm_deg / NAKSHATRA_SIZE) % 27
    nak_name = NAKSHATRAS[nak_index]

    rem = norm_deg % NAKSHATRA_SIZE
    pada = int(rem / PADA_SIZE) + 1
    pada = max(1, min(4, pada))

    return nak_name, pada


def get_nakshatra_pada(degree: float) -> tuple[str, int]:
    """Alias for calculate_nakshatra."""
    return calculate_nakshatra(degree)


def get_nakshatra_lord(nak_name: str) -> str:
    """Return the planetary lord of a given Nakshatra."""
    if nak_name in NAKSHATRAS:
        idx = NAKSHATRAS.index(nak_name)
        return NAKSHATRA_LORDS[idx]
    return "Ketu"
