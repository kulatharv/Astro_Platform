"""Dynamic transit-driven daily horoscope engine."""

from datetime import date, datetime
import swisseph as swe
from .zodiac import SIGNS_EN, SIGNS_SK

SIGN_TO_RASHI = {
    "aries": 0, "taurus": 1, "gemini": 2, "cancer": 3,
    "leo": 4, "virgo": 5, "libra": 6, "scorpio": 7,
    "sagittarius": 8, "capricorn": 9, "aquarius": 10, "pisces": 11,
}

MANTRAS = {
    "Aries": "Om Angarakaya Namaha (108×) — channel Mars' vitality with wisdom",
    "Taurus": "Om Shukraya Namaha (108×) — cultivate Venusian harmony and grace",
    "Gemini": "Om Budhaya Namaha (108×) — sharpen intellect and clear expression",
    "Cancer": "Om Chandraya Namaha (108×) — calm and harmonize emotional waters",
    "Leo": "Om Suryaya Namaha (108×) — strengthen inner sun, confidence, and dharma",
    "Virgo": "Om Budhaya Namaha (108×) — bring analytical precision to life",
    "Libra": "Om Shukraya Namaha (108×) — balance relationships and aesthetic joy",
    "Scorpio": "Om Bhaumaya Namaha (108×) — transform deep challenges into power",
    "Sagittarius": "Om Gurave Namaha (108×) — expand philosophical vision and truth",
    "Capricorn": "Om Shanaischaraya Namaha (19×) — build patient, enduring success",
    "Aquarius": "Om Sham Shanaischaraya Namaha (19×) — innovate for higher purpose",
    "Pisces": "Om Gurave Namaha (108×) — receive spiritual grace and compassion",
}

COLORS = {
    "Aries": "Crimson Red", "Taurus": "Pastel Pink", "Gemini": "Emerald Green",
    "Cancer": "Pearl White", "Leo": "Royal Gold", "Virgo": "Forest Green",
    "Libra": "Sky Blue", "Scorpio": "Deep Maroon", "Sagittarius": "Bright Yellow",
    "Capricorn": "Charcoal Navy", "Aquarius": "Electric Cyan", "Pisces": "Sea Green",
}


def generate_horoscope(sign_input: str | int) -> dict:
    """Generate dynamic transit-based horoscope for a given sign name or 0-11 index."""
    if isinstance(sign_input, int):
        sign_idx = max(0, min(11, sign_input))
        sign_en = SIGNS_EN[sign_idx]
    else:
        sign_clean = sign_input.strip().lower()
        sign_idx = SIGN_TO_RASHI.get(sign_clean, 0)
        sign_en = SIGNS_EN[sign_idx]

    swe.set_sid_mode(swe.SIDM_LAHIRI)
    flags = swe.FLG_SWIEPH | swe.FLG_SIDEREAL

    today = date.today()
    jd = swe.julday(today.year, today.month, today.day, 6.0)

    # Planetary positions
    sun_lon = swe.calc_ut(jd, swe.SUN, flags)[0][0] % 360.0
    moon_lon = swe.calc_ut(jd, swe.MOON, flags)[0][0] % 360.0
    jup_lon = swe.calc_ut(jd, swe.JUPITER, flags)[0][0] % 360.0
    ven_lon = swe.calc_ut(jd, swe.VENUS, flags)[0][0] % 360.0
    sat_lon = swe.calc_ut(jd, swe.SATURN, flags)[0][0] % 360.0

    sun_sign_idx = int(sun_lon / 30.0)
    moon_sign_idx = int(moon_lon / 30.0)
    jup_sign_idx = int(jup_lon / 30.0)

    # Relative house placement from current sign
    moon_h = ((moon_sign_idx - sign_idx) % 12) + 1
    jup_h = ((jup_sign_idx - sign_idx) % 12) + 1

    # Dynamic scores (60-95%)
    career_score = 70 + (15 if jup_h in (1, 5, 9, 10) else 0) + (5 if moon_h in (3, 6, 10, 11) else 0)
    love_score = 72 + (12 if ven_lon % 30 < 15 else 5)
    finance_score = 68 + (14 if jup_h in (2, 11, 9) else 4)
    health_score = 75 + (10 if moon_h not in (6, 8, 12) else -10)
    luck_score = 70 + (15 if jup_h in (1, 5, 9) else 5)

    lucky_num = ((sign_idx * 3 + today.day) % 9) + 1

    prediction_text = (
        f"For {sign_en}, today's cosmic transits highlight meaningful opportunities. "
        f"The Moon transit through house {moon_h} sharpens intuition and inner focus. "
        f"Jupiter's position in house {jup_h} grants steady support in professional and personal endeavors. "
        f"Stay aligned with your highest priorities, practice deliberate patience in communication, "
        f"and channel planetary energies into proactive action."
    )

    return {
        "status": "success",
        "sign": sign_en,
        "date": today.strftime("%Y-%m-%d"),
        "horoscope": prediction_text,
        "scores": {
            "career": min(98, career_score),
            "love": min(98, love_score),
            "finance": min(98, finance_score),
            "health": min(98, health_score),
            "luck": min(98, luck_score),
        },
        "lucky_number": lucky_num,
        "lucky_color": COLORS.get(sign_en, "Gold"),
        "mantra": MANTRAS.get(sign_en, "Om Namah Shivaya"),
        "tip": f"Focus constructive energy early in the day and maintain clear boundaries.",
        "compatible_signs": [SIGNS_EN[(sign_idx + 4) % 12], SIGNS_EN[(sign_idx + 8) % 12]],
    }


def generate_all_horoscopes() -> dict[str, dict]:
    """Generate horoscopes for all 12 signs."""
    return {sign: generate_horoscope(sign) for sign in SIGN_TO_RASHI}
