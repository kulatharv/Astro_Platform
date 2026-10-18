"""Unit tests for shared queue infrastructure."""

import asyncio
import pytest
from shared.queue.redis_queue import RedisQueue, JobStatus
from shared.cache.redis_client import CacheService


def test_queue_enqueue_and_get():
    async def _test():
        CacheService.clear()
        queue = RedisQueue(queue_name="test_queue")
        payload = {"input_hash": "abc123hash", "data": "test_data"}

        job_id = await queue.enqueue("test_job", payload, job_id="job_001")
        assert job_id == "job_001"

        job = await queue.get_job("job_001")
        assert job is not None
        assert job["job_id"] == "job_001"
        assert job["status"] == JobStatus.QUEUED
        assert job["payload"]["data"] == "test_data"

    asyncio.run(_test())
