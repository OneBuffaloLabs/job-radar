from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.endpoints import router as api_router
from app.core.db import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Startup: Initializing Database...")
    await init_db()
    yield
    print("Shutdown: cleanup...")


app = FastAPI(title="Job Radar API", lifespan=lifespan)

# Register the router with a prefix
app.include_router(api_router, prefix="/api")


@app.get("/")
async def root():
    return {"message": "Job Radar API is online", "status": "running"}
