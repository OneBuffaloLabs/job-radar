from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.endpoints import router as api_router
from app.core.db import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Startup: Initializing Database...")
    await init_db()
    yield
    print("Shutdown: cleanup...")


app = FastAPI(title="Job Radar API", lifespan=lifespan)

# This allows your Next.js app to talk to this Docker container.
origins = [
    "http://localhost:3000",
    "http://localhost:3001",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register the router with a prefix
app.include_router(api_router, prefix="/api")


@app.get("/")
async def root():
    return {"message": "Job Radar API is online", "status": "running"}