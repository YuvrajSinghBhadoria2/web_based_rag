import re
from typing import List, Optional, Dict, Any


def intelligent_chunk(text: str, chunk_size: int = 512, overlap: int = 50) -> List[str]:
    sentences = re.split(r"(?<=[.!?])\s+", text)

    chunks = []
    current_chunk = []
    current_length = 0

    for sentence in sentences:
        sentence_length = len(sentence.split())

        if current_length + sentence_length > chunk_size and current_chunk:
            chunks.append(" ".join(current_chunk))

            overlap_sentences = (
                current_chunk[-overlap:]
                if len(current_chunk) > overlap
                else current_chunk
            )
            current_chunk = overlap_sentences + [sentence]
            current_length = sum(len(s.split()) for s in current_chunk)
        else:
            current_chunk.append(sentence)
            current_length += sentence_length

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks


def create_chunk_metadata(
    document_id: str,
    chunk_index: int,
    page_number: Optional[int] = None,
    section: Optional[str] = None,
    total_chunks: int = 0,
) -> Dict[str, Any]:
    return {
        "document_id": document_id,
        "chunk_index": chunk_index,
        "page_number": page_number,
        "section": section,
        "total_chunks": total_chunks,
    }
