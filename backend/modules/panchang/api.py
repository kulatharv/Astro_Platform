"""
Panchang, Personalization, Decision Assistant, and Festival API routes.
Includes RFC 5545 iCalendar support, GPS coordinate validation,
profile resolution, and deterministic rule recommendations.
"""

from datetime import datetime, time as dt_time, date
from typing import Optional
from fastapi import APIRouter, HTTPException, Query, Response

from modules.panchang.schemas import PanchangRequest, ProfileResolveRequest, DecisionRequest
from modules.panchang.festival import get_today_festivals, get_upcoming_festivals
from modules.panchang.engine import get_full_panchang
from modules.panchang.image import generate_panchang_image
from modules.panchang.ics import generate_panchang_ics
from modules.panchang.personalization import derive_natal_moon, evaluate_decision
from shared.logging.logger import get_logger

logger = get_logger("modules.panchang.api")
router = APIRouter(prefix="/api", tags=["Panchang & Festivals"])


class PanchangService:
    def get_panchang(self, req: PanchangRequest) -> dict:
        target_date = None
        if req.date_str:
            target_date = datetime.strptime(req.date_str, "%Y-%m-%d").date()
        return get_full_panchang(
            city_name=req.city or "Pune",
            target_date=target_date,
            lat=req.lat,
            lon=req.lon,
            tz_str=req.timezone,
            user_rashi=req.user_rashi,
            user_nakshatra=req.user_nakshatra
        )

    def get_today_festivals(self) -> list[dict]:
        return get_today_festivals()

    def get_upcoming_festivals(self, limit: int = 14) -> list[dict]:
        return get_upcoming_festivals(limit)


@router.get("/panchang/share-image")
def panchang_share_image(
    city: str = Query(default="Pune", description="City for Panchang calculation"),
    date_str: Optional[str] = Query(default=None, alias="date", description="Target date in YYYY-MM-DD format"),
    format: str = Query(default="portrait", pattern="^(portrait|square)$", description="Image format: portrait or square"),
    type: str = Query(default="png", pattern="^(png|jpeg|jpg)$", description="Image type: png or jpeg"),
    lat: Optional[float] = Query(default=None, ge=-90.0, le=90.0, description="Optional GPS latitude"),
    lon: Optional[float] = Query(default=None, ge=-180.0, le=180.0, description="Optional GPS longitude"),
    timezone: Optional[str] = Query(default=None, description="Optional timezone string")
):
    try:
        target_date = None
        if date_str:
            try:
                target_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            except ValueError:
                raise HTTPException(status_code=400, detail="Invalid date format. Expected YYYY-MM-DD.")

        img_bytes, media_type = generate_panchang_image(
            city=city,
            target_date=target_date,
            image_format=format,
            image_type=type,
            lat=lat,
            lon=lon,
            tz_str=timezone
        )

        ext = "jpg" if "jpeg" in media_type else "png"
        filename = f"panchang_{city.lower().replace(' ', '_')}_{format}.{ext}"

        return Response(
            content=img_bytes,
            media_type=media_type,
            headers={
                "Content-Disposition": f'inline; filename="{filename}"',
                "Cache-Control": "public, max-age=3600"
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Panchang image generation failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to generate Panchang image.")


@router.post("/panchang")
def panchang_city(request: PanchangRequest):
    try:
        if request.lat is not None:
            if not (-90.0 <= request.lat <= 90.0):
                raise HTTPException(status_code=400, detail="Latitude must be between -90 and 90 degrees.")
        if request.lon is not None:
            if not (-180.0 <= request.lon <= 180.0):
                raise HTTPException(status_code=400, detail="Longitude must be between -180 and 180 degrees.")

        target_date = None
        if request.date_str:
            try:
                target_date = datetime.strptime(request.date_str, "%Y-%m-%d").date()
            except ValueError:
                raise HTTPException(status_code=400, detail="Invalid date format. Expected YYYY-MM-DD.")

        city = request.city or "Pune"
        return get_full_panchang(
            city_name=city,
            target_date=target_date,
            lat=request.lat,
            lon=request.lon,
            tz_str=request.timezone,
            user_rashi=request.user_rashi,
            user_nakshatra=request.user_nakshatra
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Panchang calculation failed: {e}", exc_info=True)
        try:
            return get_full_panchang("Pune")
        except Exception:
            raise HTTPException(status_code=500, detail="Unable to compute Panchang data at this time.")


@router.post("/panchang/resolve-profile")
def resolve_profile(request: ProfileResolveRequest):
    try:
        birth_date = datetime.strptime(request.birth_date, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid birth_date format. Expected YYYY-MM-DD.")

    birth_time = None
    if request.birth_time:
        try:
            parts = request.birth_time.split(":")
            birth_time = dt_time(int(parts[0]), int(parts[1]))
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid birth_time format. Expected HH:MM (24h).")

    try:
        result = derive_natal_moon(
            birth_date=birth_date,
            birth_time=birth_time,
            city_name=request.birth_place or "Pune",
            lat=request.lat,
            lon=request.lon
        )
        result["name"] = request.name or ""
        return result
    except Exception as e:
        logger.error(f"Profile resolution failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to resolve birth chart. Check input parameters.")


@router.post("/panchang/decision")
def decision_assistant(request: DecisionRequest):
    try:
        city = request.city or "Pune"
        panchang_data = get_full_panchang(
            city_name=city,
            lat=request.lat,
            lon=request.lon,
            user_rashi=request.user_rashi,
            user_nakshatra=request.user_nakshatra
        )

        result = evaluate_decision(
            activity_type=request.activity,
            user_rashi=request.user_rashi,
            user_nakshatra=request.user_nakshatra,
            current_panchang=panchang_data
        )
        return result
    except Exception as e:
        logger.error(f"Decision evaluation failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Decision engine encountered an error.")


@router.get("/panchang/calendar.ics")
def panchang_calendar_ics(
    city: str = Query(default="Pune", description="City for festival and muhurta timings"),
    limit: int = Query(default=45, ge=1, le=120, description="Number of upcoming events to include")
):
    try:
        ics_content = generate_panchang_ics(city=city, limit=limit)
        return Response(
            content=ics_content,
            media_type="text/calendar",
            headers={
                "Content-Disposition": f'attachment; filename="vedic_panchang_{city.lower().replace(" ", "_")}.ics"',
                "Cache-Control": "public, max-age=3600"
            }
        )
    except Exception as e:
        logger.error(f"ICS generation failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to generate iCalendar export.")


@router.get("/festivals/today")
def festivals_today():
    try:
        return {"festivals": get_today_festivals()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/festivals/upcoming")
def festivals_upcoming(limit: int = 14):
    try:
        festivals_list = get_upcoming_festivals(limit)
        return {"festivals": festivals_list}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
