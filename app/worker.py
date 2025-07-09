from app.tasks.processing import celery_app
from config import settings
import logging

logging.basicConfig(level=settings.LOG_LEVEL)

if __name__ == "__main__":
    celery_app.worker_main()