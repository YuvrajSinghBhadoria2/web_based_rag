import aiohttp
import asyncio
import time
from typing import List
from app.models.schemas import Source
from app.config import settings


class LLMService:
    def __init__(self):
        self.api_key = settings.GROQ_API_KEY
        self.model = settings.GROQ_MODEL
        self.base_url = "https://api.groq.com/openai/v1/chat/completions"
        self.max_retries = 5
        self.base_delay = 3

    async def generate_answer(self, query: str, sources: List[Source]) -> str:
        pdf_context = self._build_context([s for s in sources if s.type.value == "pdf"])
        web_context = self._build_context([s for s in sources if s.type.value == "web"])

        prompt = self._build_prompt(query, pdf_context, web_context)

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": self._get_system_prompt()},
                {"role": "user", "content": prompt},
            ],
            "temperature": settings.TEMPERATURE,
            "max_tokens": settings.MAX_TOKENS,
        }

        for attempt in range(self.max_retries):
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.post(
                        self.base_url,
                        headers=headers,
                        json=payload,
                        timeout=aiohttp.ClientTimeout(total=60),
                    ) as response:
                        if response.status == 429:
                            delay = self.base_delay * (2**attempt)
                            await asyncio.sleep(delay)
                            continue

                        if response.status != 200:
                            raise Exception(f"LLM API failed: {response.status}")

                        data = await response.json()
                        answer = data["choices"][0]["message"]["content"]
                        return answer

            except Exception as e:
                if attempt < self.max_retries - 1:
                    delay = self.base_delay * (2**attempt)
                    await asyncio.sleep(delay)
                    continue
                raise

        raise Exception("LLM generation failed after retries")

    def _build_context(self, sources: List[Source]) -> str:
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
        return """You are a precise assistant that answers questions using only the provided context.

Rules:
1. Base your answer ONLY on the provided context
2. Cite sources using [Source N] notation
3. If the context doesn't contain enough information, say "I don't have enough information to answer this question"
4. Be concise and accurate
5. Do not make assumptions or use external knowledge"""

    def _build_prompt(self, query: str, pdf_context: str, web_context: str) -> str:
        return f"""Context from Documents:
{pdf_context}

Context from Web:
{web_context}

Question: {query}

Provide a comprehensive answer based on the context above. Include source citations."""


llm_service = LLMService()
