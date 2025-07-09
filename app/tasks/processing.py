import openai
from config import settings
from database import vector_db
from utils.cache import get_cached_result, cache_result
from utils.prompt_registry import get_prompt
from celery import Celery

celery_app = Celery("tasks", broker=settings.REDIS_URL, backend=settings.REDIS_URL)
celery_app.conf.task_time_limit = settings.TASK_TIMEOUT

@celery_app.task
def process_single_task(task: dict) -> dict:
    text = task["text"]
    task_type = task["task_type"]
    
    # Check cache
    if cached := get_cached_result(text, task_type):
        return cached
    
    # Retrieve similar documents using RAG
    similar_docs = vector_db.retrieve_similar_documents(text, task_type)
    
    # Prepare context for LLM
    context = "Reference examples:\n"
    for i, doc in enumerate(similar_docs):
        context += f"Example {i+1}:\nInput: {doc['text']}\nOutput: {doc['result']}\n\n"
    
    # Get task-specific prompt from registry
    prompt_template = get_prompt(task_type)
    prompt = f"{context}{prompt_template.format(text=text)}"
    
    # Call UltraSafe API
    client = openai.OpenAI(
        api_key=settings.ULTRA_SAFE_API_KEY,
        base_url=settings.ULTRA_SAFE_BASE_URL
    )
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500
        )
        
        result_text = response.choices[0].message.content.strip()
        result_data = {"text": text, "task_type": task_type, "result": result_text}
        
        # Cache and store result
        cache_result(text, task_type, result_data)
        vector_db.store_processed_document(text, task_type, result_data)
        
        return result_data
    except Exception as e:
        # Fallback to default processing
        return {
            "text": text,
            "task_type": task_type,
            "result": f"Error processing: {str(e)}"
        }