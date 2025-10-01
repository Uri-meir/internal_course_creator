"""
Pydantic schemas for API validation
"""

from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime
from uuid import UUID

class DocumentCreate(BaseModel):
    title: str
    department: Optional[str] = None
    document_type: Optional[str] = None
    document_metadata: Optional[Dict[str, Any]] = None

class DocumentResponse(BaseModel):
    id: UUID
    title: str
    file_type: Optional[str]
    file_size: Optional[int]
    department: Optional[str]
    document_type: Optional[str]
    processed: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class DocumentUpload(BaseModel):
    title: str
    department: Optional[str] = None
    document_type: Optional[str] = None
    document_metadata: Optional[Dict[str, Any]] = None

class ChunkResponse(BaseModel):
    id: UUID
    chunk_text: str
    summary: Optional[str]
    chunk_index: int
    
    class Config:
        from_attributes = True

class SearchRequest(BaseModel):
    query: str
    limit: int = 10
    department: Optional[str] = None
    document_type: Optional[str] = None

class SearchResponse(BaseModel):
    chunks: List[ChunkResponse]
    documents: List[DocumentResponse]
    total_results: int

class CourseGenerationRequest(BaseModel):
    document_ids: List[UUID]
    topic: str
    department: Optional[str] = None

class CourseGenerationResponse(BaseModel):
    job_id: UUID
    status: str
    estimated_time: Optional[int] = None

class JobStatusResponse(BaseModel):
    job_id: UUID
    status: str
    progress: int
    result_url: Optional[str] = None
    error_message: Optional[str] = None
    created_at: datetime
    completed_at: Optional[datetime] = None

class ChatRequest(BaseModel):
    message: str
    department: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    sources: List[ChunkResponse] = []