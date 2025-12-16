from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "Job Radar"
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@db:5432/job_radar"
    CELERY_BROKER_URL: str = "redis://redis:6379/0"

    model_config = SettingsConfigDict(case_sensitive=True)

settings = Settings()