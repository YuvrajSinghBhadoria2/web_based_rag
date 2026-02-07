from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from enum import Enum


class QueryMode(str, Enum):
    WEB = "web"
    PDF = "pdf"
    HYBRID = "hybrid"
    RESTRICTED = "restricted"


class SourceType(str, Enum):
    PDF = "pdf"
    WEB = "web"


class QueryRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=1000)
    mode: QueryMode
    document_ids: Optional[List[str]] = None
    restrictions: Optional[List[str]] = None
    top_k: Optional[int] = Field(default=5, ge=1, le=20)


class Source(BaseModel):
    type: SourceType
    content: str
    reference: str
    title: str
    relevance_score: Optional[float] = None


class QueryResponse(BaseModel):
    answer: str
    sources: List[Source]
    confidence: float = Field(..., ge=0, le=100)
    mode_used: QueryMode
    query: str
    timestamp: datetime
    processing_time_ms: int


class UploadResponse(BaseModel):
    document_id: str
    filename: str
    status: str
    chunks_created: int
    upload_date: datetime


class Document(BaseModel):
    id: str
    filename: str
    upload_date: datetime
    chunk_count: int
    file_size: int
    status: str


class DocumentListResponse(BaseModel):
    documents: List[Document]
    total: int


class HealthResponse(BaseModel):
    status: str
    embedding_model: str
    vector_db: str
    llm: str
