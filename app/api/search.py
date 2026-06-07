from fastapi import APIRouter

from app.models.search_models import (
    SearchRequest,
    SearchResponse
)

from app.services.retrieval_service import (
    retrieve_chunks
)

router = APIRouter()

@router.post(
    "/search",
    response_model=SearchResponse
)

def search(request: SearchRequest):
    
    results = retrieve_chunks(
        query=request.query,
        limit=10,
    )
    
    return {
        "results": results
    }