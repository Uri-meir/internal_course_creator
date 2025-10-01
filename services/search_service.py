"""
Semantic search service using pgvector (PRODUCTION)
"""

from sqlalchemy.orm import Session
from sqlalchemy import text
from models.document import Document, Chunk, Embedding
from schemas.document import SearchRequest, SearchResponse, ChunkResponse, DocumentResponse
from services.embedding_service import EmbeddingService
from typing import List

class SearchService:
    def __init__(self, db: Session):
        self.db = db
        self.embedding_service = EmbeddingService()
    
    async def search(self, request: SearchRequest) -> SearchResponse:
        """Perform semantic search using pgvector - PRODUCTION VERSION"""
        # Generate query embedding
        query_embedding = await self.embedding_service.generate_embedding(request.query)
        
        if not query_embedding:
            return SearchResponse(chunks=[], documents=[], total_results=0)
        
        # Build SQL query with pgvector similarity search
        # Using cosine distance: <=> operator (1 - cosine similarity)
        sql = """
            SELECT 
                c.id,
                c.document_id,
                c.chunk_text,
                c.summary,
                c.chunk_index,
                c.created_at,
                1 - (e.embedding <=> :query_embedding) as similarity
            FROM chunks c
            JOIN embeddings e ON c.id = e.chunk_id
            JOIN documents d ON c.document_id = d.id
            WHERE 1=1
        """
        
        params = {"query_embedding": str(query_embedding)}
        
        # Apply filters
        if request.department:
            sql += " AND d.department = :department"
            params["department"] = request.department
        
        if request.document_type:
            sql += " AND d.document_type = :document_type"
            params["document_type"] = request.document_type
        
        # Order by similarity (highest first) and limit
        sql += """
            ORDER BY similarity DESC
            LIMIT :limit
        """
        params["limit"] = request.limit
        
        # Execute query - database does all the heavy lifting!
        result = self.db.execute(text(sql), params)
        rows = result.fetchall()
        
        print(f"🔍 Found {len(rows)} relevant chunks for query: '{request.query}'")
        
        # Convert to response format
        chunk_responses = []
        document_ids = set()
        
        for row in rows:
            chunk = ChunkResponse(
                id=row.id,
                chunk_text=row.chunk_text,
                summary=row.summary,
                chunk_index=row.chunk_index
            )
            chunk_responses.append(chunk)
            document_ids.add(row.document_id)
            print(f"  - Chunk {row.chunk_index} (similarity: {row.similarity:.3f})")
        
        # Get documents
        documents = self.db.query(Document).filter(Document.id.in_(document_ids)).all()
        document_responses = [DocumentResponse.from_orm(doc) for doc in documents]
        
        return SearchResponse(
            chunks=chunk_responses,
            documents=document_responses,
            total_results=len(chunk_responses)
        )