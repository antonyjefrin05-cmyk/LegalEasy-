import os
from functools import lru_cache

from dotenv import load_dotenv
from pydantic import BaseModel, Field


load_dotenv()


class Settings(BaseModel):
    app_name: str = "LegalEase"

    company_name: str = "LegalEase"

    gemini_api_key: str | None = None

    gemini_model: str = "gemini-3.8-flash"

    use_mock_ai: bool = False

    backend_host: str = "127.0.0.1"

    backend_port: int = 8000

    backend_url: str = "http://127.0.0.1:8000"

    cors_origins: list[str] = Field(
        default_factory=list
    )

    max_input_length: int = 12000

    max_generated_chars: int = 50000

    logo_path: str = "assets/logo.png"


@lru_cache(maxsize=1)
def get_settings():
    origins = [
        x.strip()
        for x in os.getenv(
            "CORS_ORIGINS",
            "http://localhost:8501,http://127.0.0.1:8501",
        ).split(",")
        if x.strip()
    ]

    return Settings(
        app_name="LegalEase",

        company_name=os.getenv(
            "COMPANY_NAME",
            "LegalEase",
        ),

        gemini_api_key=os.getenv(
            "GEMINI_API_KEY"
        ) or None,

        gemini_model=os.getenv(
            "GEMINI_MODEL",
            "gemini-3.8-flash",
        ),

        use_mock_ai=os.getenv(
            "USE_MOCK_AI",
            "false",
        ).lower() in {
            "true",
            "1",
            "yes",
        },

        backend_host=os.getenv(
            "BACKEND_HOST",
            "127.0.0.1",
        ),

        backend_port=int(
            os.getenv(
                "BACKEND_PORT",
                "8000",
            )
        ),

        backend_url=os.getenv(
            "BACKEND_URL",
            "http://127.0.0.1:8000",
        ),

        cors_origins=origins,

        max_input_length=int(
            os.getenv(
                "MAX_INPUT_LENGTH",
                "12000",
            )
        ),

        max_generated_chars=int(
            os.getenv(
                "MAX_GENERATED_CHARS",
                "50000",
            )
        ),

        logo_path=os.getenv(
            "LOGO_PATH",
            "assets/logo.png",
        ),
    )