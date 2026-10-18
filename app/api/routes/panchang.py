"""Panchang and Festival API routes."""

from fastapi import APIRouter, HTTPException
from app.schemas.panchang import PanchangRequest
from app.services.astrology_engine.festival import get_today_festivals, get_upcoming_festivals
from app.services.astrology_engine.panchang import get_full_panchang

router = APIRouter(prefix="/api", tags=["Panchang & Festivals"])


@router.post("/panchang")
def panchang_city(request: PanchangRequest):
    """Calculate daily Panchang (Tithi, Nakshatra, Yoga, Karana, Vara, Rahu Kaal) for a city."""
    return get_full_panchang(request.city)


@router.get("/festivals/today")
def festivals_today():
    """Return Hindu festivals falling on today's date."""
    try:
        return {"festivals": get_today_festivals()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/festivals/upcoming")
def festivals_upcoming(limit: int = 12):
    """Return upcoming Hindu festivals for the next 60 days."""
    try:
        return {"festivals": get_upcoming_festivals(limit)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
