
# Spam Detection Project - Full Package

## Contents
- `spam_detection.ipynb` - Jupyter notebook to train and save artifacts.
- `flask_app/` - Flask application with UI, API endpoints, and SQLite feedback DB.
- `Dockerfile` - Build a container image.
- `docker-compose.yml` - For local orchestration.
- `.github/workflows/ci.yml` - CI workflow for testing.

## Quickstart (local)
1. Create a virtual env: `python -m venv venv && source venv/bin/activate`
2. Install: `pip install -r requirements.txt`
3. Run app: `python flask_app/app.py` (or `docker-compose up --build`)
4. Visit http://localhost:8080

## Deploy to Render / Heroku / AWS ECS
- For Render: create a Web Service, connect repo, build using Dockerfile.
- For Heroku: use `heroku container:push web` and `heroku container:release web`.
- For AWS ECS: push image to ECR, create task & service with Fargate.

## API Endpoints
- `POST /predict` - JSON: `{"text": "..."}` -> `{"prediction": 0/1, "probability": 0.x}`
- `POST /feedback` - JSON: `{"text":"...","predicted":0,"actual":1,"prob":0.x}` stores feedback in SQLite.

## Notes
- Replace the mock training data in the notebook with the real dataset and re-train the model.
- Consider adding authentication and rate-limiting for production.
