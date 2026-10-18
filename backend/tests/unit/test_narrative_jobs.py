"""Unit tests for narrative job state management."""

import asyncio
import pytest
from shared.cache.redis_client import CacheService
from modules.narrative.schemas import NarrativeJobRequest, NarrativeJobResult
from modules.narrative.jobs import create_job, get_job, mark_running, mark_completed, mark_failed
from shared.queue.redis_queue import JobStatus


def test_narrative_job_lifecycle():
    async def _test():
        CacheService.clear()
        req = NarrativeJobRequest(
            input_hash="hash12345",
            year=1990,
            month=5,
            day=15,
            hour=14.5,
            city="Pune",
            lang="en",
        )

        job_id = await create_job(req)
        assert len(job_id) == 16

        # Check queued status
        st = await get_job(job_id)
        assert st is not None
        assert st.status == JobStatus.QUEUED

        # Transition to RUNNING
        await mark_running(job_id)
        st_running = await get_job(job_id)
        assert st_running.status == JobStatus.RUNNING

        # Transition to COMPLETED
        res = NarrativeJobResult(
            marriage_prediction="Strong marriage prospects",
            career_prediction="Leadership roles indicated",
            raw_marriage_score=85,
            raw_career_score=90,
        )
        await mark_completed(job_id, res)
        st_done = await get_job(job_id)
        assert st_done.status == JobStatus.COMPLETED
        assert st_done.result.raw_marriage_score == 85

    asyncio.run(_test())
