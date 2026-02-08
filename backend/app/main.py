from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.api.v1.routes import router as api_router
from app.config import settings
import os

app = FastAPI(
    title="RAG System API",
    description="Production-grade RAG system with PDF and web search",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")

# Serve static files (React frontend)
frontend_path = "/app"
try:
    app.mount("/", StaticFiles(directory=frontend_path, html=True), name="static")
except RuntimeError:
    # Fallback path if /app doesn't exist
    fallback_path = os.path.join(os.path.dirname(__file__), "../../frontend/dist")
    if os.path.exists(fallback_path):
        app.mount("/", StaticFiles(directory=fallback_path, html=True), name="static")


@app.get("/")
async def serve_index():
    index_path = os.path.join(frontend_path, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    # Also try fallback path
    fallback_path = os.path.join(os.path.dirname(__file__), "../../frontend/dist/index.html")
    if os.path.exists(fallback_path):
        return FileResponse(fallback_path)
    return {"message": "RAG System API", "version": "1.0.0"}


@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "RAG System"}
