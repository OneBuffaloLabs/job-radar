from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.core.db import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Startup: Initializing Database...")
    await init_db()
    yield
    print("Shutdown: cleanup...")

app = FastAPI(
    title="Job Radar API",
    lifespan=lifespan  # Inject the lifespan logic here
)

@app.get("/")
async def root():
    return {"message": "Job Radar API is online", "status": "running"}