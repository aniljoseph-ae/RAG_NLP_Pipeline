from fastapi import APIRouter, BackgroundTasks, HTTPException
from celery.result import AsyncResult
from app.tasks.processing import process_single_task
from app.api.schemas import BatchRequest, TaskResult
from app.utils.webhooks import send_webhook
import uuid

router = APIRouter(prefix="/process", tags=["Processing"])

@router.post("/", response_model=TaskResult, summary="Process batch of NLP tasks")
async def process_tasks(batch: BatchRequest, background_tasks: BackgroundTasks):
    task_id = str(uuid.uuid4())
    tasks = [task.dict() for task in batch.tasks]
    
    # Start processing
    async_result = process_single_task.apply_async(args=[tasks], task_id=task_id)
    
    # Schedule webhook if provided
    if batch.webhook_url:
        background_tasks.add_task(
            send_webhook, 
            batch.webhook_url,
            {"task_id": task_id, "status": "processing"}
        )
    
    return {"task_id": task_id, "status": "processing"}

@router.get("/{task_id}", response_model=TaskResult, summary="Get task status and results")
def get_task_result(task_id: str):
    result = AsyncResult(task_id)
    
    if not result.ready():
        return {"task_id": task_id, "status": "processing"}
    
    if result.failed():
        raise HTTPException(
            status_code=500, 
            detail="Task processing failed",
            headers={"X-Error": "Processing failed"}
        )
    
    return {
        "task_id": task_id,
        "status": "completed",
        "results": result.result
    }