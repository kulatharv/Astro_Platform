"""Vimshottari Dasha calculation engine."""

from datetime import datetime, timedelta
from shared.veda.nakshatra import NAKSHATRAS, NAKSHATRA_SIZE

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


DASHA_DEPTH = "PD"


def compute_pratyantardasha(md_lord: str, ad_lord: str, ad_start: datetime, ad_end: datetime) -> list[dict]:
    """Calculate the 9 Pratyantardasha (PD) sub-periods within an Antardasha."""
    pds = []
    ad_duration_days = (ad_end - ad_start).total_seconds() / 86400.0
    start_idx = DASHA_SEQUENCE.index(ad_lord) if ad_lord in DASHA_SEQUENCE else 0

    curr_start = ad_start
    for i in range(9):
        pd_lord = DASHA_SEQUENCE[(start_idx + i) % 9]
        pd_duration_days = ad_duration_days * (DASHA_YEARS[pd_lord] / 120.0)
        curr_end = curr_start + timedelta(days=pd_duration_days)

        pds.append({
            "md_lord": md_lord,
            "ad_lord": ad_lord,
            "pd_lord": pd_lord,
            "start": curr_start.strftime("%Y-%m-%d"),
            "end": curr_end.strftime("%Y-%m-%d"),
            "days": round(pd_duration_days, 1),
        })
        curr_start = curr_end

    return pds


def generate_dasha_chain(birth_datetime: datetime, timeline: list[dict], filter_start: str | None = None, filter_end: str | None = None) -> list[dict]:
    """
    Generate nested MD/AD/PD periods for chart forecast within optional filter date range.
    """
    chain = []
    curr_md_start = birth_datetime

    f_start = datetime.strptime(filter_start, "%Y-%m-%d") if filter_start else None
    f_end = datetime.strptime(filter_end, "%Y-%m-%d") if filter_end else None

    for md in timeline:
        md_lord = md["lord"]
        md_duration_days = md["years"] * 365.25
        curr_md_end = curr_md_start + timedelta(days=md_duration_days)

        # Quick boundary prune
        if f_end and curr_md_start > f_end:
            break
        if f_start and curr_md_end < f_start:
            curr_md_start = curr_md_end
            continue

        # Antardashas
        ads = generate_antardasha(md_lord)
        curr_ad_start = curr_md_start
        for ad in ads:
            ad_lord = ad["lord"]
            ad_duration_days = (md_duration_days * DASHA_YEARS[ad_lord]) / 120.0
            curr_ad_end = curr_ad_start + timedelta(days=ad_duration_days)

            if f_end and curr_ad_start > f_end:
                break
            if f_start and curr_ad_end < f_start:
                curr_ad_start = curr_ad_end
                continue

            # Pratyantardashas
            pds = compute_pratyantardasha(md_lord, ad_lord, curr_ad_start, curr_ad_end)
            for pd in pds:
                pd_s = datetime.strptime(pd["start"], "%Y-%m-%d")
                pd_e = datetime.strptime(pd["end"], "%Y-%m-%d")
                if f_start and pd_e < f_start:
                    continue
                if f_end and pd_s > f_end:
                    continue

                chain.append(pd)

            curr_ad_start = curr_ad_end

        curr_md_start = curr_md_end

    return chain
