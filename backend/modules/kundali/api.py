"""Kundali generation, Chart calculation, PDF download, and Kundali chat API routes."""

from datetime import datetime, timedelta
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import StreamingResponse
import swisseph as swe

from modules.kundali.schemas import BirthData, KundaliChatRequest, KundaliRequest
from modules.kundali.cities import CITIES, get_city
from modules.kundali.houses import calculate_lagna
from modules.kundali.engine import calculate_kundali
from modules.kundali.planets import calculate_all_planets
try:
    from modules.narrative.chat import chat_service
except ImportError:
    from app.services.ai_engine.chat_service import chat_service

try:
    from workers.pdf_worker import generate_kundali_pdf_buffer
except ImportError:
    from app.services.pdf_service import generate_kundali_pdf_buffer

router = APIRouter(prefix="/api", tags=["Kundali & Charts"])


from shared.cache.decorators import cached_chart


class KundaliService:
    @cached_chart(ttl=2592000)
    def compute_chart(self, req: KundaliRequest) -> dict:
        coords = get_city(req.city)
        if coords is None:
            raise HTTPException(
                status_code=400,
                detail=f"City '{req.city}' not found in database. Please try a nearby major city.",
            )
        lat, lon, tz = coords

        ist_offset = 5.5
        if tz != ist_offset:
            dt_local = datetime(req.year, req.month, req.day, req.hour, req.minute)
            dt_ist = dt_local + timedelta(hours=(ist_offset - tz))
            year, month, day = dt_ist.year, dt_ist.month, dt_ist.day
            hour, minute = dt_ist.hour, dt_ist.minute
        else:
            year, month, day, hour, minute = req.year, req.month, req.day, req.hour, req.minute

        return calculate_kundali(year, month, day, hour, minute, lat, lon)


    def get_chart(self, chart_hash: str) -> dict:
        from modules.kundali.cache import kundali_cache
        return kundali_cache.get(chart_hash) or {}

    def compute_varga(self, chart_hash: str, varga: str) -> dict:
        from modules.kundali.varga import calculate_navamsa
        return {"varga": varga, "chart_hash": chart_hash}


@router.get("/cities")
def get_cities():
    """Return sorted list of all supported city names."""
    return sorted(CITIES.keys())


@router.post("/generate-chart")
def generate_chart_api(data: BirthData):
    """Generate basic planetary degrees and Lagna for chart rendering."""
    swe.set_sid_mode(swe.SIDM_LAHIRI)
    jd = swe.julday(data.year, data.month, data.day, data.hour)
    planets = calculate_all_planets(jd)

    lagna_degree, lagna_sign = calculate_lagna(jd)

    return {
        "basic_details": {
            "date": f"{data.day:02d}-{data.month:02d}-{data.year}",
            "time": data.hour,
            "lagna": lagna_sign,
            "lagna_degree": round(lagna_degree % 30.0, 2),
        },
        "planets": planets,
    }


kundali_service = KundaliService()


@router.post("/kundali")
def get_kundali(request: Request, data: KundaliRequest):
    """Calculate comprehensive Vedic Kundali with D9, Yogas, Doshas, and Dasha."""
    result = kundali_service.compute_chart(data)
    result["disclaimer"] = (
        "Vedic astrology interpretations represent traditional symbolic frameworks for self-reflection and personal growth. "
        "Outputs are non-binding and do not constitute professional medical, legal, or financial advice."
    )

    request.session["kundali_chart"] = result
    return result



@router.get("/download-kundali")
def download_kundali(request: Request):
    """Generate and return an in-memory PDF report for the session's Kundali."""
    chart = request.session.get("kundali_chart")
    if not chart:
        raise HTTPException(
            status_code=400,
            detail="No Kundali chart found in current session. Please calculate a chart first.",
        )

    pdf_buffer = generate_kundali_pdf_buffer(chart)
    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=AstroLogic_Kundali_Report.pdf"},
    )


@router.post("/kundali-chat")
def kundali_chat(data: KundaliChatRequest):
    """Contextual life questions assistant using natal chart positions."""
    return chat_service.answer_kundali_chat(data.message, data.chart)
