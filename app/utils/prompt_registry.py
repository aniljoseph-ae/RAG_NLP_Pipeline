import os
import json
from config import settings

# In production, integrate with MLflow or similar
PROMPT_REGISTRY = {
    "classification": "Classify this text: '{text}'",
    "entity_extraction": "Extract entities from: '{text}'",
    "summarization": "Summarize this: '{text}'",
    "sentiment_analysis": "Analyze sentiment of: '{text}'"
}

def get_prompt(task_type: str, version: str = "latest") -> str:
    """Get prompt for a specific task type"""
    return PROMPT_REGISTRY.get(task_type, "Process this text: '{text}'")