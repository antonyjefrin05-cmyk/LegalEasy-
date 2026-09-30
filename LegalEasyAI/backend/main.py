from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.config import get_settings
from backend.models import HealthResponse
from backend.routes import router


settings = get_settings()


app = FastAPI(
    title="LegalEase",
    version="1.0.0",
    description="AI-assisted legal document drafting backend",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


app.include_router(router)


@app.get("/", response_model=HealthResponse)
def root():
    return HealthResponse(
        status="ok",
        service="LegalEase",
        model=settings.gemini_model,
        ai_configured=(
            bool(settings.gemini_api_key)
            or settings.use_mock_ai
        ),
    )