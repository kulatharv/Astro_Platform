"""AI Prediction, 10 Life Domains Analysis, and Contextual Chat API routes."""

from fastapi import APIRouter, HTTPException, Request
from app.schemas.prediction import ChatRequest, DomainRequest, PredictionRequest
from app.services.ai_engine.chat_service import chat_service
from app.services.ai_engine.prediction_service import prediction_service
from app.services.astrology_engine.cities import get_city
from app.services.astrology_engine.domain_analysis import analyse_all_domains
from app.services.astrology_engine.kundali import calculate_kundali

router = APIRouter(prefix="/api", tags=["Predictions & Domains"])


@router.post("/prediction")
def generate_prediction(request: Request, data: PredictionRequest):
    """Generate AI Marriage and Career predictions using Vedic chart synthesis."""
    city = data.city or "Pune"
    result = prediction_service.generate_predictions(
        year=data.year,
        month=data.month,
        day=data.day,
        hour=data.hour,
        city=city,
    )

    # Store prediction chart strictly in current user session
    request.session["prediction_chart"] = result["chart"]

    return {
        "marriage_prediction": result["marriage_prediction"],
        "career_prediction": result["career_prediction"],
        "marriage_score": result["raw_marriage_score"],
        "career_score": result["raw_career_score"],
    }


@router.post("/chat")
def astro_chat(request: Request, data: ChatRequest):
    """Chat with AstroAI using birth chart context from user session."""
    chart = request.session.get("prediction_chart") or request.session.get("kundali_chart")
    reply = chat_service.answer_general_chat(data.message, chart)
    return {"reply": reply}


@router.post("/domains")
def get_life_domains(req: DomainRequest):
    """Calculate deep analysis across all 10 life domains for prediction UI."""
    coords = get_city(req.city)
    if coords is None:
        raise HTTPException(
            status_code=404,
            detail=f"City '{req.city}' not found. Please try a nearby major city.",
        )

    lat, lon, _ = coords
    chart = calculate_kundali(
        req.year, req.month, req.day,
        req.hour, req.minute, lat, lon
    )

    return analyse_all_domains(chart)
