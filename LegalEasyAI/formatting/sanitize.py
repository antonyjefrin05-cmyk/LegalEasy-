from __future__ import annotations


_TRANSLATIONS = str.maketrans(
    {
        "“": '"',
        "”": '"',
        "‘": "'",
        "’": "'",
        "–": "-",
        "—": "-",
        "−": "-",
        "…": "...",
        "•": "-",
        "\u00a0": " ",
    }
)


def sanitize_text(text: str) -> str:
    """
    Clean AI-generated text before putting it
    into TXT, DOCX, PDF or HTML output.
    """

    if not isinstance(text, str):
        raise TypeError(
            "text must be a string"
        )

    cleaned = text.translate(
        _TRANSLATIONS
    )

    # Remove invisible control characters.
    cleaned = "".join(
        char
        for char in cleaned
        if char == "\n"
        or char == "\t"
        or ord(char) >= 32
    )

    # Avoid huge runs of blank lines.
    while "\n\n\n\n" in cleaned:
        cleaned = cleaned.replace(
            "\n\n\n\n",
            "\n\n\n",
        )

    return cleaned.strip()


def parse_terms(terms: str) -> list[str]:
    """
    Convert semicolon-separated terms into
    a clean Python list.
    """

    if not terms:
        return []

    normalized = (
        terms
        .replace("\r", "")
        .replace("\n", ";")
    )

    return [
        item.strip(" \t-*")
        for item in normalized.split(";")
        if item.strip()
    ]