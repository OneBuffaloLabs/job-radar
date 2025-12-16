from celery import Celery
from celery.schedules import crontab

from app.core.config import settings

celery_app = Celery(
    "job_radar_worker",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_BROKER_URL,
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)

# --- ADD THIS SECTION ---
celery_app.conf.beat_schedule = {
    "ingest-jobs-every-hour": {
        "task": "app.tasks.ingest_jobs_task",
        "schedule": crontab(minute=0, hour="*"),  # Runs every hour on the hour
        # For testing, you can change it to:
        # "schedule": 60.0, # Runs every 60 seconds
    },
}
