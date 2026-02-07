"""
Unified Web Search Service
Supports multiple search providers:
- Tavily (AI-optimized, RAG-ready)
- Serper (Google search)
- Brave Search (Privacy-focused)
- You.com (AI-ready)
"""

import aiohttp
import asyncio
import time
from typing import List, Dict, Optional, Literal
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
import json

from app.config import settings


class SearchProvider(Enum):
    TAVILY = "tavily"
    SERPER = "serper"
    BRAVE = "brave"
    YOUCOM = "youcom"


@dataclass
class SearchResult:
    title: str
    url: str
    snippet: str
    score: float = 0.8
    provider: str = "unknown"


@dataclass
class SearchConfig:
    provider: SearchProvider
    api_key: str
    max_results: int = 5
    timeout: int = 15
    retry_attempts: int = 3
    retry_delay: float = 2.0
    cache_ttl: int = 300  # 5 minutes


class BaseSearchProvider(ABC):
    """Abstract base class for search providers"""

    def __init__(self, config: SearchConfig):
        self.config = config
        self._cache: Dict[str, tuple] = {}

    @abstractmethod
    async def search(self, query: str) -> List[SearchResult]:
        pass

    @abstractmethod
    def _format_results(self, raw_data) -> List[SearchResult]:
        pass

    def _get_cache(self, query: str) -> Optional[List[SearchResult]]:
        if query in self._cache:
            data, timestamp = self._cache[query]
            if time.time() - timestamp < self.config.cache_ttl:
                return data
            del self._cache[query]
        return None

    def _set_cache(self, query: str, results: List[SearchResult]):
        self._cache[query] = (results, time.time())

        # Clean old cache entries
        if len(self._cache) > 100:
            oldest = sorted(self._cache.keys(), key=lambda k: self._cache[k][1])[:10]
            for k in oldest:
                del self._cache[k]

    async def _make_request(
        self, url: str, params: Dict = None, headers: Dict = None, method: str = "GET"
    ) -> Dict:
        """Make HTTP request with retry logic"""

        for attempt in range(self.config.retry_attempts):
            try:
                timeout = aiohttp.ClientTimeout(total=self.config.timeout)

                async with aiohttp.ClientSession(timeout=timeout) as session:
                    if method == "GET":
                        async with session.get(
                            url, params=params, headers=headers
                        ) as response:
                            if response.status == 429:
                                await asyncio.sleep(
                                    self.config.retry_delay * (attempt + 1)
                                )
                                continue
                            if response.status != 200:
                                return {}
                            return await response.json()
                    else:
                        async with session.post(
                            url, json=params, headers=headers
                        ) as response:
                            if response.status == 429:
                                await asyncio.sleep(
                                    self.config.retry_delay * (attempt + 1)
                                )
                                continue
                            if response.status != 200:
                                return {}
                            return await response.json()

            except Exception as e:
                if attempt < self.config.retry_attempts - 1:
                    await asyncio.sleep(self.config.retry_delay)
                continue

        return {}


class TavilySearchProvider(BaseSearchProvider):
    """Tavily AI Search - Optimized for RAG and AI applications"""

    def __init__(self, api_key: str, max_results: int = 5):
        config = SearchConfig(
            provider=SearchProvider.TAVILY, api_key=api_key, max_results=max_results
        )
        super().__init__(config)
        self.base_url = "https://api.tavily.com/search"

    async def search(self, query: str) -> List[SearchResult]:
        # Check cache first
        cached = self._get_cache(query)
        if cached:
            return cached

        payload = {
            "api_key": self.config.api_key,
            "query": query,
            "search_depth": "advanced",
            "max_results": self.config.max_results,
            "include_answer": True,
            "include_raw_content": False,
            "include_images": False,
        }

        data = await self._make_request(self.base_url, params=payload, method="POST")

        results = self._format_results(data)
        self._set_cache(query, results)
        return results

    def _format_results(self, data: Dict) -> List[SearchResult]:
        results = []

        search_results = data.get("results", [])

        for i, result in enumerate(search_results[: self.config.max_results]):
            results.append(
                SearchResult(
                    title=result.get("title", ""),
                    url=result.get("url", ""),
                    snippet=result.get("content", ""),
                    score=result.get("score", 0.9 - (i * 0.05)),
                    provider="tavily",
                )
            )

        return results


class SerperSearchProvider(BaseSearchProvider):
    """Serper.dev - Google Search API"""

    def __init__(self, api_key: str, max_results: int = 5):
        config = SearchConfig(
            provider=SearchProvider.SERPER, api_key=api_key, max_results=max_results
        )
        super().__init__(config)
        self.base_url = "https://serpapi.com/search"

    async def search(self, query: str) -> List[SearchResult]:
        cached = self._get_cache(query)
        if cached:
            return cached

        params = {
            "engine": "google",
            "q": query,
            "api_key": self.config.api_key,
            "num": self.config.max_results,
        }

        data = await self._make_request(self.base_url, params=params)

        results = self._format_results(data)
        self._set_cache(query, results)
        return results

    def _format_results(self, data: Dict) -> List[SearchResult]:
        results = []

        organic_results = data.get("organic_results", [])

        for i, result in enumerate(organic_results[: self.config.max_results]):
            results.append(
                SearchResult(
                    title=result.get("title", ""),
                    url=result.get("link", ""),
                    snippet=result.get("snippet", ""),
                    score=0.8 - (i * 0.05),
                    provider="serper",
                )
            )

        return results


class BraveSearchProvider(BaseSearchProvider):
    """Brave Search API - Privacy-focused"""

    def __init__(self, api_key: str, max_results: int = 5):
        config = SearchConfig(
            provider=SearchProvider.BRAVE, api_key=api_key, max_results=max_results
        )
        super().__init__(config)
        self.base_url = "https://api.search.brave.com/res/v1/web/search"

    async def search(self, query: str) -> List[SearchResult]:
        cached = self._get_cache(query)
        if cached:
            return cached

        headers = {
            "Accept": "application/json",
            "X-Subscription-Token": self.config.api_key,
        }

        params = {"q": query, "count": self.config.max_results}

        data = await self._make_request(self.base_url, params=params, headers=headers)

        results = self._format_results(data)
        self._set_cache(query, results)
        return results

    def _format_results(self, data: Dict) -> List[SearchResult]:
        results = []

        web_results = data.get("web", {}).get("results", [])

        for i, result in enumerate(web_results[: self.config.max_results]):
            results.append(
                SearchResult(
                    title=result.get("title", ""),
                    url=result.get("url", ""),
                    snippet=result.get("description", ""),
                    score=0.85 - (i * 0.05),
                    provider="brave",
                )
            )

        return results


class YouComSearchProvider(BaseSearchProvider):
    """You.com - AI-Optimized Search"""

    def __init__(self, api_key: str, max_results: int = 5):
        config = SearchConfig(
            provider=SearchProvider.YOUCOM, api_key=api_key, max_results=max_results
        )
        super().__init__(config)
        self.base_url = "https://api.you.com/search"

    async def search(self, query: str) -> List[SearchResult]:
        cached = self._get_cache(query)
        if cached:
            return cached

        headers = {"Authorization": f"Bearer {self.config.api_key}"}

        params = {"query": query, "num": self.config.max_results}

        data = await self._make_request(self.base_url, params=params, headers=headers)

        results = self._format_results(data)
        self._set_cache(query, results)
        return results

    def _format_results(self, data: Dict) -> List[SearchResult]:
        results = []

        search_results = data.get("results", [])

        for i, result in enumerate(search_results[: self.config.max_results]):
            results.append(
                SearchResult(
                    title=result.get("title", ""),
                    url=result.get("url", ""),
                    snippet=result.get("snippet", ""),
                    score=result.get("score", 0.85 - (i * 0.05)),
                    provider="youcom",
                )
            )

        return results


class WebSearchService:
    """
    Unified web search service with provider selection
    """

    def __init__(self):
        # Default to Tavily (RAG-optimized)
        self.default_provider = SearchProvider.TAVILY
        self._providers: Dict[SearchProvider, BaseSearchProvider] = {}
        self._initialize_providers()

    def _initialize_providers(self):
        """Initialize available search providers"""

        # Tavily (Recommended for RAG)
        tavily_key = getattr(settings, "TAVILY_API_KEY", None) or getattr(
            settings, "SERPER_API_KEY", None
        )
        if tavily_key:
            self._providers[SearchProvider.TAVILY] = TavilySearchProvider(
                tavily_key, max_results=5
            )

        # Serper
        serper_key = settings.SERPER_API_KEY
        if serper_key:
            self._providers[SearchProvider.SERPER] = SerperSearchProvider(
                serper_key, max_results=5
            )

    def set_provider(self, provider: SearchProvider):
        """Change the active search provider"""
        if provider in self._providers:
            self.default_provider = provider

    async def search(
        self,
        query: str,
        max_results: int = 5,
        provider: Optional[SearchProvider] = None,
    ) -> List[Dict]:
        """
        Search using specified or default provider

        Args:
            query: Search query
            max_results: Maximum number of results
            provider: Specific provider to use (optional)

        Returns:
            List of search results
        """
        search_provider = provider or self.default_provider

        if search_provider not in self._providers:
            # Fallback to any available provider
            if self._providers:
                search_provider = list(self._providers.keys())[0]
            else:
                return []

        provider = self._providers[search_provider]
        results = await provider.search(query)

        # Convert to dict format
        return [
            {
                "title": r.title,
                "url": r.url,
                "snippet": r.snippet,
                "score": r.score,
            }
            for r in results
        ]

    def get_available_providers(self) -> List[str]:
        """Get list of available providers"""
        return [p.value for p in self._providers.keys()]

    def get_current_provider(self) -> str:
        """Get current provider"""
        return self.default_provider.value


# Factory function to create service
def create_web_search_service(provider: str = "tavily") -> WebSearchService:
    """Create web search service with specified provider"""
    service = WebSearchService()

    provider_map = {
        "tavily": SearchProvider.TAVILY,
        "serper": SearchProvider.SERPER,
        "brave": SearchProvider.BRAVE,
        "youcom": SearchProvider.YOUCOM,
    }

    if provider.lower() in provider_map:
        service.set_provider(provider_map[provider.lower()])

    return service


# Default instance
web_search_service = WebSearchService()
