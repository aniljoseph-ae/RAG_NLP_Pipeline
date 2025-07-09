NLP Processing API
This is a simple API for handling NLP tasks like sentiment analysis or entity extraction. It’s built with FastAPI, runs in Docker, and connects to an external NLP service (UltraSafe or OpenAI-compatible). This guide shows you how to clone and run it.
What You Need

Docker and Docker Compose: To run the app in containers.
API Key: For UltraSafe or OpenAI-compatible service.

Install Docker and Docker Compose:

Docker: https://docs.docker.com/get-docker/
Docker Compose: https://docs.docker.com/compose/install/

Clone the Project
If the project is in a Git repository, clone it:
git clone (https://github.com/aniljoseph-ae/RAG_NLP_Pipeline/tree/develop)
cd nlp-api

Set Up and Run

Create a .env File:In the nlp-api folder, create a file named .env with your API key:
echo "ULTRA_SAFE_API_KEY=your_api_key_here" > .env
echo "ULTRA_SAFE_BASE_URL=https://api.ultrasafe.com/v1" >> .env
echo "REDIS_URL=redis://redis:6379/0" >> .env
echo "CHROMA_DB_PATH=./chroma_db" >> .env
echo "API_PORT=8000" >> .env
echo "TASK_TIMEOUT=300" >> .env
echo "LOG_LEVEL=INFO" >> .env

Replace your_api_key_here with your actual UltraSafe/OpenAI API key.

Create Storage Folder:Run:
mkdir -p chroma_db
chmod -R 777 chroma_db


Start the App:Run:
docker-compose up --build -d

This starts the API (port 8000), Redis, and a background worker.

Check It’s Running:Run:
docker-compose ps

Look for api, redis, and celery_worker marked as Up.

Test the API:Try a sample request:
curl -X POST "http://localhost:8000/process" \
  -H "Content-Type: application/json" \
  -d '{
    "tasks": [
      {"text": "The product is great but delivery was late", "task_type": "sentiment_analysis"}
    ]
  }'

You’ll get a task_id. Check results with:
curl "http://localhost:8000/process/<task_id>"


View Docs:Open http://localhost:8000/docs in a browser for API details.


Stop the App
Stop the containers:
docker-compose down

To clear stored data:
docker-compose down -v

Tips

Make sure your API key is correct in .env.
Check logs if something fails: docker-compose logs.
The API runs on http://localhost:8000.

