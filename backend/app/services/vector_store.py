import chromadb
from chromadb.config import Settings as ChromaSettings
from typing import List, Dict, Optional
from pathlib import Path
from app.config import settings


class VectorStore:
    def __init__(self):
        self.client = chromadb.PersistentClient(
            path=str(settings.VECTOR_DB_PATH),
            settings=ChromaSettings(anonymized_telemetry=False),
        )
        self.collection = self.client.get_or_create_collection(
            name="documents", metadata={"hnsw:space": "cosine"}
        )

    async def add_chunks(self, chunks: List[dict], embeddings: List[List[float]]):
        ids = [
            f"{chunk['metadata']['document_id']}_chunk_{chunk['metadata']['chunk_index']}"
            for chunk in chunks
        ]

        documents = [chunk["text"] for chunk in chunks]

        metadatas = [
            {
                "document_id": chunk["metadata"]["document_id"],
                "chunk_index": chunk["metadata"]["chunk_index"],
                "page_number": chunk["metadata"]["page_number"] or 0,
                "total_chunks": chunk["metadata"]["total_chunks"],
            }
            for chunk in chunks
        ]

        self.collection.add(
            ids=ids, embeddings=embeddings, documents=documents, metadatas=metadatas
        )

    async def search(
        self,
        query_embedding: List[float],
        top_k: int = 5,
        document_ids: Optional[List[str]] = None,
    ) -> List[Dict]:
        where_filter = None
        if document_ids:
            where_filter = {"document_id": {"$in": document_ids}}

        results = self.collection.query(
            query_embeddings=[query_embedding], n_results=top_k, where=where_filter
        )

        search_results = []
        for i in range(len(results["ids"][0])):
            search_results.append(
                {
                    "text": results["documents"][0][i],
                    "metadata": results["metadatas"][0][i],
                    "similarity": 1 - results["distances"][0][i],
                    "id": results["ids"][0][i],
                }
            )

        return search_results

    async def delete_document(self, document_id: str):
        self.collection.delete(where={"document_id": document_id})

    async def get_stats(self) -> Dict:
        count = self.collection.count()
        return {"total_chunks": count, "collection_name": self.collection.name}


vector_store = VectorStore()
