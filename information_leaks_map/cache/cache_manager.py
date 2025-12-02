import time
from typing import Any, Dict, Optional, Tuple


class CacheManager:
    """
    Simple cache manager with TTL support.
    """
    def __init__(self, default_ttl: int = 3600):
        """
        Initialize cache manager.
        
        :param default_ttl: Default time-to-live in seconds (default: 1 hour)
        """
        self.cache: Dict[Tuple, Tuple[Any, float]] = {}
        self.default_ttl = default_ttl

    def _make_key(self, key: str, params: Dict) -> Tuple:
        """
        Create a cache key from URL and parameters.
        
        :param key: Base URL or key
        :param params: Dictionary of parameters
        :return: Hashable tuple for use as cache key
        """
        # Convert params to a hashable format
        if isinstance(params, dict):
            params_tuple = tuple(sorted(params.items()))
        else:
            # If params is not a dict (e.g., headers), convert to string representation
            params_tuple = (str(params),)
        return (key, params_tuple)

    def get(self, key: str, params: Dict) -> Optional[Any]:
        """
        Get value from cache if it exists and hasn't expired.
        
        :param key: Cache key (usually URL)
        :param params: Parameters dictionary
        :return: Cached value or None if not found or expired
        """
        cache_key = self._make_key(key, params)
        if cache_key in self.cache:
            value, expiry_time = self.cache[cache_key]
            if time.time() < expiry_time:
                return value
            else:
                # Expired, remove from cache
                del self.cache[cache_key]
        return None

    def set(self, key: str, params: Dict, value: Any, ttl: Optional[int] = None) -> None:
        """
        Store value in cache with TTL.
        
        :param key: Cache key (usually URL)
        :param params: Parameters dictionary
        :param value: Value to cache
        :param ttl: Time-to-live in seconds (uses default if not provided)
        """
        cache_key = self._make_key(key, params)
        expiry_time = time.time() + (ttl if ttl is not None else self.default_ttl)
        self.cache[cache_key] = (value, expiry_time)
        
    def clear(self) -> None:
        """Clear all cached values."""
        self.cache.clear()
    
    def cleanup_expired(self) -> None:
        """Remove all expired entries from cache."""
        current_time = time.time()
        expired_keys = [
            key for key, (_, expiry_time) in self.cache.items()
            if current_time >= expiry_time
        ]
        for key in expired_keys:
            del self.cache[key]