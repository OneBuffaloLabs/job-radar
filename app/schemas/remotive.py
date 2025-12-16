from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


# This matches the shape of a single job object from Remotive's API
class RemotiveJobSchema(BaseModel):
    id: int
    url: str
    title: str
    company_name: str
    publication_date: datetime
    candidate_required_location: str
    salary: Optional[str] = None
    job_type: Optional[str] = None

    class Config:
        extra = "ignore"


# This matches the top-level response from Remotive
class RemotiveAPIResponse(BaseModel):
    job_count: int = Field(alias="job-count")
    jobs: List[RemotiveJobSchema]
