from pydantic import BaseModel, Field


class DocumentRequest(BaseModel):
    document_type: str = Field(
        ...,
        min_length=2,
        max_length=120,
    )

    parties: str = Field(
        ...,
        min_length=2,
        max_length=5000,
    )

    terms: str = Field(
        ...,
        min_length=2,
        max_length=10000,
    )

    dates: str = Field(
        ...,
        min_length=2,
        max_length=300,
    )

    company_name: str | None = None


class DocumentResponse(BaseModel):
    document_type: str
    content: str
    model: str
    mock: bool = False


class HealthResponse(BaseModel):
    status: str
    service: str
    model: str
    ai_configured: bool