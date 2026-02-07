from fastapi import APIRouter, HTTPException
from app.models.schemas import QueryRequest, QueryResponse
from app.services.retriever import retriever_service
from app.services.enhanced_llm import enhanced_llm_service
from app.services.prompt_guard import prompt_guard
from app.services.confidence import confidence_service
from datetime import datetime
import time

router = APIRouter(prefix="/query", tags=["query"])


@router.post("/", response_model=QueryResponse)
async def query_documents(request: QueryRequest):
    start_time = time.time()

    # Validate restricted mode
    try:
        if request.mode.value == "restricted":
            await prompt_guard.validate_input(request.query, request.restrictions)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    # Retrieve sources
    try:
        sources = await retriever_service.retrieve(
            query=request.query,
            mode=request.mode,
            top_k=request.top_k or 5,
            document_ids=request.document_ids,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Retrieval failed: {str(e)}")

    # Handle no sources
    if not sources:
        return QueryResponse(
            answer="No relevant sources found for your query.",
            sources=[],
            confidence=0,
            mode_used=request.mode,
            query=request.query,
            timestamp=datetime.utcnow(),
            processing_time_ms=int((time.time() - start_time) * 1000),
        )

    # Generate answer with enhanced LLM service
    try:
        answer = await enhanced_llm_service.generate_answer(
            query=request.query, sources=sources
        )
    except Exception as e:
        return QueryResponse(
            answer=f"Unable to generate answer at this time due to high demand. Please try again in a few moments.",
            sources=sources,
            confidence=50,
            mode_used=request.mode,
            query=request.query,
            timestamp=datetime.utcnow(),
            processing_time_ms=int((time.time() - start_time) * 1000),
        )

    # Sanitize output
    try:
        answer = await prompt_guard.sanitize_output(answer)
    except:
        pass

    # Calculate confidence
    try:
        confidence = confidence_service.calculate_confidence(
            query=request.query, answer=answer, sources=sources
        )
    except:
        confidence = 50.0

    processing_time = int((time.time() - start_time) * 1000)

    return QueryResponse(
        answer=answer,
        sources=sources,
        confidence=confidence,
        mode_used=request.mode,
        query=request.query,
        timestamp=datetime.utcnow(),
        processing_time_ms=processing_time,
    )
