from __future__ import annotations

from formatting.sanitize import sanitize_text


def format_txt(text: str) -> bytes:
    """
    Convert document text to UTF-8 bytes
    for Streamlit download.
    """

    cleaned = sanitize_text(text)

    return cleaned.encode(
        "utf-8"
    )