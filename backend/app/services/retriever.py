from typing import List, Dict, Optional
from app.services.embeddings import embedding_service
from app.services.vector_store import vector_store
from app.services.web_search import web_search_service
from app.models.schemas import Source, SourceType, QueryMode


class RetrieverService:
    async def retrieve(
        self,
        query: str,
        mode: QueryMode,
        top_k: int = 5,
        document_ids: Optional[List[str]] = None,
    ) -> List[Source]:
        if mode == QueryMode.PDF:
            return await self._retrieve_from_pdf(query, top_k, document_ids or [])

        elif mode == QueryMode.WEB:
            return await self._retrieve_from_web(query, top_k)

        elif mode == QueryMode.HYBRID:
            # Get PDF sources
            pdf_sources = await self._retrieve_from_pdf(
                query, top_k // 2, document_ids or []
            )
            # Get web sources
            web_sources = await self._retrieve_from_web(query, top_k // 2)
            # Combine and rerank
            return self._merge_and_rerank(pdf_sources + web_sources, top_k)

        elif mode == QueryMode.RESTRICTED:
            return await self._retrieve_from_pdf(query, top_k, document_ids or [])

    async def _retrieve_from_pdf(
        self, query: str, top_k: int, document_ids: Optional[List[str]] = None
    ) -> List[Source]:
        query_embedding = embedding_service.embed_text(query)

        results = await vector_store.search(
            query_embedding=query_embedding, top_k=top_k, document_ids=document_ids
        )

        sources = []
        for result in results:
            sources.append(
                Source(
                    type=SourceType.PDF,
                    content=result["text"],
                    reference=f"Page {result['metadata']['page_number']}",
                    title=f"Document {result['metadata']['document_id']}",
                    relevance_score=result["similarity"],
                )
            )

        return sources

    async def _retrieve_from_web(self, query: str, top_k: int) -> List[Source]:
        results = await web_search_service.search(query, max_results=top_k)

        sources = []
        for result in results:
            sources.append(
                Source(
                    type=SourceType.WEB,
                    content=result["snippet"],
                    reference=result["url"],
                    title=result["title"],
                    relevance_score=result.get("score", 0.8),
                )
            )

        return sources

    def _merge_and_rerank(self, sources: List[Source], top_k: int) -> List[Source]:
        sorted_sources = sorted(
            sources, key=lambda x: x.relevance_score or 0, reverse=True
        )

        return sorted_sources[:top_k]


retriever_service = RetrieverService()
