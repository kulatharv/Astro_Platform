"""Planetary Dignity, Exaltation, Debilitation, and Strength Scoring (Pure Shared Library)."""

EXALTATION = {
    "Sun": "Mesha", "Moon": "Vrishabha", "Mars": "Makara", "Mercury": "Kanya",
    "Jupiter": "Karka", "Venus": "Meena", "Saturn": "Tula", "Rahu": "Vrishabha", "Ketu": "Vrischika"
}

DEBILITATION = {
    "Sun": "Tula", "Moon": "Vrischika", "Mars": "Karka", "Mercury": "Meena",
    "Jupiter": "Makara", "Venus": "Kanya", "Saturn": "Mesha", "Rahu": "Vrischika", "Ketu": "Vrishabha"
}

OWN_SIGNS = {
    "Sun": ["Simha"],
    "Moon": ["Karka"],
    "Mars": ["Mesha", "Vrischika"],
    "Mercury": ["Mithuna", "Kanya"],
    "Jupiter": ["Dhanu", "Meena"],
    "Venus": ["Vrishabha", "Tula"],
    "Saturn": ["Makara", "Kumbha"],
    "Rahu": ["Kumbha"],
    "Ketu": ["Vrischika"],
}

FRIENDLY_SIGNS = {
    "Sun": ["Mesha", "Karka", "Vrischika", "Dhanu", "Meena"],
    "Moon": ["Mesha", "Mithuna", "Simha", "Kanya"],
    "Mars": ["Simha", "Dhanu", "Meena"],
    "Mercury": ["Simha", "Tula", "Vrishabha"],
    "Jupiter": ["Mesha", "Simha", "Vrischika"],
    "Venus": ["Mithuna", "Kanya", "Makara", "Kumbha"],
    "Saturn": ["Mithuna", "Kanya", "Tula", "Vrishabha"],
    "Rahu": ["Mithuna", "Kanya", "Tula"],
    "Ketu": ["Mesha", "Dhanu", "Meena"],
}


def planet_strength_label(planet: str, sign: str) -> str:
    """Return categorical dignity label for a planet in a given sign."""
    if EXALTATION.get(planet) == sign:
        return "Exalted"
    if DEBILITATION.get(planet) == sign:
        return "Debilitated"
    if sign in OWN_SIGNS.get(planet, []):
        return "Own Sign"
    if sign in FRIENDLY_SIGNS.get(planet, []):
        return "Friendly Sign"
    return "Neutral"


def final_strength(planet: str, rasi_sign: str, navamsa_sign: str) -> str:
    """Calculate combined Rasi & Navamsa strength."""
    r_label = planet_strength_label(planet, rasi_sign)
    n_label = planet_strength_label(planet, navamsa_sign)

    if rasi_sign == navamsa_sign:
        return f"Vargottama ({r_label})"
    if r_label == "Exalted":
        return "Exalted"
    if r_label == "Debilitated":
        if n_label in ("Exalted", "Own Sign"):
            return "Debilitated (Neecha Bhanga)"
        return "Debilitated"
    if r_label == "Own Sign":
        return "Own Sign"
    if r_label == "Friendly Sign":
        return "Friendly Sign"
    return "Neutral"


def calculate_weighted_strength(chart: dict) -> dict[str, float]:
    """Calculate numerical weighted strength (0.0 to 10.0) for each planet."""
    scores = {}
    planets_by_house = chart.get("planets_by_house", {})

    for house_num, p_list in planets_by_house.items():
        for p in p_list:
            name = p.get("planet")
            sign = p.get("sign")
            st = p.get("strength", "Neutral")

            base = 5.0
            if "Exalted" in st:
                base = 9.5
            elif "Own Sign" in st:
                base = 8.0
            elif "Vargottama" in st:
                base = 8.5
            elif "Friendly" in st:
                base = 6.5
            elif "Debilitated" in st:
                base = 2.5 if "Neecha Bhanga" in st else 1.5

            try:
                h_int = int(house_num)
                if h_int in (1, 4, 7, 10):
                    base += 1.0
                elif h_int in (5, 9):
                    base += 1.0
                elif h_int in (6, 8, 12):
                    base -= 1.5
            except (ValueError, TypeError):
                pass

            scores[name] = max(1.0, min(10.0, round(base, 1)))

    return scores
