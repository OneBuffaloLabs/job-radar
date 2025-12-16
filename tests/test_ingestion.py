from unittest.mock import patch

import pytest
import respx
from httpx import Response
from sqlalchemy import select

from app.models.job import JobPosting
from app.services.ingestion import REMOTIVE_URL, fetch_and_store_jobs

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
            "job_type": "full_time",
        }
    ],
}


@pytest.mark.asyncio
async def test_fetch_and_store_jobs_service(db_session):
    """
    Unit test for the ingestion service logic.
    Mocks the external API and verifies DB insertion.
    """
    # Use the exact URL from the service to ensure we catch the request
    with respx.mock(base_url="https://remotive.com") as respx_mock:
        respx_mock.get(REMOTIVE_URL).mock(
            return_value=Response(200, json=MOCK_REMOTIVE_DATA)
        )

        # Call the service function directly
        count = await fetch_and_store_jobs(db_session)

        # Assertions
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
    Since the endpoint now offloads to Celery, we mock the task.delay() call
    instead of mocking the HTTP API.
    """
    # Patch the Celery task where it is IMPORTED in the endpoints file
    with patch("app.api.endpoints.ingest_jobs_task.delay") as mock_task:
        # Mock the return value of .delay() (which is an AsyncResult)
        mock_task.return_value.id = "test-task-id-123"

        # 1. Hit the endpoint
        response = await client.post("/api/jobs/ingest")

        # 2. Verify response
        assert response.status_code == 200
        data = response.json()

        # Expect the new async message
        assert "Ingestion started in background" in data["message"]
        assert data["task_id"] == "test-task-id-123"

        # Verify the task was actually called
        mock_task.assert_called_once()


@pytest.mark.asyncio
async def test_ingest_idempotency(db_session):
    """
    Ensure running ingestion twice doesn't create duplicate jobs.
    """
    with respx.mock(base_url="https://remotive.com") as respx_mock:
        # Catch ANY request to the Remotive URL
        respx_mock.get(REMOTIVE_URL).mock(
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
