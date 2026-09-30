from fastapi import APIRouter, Depends, HTTPException

from ai_core.gemini_generator import (
    GeminiDocumentGenerator,
    GeminiGenerationError,
)

from backend.config import Settings, get_settings
from backend.models import DocumentRequest, DocumentResponse


router = APIRouter(
    tags=["documents"]
)


def get_generator(
    settings: Settings = Depends(get_settings),
) -> GeminiDocumentGenerator:

    return GeminiDocumentGenerator(
        settings=settings
    )


@router.post(
    "/generate",
    response_model=DocumentResponse,
)
def generate_document(
    payload: DocumentRequest,
    settings: Settings = Depends(get_settings),
    generator: GeminiDocumentGenerator = Depends(
        get_generator
    ),
) -> DocumentResponse:

    values = [
        payload.document_type,
        payload.parties,
        payload.terms,
        payload.dates,
    ]

    if any(
        len(value) > settings.max_input_length
        for value in values
    ):
        raise HTTPException(
            status_code=413,
            detail=(
                "One or more input fields are "
                "too large."
            ),
        )

    try:

        content = generator.generate_document(
            document_type=payload.document_type,
            parties=payload.parties,
            terms=payload.terms,
            dates=payload.dates,
            company_name=(
                payload.company_name
                or settings.company_name
            ),
        )

    except GeminiGenerationError as exc:

        raise HTTPException(
            status_code=503,
            detail=str(exc),
        ) from exc

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=(
                "Unexpected error while "
                "generating the document."
            ),
        ) from exc

    return DocumentResponse(
        document_type=payload.document_type,
        content=content,
        model=settings.gemini_model,
        mock=settings.use_mock_ai,
    )