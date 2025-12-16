import pytest
import respx
from httpx import Response
from sqlalchemy import select
from app.models.job import JobPosting
from app.services.ingestion import fetch_and_store_jobs, REMOTIVE_URL

# Define a fake job payload that matches Remotive's structure
MOCK_REMOTIVE_DATA = {
    "job-count": 1,
    "jobs": [
        {
            "id": 12345,
            "url": "https://remotive.com/remote-jobs/software-dev/fake-job-123",
            "title": "Senior Python Ninja",
            "company_name": "Hidden Leaf Village",
            "publication_date": "2024-01-01T12:00:00",
            "candidate_required_location": "Konoha",
            "salary": "$100k - $150k",
            "job_type": "full_time"
        }
    ]
}

@pytest.mark.asyncio
async def test_fetch_and_store_jobs_service(db_session):
    """
    Unit test for the ingestion service logic.
    Mocks the external API and verifies DB insertion.
    """
    # 1. Mock the Remotive API to return our fake data
    with respx.mock(base_url="https://remotive.com") as respx_mock:
        respx_mock.get("/api/remote-jobs", name="remotive").mock(
            return_value=Response(200, json=MOCK_REMOTIVE_DATA)
        )

        # 2. Call the service function directly
        count = await fetch_and_store_jobs(db_session)

        # 3. Assertions
        assert count == 1

        # Verify data is actually in the DB
        result = await db_session.execute(select(JobPosting))
        jobs = result.scalars().all()

        assert len(jobs) == 1
        assert jobs[0].title == "Senior Python Ninja"
        assert jobs[0].company == "Hidden Leaf Village"
        assert jobs[0].source == "Remotive"

@pytest.mark.asyncio
async def test_ingest_endpoint(client, db_session):
    """
    Integration test for the /jobs/ingest endpoint.
    Ensures the API route connects to the service correctly.
    """
    with respx.mock(base_url="https://remotive.com") as respx_mock:
        respx_mock.get("/api/remote-jobs").mock(
            return_value=Response(200, json=MOCK_REMOTIVE_DATA)
        )

        # 1. Hit the endpoint
        response = await client.post("/api/jobs/ingest")

        # 2. Verify response
        assert response.status_code == 200
        assert "Ingestion complete" in response.json()["message"]
        assert "Added 1 new jobs" in response.json()["message"]

@pytest.mark.asyncio
async def test_ingest_idempotency(db_session):
    """
    Ensure running ingestion twice doesn't create duplicate jobs.
    """
    with respx.mock(base_url="https://remotive.com") as respx_mock:
        respx_mock.get("/api/remote-jobs").mock(
            return_value=Response(200, json=MOCK_REMOTIVE_DATA)
        )

        # Run 1st time
        await fetch_and_store_jobs(db_session)

        # Run 2nd time (Same data)
        count_2 = await fetch_and_store_jobs(db_session)

        # Should add 0 new jobs
        assert count_2 == 0

        # DB should still only have 1 row
        result = await db_session.execute(select(JobPosting))
        jobs = result.scalars().all()
        assert len(jobs) == 1