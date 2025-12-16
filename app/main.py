from fastapi import FastAPI

# Initialize the app with metadata (this populates your Swagger UI)
app = FastAPI(
    title="Job Radar API",
    description="High-performance job aggregation engine.",
    version="0.1.0",
    docs_url="/docs",  # location of Swagger UI
    redoc_url="/redoc",  # location of ReDoc (alternative docs)
)

# 1. @app.get is a "Decorator". In Node/Express, this is app.get('/').
# 2. "async def" enables non-blocking I/O (like Node's event loop).
@app.get("/")
async def root():
    """
    Root entry point.
    """
    return {
        "message": "Job Radar API is online",
        "service": "One Buffalo Labs Job Radar",
        "status": "running"
    }

# Standard health check for container orchestration
@app.get("/health")
async def health_check():
    return {"status": "ok"}