"""Cache metrics counter registry for observability."""

import logging
from typing import Dict, Any

logger = logging.getLogger("shared.cache.metrics")


class CacheMetrics:
    def __init__(self):
        self._hits = 0
        self._misses = 0
        self._errors = 0

    def record_hit(self, trace_id: str | None = None) -> None:
        self._hits += 1
        logger.info(f"[Cache HIT] trace_id={trace_id or 'none'} total_hits={self._hits}")

    def record_miss(self, trace_id: str | None = None) -> None:
        self._misses += 1
        logger.info(f"[Cache MISS] trace_id={trace_id or 'none'} total_misses={self._misses}")

    def record_error(self, err_msg: str, trace_id: str | None = None) -> None:
        self._errors += 1
        logger.warning(f"[Cache ERROR] trace_id={trace_id or 'none'} err={err_msg} total_errors={self._errors}")

    def get_stats(self) -> Dict[str, Any]:
        total = self._hits + self._misses
        hit_ratio = round((self._hits / total) * 100, 2) if total > 0 else 0.0
        return {
            "hits": self._hits,
            "misses": self._misses,
            "errors": self._errors,
            "total_requests": total,
            "hit_ratio_percent": hit_ratio,
        }

    def reset(self) -> None:
        self._hits = 0
        self._misses = 0
        self._errors = 0


cache_metrics = CacheMetrics()
