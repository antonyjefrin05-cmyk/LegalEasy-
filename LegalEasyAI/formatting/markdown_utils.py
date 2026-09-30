from __future__ import annotations

import html
import re


def inline_to_html(text: str) -> str:
    """
    Convert simple Markdown formatting into safe HTML.
    """

    escaped = html.escape(text)

    # Bold: **text**
    escaped = re.sub(
        r"\*\*(.+?)\*\*",
        r"<strong>\1</strong>",
        escaped,
    )

    # Italic: *text*
    escaped = re.sub(
        r"\*(.+?)\*",
        r"<em>\1</em>",
        escaped,
    )

    return escaped


def format_html_preview(
    text: str,
    title: str = "Legal Document",
) -> str:
    """
    Convert Markdown-style legal document text into
    a clean HTML preview.

    Consecutive normal lines are combined into a single
    paragraph so the preview does not contain large gaps.
    """

    lines = text.splitlines()

    blocks: list[str] = []

    paragraph_lines: list[str] = []
    list_items: list[str] = []

    def flush_paragraph() -> None:
        nonlocal paragraph_lines

        if paragraph_lines:

            paragraph_text = " ".join(
                line.strip()
                for line in paragraph_lines
                if line.strip()
            )

            if paragraph_text:

                blocks.append(
                    "<p>"
                    + inline_to_html(
                        paragraph_text
                    )
                    + "</p>"
                )

        paragraph_lines = []

    def flush_list() -> None:
        nonlocal list_items

        if list_items:

            blocks.append("<ul>")

            for item in list_items:

                blocks.append(
                    "<li>"
                    + inline_to_html(item)
                    + "</li>"
                )

            blocks.append("</ul>")

        list_items = []

    for raw_line in lines:

        line = raw_line.strip()

        # -------------------------------------------------
        # Blank line
        # -------------------------------------------------

        if not line:

            flush_paragraph()
            flush_list()

            continue

        # -------------------------------------------------
        # Bullet point
        # -------------------------------------------------

        if line.startswith(
            ("- ", "* ")
        ):

            flush_paragraph()

            list_items.append(
                line[2:].strip()
            )

            continue

        # -------------------------------------------------
        # Heading 3
        # -------------------------------------------------

        if line.startswith("### "):

            flush_paragraph()
            flush_list()

            blocks.append(
                "<h3>"
                + inline_to_html(
                    line[4:].strip()
                )
                + "</h3>"
            )

            continue

        # -------------------------------------------------
        # Heading 2
        # -------------------------------------------------

        if line.startswith("## "):

            flush_paragraph()
            flush_list()

            blocks.append(
                "<h2>"
                + inline_to_html(
                    line[3:].strip()
                )
                + "</h2>"
            )

            continue

        # -------------------------------------------------
        # Heading 1
        # -------------------------------------------------

        if line.startswith("# "):

            flush_paragraph()
            flush_list()

            blocks.append(
                "<h1>"
                + inline_to_html(
                    line[2:].strip()
                )
                + "</h1>"
            )

            continue

        # -------------------------------------------------
        # Blockquote
        # -------------------------------------------------

        if line.startswith("> "):

            flush_paragraph()
            flush_list()

            blocks.append(
                "<blockquote>"
                + inline_to_html(
                    line[2:].strip()
                )
                + "</blockquote>"
            )

            continue

        # -------------------------------------------------
        # Numbered section
        # Example: 1. Parties
        # -------------------------------------------------

        if re.match(
            r"^\d+[.)]\s+",
            line,
        ):

            flush_paragraph()
            flush_list()

            blocks.append(
                "<h3>"
                + inline_to_html(line)
                + "</h3>"
            )

            continue

        # -------------------------------------------------
        # Normal text
        # -------------------------------------------------

        flush_list()

        paragraph_lines.append(
            line
        )

    # Flush anything remaining.
    flush_paragraph()
    flush_list()

    content = "".join(blocks)

    return (
        '<div class="legal-preview">'
        '<div class="preview-title">'
        + inline_to_html(title)
        + "</div>"
        + content
        + "</div>"
    )