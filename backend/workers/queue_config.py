"""Background task queue configuration."""

import os
from typing import Dict, Any

QUEUE_NAME = "pdf_generation_queue"
MAX_RETRIES = 3
TASK_TIMEOUT = 60

queue_settings: Dict[str, Any] = {
    "queue_name": QUEUE_NAME,
    "max_retries": MAX_RETRIES,
    "task_timeout": TASK_TIMEOUT,
    "redis_url": os.getenv("REDIS_URL", "redis://localhost:6379/0"),
}
