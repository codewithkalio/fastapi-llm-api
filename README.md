# fastapi-llm-api

A lightweight FastAPI application that exposes LLM-powered text analysis via a REST API. Built and deployed as part of a prompt engineering exercise.

## Live API

**Base URL:** `https://your-app.onrender.com`  
Interactive docs: `https://your-app.onrender.com/docs`

## Endpoints

### `GET /health`
Returns the current status and timestamp of the API.

**Response:**
```json
{
  "status": "ok",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

---

### `POST /summarize`
Summarizes a block of text to a specified maximum length.

**Request body:**
```json
{
  "text": "Your long text here...",
  "max_length": 100
}
```

**Response:**
```json
{
  "summary": "A concise summary of your text."
}
```

---

### `POST /analyze-sentiment`
Analyzes the sentiment of a given text and returns a label, confidence score, and explanation.

**Request body:**
```json
{
  "text": "I absolutely loved this product!"
}
```

**Response:**
```json
{
  "sentiment": "positive",
  "confidence": 0.95,
  "explanation": "The text uses strongly positive language such as 'absolutely loved'."
}
```

---

## Running Locally

**1. Clone the repo**
```bash
git clone https://github.com/your-username/fastapi-llm-api.git
cd fastapi-llm-api
```

**2. Create and activate a virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Set up environment variables**

Create a `.env` file in the root directory:
```
OPENAI_API_KEY=your_key_here
```

**5. Start the server**
```bash
uvicorn main:app --reload
```

The API will be running at `http://localhost:8000`. Visit `http://localhost:8000/docs` for the interactive Swagger UI.

---

## Deployment

This app is deployed on [Render](https://render.com) (free tier).

- The `main` branch is connected to Render and deploys automatically on push.
- The `OPENAI_API_KEY` environment variable is set in the Render dashboard and is never committed to this repo.

---

## Tech Stack

- [FastAPI](https://fastapi.tiangolo.com/)
- [Uvicorn](https://www.uvicorn.org/)
- [OpenAI Python SDK](https://github.com/openai/openai-python)
- [Python Dotenv](https://pypi.org/project/python-dotenv/)

---

## Notes

This project was built as a hands-on exercise in prompt engineering. Each LLM endpoint was tested with multiple prompt variations to evaluate output quality. See the [project write-up](#) for full documentation of prompt experiments and results.
