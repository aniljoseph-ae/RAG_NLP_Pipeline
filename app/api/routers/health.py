from fastapi import APIRouter
from app.database.vector_db import client
import redis
from config import settings
import logging

router = APIRouter(tags=["Health"])
logger = logging.getLogger(__name__)

@router.get("/health", summary="Check API health")
def health_check():
    status = {"status": "healthy", "components": {}}
    
    try:
        # Check vector DB
        client.heartbeat()
        status["components"]["vector_db"] = "healthy"
    except Exception as e:
        status["components"]["vector_db"] = f"unhealthy: {str(e)}"
        status["status"] = "unhealthy"
        logger.error(f"Vector DB health check failed: {str(e)}")
    
    try:
        # Check Redis
        redis_client = redis.Redis.from_url(settings.REDIS_URL)
        redis_client.ping()
        status["components"]["redis"] = "healthy"
    except Exception as e:
        status["components"]["redis"] = f"unhealthy: {str(e)}"
        status["status"] = "unhealthy"
        logger.error(f"Redis health check failed: {str(e)}")
    
    return status