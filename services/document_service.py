"""
Document processing service
"""

from sqlalchemy.orm import Session
from models.document import Document, Chunk, Embedding
from schemas.document import DocumentCreate, DocumentResponse
from services.chunking_service import ChunkingService
from services.summarization_service import SummarizationService
from services.embedding_service import EmbeddingService
from services.document_reader import DocumentReader
from config import settings
from typing import List, Optional
import uuid

class DocumentService:
    def __init__(self, db: Session):
        self.db = db
        self.chunking_service = ChunkingService()
        self.summarization_service = SummarizationService()
        self.embedding_service = EmbeddingService()
        self.document_reader = DocumentReader()
    
    async def create_document(self, document_data: DocumentCreate, file_path: str, file_type: str, file_size: int) -> DocumentResponse:
        # Create document record
        document = Document(
            title=document_data.title,
            file_path=file_path,
            file_type=file_type,
            file_size=file_size,
            department=document_data.department,
            document_type=document_data.document_type,
            document_metadata=document_data.document_metadata
        )
        
        self.db.add(document)
        self.db.commit()
        self.db.refresh(document)
        
        return DocumentResponse.from_orm(document)
    
    async def process_document(self, document_id: uuid.UUID) -> bool:
        """Process document: chunk, summarize, embed"""
        document = self.db.query(Document).filter(Document.id == document_id).first()
        if not document:
            return False
        
        try:
            # Read document content using proper document reader
            print(f"Reading document: {document.file_path} (type: {document.file_type})")
            content = self.document_reader.read_document(document.file_path, document.file_type)
            
            print(f"Document content length: {len(content)} characters")
            
            if not content or len(content.strip()) < 10:
                print("Warning: Document content is very short or empty")
                content = f"Document content for {document.title}"
            
            # Chunk the document
            chunks = await self.chunking_service.chunk_text(content)
            print(f"Created {len(chunks)} chunks")
            
            # Process each chunk
            for i, chunk_text in enumerate(chunks):
                print(f"Processing chunk {i+1}/{len(chunks)} (length: {len(chunk_text)})")
                
                # Create chunk record
                chunk = Chunk(
                    document_id=document_id,
                    chunk_text=chunk_text,
                    chunk_index=i
                )
                self.db.add(chunk)
                self.db.commit()
                self.db.refresh(chunk)
                
                # Summarize chunk
                try:
                    summary = await self.summarization_service.summarize(chunk_text)
                    chunk.summary = summary
                    print(f"Chunk {i+1} summarized: {summary[:100]}...")
                except Exception as e:
                    print(f"Error summarizing chunk {i+1}: {e}")
                    chunk.summary = chunk_text[:200] + "..." if len(chunk_text) > 200 else chunk_text
                
                # Generate embedding
                try:
                    embedding_vector = await self.embedding_service.generate_embedding(chunk_text)
                    if embedding_vector:
                        # Store embedding - pgvector handles the vector directly
                        embedding = Embedding(
                            chunk_id=chunk.id,
                            embedding=embedding_vector,  # pgvector accepts list directly
                            model=settings.EMBEDDING_MODEL
                        )
                        self.db.add(embedding)
                        print(f"Chunk {i+1} embedded successfully (vector dim: {len(embedding_vector)})")
                    else:
                        print(f"Warning: No embedding generated for chunk {i+1}")
                except Exception as e:
                    print(f"Error embedding chunk {i+1}: {e}")
            
            # Mark document as processed
            document.processed = True
            self.db.commit()
            
            print(f"✅ Document processing completed: {len(chunks)} chunks processed")
            return True
            
        except Exception as e:
            print(f"❌ Error processing document: {e}")
            return False
    
    async def get_document(self, document_id: uuid.UUID) -> Optional[DocumentResponse]:
        document = self.db.query(Document).filter(Document.id == document_id).first()
        if document:
            return DocumentResponse.from_orm(document)
        return None
    
    async def list_documents(self, department: Optional[str] = None) -> List[DocumentResponse]:
        query = self.db.query(Document)
        if department:
            query = query.filter(Document.department == department)
        
        documents = query.all()
        return [DocumentResponse.from_orm(doc) for doc in documents]