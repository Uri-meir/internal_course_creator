"""
Search API router
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from services.database import get_db
from services.search_service import SearchService
from schemas.document import SearchRequest, SearchResponse

router = APIRouter()

@router.post("/", response_model=SearchResponse)
async def search_documents(
    request: SearchRequest,
    db: Session = Depends(get_db)
):
    """Search documents using semantic search"""
    search_service = SearchService(db)
    return await search_service.search(request)
