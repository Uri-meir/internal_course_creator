"""
Chat service for RAG-based conversations
"""

from sqlalchemy.orm import Session
from models.document import Document, Chunk, Embedding
from schemas.document import ChatRequest, ChatResponse, ChunkResponse, SearchRequest
from services.embedding_service import EmbeddingService
from services.search_service import SearchService
from openai import AsyncOpenAI
from config import settings
from typing import List
import json

class ChatService:
    def __init__(self, db: Session):
        self.db = db
        self.embedding_service = EmbeddingService()
        self.search_service = SearchService(db)
        self.openai_client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
    
    async def chat(self, request: ChatRequest) -> ChatResponse:
        """Handle chat request with RAG"""
        # Search for relevant content
        search_request = SearchRequest(
            query=request.message,
            limit=5,
            department=request.department
        )
        
        search_results = await self.search_service.search(search_request)
        
        # Prepare context
        context = ""
        sources = []
        
        for chunk in search_results.chunks:
            context += f"{chunk.chunk_text}\n\n"
            sources.append(chunk)
        
        # Generate response
        try:
            response = await self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a helpful corporate assistant. Answer questions based on the provided context. Be professional, accurate, and helpful. If you don't know something, say so."},
                    {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {request.message} answer the question based on the context!"}
                ],
                max_tokens=500,
                temperature=0.3
            )
            
            return ChatResponse(
                response=response.choices[0].message.content,
                sources=sources
            )
            
        except Exception as e:
            print(f"Error in chat: {e}")
            return ChatResponse(
                response="I'm sorry, I encountered an error processing your request.",
                sources=[]
            )