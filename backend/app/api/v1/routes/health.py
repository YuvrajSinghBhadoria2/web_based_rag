from fastapi import APIRouter
from app.models.schemas import HealthResponse

router = APIRouter(prefix="/health", tags=["health"])


@router.get("/", response_model=HealthResponse)
async def health_check():
    return HealthResponse(
        status="healthy",
        embedding_model="all-MiniLM-L6-v2",
        vector_db="chromadb",
        llm="groq",
    )
