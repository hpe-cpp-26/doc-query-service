from fastapi import APIRouter

from app.models.search_models import (
    SearchRequest,
    SearchResponse
)

from app.services.retrieval_service import (
    retrieve_chunks
)

from app.services.llm_service import generate_answer

router = APIRouter()

def build_document_url(doc_path: str):
    BASE_URL = (
        "https://github.com/hpe-cpp-26/"
        "test-central-data-store/tree/main/"
    )

    return BASE_URL + doc_path

@router.post(
    "/search",
    response_model=SearchResponse
)

def search(request: SearchRequest):
    
    chunks = retrieve_chunks(
        query=request.query,
        limit=5
    )
    
    confidence_score=0
    
    if chunks:
        confidence_score= round(
            chunks[0]["similarity"] * 100
        )
    
    answer = generate_answer(
        request.query,
        chunks
    )
    
    
    return {
        "answer": answer,
        "confidence_score": confidence_score,
        "sources": [
            {
                "doc_id": chunk["doc_id"],
                "doc_path": chunk["doc_path"],
                "url": build_document_url(
                    chunk["doc_path"]
                )
            }
            for chunk in chunks
        ]
    }