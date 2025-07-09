import json
import redis
from config import settings

redis_client = redis.Redis.from_url(settings.REDIS_URL)

def get_cache_key(text: str, task_type: str) -> str:
    return f"cache:{task_type}:{hash(text)}"

def cache_result(text: str, task_type: str, result: dict):
    try:
        key = get_cache_key(text, task_type)
        redis_client.setex(key, 3600, json.dumps(result))  # Cache for 1 hour
    except Exception as e:
        print(f"Caching error: {str(e)}")

def get_cached_result(text: str, task_type: str) -> dict | None:
    try:
        key = get_cache_key(text, task_type)
        cached = redis_client.get(key)
        return json.loads(cached) if cached else None
    except Exception as e:
        print(f"Cache retrieval error: {str(e)}")
        return None