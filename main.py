from datetime import datetime, timezone
from dotenv import load_dotenv
import json
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


class SentimentRequest(BaseModel):
    text: str = Field(..., description="Text to analyze for sentiment")
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "text": "I loved the product quality but the shipping was slow.",
                }
            ]
        }
    }


class SentimentResponse(BaseModel):
    label: str = Field(..., description='Sentiment label: "positive", "negative", or "neutral"')
    confidence: float = Field(..., ge=0.0, le=1.0, description="Model confidence for the chosen label (0.0–1.0)")
    explanation: str = Field(..., description="Short explanation of why this label was chosen")


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
            detail="Summarization is temporarily unavailable.",
        ) from e


@app.post("/analyze-sentiment", response_model=SentimentResponse)
def analyze_sentiment(body: SentimentRequest) -> SentimentResponse:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or not api_key.strip():
        raise HTTPException(
            status_code=503,
            detail="Sentiment analysis is unavailable: OPENAI_API_KEY is not configured.",
        )

    sentiment_model = os.getenv("OPENAI_SENTIMENT_MODEL") or os.getenv("OPENAI_SUMMARIZE_MODEL", "gpt-4o-mini")
    client = OpenAI(api_key=api_key)

    system_message = (
        "You are a precise sentiment analysis system. "
        "Given some input text, you must decide whether the overall sentiment is positive, negative, or neutral. "
        "Respond ONLY with a JSON object that has these keys: "
        '"label" (one of "positive", "negative", "neutral"), '
        '"confidence" (a number between 0 and 1), and '
        '"explanation" (a short explanation of why you chose this label).'
    )

    try:
        response = client.chat.completions.create(
            model=sentiment_model,
            messages=[
                {"role": "system", "content": system_message},
                {
                    "role": "user",
                    "content": f"Analyze the sentiment of the following text:\n\n{body.text}",
                },
            ],
            max_tokens=300,
            response_format={"type": "json_object"},
        )

        raw_content = (response.choices[0].message.content or "{}").strip()
        data = json.loads(raw_content)

        label = str(data.get("label", "neutral")).strip().lower()
        allowed_labels = {"positive", "negative", "neutral"}
        if label not in allowed_labels:
            label = "neutral"

        confidence_raw = data.get("confidence", 0.5)
        try:
            confidence = float(confidence_raw)
        except (TypeError, ValueError):
            confidence = 0.5
        confidence = max(0.0, min(1.0, confidence))

        explanation = str(data.get("explanation", "") or "").strip() or "No explanation provided."

        return SentimentResponse(label=label, confidence=confidence, explanation=explanation)
    except (json.JSONDecodeError, KeyError) as e:
        raise HTTPException(
            status_code=503,
            detail="Sentiment analysis is temporarily unavailable.",
        ) from e
    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail="Sentiment analysis is temporarily unavailable.",
        ) from e


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", "8000")),
        reload=DEBUG,
    )
