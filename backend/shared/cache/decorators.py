"""Decorator for chart computation caching with fail-open semantics."""

import functools
import logging
from typing import Any, Callable
from shared.cache.keys import compute_input_hash, chart_cache_key
from shared.cache.envelope import serialize_chart, deserialize_chart
from shared.cache.redis_client import CacheService
from shared.cache.metrics import cache_metrics

logger = logging.getLogger("shared.cache.decorators")


def cached_chart(ttl: int = 2592000, engine_version: str = "2.0.0") -> Callable:
    """
    Decorator for birth chart calculation methods.
    Checks cache first by input hash; computes & stores on miss.
    Guarantees fail-open behavior (never raises cache errors to callers).
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            # 1. Extract request object or kwargs
            req_data = None
            if args:
                for arg in args:
                    if isinstance(arg, dict) or (hasattr(arg, "__dict__") and not hasattr(arg, "__class__") and not hasattr(arg, "__module__")):
                        req_data = arg
                        break
                    elif hasattr(arg, "__dict__") and type(arg).__name__ not in ("DummyService", "KundaliService") and "Service" not in type(arg).__name__:
                        req_data = arg
                        break
            if not req_data:
                req_data = kwargs



            # 2. Try cache lookup
            key = None
            try:
                input_hash = compute_input_hash(req_data)
                key = chart_cache_key(input_hash, engine_version=engine_version)
                cached_bytes = CacheService.get(key)
                if cached_bytes:
                    payload = deserialize_chart(cached_bytes)
                    cache_metrics.record_hit(trace_id=key)
                    logger.info(f"Chart cache HIT for key: {key}")
                    return payload
                else:
                    cache_metrics.record_miss(trace_id=key)
            except Exception as exc:
                cache_metrics.record_error(str(exc), trace_id=key)
                logger.warning(f"Chart cache lookup error (failing open): {exc}")

            # 3. Compute chart on miss or error
            logger.info(f"Chart cache MISS for key: {key or 'unknown'}")
            res = func(*args, **kwargs)

            # 4. Store in cache
            if key and res:
                try:
                    serialized = serialize_chart(res, engine_version=engine_version)
                    CacheService.set(key, serialized, ttl=ttl)
                except Exception as exc:
                    cache_metrics.record_error(str(exc), trace_id=key)
                    logger.warning(f"Chart cache store error (failing open): {exc}")

            return res


        return wrapper

    return decorator


cached_by_hash = cached_chart

