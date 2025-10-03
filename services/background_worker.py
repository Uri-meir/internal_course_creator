"""
Background worker service for long-running tasks
"""

from celery import Celery
from config import settings
from services.database import get_db
from services.script_service import ScriptService
from services.video_service import VideoService
from models.document import CourseGenerationJob, Document, Chunk
import uuid
import asyncio

# Initialize Celery
celery_app = Celery(
    "knowledge_management",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL
)

@celery_app.task
def generate_course_task(job_id: str):
    """Background task to generate course - using the working synchronous flow"""
    print(f"🎬 Starting course generation for job: {job_id}")
    
    try:
        # Get database session
        db = next(get_db())
        
        # Get the job
        job = db.query(CourseGenerationJob).filter(CourseGenerationJob.id == uuid.UUID(job_id)).first()
        if not job:
            print(f"❌ Job not found: {job_id}")
            return {"status": "failed", "error": "Job not found"}
        
        # Update status to processing (same as working flow)
        job.status = "processing"
        job.progress = 10
        db.commit()
        
        # Get document summaries (same logic as working flow)
        summaries = []
        for doc_id_str in job.document_ids:
            doc_id = uuid.UUID(doc_id_str)
            document = db.query(Document).filter(Document.id == doc_id).first()
            if document:
                chunks = db.query(Chunk).filter(Chunk.document_id == doc_id).all()
                doc_summary = " ".join([chunk.summary for chunk in chunks if chunk.summary])
                if doc_summary:
                    summaries.append(f"Document: {document.title}\n{doc_summary}")
        
        job.progress = 30
        db.commit()
        
        # Generate script (same as working flow)
        script_service = ScriptService()
        script = asyncio.run(script_service.generate_script(summaries, job.topic))
        
        job.progress = 60
        db.commit()
        
        # Generate video (same as working flow)
        video_service = VideoService()
        video_url = asyncio.run(video_service.generate_video(script))
        
        # FIXED: Only mark as completed when video is actually ready
        if video_url:
            job.status = "completed"
            job.progress = 100
            job.result_url = video_url
            db.commit()
            
            print(f"✅ Course generation completed for job: {job_id}")
            print(f"🎥 Video URL: {video_url}")
            return {"status": "completed", "job_id": job_id, "video_url": video_url}
        else:
            # Video generation failed
            job.status = "failed"
            job.error_message = "Video generation failed"
            db.commit()
            
            print(f"❌ Video generation failed for job: {job_id}")
            return {"status": "failed", "job_id": job_id, "error": "Video generation failed"}
        
    except Exception as e:
        print(f"❌ Course generation failed for job {job_id}: {e}")
        
        # Update job status to failed (same as working flow)
        try:
            db = next(get_db())
            job = db.query(CourseGenerationJob).filter(CourseGenerationJob.id == uuid.UUID(job_id)).first()
            if job:
                job.status = "failed"
                job.error_message = str(e)
                db.commit()
        except Exception as db_error:
            print(f"❌ Failed to update job status: {db_error}")
        
        return {"status": "failed", "job_id": job_id, "error": str(e)}

async def init_workers():
    """Initialize background workers"""
    # For now, just print a message
    # In production, this would start Celery workers
    print("Background workers initialized (Celery workers would start here)")
    pass