import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_create_job(client: AsyncClient):
    """
    Test creating a job (POST /api/jobs)
    """
    payload = {
        "title": "Senior Python Engineer",
        "company": "Test Corp",
        "url": "https://test.com/jobs/1",
        "source": "Automated Test",
        "salary_range": "$200k",
        "location": "Remote"
    }

    response = await client.post("/api/jobs", json=payload)

    # Assertions - This is what makes it a test!
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Senior Python Engineer"
    assert "id" in data

@pytest.mark.asyncio
async def test_read_jobs(client: AsyncClient):
    """
    Test reading the list of jobs (GET /api/jobs)
    """
    # Create a job first so we have data
    await client.post("/api/jobs", json={
        "title": "Another Job",
        "company": "Test Co",
        "url": "https://test.com/jobs/2",
        "source": "Test",
        "is_active": True
    })

    response = await client.get("/api/jobs")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0