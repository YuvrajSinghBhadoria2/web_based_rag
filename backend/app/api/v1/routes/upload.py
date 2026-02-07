from fastapi import APIRouter, UploadFile, File, HTTPException
from app.models.schemas import UploadResponse
from app.services.pdf_processor import pdf_processor
from app.services.embeddings import embedding_service
from app.services.vector_store import vector_store
from pathlib import Path
import uuid
from datetime import datetime
import shutil
import os
import json

router = APIRouter(prefix="/upload", tags=["upload"])

DOCUMENTS_DB = "./storage/documents.json"


def load_documents_db():
    if Path(DOCUMENTS_DB).exists():
        with open(DOCUMENTS_DB, "r") as f:
            return json.load(f)
    return {}


def save_documents_db(documents):
    Path(DOCUMENTS_DB).parent.mkdir(exist_ok=True, parents=True)
    with open(DOCUMENTS_DB, "w") as f:
        json.dump(documents, f, default=str)


@router.post("/", response_model=UploadResponse)
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")

    document_id = str(uuid.uuid4())

    upload_dir = Path("./storage/uploads")
    upload_dir.mkdir(exist_ok=True, parents=True)
    file_path = upload_dir / f"{document_id}.pdf"

    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        pdf_processor.validate_file(file_path)
    except Exception as e:
        if file_path.exists():
            os.remove(file_path)
        raise HTTPException(status_code=400, detail=str(e))

    try:
        chunks = await pdf_processor.process_document(file_path, document_id)
    except Exception as e:
        if file_path.exists():
            os.remove(file_path)
        raise HTTPException(status_code=500, detail=f"Failed to process PDF: {str(e)}")

    try:
        texts = [chunk["text"] for chunk in chunks]
        embeddings = embedding_service.embed_batch(texts)
        await vector_store.add_chunks(chunks, embeddings)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to index document: {str(e)}"
        )

    file_size = file_path.stat().st_size if file_path.exists() else 0

    documents_db = load_documents_db()
    documents_db[document_id] = {
        "id": document_id,
        "filename": file.filename,
        "upload_date": datetime.utcnow().isoformat(),
        "chunk_count": len(chunks),
        "file_size": file_size,
        "status": "ready",
    }
    save_documents_db(documents_db)

    return UploadResponse(
        document_id=document_id,
        filename=file.filename,
        status="completed",
        chunks_created=len(chunks),
        upload_date=datetime.utcnow(),
    )
