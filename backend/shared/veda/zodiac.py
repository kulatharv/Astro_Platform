

"""Zodiac signs and degree conversion utilities (Pure Shared Library)."""

SIGNS_SK = [
    "Mesha", "Vrishabha", "Mithuna", "Karka",
    "Simha", "Kanya", "Tula", "Vrischika",
    "Dhanu", "Makara", "Kumbha", "Meena"
]

SIGNS_EN = [
    "Aries", "Taurus", "Gemini", "Cancer",
    "Leo", "Virgo", "Libra", "Scorpio",
    "Sagittarius", "Capricorn", "Aquarius", "Pisces"
]

SIGNS = SIGNS_SK

SIGN_LORDS = {
    "Mesha": "Mars", "Vrishabha": "Venus", "Mithuna": "Mercury", "Karka": "Moon",
    "Simha": "Sun", "Kanya": "Mercury", "Tula": "Venus", "Vrischika": "Mars",
    "Dhanu": "Jupiter", "Makara": "Saturn", "Kumbha": "Saturn", "Meena": "Jupiter"
}

ELEMENTS = [
    "Fire", "Earth", "Air", "Water",
    "Fire", "Earth", "Air", "Water",
    "Fire", "Earth", "Air", "Water"
]

MODALITIES = [
    "Cardinal", "Fixed", "Mutable", "Cardinal",
    "Fixed", "Mutable", "Cardinal", "Fixed",
    "Mutable", "Cardinal", "Fixed", "Mutable"
]


def degree_to_sign(degree: float) -> tuple[str, float]:
    """Convert an absolute degree (0-360) to (sign_name, degree_in_sign)."""
    norm_deg = degree % 360
    sign_index = int(norm_deg / 30)
    sign_degree = norm_deg % 30
    return SIGNS_SK[sign_index], round(sign_degree, 4)


def to_dms(degrees: float) -> str:
    """Format decimal degrees into a human-readable degree, minute, second string."""
    deg = int(degrees)
    minute_float = (degrees - deg) * 60
    minute = int(minute_float)
    second = int((minute_float - minute) * 60)
    return f"{deg}° {minute:02d}' {second:02d}\""
