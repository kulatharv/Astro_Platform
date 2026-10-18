"""Background narrative generation worker process."""

import asyncio
import logging
from shared.logging.logger import get_logger
from shared.queue.redis_queue import default_queue, JobStatus
from modules.narrative.jobs import get_job, mark_running, mark_completed, mark_failed
from modules.narrative.engine import NarrativeEngine
from modules.narrative.schemas import NarrativeJobResult

logger = get_logger("workers.narrative_worker")


async def process_job(job_id: str, max_retries: int = 3):
    """Execute narrative LLM generation for a queued job."""
    job_status = await get_job(job_id)
    if not job_status or job_status.status == JobStatus.COMPLETED:
        return

    await mark_running(job_id)
    logger.info(f"Processing narrative job {job_id}...")

    # Load original request params from state
    from shared.cache.redis_client import CacheService
    import json
    raw = CacheService.get(f"narrative:job:{job_id}")
    data = json.loads(raw) if isinstance(raw, str) else raw
    req_dict = data.get("request", {})

    attempt = 0
    while attempt < max_retries:
        attempt += 1
        try:
            res_dict = NarrativeEngine.generate_predictions(
                year=req_dict.get("year", 1990),
                month=req_dict.get("month", 1),
                day=req_dict.get("day", 1),
                hour=req_dict.get("hour", 12.0),
                city=req_dict.get("city", "Pune"),
                lang=req_dict.get("lang", "en"),
            )
            result = NarrativeJobResult(
                marriage_prediction=res_dict.get("marriage_prediction"),
                career_prediction=res_dict.get("career_prediction"),
                raw_marriage_score=res_dict.get("raw_marriage_score"),
                raw_career_score=res_dict.get("raw_career_score"),
                chart=res_dict.get("chart"),
            )
            await mark_completed(job_id, result)
            logger.info(f"Narrative job {job_id} completed successfully.")
            return
        except Exception as exc:
            logger.warning(f"Attempt {attempt}/{max_retries} failed for job {job_id}: {exc}")
            if attempt >= max_retries:
                await mark_failed(job_id, f"LLM narrative generation failed after {max_retries} attempts: {exc}")
                return
            await asyncio.sleep(2 ** attempt)


async def run_worker():
    """Worker event loop pulling jobs from Redis queue."""
    logger.info("Narrative worker started listening for jobs...")
    while True:
        try:
            from shared.cache.redis_client import CacheService
            import json
            queue_key = "queue:narrative_queue"
            raw_list = CacheService.get(queue_key)
            job_ids = json.loads(raw_list) if isinstance(raw_list, str) else (raw_list or [])

            if job_ids:
                job_id = job_ids.pop(0)
                CacheService.set(queue_key, json.dumps(job_ids))
                await process_job(job_id)
            else:
                await asyncio.sleep(0.5)
        except Exception as exc:
            logger.error(f"Worker loop error: {exc}")
            await asyncio.sleep(1)


if __name__ == "__main__":
    asyncio.run(run_worker())
