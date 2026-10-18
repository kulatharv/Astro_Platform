"""9-Tier Dignity and Naisargika Maitri Planetary Friendship Engine (Pure Shared Library)."""

from .strength import EXALTATION, DEBILITATION, OWN_SIGNS

# Naisargika Maitri (Classical Natural Friendships)
PLANET_FRIENDS = {
    "Sun": ["Moon", "Mars", "Jupiter"],
    "Moon": ["Sun", "Mercury"],
    "Mars": ["Sun", "Moon", "Jupiter"],
    "Mercury": ["Sun", "Venus"],
    "Jupiter": ["Sun", "Moon", "Mars"],
    "Venus": ["Mercury", "Saturn"],
    "Saturn": ["Mercury", "Venus"],
    "Rahu": ["Mercury", "Venus", "Saturn"],
    "Ketu": ["Mars", "Venus", "Saturn"],
}

PLANET_ENEMIES = {
    "Sun": ["Venus", "Saturn", "Rahu", "Ketu"],
    "Moon": [],  # Moon has no natural enemies
    "Mars": ["Mercury"],
    "Mercury": ["Moon"],
    "Jupiter": ["Mercury", "Venus"],
    "Venus": ["Sun", "Moon"],
    "Saturn": ["Sun", "Moon", "Mars"],
    "Rahu": ["Sun", "Moon", "Mars"],
    "Ketu": ["Sun", "Moon"],
}

MOOLATRIKONA = {
    "Sun": "Simha",
    "Moon": "Vrishabha",
    "Mars": "Mesha",
    "Mercury": "Kanya",
    "Jupiter": "Dhanu",
    "Venus": "Tula",
    "Saturn": "Kumbha",
}


def get_naisargika_dignity(planet: str, sign: str) -> str:
    """Return 9-tier dignity classification for a planet in a sign."""
    if EXALTATION.get(planet) == sign:
        return "Exalted"
    if MOOLATRIKONA.get(planet) == sign:
        return "Moolatrikona"
    if sign in OWN_SIGNS.get(planet, []):
        return "Own Sign"
    if DEBILITATION.get(planet) == sign:
        return "Debilitated"

    from .zodiac import SIGN_LORDS
    dispositor = SIGN_LORDS.get(sign)
    if not dispositor or dispositor == planet:
        return "Own Sign"

    friends = PLANET_FRIENDS.get(planet, [])
    enemies = PLANET_ENEMIES.get(planet, [])

    if dispositor in friends:
        return "Great Friend" if dispositor in OWN_SIGNS.get(planet, []) else "Friend"
    if dispositor in enemies:
        return "Great Enemy" if dispositor in DEBILITATION.get(planet, []) else "Enemy"
    return "Neutral"


def get_positional_strength(name: str, sign: str, navamsa: str = "", degree: float = 0.0) -> float:
    """
    Calculate numerical positional strength score (-2.0 to +2.0) using 9-tier dignity.
    """
    dignity = get_naisargika_dignity(name, sign)
    score_map = {
        "Exalted": 2.0,
        "Moolatrikona": 1.5,
        "Own Sign": 1.0,
        "Great Friend": 0.75,
        "Friend": 0.50,
        "Neutral": 0.0,
        "Enemy": -0.50,
        "Great Enemy": -0.75,
        "Debilitated": -2.0,
    }
    score = score_map.get(dignity, 0.0)

    # Navamsa dignity bonus
    if navamsa:
        nav_dignity = get_naisargika_dignity(name, navamsa)
        if nav_dignity in ("Exalted", "Moolatrikona", "Own Sign"):
            score += 0.5
        elif nav_dignity in ("Debilitated", "Great Enemy"):
            score -= 0.5

    return max(-2.0, min(2.0, round(score, 2)))
