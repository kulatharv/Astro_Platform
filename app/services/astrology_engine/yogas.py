"""Classical Vedic Astrology Yogas Detection Engine."""

from .zodiac import SIGNS_SK, SIGN_LORDS
from .strength import EXALTATION, OWN_SIGNS

KENDRA = {1, 4, 7, 10}
TRIKONA = {1, 5, 9}
DUSTHANA = {6, 8, 12}


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


def calculate_yogas(planets: list[dict], lagna_sign: str, houses: dict) -> list[dict]:
    """Detect and score classical Vedic yogas in a natal chart."""
    pmap = _get_planet_map(planets)
    yogas = []
    lagna_idx = SIGNS_SK.index(lagna_sign) if lagna_sign in SIGNS_SK else 0

    def add(name: str, desc: str, present: bool, strength: str = "Medium"):
        yogas.append({
            "name": name,
            "description": desc,
            "present": bool(present),
            "strength": strength if present else "Absent",
        })

    sun_h = _house_of(pmap, "Sun")
    moon_h = _house_of(pmap, "Moon")
    mar_h = _house_of(pmap, "Mars")
    mer_h = _house_of(pmap, "Mercury")
    jup_h = _house_of(pmap, "Jupiter")
    ven_h = _house_of(pmap, "Venus")
    sat_h = _house_of(pmap, "Saturn")

    jup_s = _sign_of(pmap, "Jupiter")
    mar_s = _sign_of(pmap, "Mars")
    mer_s = _sign_of(pmap, "Mercury")
    ven_s = _sign_of(pmap, "Venus")
    sat_s = _sign_of(pmap, "Saturn")

    # 1. Gajakesari Yoga (Jupiter in Kendra from Moon)
    gaja = bool(moon_h and jup_h and abs(jup_h - moon_h) in {0, 3, 6, 9})
    add(
        "Gajakesari Yoga",
        "Jupiter in kendra from Moon — wisdom, fame, leadership, and prosperity.",
        gaja,
        "Strong" if gaja and jup_s in OWN_SIGNS.get("Jupiter", []) else "Medium",
    )

    # 2. Pancha Mahapurusha Yogas
    mahapurusha = [
        ("Mars", mar_h, mar_s, "Ruchaka Yoga", "Mars in own/exaltation sign in kendra — courage, leadership, and authority."),
        ("Mercury", mer_h, mer_s, "Bhadra Yoga", "Mercury in own/exaltation sign in kendra — sharp intellect, commerce, and communication."),
        ("Jupiter", jup_h, jup_s, "Hamsa Yoga", "Jupiter in own/exaltation sign in kendra — spiritual wisdom, grace, and noble status."),
        ("Venus", ven_h, ven_s, "Malavya Yoga", "Venus in own/exaltation sign in kendra — luxury, artistic mastery, beauty, and prosperity."),
        ("Saturn", sat_h, sat_s, "Sasa Yoga", "Saturn in own/exaltation sign in kendra — perseverance, discipline, authority, and mass leadership."),
    ]
    for pname, ph, ps, yname, ydesc in mahapurusha:
        present = ph in KENDRA and (ps in OWN_SIGNS.get(pname, []) or EXALTATION.get(pname) == ps)
        add(yname, ydesc, present, "Strong" if present else "Absent")

    # 3. Budhaditya Yoga (Sun & Mercury Conjunction)
    add(
        "Budhaditya Yoga",
        "Sun and Mercury conjunct — analytical mind, government/academic success, and eloquence.",
        sun_h == mer_h and sun_h != 0,
        "Strong" if sun_h in KENDRA or sun_h in TRIKONA else "Medium",
    )

    # 4. Chandra-Mangala Yoga (Moon & Mars Conjunction or 7th)
    cm_present = bool((moon_h == mar_h and moon_h != 0) or (moon_h and mar_h and abs(moon_h - mar_h) == 6))
    add(
        "Chandra-Mangala Yoga",
        "Moon-Mars association — intense financial drive, commercial success, and enterprising nature.",
        cm_present,
    )

    # 5. Dharma-Karmadhipati Yoga (9th & 10th lords conjunct or exchanging houses)
    lord_9 = SIGN_LORDS.get(SIGNS_SK[(lagna_idx + 8) % 12])
    lord_10 = SIGN_LORDS.get(SIGNS_SK[(lagna_idx + 9) % 12])
    h9 = _house_of(pmap, lord_9) if lord_9 else 0
    h10 = _house_of(pmap, lord_10) if lord_10 else 0
    dkd = bool(lord_9 and lord_10 and lord_9 != lord_10 and ((h9 == h10 and h9 != 0) or (h9 == 10 and h10 == 9)))
    add(
        "Dharma-Karmadhipati Yoga",
        "9th and 10th lords conjunct or exchanging signs — exceptional career, highest honor, and dharmic success.",
        dkd,
        "Strong" if dkd else "Absent",
    )

    # 6. Viparita Raja Yoga (Dusthana lords in Dusthana)
    l6 = SIGN_LORDS.get(SIGNS_SK[(lagna_idx + 5) % 12])
    l8 = SIGN_LORDS.get(SIGNS_SK[(lagna_idx + 7) % 12])
    l12 = SIGN_LORDS.get(SIGNS_SK[(lagna_idx + 11) % 12])
    h6 = _house_of(pmap, l6) if l6 else 0
    h8 = _house_of(pmap, l8) if l8 else 0
    h12 = _house_of(pmap, l12) if l12 else 0
    vip = bool((h6 in DUSTHANA and h8 in DUSTHANA) or (h6 in DUSTHANA and h12 in DUSTHANA))
    add(
        "Viparita Raja Yoga",
        "Lords of 6th, 8th, or 12th placed in dusthanas — triumph over adversaries and resilience after hardship.",
        vip,
    )

    # 7. Neecha Bhanga Raja Yoga (Debilitation cancelled)
    nbry = False
    for planet, deb_sign in [("Sun", "Tula"), ("Moon", "Vrischika"), ("Mars", "Karka"),
                             ("Mercury", "Meena"), ("Jupiter", "Makara"), ("Venus", "Kanya"), ("Saturn", "Mesha")]:
        p = pmap.get(planet)
        if p and p.get("sign") == deb_sign:
            disp = SIGN_LORDS.get(deb_sign)
            if disp and _house_of(pmap, disp) in KENDRA:
                nbry = True
                break
    add(
        "Neecha Bhanga Raja Yoga",
        "Debilitation cancelled by dispositor in kendra — initial disadvantage transforms into great strength.",
        nbry,
        "Strong" if nbry else "Absent",
    )

    # 8. Dhana Yoga (2nd & 11th lord conjunction)
    lord_2 = SIGN_LORDS.get(SIGNS_SK[(lagna_idx + 1) % 12])
    lord_11 = SIGN_LORDS.get(SIGNS_SK[(lagna_idx + 10) % 12])
    dhana = bool(lord_2 and lord_11 and _house_of(pmap, lord_2) == _house_of(pmap, lord_11) and _house_of(pmap, lord_2) != 0)
    add(
        "Dhana Yoga",
        "Lords of 2nd and 11th houses conjunct — strong wealth accumulation and prosperity.",
        dhana,
    )

    return yogas


def detect_advanced_yogas(chart: dict) -> list[str]:
    """Lightweight yogas extractor returning list of active yoga names."""
    planets = []
    planets_by_house = chart.get("planets_by_house", {})
    for h, p_list in planets_by_house.items():
        for p in p_list:
            p_copy = dict(p)
            p_copy["house"] = int(h)
            planets.append(p_copy)

    lagna = chart.get("basic_details", {}).get("lagna", "Mesha")
    yogas = calculate_yogas(planets, lagna, {})
    return [y["name"] for y in yogas if y["present"]]
