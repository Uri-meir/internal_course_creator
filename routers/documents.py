"""
Documents API router
"""

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from services.database import get_db
from services.document_service import DocumentService
from schemas.document import DocumentResponse, DocumentUpload
from typing import List, Optional
import os
import uuid

router = APIRouter()

@router.post("/upload", response_model=DocumentResponse)
async def upload_document(
    file: UploadFile = File(...),
    title: str = Form(...),
    department: Optional[str] = Form(None),
    document_type: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    """Upload and process a document"""
    
    # Create upload directory if it doesn't exist
    upload_dir = "uploads"
    os.makedirs(upload_dir, exist_ok=True)
    
    # Generate unique filename
    file_extension = file.filename.split('.')[-1] if '.' in file.filename else 'txt'
    filename = f"{uuid.uuid4()}.{file_extension}"
    file_path = os.path.join(upload_dir, filename)
    
    # Save file
    with open(file_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)
    
    # Create document record
    document_data = DocumentUpload(
        title=title,
        department=department,
        document_type=document_type
    )
    
    document_service = DocumentService(db)
    document = await document_service.create_document(
        document_data, file_path, file.content_type, len(content)
    )
    
    # Start background processing
    await document_service.process_document(document.id)
    
    return document

@router.get("/", response_model=List[DocumentResponse])
async def list_documents(
    department: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """List all documents"""
    document_service = DocumentService(db)
    return await document_service.list_documents(department)

@router.get("/{document_id}", response_model=DocumentResponse)
async def get_document(
    document_id: uuid.UUID,
    db: Session = Depends(get_db)
):
    """Get a specific document"""
    document_service = DocumentService(db)
    document = await document_service.get_document(document_id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    return document
