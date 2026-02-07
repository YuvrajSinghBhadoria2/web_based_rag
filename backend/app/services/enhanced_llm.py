"""
Enhanced LLM Service with Multi-Model Support
- Groq llama-3.1-8b-instant (Primary - Fast)
- Groq mixtral-8x7b-32768 (Secondary - Quality)
- Request queuing to prevent rate limits
- Response caching for repeated queries
"""

import aiohttp
import asyncio
import time
import hashlib
import json
from typing import List, Optional, Dict
from datetime import datetime
from dataclasses import dataclass
from enum import Enum

from app.models.schemas import Source
from app.config import settings


class ModelType(Enum):
    PRIMARY = "llama-3.1-8b-instant"  # Fast, good for simple queries
    SECONDARY = "mixtral-8x7b-32768"  # Better for complex queries
    FALLBACK = "llama-3.1-70b-versatile"  # Highest quality


@dataclass
class ModelConfig:
    name: str
    max_tokens: int
    temperature: float
    priority: int  # Lower = higher priority


# Model configurations
MODEL_CONFIGS: Dict[ModelType, ModelConfig] = {
    ModelType.PRIMARY: ModelConfig(
        name=getattr(settings, "GROQ_MODEL_PRIMARY", "llama-3.1-8b-instant"),
        max_tokens=2048,
        temperature=0.1,
        priority=1,
    ),
    ModelType.SECONDARY: ModelConfig(
        name=getattr(settings, "GROQ_MODEL_SECONDARY", "mixtral-8x7b-32768"),
        max_tokens=4096,
        temperature=0.1,
        priority=2,
    ),
    ModelType.FALLBACK: ModelConfig(
        name=getattr(settings, "GROQ_MODEL_FALLBACK", "llama-3.1-70b-versatile"),
        max_tokens=4096,
        temperature=0.1,
        priority=3,
    ),
}


class RequestQueue:
    """Simple async queue for serializing LLM requests"""

    def __init__(self, min_delay: float = 1.0):
        self.min_delay = min_delay
        self.last_request_time: float = 0
        self.lock = asyncio.Lock()

    async def acquire(self):
        """Wait until enough time has passed since last request"""
        async with self.lock:
            now = time.time()
            elapsed = now - self.last_request_time
            if elapsed < self.min_delay:
                await asyncio.sleep(self.min_delay - elapsed)
            self.last_request_time = time.time()


class ResponseCache:
    """Simple TTL cache for LLM responses"""

    def __init__(self, ttl_seconds: int = 300):
        self.ttl = ttl_seconds
        self._cache: Dict[str, tuple] = {}
        self.lock = asyncio.Lock()

    def _make_key(self, prompt: str, model: str) -> str:
        """Create cache key from prompt and model"""
        content = f"{model}:{prompt}"
        return hashlib.md5(content.encode()).hexdigest()

    async def get(self, prompt: str, model: str) -> Optional[str]:
        """Get cached response"""
        key = self._make_key(prompt, model)
        async with self.lock:
            if key in self._cache:
                response, timestamp = self._cache[key]
                if (datetime.now() - timestamp).total_seconds() < self.ttl:
                    return response
                del self._cache[key]
        return None

    async def set(self, prompt: str, model: str, response: str):
        """Cache a response"""
        key = self._make_key(prompt, model)
        async with self.lock:
            self._cache[key] = (response, datetime.now())

            # Clean old entries if cache is too large
            if len(self._cache) > 100:
                oldest = sorted(self._cache.items(), key=lambda x: x[1][1])[:10]
                for k, _ in oldest:
                    del self._cache[k]

    def clear(self):
        """Clear all cached responses"""
        self._cache.clear()


class EnhancedLLMService:
    """Enhanced LLM service with multi-model support and rate limiting"""

    def __init__(self):
        self.api_key = settings.GROQ_API_KEY
        self.base_url = "https://api.groq.com/openai/v1/chat/completions"
        self.request_queue = RequestQueue(min_delay=1.0)
        self.cache = ResponseCache(ttl_seconds=300)
        self.model_order = [
            ModelType.PRIMARY,
            ModelType.SECONDARY,
            ModelType.FALLBACK,
        ]
        self.max_retries = int(getattr(settings, "LLM_MAX_RETRIES", 5))
        self.retry_delay = int(getattr(settings, "LLM_RETRY_DELAY", 2))

    def _build_context(self, sources: List[Source]) -> str:
        """Build context string from sources"""
        if not sources:
            return "No context available."

        context_parts = []
        for i, source in enumerate(sources, 1):
            context_parts.append(
                f"[Source {i}] {source.title}\n"
                f"Reference: {source.reference}\n"
                f"Content: {source.content}\n"
            )

        return "\n\n".join(context_parts)

    def _get_system_prompt(self) -> str:
        """Get system prompt"""
        return """You are a precise assistant that answers questions using only the provided context.

Rules:
1. Base your answer ONLY on the provided context
2. When citing sources, use the actual page number or reference provided (e.g., "According to Page 21..." or "As stated on Page 34...")
3. Do NOT use generic citations like [Source 1] or [Source 2]
4. If the context doesn't contain enough information, say "I don't have enough information to answer this question"
5. Be concise and accurate
6. Do not make assumptions or use external knowledge
7. Write in a clear, professional tone"""

    def _build_prompt(self, query: str, pdf_context: str, web_context: str) -> str:
        """Build final prompt"""
        return f"""Context from Documents:
{pdf_context}

Context from Web:
{web_context}

Question: {query}

Provide a comprehensive answer based on the context above. Include source citations."""

    async def _call_groq(self, model: ModelType, prompt: str) -> Optional[str]:
        """Make API call to Groq with specific model"""
        config = MODEL_CONFIGS[model]

        payload = {
            "model": config.name,
            "messages": [
                {"role": "system", "content": self._get_system_prompt()},
                {"role": "user", "content": prompt},
            ],
            "temperature": config.temperature,
            "max_tokens": config.max_tokens,
        }

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        for attempt in range(self.max_retries):
            try:
                async with aiohttp.ClientSession() as session:
                    timeout = aiohttp.ClientTimeout(total=60)
                    async with session.post(
                        self.base_url, headers=headers, json=payload, timeout=timeout
                    ) as response:
                        if response.status == 429:
                            # Rate limited - wait and retry
                            delay = self.retry_delay * (2**attempt)
                            await asyncio.sleep(delay)
                            continue

                        if response.status != 200:
                            return None

                        data = await response.json()
                        return data["choices"][0]["message"]["content"]

            except Exception as e:
                if attempt < self.max_retries - 1:
                    delay = self.retry_delay * (2**attempt)
                    await asyncio.sleep(delay)
                    continue

        return None

    async def generate_answer(self, query: str, sources: List[Source]) -> str:
        """Generate answer with multi-model fallback"""

        # Build prompt
        pdf_context = self._build_context([s for s in sources if s.type.value == "pdf"])
        web_context = self._build_context([s for s in sources if s.type.value == "web"])
        prompt = self._build_prompt(query, pdf_context, web_context)

        # Acquire queue lock (prevent burst requests)
        await self.request_queue.acquire()

        # Try each model in order
        for model_type in self.model_order:
            # Check cache first
            cached = await self.cache.get(prompt, MODEL_CONFIGS[model_type].name)
            if cached:
                return cached

            # Try this model
            response = await self._call_groq(model_type, prompt)

            if response:
                # Cache successful response
                await self.cache.set(prompt, MODEL_CONFIGS[model_type].name, response)
                return response

        # All models failed
        raise Exception("All LLM models failed after retries")

    def get_model_info(self) -> Dict:
        """Get information about configured models"""
        return {
            "primary": MODEL_CONFIGS[ModelType.PRIMARY].name,
            "secondary": MODEL_CONFIGS[ModelType.SECONDARY].name,
            "fallback": MODEL_CONFIGS[ModelType.FALLBACK].name,
            "max_retries": self.max_retries,
            "retry_delay": self.retry_delay,
            "cache_ttl": self.cache.ttl,
        }

    def clear_cache(self):
        """Clear the response cache"""
        self.cache.clear()


# Create singleton instance
enhanced_llm_service = EnhancedLLMService()
