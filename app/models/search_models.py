from pydantic import BaseModel

class Source(BaseModel):
    doc_id: str
    doc_path: str
    url: str

class SearchRequest(BaseModel):
    query:str
    
class SearchResponse(BaseModel):
    answer: str
    confidence_score: float
    sources: list[Source]