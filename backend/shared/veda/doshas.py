"""Vedic Doshas detection engine with remedies (Pure Shared Library)."""

from .zodiac import SIGNS_SK

GANDMOOL_NAKSHATRAS = {"Ashwini", "Ashlesha", "Magha", "Jyeshtha", "Mula", "Revati"}


def _get_planet_map(planets: list[dict] | dict[str, dict]) -> dict[str, dict]:
    if isinstance(planets, dict):
        return planets
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


MANGLIK_HOUSES = {1, 2, 4, 7, 8, 12}


def evaluate_mangal_dosha(planet_data: dict[str, dict] | list[dict]) -> dict:
    """
    Consolidated Mangal Dosh (Manglik) evaluator used across the system.
    Checks houses {1, 2, 4, 7, 8, 12} and classical cancellation rules:
      - Mars in own sign (Mesha, Vrischika) or exaltation (Makara)
      - Jupiter conjunct Mars (same house)
      - Jupiter aspecting Mars (5th, 7th, 9th aspect)
      - Jupiter occupying 7th house
    """
    pmap = _get_planet_map(planet_data)

    mars = pmap.get("Mars", {})
    mar_h = _house_of(pmap, "Mars")
    mars_sign = _sign_of(pmap, "Mars")

    jup = pmap.get("Jupiter", {})
    jup_h = _house_of(pmap, "Jupiter")

    raw = mar_h in MANGLIK_HOUSES

    reasons = []
    if raw:
        if mars_sign in ("Mesha", "Vrischika", "Makara"):
            reasons.append(f"Mars in own/exalted sign ({mars_sign})")
        if jup_h > 0 and mar_h > 0:
            if jup_h == mar_h:
                reasons.append("Jupiter conjunct Mars")
            elif (mar_h - jup_h) % 12 in (4, 6, 8):
                aspect_num = {4: "5th", 6: "7th", 8: "9th"}[(mar_h - jup_h) % 12]
                reasons.append(f"Jupiter {aspect_num} aspect on Mars")
        if jup_h == 7 and jup_h != mar_h:
            reasons.append("Jupiter in 7th house")

    cancelled = raw and bool(reasons)
    present = raw and not cancelled
    cancellation_reason = ", ".join(reasons) if cancelled else ""

    return {
        "raw": raw,
        "present": present,
        "cancelled": cancelled,
        "house": mar_h,
        "sign": mars_sign,
        "cancellation_reason": cancellation_reason,
    }


def evaluate_pitru_dosha(planet_data: dict[str, dict] | list[dict]) -> dict:
    """
    Consolidated Pitru Dosh evaluator used across the system.
    Checks:
      - Rahu or Ketu in 9th house
      - Sun in 9th house afflicted by Rahu, Ketu, or Saturn
      - Sun conjunct Rahu or Ketu in any house
    """
    pmap = _get_planet_map(planet_data)

    rahu_h = _house_of(pmap, "Rahu")
    ketu_h = _house_of(pmap, "Ketu")
    sun_h = _house_of(pmap, "Sun")
    sat_h = _house_of(pmap, "Saturn")

    h9_planets = [p for p, d in pmap.items() if (d.get("house") if isinstance(d, dict) else 0) == 9]

    in_9th = (rahu_h == 9 or ketu_h == 9)
    sun_in_9_afflicted = (sun_h == 9 and (rahu_h == 9 or ketu_h == 9 or sat_h == 9 or any(p in {"Rahu", "Ketu", "Saturn"} for p in h9_planets)))
    sun_conj_nodes = (sun_h > 0 and (sun_h == rahu_h or sun_h == ketu_h))

    present = bool(in_9th or sun_in_9_afflicted or sun_conj_nodes)
    reasons = []
    if in_9th:
        reasons.append("Rahu/Ketu in 9th house")
    if sun_in_9_afflicted:
        reasons.append("Sun in 9th house afflicted by malefic")
    if sun_conj_nodes and not in_9th:
        reasons.append("Sun conjunct Rahu/Ketu")

    return {
        "present": present,
        "reason": ", ".join(reasons) if present else "",
    }


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

    rahu_h = _house_of(pmap, "Rahu")
    ketu_h = _house_of(pmap, "Ketu")
    sun_h = _house_of(pmap, "Sun")
    moon_h = _house_of(pmap, "Moon")
    moon_s = _sign_of(pmap, "Moon")
    sat_s = _sign_of(pmap, "Saturn")

    # 1. Mangal Dosha (Manglik)
    eval_m = evaluate_mangal_dosha(pmap)
    manglik_raw = eval_m["raw"]
    mars_canceled = eval_m["cancelled"]
    mar_h = eval_m["house"]

    severity = "Low (Canceled)" if (manglik_raw and mars_canceled) else ("High" if mar_h in {1, 7, 8} else ("Medium" if manglik_raw else "None"))

    manglik_desc = (
        f"Mars placed in house {mar_h}. "
        + (f"Mangal Dosh is present but cancelled due to: {eval_m['cancellation_reason']}." if mars_canceled else
           "Traditionally evaluated in Vedic horoscope matching for relationship intensity and partnership harmony.")
    )

    add(
        "Mangal Dosha (Manglik)",
        manglik_raw,
        severity,
        manglik_desc,
        [
            "Recite Hanuman Chalisa or Mangal Gayatri daily",
            "Donate red lentils or sweet jaggery on Tuesdays",
            "Practice mindful communication and patience in partnerships",
            "Consult a qualified astrologer for comprehensive Koota Milan matching",
        ],
    )

    # 2. Shani Sade Sati
    moon_idx = SIGNS_SK.index(moon_s) if moon_s in SIGNS_SK else -1
    sat_idx = SIGNS_SK.index(sat_s) if sat_s in SIGNS_SK else -1
    sade = moon_idx >= 0 and sat_idx >= 0 and (sat_idx - moon_idx) % 12 in {0, 1, 11}
    add(
        "Shani Sade Sati",
        sade,
        "Moderate" if sade else "None",
        "Saturn transiting within ±1 sign of natal Moon — a traditional 7.5-year phase associated with discipline, "
        "patience, and personal restructuring. Classical Vedic texts view this as a period for inner maturity.",
        [
            "Chant 'Om Sham Shanaischaraya Namaha' 108 times on Saturdays",
            "Engage in selfless service and support community welfare",
            "Feed birds or domestic animals regularly",
            "Practice patience, daily meditation, and long-term planning",
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
        "Moderate" if ks else "None",
        "Planetary positions bounded within the Rahu-Ketu axis. Traditionally associated with focused drive; "
        "many prominent classical and modern figures carry this chart pattern successfully.",
        [
            "Practice daily meditation or Pranayama",
            "Engage in regular spiritual or charitable pursuits",
            "Worship Lord Shiva or recite Maha Mrityunjaya Mantra",
        ],
    )

    # 4. Pitru Dosha
    eval_p = evaluate_pitru_dosha(pmap)
    pitru = eval_p["present"]
    add(
        "Pitru Dosha",
        pitru,
        "Medium",
        f"Karmic ancestral debt or affliction in the 9th house of Dharma/Father. ({eval_p['reason']})" if pitru else "Karmic ancestral debt or affliction in the 9th house of Dharma/Father.",
        [
            "Perform Pitru Tarpan or Shraddha on Amavasya",
            "Feed cows and stray dogs regularly",
            "Recite Gayatri Mantra 108 times every morning",
            "Plant a sacred Peepal (Banyan) tree",
        ],
    )

    # 5. Grahan Dosha
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
