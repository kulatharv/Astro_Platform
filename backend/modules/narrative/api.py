from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import StreamingResponse
import asyncio

from modules.narrative.schemas import (
    NarrativeRequest,
    NarrativeResponse,
    ChatRequest,
    ChatResponse,
    NarrativeJobRequest,
    NarrativeJobStatus,
)
from modules.narrative.engine import NarrativeEngine
from modules.narrative.chat import ChatService
from modules.narrative.jobs import create_job, get_job
from shared.cache.keys import compute_input_hash
from shared.logging.logger import get_logger

logger = get_logger("modules.narrative.api")
router = APIRouter(prefix="/api/narrative", tags=["narrative"])


class NarrativeService:
    def generate(self, req: NarrativeRequest) -> NarrativeResponse:
        result = NarrativeEngine.generate_predictions(
            year=req.year,
            month=req.month,
            day=req.day,
            hour=req.hour,
            city=req.city,
            lang=req.lang
        )
        return NarrativeResponse(**result)

    async def generate_async(self, req: NarrativeRequest) -> str:
        input_hash = compute_input_hash(req.dict())
        job_req = NarrativeJobRequest(
            input_hash=input_hash,
            year=req.year,
            month=req.month,
            day=req.day,
            hour=req.hour,
            city=req.city,
            lang=req.lang,
        )
        return await create_job(job_req)

    async def get_status(self, job_id: str) -> NarrativeJobStatus:
        st = await get_job(job_id)
        if not st:
            raise HTTPException(status_code=404, detail="Narrative job not found.")
        return st

    def chat(self, req: ChatRequest) -> ChatResponse:
        result = ChatService.answer_kundali_chat(
            message=req.message,
            chart=req.chart,
            lang=req.lang
        )
        return ChatResponse(**result)


@router.post("/generate", response_model=NarrativeResponse)
async def generate_narrative(req: NarrativeRequest, async_job: bool = Query(False, alias="async")):
    try:
        service = NarrativeService()
        if async_job:
            job_id = await service.generate_async(req)
            return {"job_id": job_id, "status": "queued"}
        return service.generate(req)
    except Exception as e:
        logger.error(f"Narrative generation failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Narrative generation failed.")


@router.get("/{job_id}", response_model=NarrativeJobStatus)
async def get_narrative_job_status(job_id: str):
    service = NarrativeService()
    return await service.get_status(job_id)


@router.get("/{job_id}/stream")
async def stream_narrative_job(job_id: str):
    """Server-Sent Events (SSE) streaming endpoint for job progress."""
    async def event_generator():
        service = NarrativeService()
        while True:
            st = await service.get_status(job_id)
            payload = st.model_dump_json() if hasattr(st, "model_dump_json") else st.json()
            yield f"data: {payload}\n\n"
            if st.status in ("completed", "failed"):
                break
            await asyncio.sleep(1)

    return StreamingResponse(event_generator(), media_type="text/event-stream")


@router.post("/chat", response_model=ChatResponse)
def chat_narrative(req: ChatRequest):
    try:
        service = NarrativeService()
        return service.chat(req)
    except Exception as e:
        logger.error(f"Chat service failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Chat engine failed.")
