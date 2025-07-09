import uuid
import json
import chromadb
from chromadb.utils import embedding_functions
from config import settings
from typing import List, Dict

client = None
collection = None

def initialize():
    global client, collection
    client = chromadb.PersistentClient(path=settings.CHROMA_DB_PATH)
    ultrasafe_ef = embedding_functions.OpenAIEmbeddingFunction(
        api_key=settings.ULTRA_SAFE_API_KEY,
        model_name="text-embedding-ada-002",
        api_base=settings.ULTRA_SAFE_BASE_URL
    )
    collection = client.get_or_create_collection(
        name="nlp_documents",
        embedding_function=ultrasafe_ef
    )

def retrieve_similar_documents(query_text: str, task_type: str, top_k: int = 5) -> List[Dict]:
    try:
        results = collection.query(
            query_texts=[query_text],
            n_results=top_k,
            include=["metadatas", "distances", "documents"]
        )
        
        # Rerank based on task relevance
        reranked = []
        for i in range(len(results["ids"][0])):
            metadata = results["metadatas"][0][i]
            if metadata.get("task_type") == task_type:
                reranked.insert(0, {
                    "text": results["documents"][0][i],
                    "result": json.loads(metadata["result"])
                })
            else:
                reranked.append({
                    "text": results["documents"][0][i],
                    "result": json.loads(metadata["result"])
                })
        
        return reranked[:3]  # Return top 3 most relevant
    except Exception as e:
        print(f"Retrieval error: {str(e)}")
        return []

def store_processed_document(text: str, task_type: str, result: Dict):
    try:
        collection.upsert(
            ids=[str(uuid.uuid4())],
            documents=[text],
            metadatas=[{
                "task_type": task_type,
                "result": json.dumps(result)
            }]
        )
    except Exception as e:
        print(f"Storage error: {str(e)}")