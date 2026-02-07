from fastapi import APIRouter
from app.models.schemas import DocumentListResponse, Document
from app.services.vector_store import vector_store
from pathlib import Path
from datetime import datetime
import json

router = APIRouter(prefix="/documents", tags=["documents"])

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


@router.get("/", response_model=DocumentListResponse)
async def list_documents():
    documents_db = load_documents_db()

    documents = []
    for doc_id, doc_data in documents_db.items():
        documents.append(
            Document(
                id=doc_id,
                filename=doc_data.get("filename", "Unknown"),
                upload_date=datetime.fromisoformat(
                    doc_data.get("upload_date", datetime.utcnow().isoformat())
                ),
                chunk_count=doc_data.get("chunk_count", 0),
                file_size=doc_data.get("file_size", 0),
                status=doc_data.get("status", "ready"),
            )
        )

    return DocumentListResponse(
        documents=sorted(documents, key=lambda x: x.upload_date, reverse=True),
        total=len(documents),
    )


@router.delete("/{document_id}")
async def delete_document(document_id: str):
    documents_db = load_documents_db()

    if document_id not in documents_db:
        return {"message": "Document not found"}

    file_path = Path(f"./storage/uploads/{document_id}.pdf")
    if file_path.exists():
        file_path.unlink()

    del documents_db[document_id]
    save_documents_db(documents_db)

    try:
        await vector_store.delete_document(document_id)
    except:
        pass

    return {"message": "Document deleted"}
