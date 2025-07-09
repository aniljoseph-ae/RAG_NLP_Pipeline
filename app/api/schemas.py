from pydantic import BaseModel
from typing import List, Optional, Dict

class TaskRequest(BaseModel):
    text: str
    task_type: str  # classification, entity_extraction, summarization, sentiment_analysis

class BatchRequest(BaseModel):
    tasks: List[TaskRequest]
    webhook_url: Optional[str] = None

class TaskResult(BaseModel):
    task_id: str
    status: str
    results: Optional[List[Dict]] = None

class FeedbackRequest(BaseModel):
    task_id: str
    expected_result: str
    actual_result: str
    rating: int  # 1-5