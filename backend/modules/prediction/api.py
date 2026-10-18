from fastapi import APIRouter, HTTPException, Request, Query
from modules.prediction.schemas import PredictionRequest, DomainRequest, ChatRequest
from modules.prediction.engine import analyse_all_domains
from modules.narrative.engine import NarrativeEngine
from modules.narrative.chat import ChatService
from modules.narrative.schemas import NarrativeJobRequest
from modules.narrative.jobs import create_job
from modules.kundali.cities import get_city
from modules.kundali.engine import calculate_kundali
from modules.kundali.api import KundaliService, KundaliRequest
from shared.cache.keys import compute_input_hash
from shared.logging.logger import get_logger

logger = get_logger("modules.prediction.api")
router = APIRouter(prefix="/api", tags=["Predictions & Domains"])

GLOBAL_DISCLAIMER = (
    "Vedic astrology interpretations represent traditional symbolic frameworks for self-reflection and personal growth. "
    "Outputs are non-binding and do not constitute professional medical, legal, or financial advice."
)

kundali_service = KundaliService()


class PredictionService:
    def analyse_domains(self, req: DomainRequest | PredictionRequest) -> dict:
        city = req.city or "Pune"
        k_req = KundaliRequest(
            year=req.year,
            month=req.month,
            day=req.day,
            hour=int(req.hour),
            minute=getattr(req, "minute", 0),
            city=city,
        )
        chart = kundali_service.compute_chart(k_req)
        res = analyse_all_domains(chart)
        res["disclaimer"] = GLOBAL_DISCLAIMER
        return res


@router.post("/prediction")
async def generate_prediction(
    request: Request,
    data: PredictionRequest,
    sync: bool = Query(False),
    include_narrative: bool = Query(True),
):
    """Generate AI Marriage and Career predictions using Vedic chart synthesis."""
    city = data.city or "Pune"

    # Synchronous legacy path if explicitly requested
    if sync:
        result = NarrativeEngine.generate_predictions(
            year=data.year,
            month=data.month,
            day=data.day,
            hour=data.hour,
            city=city,
        )
        request.session["prediction_chart"] = result["chart"]
        return {
            "marriage_prediction": result["marriage_prediction"],
            "career_prediction": result["career_prediction"],
            "marriage_score": result["raw_marriage_score"],
            "career_score": result["raw_career_score"],
            "disclaimer": GLOBAL_DISCLAIMER,
        }

    # Fast async path (< 500ms): Calculate domain scores immediately
    service = PredictionService()
    domains_res = service.analyse_domains(data)
    marriage_score = domains_res.get("domains", {}).get("marriage", {}).get("score", 75)
    career_score = domains_res.get("domains", {}).get("career", {}).get("score", 80)

    # Fail-open job enqueueing
    narrative_job_id = None
    if include_narrative:
        try:
            req_dict = {
                "year": data.year,
                "month": data.month,
                "day": data.day,
                "hour": data.hour,
                "city": city,
            }
            input_hash = compute_input_hash(req_dict)
            job_req = NarrativeJobRequest(
                input_hash=input_hash,
                year=data.year,
                month=data.month,
                day=data.day,
                hour=data.hour,
                city=city,
            )
            narrative_job_id = await create_job(job_req)
        except Exception as exc:
            logger.warning(f"Failed to enqueue narrative job (failing open): {exc}")

    return {
        "marriage_score": marriage_score,
        "career_score": career_score,
        "narrative_job_id": narrative_job_id,
        "domains": domains_res.get("domains"),
        "disclaimer": GLOBAL_DISCLAIMER,
    }


@router.post("/chat")
def astro_chat(request: Request, data: ChatRequest):
    """Chat with AstroAI using birth chart context from user session."""
    chart = request.session.get("prediction_chart") or request.session.get("kundali_chart")
    reply = ChatService.answer_general_chat(data.message, chart)
    return {"reply": reply, "disclaimer": GLOBAL_DISCLAIMER}


@router.post("/domains")
def get_life_domains(req: DomainRequest):
    """Calculate deep analysis across all 10 life domains for prediction UI."""
    service = PredictionService()
    return service.analyse_domains(req)


@router.post("/prediction/timing/{domain}")
def get_domain_timing(domain: str, req: DomainRequest):
    """Standalone endpoint returning concrete Dasha + Gochara timing windows for a specific domain."""
    k_req = KundaliRequest(
        year=req.year,
        month=req.month,
        day=req.day,
        hour=int(req.hour),
        minute=getattr(req, "minute", 0),
        city=req.city or "Pune",
    )
    chart = kundali_service.compute_chart(k_req)
    from modules.prediction.timing import compute_timing
    return compute_timing(chart, domain)
