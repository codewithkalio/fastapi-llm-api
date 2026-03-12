from datetime import datetime, timezone
from dotenv import load_dotenv
import os

from openai import OpenAI

# Load environment variables from .env file (call before reading any env vars)
load_dotenv()

# Config from environment
DEBUG = os.getenv("DEBUG", "false").lower() in ("true", "1", "yes")
SECRET_KEY = os.getenv("SECRET_KEY", "")

# Optional: fail fast if SECRET_KEY is missing in production
# if not DEBUG and not SECRET_KEY:
#     raise ValueError("SECRET_KEY must be set when DEBUG is false")

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(debug=DEBUG)


class SummarizeRequest(BaseModel):
    text: str = Field(..., description="Text to summarize")
    max_length: int = Field(default=150, ge=1, le=2000, description="Maximum length of the summary in words")
    model_config = {
        "json_schema_extra": {
            "examples": [{"text": "Your long article or document text goes here.", "max_length": 150}]
        }
    }


@app.get("/")
def root():
    return {"message": "Hello, World!"}


@app.get("/health")
def health():
    return {
        "status": "ok",
        "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
    }


@app.post("/summarize")
def summarize(body: SummarizeRequest):
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or not api_key.strip():
        raise HTTPException(
            status_code=503,
            detail="Summarization is unavailable: OPENAI_API_KEY is not configured.",
        )
    model = os.getenv("OPENAI_SUMMARIZE_MODEL", "gpt-4o-mini")
    client = OpenAI(api_key=api_key)
    prompt = (
        f"Summarize the following text in at most {body.max_length} words. "
        "Return only the summary, no preamble.\n\n"
        f"{body.text}"
    )
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a concise summarizer. Output only the summary."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=min(2000, body.max_length * 2),
        )
        summary = (response.choices[0].message.content or "").strip()
        return {"summary": summary}
    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail="Summarization service is temporarily unavailable.",
        ) from e


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", "8000")),
        reload=DEBUG,
    )
