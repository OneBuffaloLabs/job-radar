from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.core.db import get_session
from app.models.job import JobPosting
from app.tasks import ingest_jobs_task

router = APIRouter()


# CREATE (POST)
@router.post("/jobs", response_model=JobPosting)
async def create_job(job: JobPosting, session: AsyncSession = Depends(get_session)):
    """
    Create a new job posting manually.
    """
    try:
        session.add(job)
        await session.commit()
        await session.refresh(job)  # Refresh to get the ID assigned by Postgres
        return job
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=400, detail=str(e))


# READ (GET List)
@router.get("/jobs", response_model=List[JobPosting])
async def get_jobs(
    skip: int = 0, limit: int = 100, session: AsyncSession = Depends(get_session)
):
    """
    Get a list of job postings with pagination.
    """
    # SQLModel syntax is slightly different from raw SQLAlchemy but cleaner
    query = select(JobPosting).offset(skip).limit(limit)
    result = await session.execute(query)
    jobs = result.scalars().all()
    return jobs


# READ (GET Single)
@router.get("/jobs/{job_id}", response_model=JobPosting)
async def get_job(job_id: int, session: AsyncSession = Depends(get_session)):
    """
    Get a specific job by ID.
    """
    job = await session.get(JobPosting, job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job


# INGESTION (Trigger)
@router.post("/jobs/ingest")
async def ingest_jobs():
    """
    Trigger the background ingestion of jobs from Remotive.
    Returns immediately with a task ID.
    """
    # Trigger the Celery task
    task = ingest_jobs_task.delay()

    # Respond immediately
    return {"message": "Ingestion started in background", "task_id": task.id}