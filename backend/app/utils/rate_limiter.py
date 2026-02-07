"""
Rate Limiting Handler for Web Search API

This module provides:
1. Exponential backoff retry logic
2. Request caching
3. Rate limit detection and handling
4. Request queuing
"""

import asyncio
import time
from typing import List, Dict, Optional, Callable
from dataclasses import dataclass
from datetime import datetime, timedelta
import threading


@dataclass
class RateLimitConfig:
    max_requests_per_minute: int = 30
    max_requests_per_hour: int = 500
    retry_base_delay: float = 2.0
    max_retry_attempts: int = 3
    cache_ttl_seconds: int = 300


class RateLimiter:
    """Token bucket rate limiter"""

    def __init__(self, config: RateLimitConfig = None):
        self.config = config or RateLimitConfig()
        self.tokens = self.config.max_requests_per_minute
        self.last_update = datetime.now()
        self.lock = threading.Lock()

    def acquire(self) -> bool:
        with self.lock:
            now = datetime.now()
            elapsed = (now - self.last_update).total_seconds()

            # Refill tokens
            tokens_to_add = elapsed * (self.config.max_requests_per_minute / 60)
            self.tokens = min(
                self.config.max_requests_per_minute, self.tokens + tokens_to_add
            )

            if self.tokens >= 1:
                self.tokens -= 1
                self.last_update = now
                return True

            return False

    def wait_for_token(self, timeout: float = 60) -> bool:
        start = time.time()
        while time.time() - start < timeout:
            if self.acquire():
                return True
            time.sleep(0.1)
        return False


class RequestCache:
    """Simple TTL-based cache"""

    def __init__(self, ttl_seconds: int = 300):
        self.ttl = ttl_seconds
        self._cache: Dict[str, tuple] = {}
        self.lock = threading.Lock()

    def get(self, key: str) -> Optional[List[Dict]]:
        with self.lock:
            if key in self._cache:
                data, timestamp = self._cache[key]
                if (datetime.now() - timestamp).total_seconds() < self.ttl:
                    return data
                del self._cache[key]
        return None

    def set(self, key: str, data: List[Dict]):
        with self.lock:
            self._cache[key] = (data, datetime.now())

            # Clean old entries if cache is too large
            if len(self._cache) > 100:
                oldest = sorted(self._cache.items(), key=lambda x: x[1][1])[:10]
                for k, _ in oldest:
                    del self._cache[k]

    def clear(self):
        with self.lock:
            self._cache.clear()


class RateLimitedWebSearch:
    """Web search with rate limiting and caching"""

    def __init__(self, search_func: Callable, config: RateLimitConfig = None):
        self.config = config or RateLimitConfig()
        self.rate_limiter = RateLimiter(self.config)
        self.cache = RequestCache(self.config.cache_ttl_seconds)
        self.search_func = search_func

    async def search(
        self, query: str, max_results: int = 5, use_cache: bool = True
    ) -> List[Dict]:
        cache_key = f"{query}_{max_results}"

        # Check cache
        if use_cache:
            cached = self.cache.get(cache_key)
            if cached:
                return cached

        # Wait for rate limit
        if not self.rate_limiter.wait_for_token():
            return []

        # Retry with exponential backoff
        for attempt in range(self.config.max_retry_attempts):
            try:
                results = await self.search_func(query, max_results)

                if results:
                    if use_cache:
                        self.cache.set(cache_key, results)
                    return results

                # If empty results, might be rate limited
                await asyncio.sleep(self.config.retry_base_delay * (attempt + 1))

            except Exception as e:
                if attempt < self.config.max_retry_attempts - 1:
                    await asyncio.sleep(self.config.retry_base_delay * (2**attempt))
                continue

        return []

    def get_cache_stats(self) -> Dict:
        return {
            "cached_items": len(self.cache._cache),
            "ttl_seconds": self.config.cache_ttl_seconds,
            "rate_limit_per_minute": self.config.max_requests_per_minute,
        }

    def clear_cache(self):
        self.cache.clear()


# Example usage with Serper API
async def serper_search(query: str, max_results: int = 5) -> List[Dict]:
    """Example Serper API search function"""
    import aiohttp

    api_key = "92dc65b1fe92ca96ece7d0b02729f2d29f68f4fda5e31908e8d447a808e9797f"
    url = "https://serpapi.com/search"

    params = {
        "engine": "google",
        "q": query,
        "api_key": api_key,
        "num": max_results,
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            if response.status == 200:
                data = await response.json()
                results = data.get("organic_results", [])
                return [
                    {
                        "title": r.get("title", ""),
                        "url": r.get("link", ""),
                        "snippet": r.get("snippet", ""),
                        "score": 0.8,
                    }
                    for r in results[:max_results]
                ]
            return []


# Create rate-limited instance
rate_limited_search = RateLimitedWebSearch(serper_search)


if __name__ == "__main__":

    async def test():
        # Test the rate-limited search
        results = await rate_limited_search.search("Python programming", 3)
        print(f"Found {len(results)} results")
        print(f"Cache stats: {rate_limited_search.get_cache_stats()}")

        # Test cache hit
        results2 = await rate_limited_search.search("Python programming", 3)
        print(f"Cache hit: {len(results2)} results")

    asyncio.run(test())
