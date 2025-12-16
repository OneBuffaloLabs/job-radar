import httpx
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.job import JobPosting
from app.schemas.remotive import RemotiveAPIResponse

REMOTIVE_URL = "https://remotive.com/api/remote-jobs?limit=50" # Limiting to 50 for dev

async def fetch_and_store_jobs(session: AsyncSession):
    # Fetch data from external API
    async with httpx.AsyncClient() as client:
        response = await client.get(REMOTIVE_URL)
        response.raise_for_status()

    # Validate/Parse with Pydantic (Clean the dirty data)
    data = response.json()
    # validated_data will be a RemotiveAPIResponse object
    validated_data = RemotiveAPIResponse(**data)

    jobs_added = 0

    # Iterate and Save to DB
    for remote_job in validated_data.jobs:
        # Check if job already exists to avoid duplicates (based on URL)
        # Note: In a high-perf production app, we might use "ON CONFLICT" SQL syntax,
        # but a select-check is fine for learning.
        existing_job = await session.execute(
            select(JobPosting).where(JobPosting.url == remote_job.url)
        )
        if existing_job.scalars().first():
            continue # Skip if exists

        # Map External Schema -> Internal DB Model
        new_job = JobPosting(
            title=remote_job.title,
            company=remote_job.company_name,
            url=remote_job.url,
            location=remote_job.candidate_required_location,
            salary_range=remote_job.salary if remote_job.salary else "Not specified",
            source="Remotive",
            date_posted=remote_job.publication_date,
            is_active=True
        )

        session.add(new_job)
        jobs_added += 1

    await session.commit()
    return jobs_added