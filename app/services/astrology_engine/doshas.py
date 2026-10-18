"""Vedic Doshas detection engine with remedies."""

from .zodiac import SIGNS_SK

GANDMOOL_NAKSHATRAS = {"Ashwini", "Ashlesha", "Magha", "Jyeshtha", "Mula", "Revati"}


def _get_planet_map(planets: list[dict]) -> dict[str, dict]:
    return {p.get("name") or p.get("planet"): p for p in planets if p.get("name") or p.get("planet")}


def _house_of(pmap: dict, name: str) -> int:
    p = pmap.get(name, {})
    h = p.get("house", 0)
    if isinstance(h, int):
        return h
    try:
        return int(str(h).split("/")[0])
    except (ValueError, TypeError):
        return 0


def _sign_of(pmap: dict, name: str) -> str:
    return pmap.get(name, {}).get("sign", "")


def calculate_doshas(planets: list[dict], lagna_sign: str, houses: dict) -> list[dict]:
    """Detect and score major astrological doshas with authentic Vedic remedies."""
    pmap = _get_planet_map(planets)
    doshas = []

    def add(name: str, present: bool, severity: str, desc: str, remedies: list[str]):
        doshas.append({
            "name": name,
            "present": bool(present),
            "severity": severity if present else "None",
            "description": desc,
            "remedies": remedies if present else [],
        })

    mar_h = _house_of(pmap, "Mars")
    rahu_h = _house_of(pmap, "Rahu")
    ketu_h = _house_of(pmap, "Ketu")
    sun_h = _house_of(pmap, "Sun")
    moon_h = _house_of(pmap, "Moon")
    moon_s = _sign_of(pmap, "Moon")
    sat_s = _sign_of(pmap, "Saturn")

    # 1. Mangal Dosha (Manglik)
    manglik = mar_h in {1, 2, 4, 7, 8, 12}
    add(
        "Mangal Dosha (Manglik)",
        manglik,
        "High" if mar_h in {1, 7, 8} else "Medium",
        f"Mars placed in house {mar_h}. Indicates strong martial passion requiring balanced partnership.",
        [
            "Recite Hanuman Chalisa daily",
            "Donate red lentils on Tuesdays",
            "Wear Red Coral after astrological gemstone consultation",
            "Kumbh Vivah ritual before marriage if applicable",
        ],
    )

    # 2. Shani Sade Sati
    moon_idx = SIGNS_SK.index(moon_s) if moon_s in SIGNS_SK else -1
    sat_idx = SIGNS_SK.index(sat_s) if sat_s in SIGNS_SK else -1
    sade = moon_idx >= 0 and sat_idx >= 0 and (sat_idx - moon_idx) % 12 in {0, 1, 11}
    add(
        "Shani Sade Sati",
        sade,
        "High",
        "Saturn transiting within ±1 sign of natal Moon — 7.5-year karmic refining phase.",
        [
            "Chant 'Om Sham Shanaischaraya Namaha' 108 times on Saturdays",
            "Donate black sesame seeds and mustard oil",
            "Feed crows and serve elderly or disabled individuals",
            "Recite Dasharatha Shani Stotra",
        ],
    )

    # 3. Kaal Sarp Dosha
    if rahu_h and ketu_h:
        all_h = [_house_of(pmap, p) for p in ("Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn")]
        all_h = [h for h in all_h if h > 0]

        def is_between(h):
            if rahu_h < ketu_h:
                return rahu_h < h < ketu_h
            return h > rahu_h or h < ketu_h

        ks = bool(all_h) and (all(is_between(h) for h in all_h) or all(not is_between(h) for h in all_h))
    else:
        ks = False

    add(
        "Kaal Sarp Dosha",
        ks,
        "High",
        "Planetary hemisphere bounded entirely by the Rahu-Ketu axis.",
        [
            "Perform Maha Mrityunjaya Japa",
            "Offer milk to Shiva Linga on Mondays",
            "Kaal Sarp Shanti Puja at Trimbakeshwar or Kalahasti",
            "Keep a silver snake figure or wear Nag Rahu Yantra",
        ],
    )

    # 4. Pitru Dosha (Affliction in 9th house or Sun afflicted by Rahu/Ketu/Saturn)
    h9_planets = [p for p in pmap if _house_of(pmap, p) == 9]
    pitru = (sun_h == 9 and any(p in {"Rahu", "Ketu", "Saturn"} for p in h9_planets)) or ("Rahu" in h9_planets) or ("Ketu" in h9_planets)
    add(
        "Pitru Dosha",
        pitru,
        "Medium",
        "Karmic ancestral debt or affliction in the 9th house of Dharma/Father.",
        [
            "Perform Pitru Tarpan or Shraddha on Amavasya",
            "Feed cows and stray dogs regularly",
            "Recite Gayatri Mantra 108 times every morning",
            "Plant a sacred Peepal (Banyan) tree",
        ],
    )

    # 5. Grahan Dosha (Eclipsed Sun/Moon with Rahu/Ketu)
    grahan = bool(
        (sun_h == rahu_h and sun_h != 0) or (sun_h == ketu_h and sun_h != 0) or
        (moon_h == rahu_h and moon_h != 0) or (moon_h == ketu_h and moon_h != 0)
    )
    add(
        "Grahan Dosha",
        grahan,
        "High",
        "Sun or Moon conjunct Rahu/Ketu — indicates emotional or identity sensitivity.",
        [
            "Worship Lord Surya at sunrise offering water with copper vessel",
            "Chant Chandra Gayatri mantra during full moon",
            "Donate white food (rice, milk) on Mondays and wheat on Sundays",
        ],
    )

    # 6. Gandmool Dosha
    moon_nak = pmap.get("Moon", {}).get("nakshatra", "")
    gand = moon_nak in GANDMOOL_NAKSHATRAS
    add(
        "Gandmool Dosha",
        gand,
        "Medium",
        f"Moon situated in {moon_nak} Gandmool nakshatra at birth.",
        [
            "Perform Gandmool Shanti ritual",
            "Worship Lord Ganesha daily",
            "Donate green moong dal or white items on Nakshatra transit days",
        ],
    )

    return doshas
