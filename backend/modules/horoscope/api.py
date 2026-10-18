"""Daily Horoscope API routes."""

from datetime import date
from fastapi import APIRouter, HTTPException
from shared.veda.constants import ZODIAC_SIGNS
from modules.horoscope.engine import generate_horoscope, generate_all_horoscopes

router = APIRouter(prefix="/api", tags=["Horoscope"])

# Thread-safe daily cache
daily_cache: dict[str, dict] = {
    "date": None,
    "data": {},
}


class HoroscopeService:
    def get_daily_horoscope(self, sign: str) -> dict:
        return get_daily_horoscope(sign)

    def get_horoscope_by_index(self, sign_idx: int) -> dict:
        return generate_horoscope(sign_idx)

    def get_all_horoscopes(self) -> dict[str, dict]:
        return generate_all_horoscopes()


@router.get("/daily-horoscope/{sign}")
def get_daily_horoscope(sign: str):
    """Retrieve transit-based daily horoscope for a given zodiac sign name."""
    global daily_cache
    sign_lower = sign.strip().lower()

    if sign_lower not in ZODIAC_SIGNS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid zodiac sign '{sign}'. Must be one of {ZODIAC_SIGNS}",
        )

    today = str(date.today())
    if daily_cache.get("date") != today:
        daily_cache["date"] = today
        daily_cache["data"] = {}

    if sign_lower in daily_cache["data"]:
        return daily_cache["data"][sign_lower]

    result = generate_horoscope(sign_lower)
    daily_cache["data"][sign_lower] = result
    return result


@router.get("/horoscope/{sign_idx}")
def horoscope_by_sign_index(sign_idx: int):
    """Retrieve daily horoscope by 0-11 zodiac index."""
    if not (0 <= sign_idx <= 11):
        raise HTTPException(status_code=400, detail="sign_idx must be between 0 and 11")

    try:
        return generate_horoscope(sign_idx)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
