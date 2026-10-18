"""Kundali cache wrapper keyed by input_hash / chart parameters."""

from typing import Optional, Dict, Any
from shared.cache.redis_client import CacheService


class KundaliCache:
    def get(self, key: str) -> Optional[Dict[str, Any]]:
        return CacheService.get(f"kundali:{key}")

    def set(self, key: str, value: Dict[str, Any], ttl: int = 86400) -> None:
        CacheService.set(f"kundali:{key}", value, ttl=ttl)


kundali_cache = KundaliCache()
