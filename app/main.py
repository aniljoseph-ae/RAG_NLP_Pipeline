from fastapi import FastAPI
from config import settings
from database import vector_db
from app.api.routers import processing, tasks, health, feedback
import logging

# Configure logging
logging.basicConfig(level=settings.LOG_LEVEL)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="UltraSafe NLP Processing API",
    description="API for advanced NLP tasks with RAG integration",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Initialize components
@app.on_event("startup")
async def startup_event():
    logger.info("Initializing application...")
    vector_db.initialize()
    logger.info("Vector database initialized")

# Include routers
app.include_router(processing.router)
app.include_router(tasks.router)
app.include_router(health.router)
app.include_router(feedback.router)

# Health check endpoint
@app.get("/", include_in_schema=False)
def root():
    return {"status": "running", "version": app.version}