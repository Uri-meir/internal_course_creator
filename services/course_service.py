"""
Course generation service
"""

from sqlalchemy.orm import Session
from models.document import Document, Chunk, CourseGenerationJob
from schemas.document import CourseGenerationRequest, CourseGenerationResponse, JobStatusResponse
from services.script_service import ScriptService
from services.video_service import VideoService
from typing import List, Optional
import uuid
import asyncio

class CourseService:
    def __init__(self, db: Session):
        self.db = db
        self.script_service = ScriptService()
        self.video_service = VideoService()
    
    async def generate_course(self, request: CourseGenerationRequest) -> CourseGenerationResponse:
        """Start course generation job"""
        # Create job record
        job = CourseGenerationJob(
            document_ids=request.document_ids,
            topic=request.topic,
            department=request.department
        )
        
        self.db.add(job)
        self.db.commit()
        self.db.refresh(job)
        
        # Start background processing
        await self._process_course_generation(job.id)
        
        return CourseGenerationResponse(
            job_id=job.id,
            status=job.status,
            estimated_time=300  # 5 minutes estimate
        )
    
    async def get_job_status(self, job_id: uuid.UUID) -> Optional[JobStatusResponse]:
        """Get job status"""
        job = self.db.query(CourseGenerationJob).filter(CourseGenerationJob.id == job_id).first()
        if not job:
            return None
        
        return JobStatusResponse.from_orm(job)
    
    async def _process_course_generation(self, job_id: uuid.UUID):
        """Background processing for course generation"""
        job = self.db.query(CourseGenerationJob).filter(CourseGenerationJob.id == job_id).first()
        if not job:
            return
        
        try:
            # Update status
            job.status = "processing"
            job.progress = 10
            self.db.commit()
            
            # Get document summaries
            summaries = await self._get_document_summaries(job.document_ids)
            
            job.progress = 30
            self.db.commit()
            
            # Generate script
            script = await self.script_service.generate_script(summaries, job.topic)
            
            job.progress = 60
            self.db.commit()
            
            # Generate video
            video_url = await self.video_service.generate_video(script)
            
            # Update job
            job.status = "completed"
            job.progress = 100
            job.result_url = video_url
            self.db.commit()
            
        except Exception as e:
            job.status = "failed"
            job.error_message = str(e)
            self.db.commit()
    
    async def _get_document_summaries(self, document_ids: List[uuid.UUID]) -> List[str]:
        """Get summaries for documents"""
        summaries = []
        
        for doc_id in document_ids:
            # Get document
            document = self.db.query(Document).filter(Document.id == doc_id).first()
            if document:
                # Get chunks
                chunks = self.db.query(Chunk).filter(Chunk.document_id == doc_id).all()
                
                # Combine summaries
                doc_summary = " ".join([chunk.summary for chunk in chunks if chunk.summary])
                if doc_summary:
                    summaries.append(f"Document: {document.title}\n{doc_summary}")
        
        return summaries
