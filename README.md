# fastapi-llm-api

A lightweight FastAPI application that exposes LLM-powered text analysis via a REST API. Built and deployed as part of a prompt engineering exercise.


## Endpoints

### `GET /`
Returns a simple greeting.

**Response:**
```json
{
  "message": "Hello, World!"
}
```

---

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

**Request body:** `max_length` is in words (1–2000), default 150.

```json
{
  "text": "Your long text here...",
  "max_length": 150
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
Analyzes the sentiment of a given text and returns a label, confidence score, and explanation. Accepts JSON or `application/x-www-form-urlencoded` with a `text` field.

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
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Set up environment variables**

Copy `.env.example` to `.env` in the root directory and fill in your values.

- **Required:** `OPENAI_API_KEY` (for `/summarize` and `/analyze-sentiment`).
- **Optional:** `OPENAI_SUMMARIZE_MODEL`, `OPENAI_SENTIMENT_MODEL` (default: `gpt-4o-mini`).

**5. Start the server**
```bash
uvicorn main:app --reload
```

The API will be running at `http://localhost:8000`. Visit `http://localhost:8000/docs` for the interactive Swagger UI.

---

## Deployment

This app is deployed on Render.

- The `main` branch is connected to Render and deploys automatically on push.
- Set `OPENAI_API_KEY` in the Render dashboard (never commit it to this repo). You can also set `OPENAI_SUMMARIZE_MODEL` and `OPENAI_SENTIMENT_MODEL` there to override the default model.

---

## Tech Stack

- [FastAPI](https://fastapi.tiangolo.com/)
- [Uvicorn](https://www.uvicorn.org/)
- [OpenAI Python SDK](https://github.com/openai/openai-python)
- [Python Dotenv](https://pypi.org/project/python-dotenv/)

---
