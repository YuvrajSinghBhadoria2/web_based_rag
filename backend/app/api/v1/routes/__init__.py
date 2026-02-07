from fastapi import APIRouter
from .upload import router as upload_router
from .query import router as query_router
from .documents import router as documents_router
from .health import router as health_router

router = APIRouter()

router.include_router(upload_router)
router.include_router(query_router)
router.include_router(documents_router)
router.include_router(health_router)
