from __future__ import annotations

from io import BytesIO

from fpdf import FPDF

from formatting.sanitize import (
    parse_terms,
    sanitize_text,
)


def safe_text(text: str) -> str:
    """
    Convert Unicode text to something the default
    Helvetica font can safely display.
    """

    return (
        text
        .encode(
            "latin-1",
            errors="replace",
        )
        .decode(
            "latin-1"
        )
    )


class LegalEasePDF(FPDF):

    def __init__(
        self,
        company_name: str,
    ) -> None:

        super().__init__(
            "P",
            "mm",
            "A4",
        )

        self.company_name = (
            company_name
        )

    def header(self) -> None:

        self.set_font(
            "Helvetica",
            "B",
            9,
        )

        self.set_text_color(
            80,
            80,
            80,
        )

        self.cell(
            0,
            6,
            safe_text(
                self.company_name
            ),
            align="C",
        )

        self.ln(6)

        self.set_draw_color(
            200,
            200,
            200,
        )

        self.line(
            10,
            self.get_y(),
            200,
            self.get_y(),
        )

        self.ln(5)

    def footer(self) -> None:

        self.set_y(
            -18
        )

        self.set_draw_color(
            200,
            200,
            200,
        )

        self.line(
            10,
            self.get_y(),
            200,
            self.get_y(),
        )

        self.ln(3)

        self.set_font(
            "Helvetica",
            "",
            7,
        )

        self.set_text_color(
            100,
            100,
            100,
        )

        self.cell(
            0,
            4,
            safe_text(
                f"{self.company_name} | "
                "Drafting assistance - "
                "review before use"
            ),
            align="C",
        )

        self.ln(4)

        self.cell(
            0,
            4,
            f"Page {self.page_no()}",
            align="C",
        )


def write_text(
    pdf: FPDF,
    text: str,
    *,
    size: float = 10.5,
    bold: bool = False,
) -> None:

    pdf.set_font(
        "Helvetica",
        "B" if bold else "",
        size,
    )

    pdf.set_text_color(
        30,
        30,
        30,
    )

    pdf.multi_cell(
        0,
        5.5,
        safe_text(
            text
        ),
    )

    pdf.ln(1)


def format_pdf(
    text: str,
    doc_type: str,
    *,
    terms: str = "",
    logo_path: str | None = None,
    logo_bytes: bytes | None = None,
    company_name: str = "LegalEase",
) -> bytes:

    pdf = LegalEasePDF(
        company_name=company_name
    )

    pdf.set_auto_page_break(
        True,
        22,
    )

    pdf.add_page()

    # Document title.
    pdf.set_font(
        "Helvetica",
        "B",
        16,
    )

    pdf.cell(
        0,
        10,
        safe_text(
            doc_type.upper()
        ),
        align="C",
    )

    pdf.ln(10)

    clean_text = sanitize_text(
        text
    )

    for raw_line in clean_text.splitlines():

        line = raw_line.strip()

        if not line:

            pdf.ln(2)
            continue

        if line.startswith("# "):

            write_text(
                pdf,
                line[2:].strip(),
                size=14,
                bold=True,
            )

        elif line.startswith("## "):

            write_text(
                pdf,
                line[3:].strip(),
                size=12,
                bold=True,
            )

        elif line.startswith("### "):

            write_text(
                pdf,
                line[4:].strip(),
                size=11,
                bold=True,
            )

        elif line.startswith(
            ("- ", "* ")
        ):

            write_text(
                pdf,
                "- " + line[2:].strip(),
            )

        elif line.startswith("> "):

            write_text(
                pdf,
                line[2:].strip(),
                size=9.5,
            )

        else:

            write_text(
                pdf,
                line,
            )

    term_items = parse_terms(
        terms
    )

    if term_items:

        write_text(
            pdf,
            "KEY TERMS",
            size=12,
            bold=True,
        )

        for index, term in enumerate(
            term_items,
            start=1,
        ):

            write_text(
                pdf,
                f"{index}. {term}",
                size=9.5,
            )

    write_text(
        pdf,
        "SIGNATURES",
        size=12,
        bold=True,
    )

    write_text(
        pdf,
        "Party 1: ______________________________",
        size=9.5,
    )

    write_text(
        pdf,
        "Date: _________________________________",
        size=9.5,
    )

    write_text(
        pdf,
        "Party 2: ______________________________",
        size=9.5,
    )

    write_text(
        pdf,
        "Date: _________________________________",
        size=9.5,
    )

    write_text(
        pdf,
        "Drafting notice: AI-generated content "
        "is not a substitute for advice from a "
        "qualified lawyer licensed in the relevant "
        "jurisdiction.",
        size=8,
    )

    output = pdf.output()

    if isinstance(
        output,
        bytearray,
    ):
        return bytes(
            output
        )

    return output