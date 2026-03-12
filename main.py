from datetime import datetime, timezone
from dotenv import load_dotenv
import os

# Load environment variables from .env file (call before reading any env vars)
load_dotenv()

# Config from environment
DEBUG = os.getenv("DEBUG", "false").lower() in ("true", "1", "yes")
SECRET_KEY = os.getenv("SECRET_KEY", "")

# Optional: fail fast if SECRET_KEY is missing in production
# if not DEBUG and not SECRET_KEY:
#     raise ValueError("SECRET_KEY must be set when DEBUG is false")

from fastapi import FastAPI

app = FastAPI(debug=DEBUG)


@app.get("/")
def root():
    return {"message": "Hello, World!"}


@app.get("/health")
def health():
    return {
        "status": "ok",
        "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", "8000")),
        reload=DEBUG,
    )
