"""Master Kundali Engine assembling Rasi, Navamsa D9, Dasha, Yogas, Doshas, and Scores."""

from datetime import datetime, timedelta
import swisseph as swe

from .zodiac import SIGNS_SK, SIGN_LORDS, to_dms
from .nakshatra import calculate_nakshatra
from .navamsa import calculate_navamsa
from .strength import planet_strength_label
from .dasha import calculate_mahadasha, generate_antardasha
from .yogas import calculate_yogas
from .doshas import calculate_doshas

PLANET_LIST = [
    ("Sun", swe.SUN),
    ("Moon", swe.MOON),
    ("Mars", swe.MARS),
    ("Mercury", swe.MERCURY),
    ("Jupiter", swe.JUPITER),
    ("Venus", swe.VENUS),
    ("Saturn", swe.SATURN),
    ("Rahu", swe.MEAN_NODE),
]

TITHI_NAMES = [
    "Pratipada", "Dwitiya", "Tritiya", "Chaturthi", "Panchami",
    "Shashthi", "Saptami", "Ashtami", "Navami", "Dashami",
    "Ekadashi", "Dwadashi", "Trayodashi", "Chaturdashi", "Purnima",
    "Pratipada", "Dwitiya", "Tritiya", "Chaturthi", "Panchami",
    "Shashthi", "Saptami", "Ashtami", "Navami", "Dashami",
    "Ekadashi", "Dwadashi", "Trayodashi", "Chaturdashi", "Amavasya",
]

YOGA_NAMES = [
    "Vishkumbha", "Preeti", "Ayushman", "Saubhagya", "Shobhana",
    "Atiganda", "Sukarma", "Dhriti", "Shoola", "Ganda", "Vriddhi",
    "Dhruva", "Vyaghata", "Harshana", "Vajra", "Siddhi", "Vyatipata",
    "Variyana", "Parigha", "Shiva", "Siddha", "Sadhya", "Shubha",
    "Shukla", "Brahma", "Indra", "Vaidhriti",
]

KARANA_NAMES = ["Bava", "Balava", "Kaulava", "Taitila", "Garaja", "Vanija", "Vishti"]


def calculate_chart_scores(planets: list[dict], lagna_sign: str, houses: dict) -> dict[str, int]:
    """Calculate normalized scores (0-100) across all life areas."""
    pmap = {p.get("name"): p for p in planets}
    KENDRA = {1, 4, 7, 10}
    TRIKONA = {1, 5, 9}
    DUSTHANA = {6, 8, 12}
    lagna_idx = SIGNS_SK.index(lagna_sign) if lagna_sign in SIGNS_SK else 0

    def ps(name: str) -> float:
        p = pmap.get(name)
        if not p:
            return 5.0
        label = p.get("strength", "Neutral")
        b = 10.0 if "Exalted" in label else 8.0 if "Own" in label else 2.0 if "Debilitated" in label else 5.0
        h = p.get("house", 1)
        if isinstance(h, int):
            if h in KENDRA or h in TRIKONA:
                b += 1.0
            elif h in DUSTHANA:
                b -= 1.5
        if p.get("retrograde"):
            b -= 0.5
        return max(1.0, min(10.0, b))

    def lord_of(house_num: int) -> str:
        return SIGN_LORDS.get(SIGNS_SK[(lagna_idx + house_num - 1) % 12], "Mars")

    overall = sum(ps(p) for p in ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"])
    career = ps("Sun") * 1.5 + ps("Saturn") * 1.5 + ps("Mars") + ps(lord_of(10)) * 2.0
    finance = ps("Jupiter") * 2.0 + ps("Venus") * 1.5 + ps(lord_of(2)) * 1.5 + ps(lord_of(11))
    marriage = ps("Venus") * 2.0 + ps("Jupiter") * 1.5 + ps(lord_of(7)) * 2.0 + ps("Moon") * 0.5
    health = ps("Sun") * 1.5 + ps("Mars") * 1.5 + ps(lord_of(1)) * 2.0 + ps(lord_of(6))
    mental = ps("Moon") * 2.5 + ps("Mercury") * 2.0 + ps(lord_of(4)) * 1.5
    ketu_h = pmap.get("Ketu", {}).get("house", 1)
    spirit = ps("Jupiter") * 2.0 + ps(lord_of(9)) * 2.0 + (7.0 if ketu_h in {1, 5, 9, 12} else 5.0)

    def norm(val: float, denom: float) -> int:
        return round(min((val / denom) * 100.0, 100.0))

    return {
        "overall_strength": norm(overall, 70.0),
        "career_score": norm(career, 60.0),
        "finance_score": norm(finance, 60.0),
        "marriage_score": norm(marriage, 60.0),
        "health_score": norm(health, 60.0),
        "mental_score": norm(mental, 60.0),
        "spirituality_score": norm(spirit, 40.0),
    }


def calculate_kundali(year: int, month: int, day: int, hour: int, minute: int, lat: float, lon: float) -> dict:
    """
    Master Kundali engine returning complete Rasi, Navamsa D9, Panchang, Dasha, Yogas, Doshas, and Scores.
    """
    swe.set_sid_mode(swe.SIDM_LAHIRI)
    flags = swe.FLG_SWIEPH | swe.FLG_SIDEREAL | swe.FLG_SPEED

    # Convert IST/Local to UTC Julian Day
    ist_offset = 5.5
    utc_hours = (hour + minute / 60.0) - ist_offset
    calc_day = day
    if utc_hours < 0:
        utc_hours += 24.0
        calc_day -= 1

    jd = swe.julday(year, month, calc_day, utc_hours)

    # 1. Calculate Lagna
    cusps, ascmc = swe.houses_ex(jd, lat, lon, b'W', flags)
    lagna_lon = ascmc[0] % 360.0
    lagna_idx = int(lagna_lon / 30.0)
    lagna_sign = SIGNS_SK[lagna_idx]
    lagna_nak, lagna_pada = calculate_nakshatra(lagna_lon)

    # 2. Build 12 Houses
    houses = {i: [] for i in range(1, 13)}
    houses[1].append("Lagna")
    planet_data = []

    rahu_raw = 0.0

    for name, planet_id in PLANET_LIST:
        data = swe.calc_ut(jd, planet_id, flags)
        raw_lon = data[0][0] % 360.0
        speed = data[0][3]

        if name == "Rahu":
            rahu_raw = raw_lon

        sign_idx = int(raw_lon / 30.0)
        sign_name = SIGNS_SK[sign_idx]
        house_num = ((sign_idx - lagna_idx) % 12) + 1
        nak_name, pada = calculate_nakshatra(raw_lon)
        nav_sign = calculate_navamsa(raw_lon)
        strength = planet_strength_label(name, sign_name)

        houses[house_num].append(name)
        planet_data.append({
            "name": name,
            "sign": sign_name,
            "degree": to_dms(raw_lon % 30.0),
            "degree_decimal": round(raw_lon % 30.0, 4),
            "house": house_num,
            "nakshatra": nak_name,
            "pada": pada,
            "navamsa": nav_sign,
            "strength": strength,
            "retrograde": speed < 0 or name in ("Rahu", "Ketu"),
            "_raw_lon": raw_lon,
        })

    # 3. Add Ketu (180° from Rahu)
    ketu_lon = (rahu_raw + 180.0) % 360.0
    ketu_sign_idx = int(ketu_lon / 30.0)
    ketu_sign = SIGNS_SK[ketu_sign_idx]
    ketu_house = ((ketu_sign_idx - lagna_idx) % 12) + 1
    ketu_nak, ketu_pada = calculate_nakshatra(ketu_lon)

    houses[ketu_house].append("Ketu")
    planet_data.append({
        "name": "Ketu",
        "sign": ketu_sign,
        "degree": to_dms(ketu_lon % 30.0),
        "degree_decimal": round(ketu_lon % 30.0, 4),
        "house": ketu_house,
        "nakshatra": ketu_nak,
        "pada": ketu_pada,
        "navamsa": calculate_navamsa(ketu_lon),
        "strength": planet_strength_label("Ketu", ketu_sign),
        "retrograde": True,
        "_raw_lon": ketu_lon,
    })

    # 4. Panchang metrics
    sun_lon = next(p["_raw_lon"] for p in planet_data if p["name"] == "Sun")
    moon_lon = next(p["_raw_lon"] for p in planet_data if p["name"] == "Moon")
    diff = (moon_lon - sun_lon) % 360.0

    tithi_num = int(diff / 12.0) + 1
    tithi_name = TITHI_NAMES[(tithi_num - 1) % 30]
    paksha = "Shukla" if tithi_num <= 15 else "Krishna"
    moon_nak, moon_pada = calculate_nakshatra(moon_lon)
    yoga_name = YOGA_NAMES[int(((sun_lon + moon_lon) % 360.0) / (360.0 / 27.0)) % 27]
    karana_name = KARANA_NAMES[int(diff / 6.0) % 7]
    ayanamsa = swe.get_ayanamsa(jd)

    # 5. Dasha
    maha_lord, balance_years = calculate_mahadasha(moon_lon, moon_nak)
    antardasha = generate_antardasha(maha_lord)

    # 6. Navamsa D9 Houses
    d9_houses = {i: [] for i in range(1, 13)}
    d9_lagna_nav = calculate_navamsa(lagna_lon)
    d9_lagna_idx = SIGNS_SK.index(d9_lagna_nav)
    d9_houses[1].append("Lagna")

    for p in planet_data:
        nav = p.get("navamsa", "")
        if nav in SIGNS_SK:
            nav_idx = SIGNS_SK.index(nav)
            d9_h = ((nav_idx - d9_lagna_idx) % 12) + 1
            d9_houses[d9_h].append(p["name"])

    # 7. Scores, Yogas, and Doshas
    planets_out = [{k: v for k, v in p.items() if k != "_raw_lon"} for p in planet_data]
    scores = calculate_chart_scores(planet_data, lagna_sign, houses)
    yogas = calculate_yogas(planet_data, lagna_sign, houses)
    doshas = calculate_doshas(planet_data, lagna_sign, houses)

    return {
        "lagna": lagna_sign,
        "lagna_degree": to_dms(lagna_lon % 30.0),
        "lagna_degree_decimal": round(lagna_lon % 30.0, 4),
        "lagna_nakshatra": lagna_nak,
        "lagna_pada": lagna_pada,
        "houses": houses,
        "d9_houses": d9_houses,
        "d9_lagna": d9_lagna_nav,
        "planets": planets_out,
        "tithi_number": tithi_num,
        "tithi_name": tithi_name,
        "paksha": paksha,
        "nakshatra": moon_nak,
        "nakshatra_pada": moon_pada,
        "yoga_name": yoga_name,
        "karana_name": karana_name,
        "ayanamsa": round(ayanamsa, 4),
        "jd": round(jd, 6),
        "mahadasha": maha_lord,
        "dasha_balance": f"{balance_years:.1f} years",
        "antardasha": antardasha[0]["lord"] if antardasha else "",
        "antardasha_list": antardasha,
        "scores": scores,
        "yogas": yogas,
        "doshas": doshas,
    }
