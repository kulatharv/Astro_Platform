"""Vedic Panchang Calculation Engine."""

from datetime import datetime, timedelta
import swisseph as swe
from .cities import get_city
from .nakshatra import NAKSHATRAS, NAKSHATRA_SIZE

TITHI_NAMES = [
    "Shukla Pratipada", "Shukla Dwitiya", "Shukla Tritiya", "Shukla Chaturthi", "Shukla Panchami",
    "Shukla Shashthi", "Shukla Saptami", "Shukla Ashtami", "Shukla Navami", "Shukla Dashami",
    "Shukla Ekadashi", "Shukla Dwadashi", "Shukla Trayodashi", "Shukla Chaturdashi", "Purnima",
    "Krishna Pratipada", "Krishna Dwitiya", "Krishna Tritiya", "Krishna Chaturthi", "Krishna Panchami",
    "Krishna Shashthi", "Krishna Saptami", "Krishna Ashtami", "Krishna Navami", "Krishna Dashami",
    "Krishna Ekadashi", "Krishna Dwadashi", "Krishna Trayodashi", "Krishna Chaturdashi", "Amavasya",
]

YOGA_NAMES = [
    "Vishkumbha", "Preeti", "Ayushman", "Saubhagya", "Shobhana",
    "Atiganda", "Sukarma", "Dhriti", "Shoola", "Ganda", "Vriddhi",
    "Dhruva", "Vyaghata", "Harshana", "Vajra", "Siddhi", "Vyatipata",
    "Variyana", "Parigha", "Shiva", "Siddha", "Sadhya", "Shubha",
    "Shukla", "Brahma", "Indra", "Vaidhriti",
]

KARANA_NAMES = [
    "Bava", "Balava", "Kaulava", "Taitila", "Garaja", "Vanija", "Vishti (Bhadra)",
    "Shakuni", "Chatushpada", "Naga", "Kintughna",
]

VARAS = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]

# Rahu Kaal periods (1/8th of day from sunrise to sunset) on Sunday-Saturday
RAHU_KAAL_PERIOD = [8, 2, 7, 5, 6, 4, 3]  # Period index (1-8)


def calculate_panchang_for_datetime(dt: datetime, lat: float = 18.5204, lon: float = 73.8567, tz: float = 5.5) -> dict:
    """Calculate 5 Limbs of Panchang + Muhurta metrics for a given datetime and coordinates."""
    swe.set_sid_mode(swe.SIDM_LAHIRI)
    flags = swe.FLG_SWIEPH | swe.FLG_SIDEREAL

    # Convert local datetime to UTC Julian Day
    utc_dt = dt - timedelta(hours=tz)
    utc_hour = utc_dt.hour + utc_dt.minute / 60.0 + utc_dt.second / 3600.0
    jd = swe.julday(utc_dt.year, utc_dt.month, utc_dt.day, utc_hour)

    # 1. Solar & Lunar Longitudes
    sun_lon = swe.calc_ut(jd, swe.SUN, flags)[0][0] % 360.0
    moon_lon = swe.calc_ut(jd, swe.MOON, flags)[0][0] % 360.0

    # 2. Tithi
    diff = (moon_lon - sun_lon) % 360.0
    tithi_index = int(diff / 12.0)
    tithi_name = TITHI_NAMES[tithi_index % 30]

    # 3. Nakshatra
    nak_index = int(moon_lon / NAKSHATRA_SIZE) % 27
    nak_name = NAKSHATRAS[nak_index]

    # 4. Yoga
    yoga_index = int(((sun_lon + moon_lon) % 360.0) / NAKSHATRA_SIZE) % 27
    yoga_name = YOGA_NAMES[yoga_index]

    # 5. Karana
    if tithi_index == 0 and diff < 6.0:
        karana_name = "Kintughna"
    elif tithi_index == 28 and diff >= 348.0:
        karana_name = "Shakuni"
    elif tithi_index == 29:
        karana_name = "Chatushpada" if diff < 354.0 else "Naga"
    else:
        karana_idx = int(diff / 6.0) % 7
        karana_name = KARANA_NAMES[karana_idx]

    # 6. Vara (Weekday)
    weekday_idx = (dt.weekday() + 1) % 7  # 0=Sunday, 6=Saturday
    vara = VARAS[weekday_idx]

    # 7. Sunrise / Sunset (Approximate standard model)
    sunrise_hour = 6.0 + (lat - 20.0) * 0.02
    sunset_hour = 18.0 - (lat - 20.0) * 0.02
    day_span = sunset_hour - sunrise_hour
    slot_span = day_span / 8.0

    rk_slot = RAHU_KAAL_PERIOD[weekday_idx] - 1
    rk_start = sunrise_hour + (rk_slot * slot_span)
    rk_end = rk_start + slot_span

    def format_hour(h: float) -> str:
        h_int = int(h) % 24
        m_int = int((h - int(h)) * 60)
        return f"{h_int:02d}:{m_int:02d}"

    return {
        "date": dt.strftime("%Y-%m-%d"),
        "tithi": tithi_name,
        "nakshatra": nak_name,
        "yoga": yoga_name,
        "karana": karana_name,
        "vara": vara,
        "sunrise": format_hour(sunrise_hour),
        "sunset": format_hour(sunset_hour),
        "rahu_kaal": f"{format_hour(rk_start)} - {format_hour(rk_end)}",
        "abhijit_muhurta": f"{format_hour(sunrise_hour + 5.5)} - {format_hour(sunrise_hour + 6.3)}",
    }


def get_full_panchang(city: str) -> dict:
    """Entrypoint for /api/panchang returning complete daily panchang for a given city name."""
    coords = get_city(city)
    if coords is None:
        lat, lon, tz = 18.5204, 73.8567, 5.5
    else:
        lat, lon, tz = coords

    now = datetime.now()
    result = calculate_panchang_for_datetime(now, lat, lon, tz)
    result["city"] = city
    return result
