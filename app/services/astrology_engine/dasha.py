"""Vimshottari Dasha calculation engine."""

from datetime import datetime, timedelta
from .nakshatra import NAKSHATRAS, NAKSHATRA_SIZE

DASHA_SEQUENCE = [
    "Ketu", "Venus", "Sun", "Moon",
    "Mars", "Rahu", "Jupiter", "Saturn", "Mercury"
]

DASHA_YEARS = {
    "Ketu": 7,
    "Venus": 20,
    "Sun": 6,
    "Moon": 10,
    "Mars": 7,
    "Rahu": 18,
    "Jupiter": 16,
    "Saturn": 19,
    "Mercury": 17
}


def calculate_mahadasha(moon_longitude: float, nak_name: str) -> tuple[str, float]:
    """
    Calculate the starting Mahadasha lord and remaining balance years at birth.
    Returns: (lord_name, balance_years).
    """
    if nak_name in NAKSHATRAS:
        nak_index = NAKSHATRAS.index(nak_name)
    else:
        nak_index = int((moon_longitude % 360.0) / NAKSHATRA_SIZE) % 27

    lord = DASHA_SEQUENCE[nak_index % 9]
    full_years = DASHA_YEARS[lord]

    remainder = (moon_longitude % 360.0) % NAKSHATRA_SIZE
    balance_fraction = (NAKSHATRA_SIZE - remainder) / NAKSHATRA_SIZE
    balance_years = balance_fraction * full_years

    return lord, round(balance_years, 2)


def generate_dasha_timeline(start_lord: str, balance_years: float) -> list[dict]:
    """Generate the full 120-year Vimshottari Mahadasha progression timeline."""
    timeline = []
    current_index = DASHA_SEQUENCE.index(start_lord) if start_lord in DASHA_SEQUENCE else 0

    timeline.append({
        "lord": start_lord,
        "years": round(balance_years, 2)
    })

    total_years = balance_years
    next_index = (current_index + 1) % 9

    while total_years < 120:
        lord = DASHA_SEQUENCE[next_index]
        years = DASHA_YEARS[lord]

        timeline.append({
            "lord": lord,
            "years": years
        })

        total_years += years
        next_index = (next_index + 1) % 9

    return timeline


def generate_antardasha(mahadasha_lord: str) -> list[dict]:
    """Calculate the 9 Antardasha periods for a given Mahadasha lord."""
    antardashas = []
    start_idx = DASHA_SEQUENCE.index(mahadasha_lord) if mahadasha_lord in DASHA_SEQUENCE else 0
    md_years = DASHA_YEARS.get(mahadasha_lord, 10)

    for i in range(9):
        lord = DASHA_SEQUENCE[(start_idx + i) % 9]
        ad_years = (md_years * DASHA_YEARS[lord]) / 120.0
        antardashas.append({
            "lord": lord,
            "years": round(ad_years, 2)
        })

    return antardashas


def generate_dasha_calendar(birth_datetime: datetime, timeline: list[dict]) -> list[dict]:
    """Calculate concrete start and end dates for Mahadashas based on birth datetime."""
    calendar = []
    current_date = birth_datetime

    for period in timeline:
        duration_days = period["years"] * 365.25
        end_date = current_date + timedelta(days=duration_days)
        calendar.append({
            "lord": period["lord"],
            "start": current_date.strftime("%Y-%m-%d"),
            "end": end_date.strftime("%Y-%m-%d"),
            "years": period["years"],
        })
        current_date = end_date

    return calendar
