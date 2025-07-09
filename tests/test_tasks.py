import pytest
from app.tasks.processing import process_single_task
from celery.exceptions import TimeoutError

def test_process_single_task():
    task = {
        "text": "The product is great but delivery was late",
        "task_type": "sentiment_analysis"
    }
    result = process_single_task.apply(args=[task]).get(timeout=10)
    assert isinstance(result, dict)
    assert result["task_type"] == "sentiment_analysis"
    assert "result" in result