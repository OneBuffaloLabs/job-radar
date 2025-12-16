import asyncio

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from app.core.celery_app import celery_app
from app.core.config import settings
from app.services.ingestion import fetch_and_store_jobs


@celery_app.task
def ingest_jobs_task():
    """
    Synchronous Celery task that wraps the async ingestion logic.
    """

    async def _async_runner():
        # 1. Create a fresh engine specifically for this task execution.
        # We use NullPool to prevent connection pooling issues across different event loops.
        task_engine = create_async_engine(
            settings.DATABASE_URL,
            echo=True,  # Set to False in production to reduce log noise
            future=True,
            poolclass=NullPool,
        )

        # 2. Create a session factory using this fresh engine
        async_session_factory = sessionmaker(
            task_engine, class_=AsyncSession, expire_on_commit=False
        )

        try:
            async with async_session_factory() as session:
                jobs_count = await fetch_and_store_jobs(session)
                return jobs_count
        finally:
            # 3. Always clean up the engine
            await task_engine.dispose()

    # asyncio.run() sets up a new event loop for this task execution
    try:
        result = asyncio.run(_async_runner())
        return f"Successfully ingested {result} jobs."
    except Exception as e:
        return f"Error during ingestion: {str(e)}"
