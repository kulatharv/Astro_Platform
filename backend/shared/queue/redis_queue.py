"""Async Task Queue Interface & Redis Queue Wrapper."""

import os
import json
import logging
from typing import Any, Dict, Optional
from shared.cache.redis_client import CacheService

logger = logging.getLogger("shared.queue.redis_queue")


class JobStatus:
    QUEUED = "queued"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class RedisQueue:
    """Lightweight Redis/In-Memory task queue abstraction."""

    def __init__(self, queue_name: str = "narrative_queue", ttl: int = 86400):
        self.queue_name = queue_name
        self.ttl = ttl

    async def enqueue(self, job_name: str, payload: Dict[str, Any], job_id: Optional[str] = None) -> str:
        """Enqueue job metadata and payload into Redis list and state store."""
        jid = job_id or f"job:{payload.get('input_hash', 'unknown')}"
        state_key = f"narrative:job:{jid}"

        job_data = {
            "job_id": jid,
            "job_name": job_name,
            "payload": payload,
            "status": JobStatus.QUEUED,
            "result": None,
            "error": None,
            "retries": 0,
        }

        try:
            # Store initial job state
            CacheService.set(state_key, json.dumps(job_data), ttl=self.ttl)
            # Push job id into queue list
            queue_key = f"queue:{self.queue_name}"
            raw_list = CacheService.get(queue_key) or []
            if isinstance(raw_list, str):
                try:
                    raw_list = json.loads(raw_list)
                except Exception:
                    raw_list = []
            if jid not in raw_list:
                raw_list.append(jid)
            CacheService.set(queue_key, json.dumps(raw_list), ttl=self.ttl)
            logger.info(f"Enqueued job {jid} into queue {self.queue_name}")
        except Exception as exc:
            logger.error(f"Failed to enqueue job {jid}: {exc}")
            raise exc

        return jid

    async def get_job(self, job_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve job state payload."""
        state_key = f"narrative:job:{job_id}"
        val = CacheService.get(state_key)
        if not val:
            return None
        if isinstance(val, str):
            try:
                return json.loads(val)
            except Exception:
                return None
        return val


default_queue = RedisQueue()
