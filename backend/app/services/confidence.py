from typing import List
from app.models.schemas import Source
from app.services.embeddings import embedding_service


class ConfidenceService:
    def calculate_confidence(
        self, query: str, answer: str, sources: List[Source]
    ) -> float:
        factors = {}

        # Factor 1: Source count (25%)
        source_count = len(sources)
        if source_count == 0:
            factors["source_count"] = 0
        elif source_count == 1:
            factors["source_count"] = 15
        elif source_count == 2:
            factors["source_count"] = 20
        else:
            factors["source_count"] = 25

        # Factor 2: Average relevance score (30%)
        if sources:
            avg_relevance = sum(s.relevance_score or 0 for s in sources) / len(sources)
            factors["source_relevance"] = avg_relevance * 30
        else:
            factors["source_relevance"] = 0

        # Factor 3: Semantic similarity (30%)
        try:
            query_emb = embedding_service.embed_text(query)
            answer_text = answer[:1000] if len(answer) > 1000 else answer
            answer_emb = embedding_service.embed_text(answer_text)
            similarity = embedding_service.calculate_similarity(query_emb, answer_emb)
            factors["semantic_similarity"] = similarity * 30
        except Exception:
            factors["semantic_similarity"] = 0

        # Factor 4: Citation density (15%)
        citation_count = answer.count("[Source")
        if citation_count == 0:
            factors["citation_density"] = 0
        elif citation_count == 1:
            factors["citation_density"] = 10
        elif citation_count == 2:
            factors["citation_density"] = 13
        else:
            factors["citation_density"] = 15

        # Calculate total
        total_confidence = sum(factors.values())

        # Ensure minimum confidence for valid responses
        if source_count > 0 and total_confidence < 30:
            total_confidence = 35

        return round(min(total_confidence, 100), 2)


confidence_service = ConfidenceService()
