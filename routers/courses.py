"""
Courses API router
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from services.database import get_db
from services.course_service import CourseService
from schemas.document import CourseGenerationRequest, CourseGenerationResponse, JobStatusResponse
from typing import List
import uuid

router = APIRouter()

@router.post("/generate", response_model=CourseGenerationResponse)
async def generate_course(
    request: CourseGenerationRequest,
    db: Session = Depends(get_db)
):
    """Generate a course from selected documents"""
    course_service = CourseService(db)
    return await course_service.generate_course(request)

@router.get("/{job_id}/status", response_model=JobStatusResponse)
async def get_job_status(
    job_id: uuid.UUID,
    db: Session = Depends(get_db)
):
    """Get course generation job status"""
    course_service = CourseService(db)
    status = await course_service.get_job_status(job_id)
    if not status:
        raise HTTPException(status_code=404, detail="Job not found")
    return status
