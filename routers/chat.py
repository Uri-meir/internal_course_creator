"""
Chat API router
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from services.database import get_db
from services.chat_service import ChatService
from schemas.document import ChatRequest, ChatResponse

router = APIRouter()

@router.post("/", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    db: Session = Depends(get_db)
):
    """Chat with the knowledge base"""
    chat_service = ChatService(db)
    return await chat_service.chat(request)
