from fastapi import APIRouter
import os
from dotenv import load_dotenv

# Load frontend/.env to get GitHub config

load_dotenv()

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
    if not doc_path:
        return ""
        
    github_org = os.getenv("GITHUB_ORG", "")
    github_repo = os.getenv("GITHUB_REPO", "")
    
    if not (github_org and github_repo):
        return ""
        
    # Remove leading slash from doc_path if present to avoid double slashes
    doc_path = doc_path.lstrip("/")
    
    return f"https://github.com/{github_org}/{github_repo}/blob/main/{doc_path}"

@router.post(
    "/search",
    response_model=SearchResponse
)
def search(request: SearchRequest):
    
    chunks = retrieve_chunks(
        query=request.query,
        limit=3
    )
    
    confidence_score=0
    
    if chunks:
        confidence_score= round(
            chunks[0]["similarity"] * 100
        )
        
    for chunk in chunks:
        chunk["url"] = build_document_url(chunk.get("doc_path", ""))
    
    answer = generate_answer(
        request.query,
        chunks
    )
    
    return {
        "answer": answer,
        "confidence_score": confidence_score,
        "sources": [
            {
                "doc_id": chunk.get("doc_id", ""),
                "doc_path": chunk.get("doc_path", ""),
                "url": chunk.get("url", ""),
                "chunk_text": chunk.get("chunk_text", ""),
                "similarity": float(chunk.get("similarity", 0.0))
            }
            for chunk in chunks
        ]
    }