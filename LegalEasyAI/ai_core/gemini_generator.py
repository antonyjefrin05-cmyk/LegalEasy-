from __future__ import annotations

from dataclasses import dataclass

from backend.config import Settings

from ai_core.prompt_builder import (
    SYSTEM_INSTRUCTION,
    build_prompt,
)


try:
    from google import genai
    from google.genai import types

except ImportError:
    genai = None
    types = None


class GeminiGenerationError(RuntimeError):
    """Raised when document generation fails."""


@dataclass
class GeminiDocumentGenerator:

    settings: Settings

    def _get_client(self):

        if genai is None:

            raise GeminiGenerationError(
                "The google-genai package is not installed. "
                "Run: python -m pip install -r requirements.txt"
            )

        if not self.settings.gemini_api_key:

            raise GeminiGenerationError(
                "GEMINI_API_KEY is not configured."
            )

        return genai.Client(
            api_key=self.settings.gemini_api_key
        )

    def generate_document(
        self,
        *,
        document_type: str,
        parties: str,
        terms: str,
        dates: str,
        company_name: str | None = None,
    ) -> str:

        # -------------------------------------------------
        # OFFLINE TEST MODE
        # -------------------------------------------------

        if self.settings.use_mock_ai:

            return self._mock_document(
                document_type=document_type,
                parties=parties,
                terms=terms,
                dates=dates,
            )

        # -------------------------------------------------
        # REAL GEMINI MODE
        # -------------------------------------------------

        prompt = build_prompt(
            document_type=document_type,
            parties=parties,
            terms=terms,
            dates=dates,
            company_name=company_name,
        )

        client = self._get_client()

        try:

            response = client.models.generate_content(
                model=self.settings.gemini_model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_INSTRUCTION,
                    max_output_tokens=8000,
                ),
            )

        except Exception as exc:

            raise GeminiGenerationError(
                f"Gemini API request failed: {exc}"
            ) from exc

        generated_text = getattr(
            response,
            "text",
            None,
        )

        if not generated_text:

            raise GeminiGenerationError(
                "Gemini returned an empty response."
            )

        generated_text = generated_text.strip()

        if not generated_text:

            raise GeminiGenerationError(
                "Gemini returned an empty document."
            )

        # Safety limit.
        if len(generated_text) > self.settings.max_generated_chars:

            generated_text = (
                generated_text[
                    : self.settings.max_generated_chars
                ].rstrip()
                + "\n\n"
                "[Document truncated by the configured "
                "output limit.]"
            )

        return generated_text

    @staticmethod
    def _mock_document(
        *,
        document_type: str,
        parties: str,
        terms: str,
        dates: str,
    ) -> str:

        term_items = [
            item.strip()
            for item in (
                terms
                .replace("\r", "")
                .replace("\n", ";")
                .split(";")
            )
            if item.strip()
        ]

        if term_items:

            terms_text = "\n".join(
                f"- {item}"
                for item in term_items
            )

        else:

            terms_text = "- [INSERT TERMS]"

        return f"""
# {document_type.upper()}

## 1. Parties

{parties}

## 2. Effective Date

{dates}

## 3. Purpose

This agreement records the understanding
between the parties identified above.

## 4. Terms and Conditions

{terms_text}

## 5. General Provisions

The parties may amend this document only
through a written agreement signed by
the relevant parties.

If any provision of this document is found
to be unenforceable, the remaining
provisions will continue to apply to the
extent permitted by applicable law.

## 6. Signatures

Party 1: ______________________________

Date: _________________________________

Party 2: ______________________________

Date: _________________________________

> Drafting notice: This document was
> generated in offline test mode and
> is not legal advice.
""".strip()