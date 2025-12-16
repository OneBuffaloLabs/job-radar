from typing import Optional
from datetime import datetime
from sqlmodel import Field, SQLModel

class JobPosting(SQLModel, table=True):
    __tablename__ = "job_postings"

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    company: str = Field(index=True)
    url: str = Field(unique=True)  # Prevent duplicate job entries
    salary_range: Optional[str] = None
    location: Optional[str] = None
    source: str  # e.g. "StackOverflow", "WeWorkRemotely"
    date_posted: datetime = Field(default_factory=datetime.utcnow)
    is_active: bool = Field(default=True)