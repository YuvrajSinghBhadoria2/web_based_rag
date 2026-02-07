import pypdf
import pdfplumber
from pathlib import Path
from typing import List, Tuple
from app.utils.chunking import intelligent_chunk, create_chunk_metadata


class PDFProcessor:
    def __init__(self):
        self.max_file_size = 10 * 1024 * 1024

    async def extract_text(self, file_path: Path) -> List[Tuple[str, int]]:
        pages_text = []

        try:
            with pdfplumber.open(file_path) as pdf:
                for i, page in enumerate(pdf.pages, 1):
                    text = page.extract_text() or ""
                    if text.strip():
                        pages_text.append((text, i))
        except Exception as e:
            try:
                with open(file_path, "rb") as file:
                    reader = pypdf.PdfReader(file)
                    for i, page in enumerate(reader.pages, 1):
                        text = page.extract_text() or ""
                        if text.strip():
                            pages_text.append((text, i))
            except Exception as fallback_error:
                raise Exception(f"Failed to extract text: {fallback_error}")

        return pages_text

    async def process_document(self, file_path: Path, document_id: str) -> List[dict]:
        pages_text = await self.extract_text(file_path)

        full_text = "\n\n".join([text for text, _ in pages_text])

        chunks = intelligent_chunk(text=full_text, chunk_size=512, overlap=50)

        processed_chunks = []
        for idx, chunk in enumerate(chunks):
            page_num = self._find_page_number(chunk, pages_text)

            chunk_data = {
                "text": chunk,
                "metadata": create_chunk_metadata(
                    document_id=document_id,
                    chunk_index=idx,
                    page_number=page_num,
                    total_chunks=len(chunks),
                ),
            }
            processed_chunks.append(chunk_data)

        return processed_chunks

    def _find_page_number(self, chunk: str, pages_text: List[Tuple[str, int]]) -> int:
        chunk_start = chunk[:50]

        for text, page_num in pages_text:
            if chunk_start in text:
                return page_num

        return 0

    def validate_file(self, file_path: Path) -> bool:
        if not file_path.exists():
            raise Exception("File does not exist")

        if file_path.stat().st_size > self.max_file_size:
            raise Exception("File size exceeds limit")

        try:
            with open(file_path, "rb") as f:
                pypdf.PdfReader(f)
            return True
        except Exception:
            raise Exception("Invalid PDF file")


pdf_processor = PDFProcessor()
