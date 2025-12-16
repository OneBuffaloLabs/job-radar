from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Job Radar"
    # This defaults to the docker-compose string but can be overridden by env vars
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@db:5432/job_radar"

    class Config:
        case_sensitive = True

settings = Settings()