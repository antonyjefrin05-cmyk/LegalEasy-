from __future__ import annotations

from pathlib import Path

import requests
import streamlit as st

from backend.config import get_settings
from formatting.branding import ensure_logo_png
from formatting.docx_formatter import format_docx
from formatting.markdown_utils import format_html_preview
from formatting.pdf_formatter import format_pdf
from formatting.txt_formatter import format_txt


# =========================================================
# PROJECT SETUP
# =========================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

settings = get_settings()

logo_path = PROJECT_ROOT / settings.logo_path

# Create PNG logo automatically if it does not exist.
logo_path = ensure_logo_png(logo_path)


# =========================================================
# STREAMLIT PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="LegalEase",
    page_icon=str(logo_path),
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# CUSTOM STYLING
# =========================================================

st.markdown(
    """
<style>

.block-container {
    max-width: 1200px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}


/* -----------------------------
   Header
------------------------------ */

.legal-header {
    text-align: center;
    margin-bottom: 30px;
}

.legal-header h1 {
    font-size: 3rem;
    margin-bottom: 5px;
}

.legal-header p {
    color: #94a3b8;
    font-size: 1.1rem;
}


/* -----------------------------
   Legal document preview
------------------------------ */

.legal-preview {
    background: #111827;
    color: #f8fafc;
    border: 1px solid #1f2937;
    border-radius: 14px;
    padding: 32px;
    min-height: 420px;
    max-height: 700px;
    overflow-y: auto;
    overflow-x: hidden;
    box-sizing: border-box;
}

.legal-preview h1 {
    color: #f8fafc;
    font-size: 1.8rem;
    margin-top: 0;
    margin-bottom: 20px;
}

.legal-preview h2 {
    color: #93c5fd;
    font-size: 1.3rem;
    margin-top: 26px;
    margin-bottom: 10px;
}

.legal-preview h3 {
    color: #bfdbfe;
    font-size: 1.05rem;
    margin-top: 18px;
    margin-bottom: 8px;
}

.legal-preview p {
    color: #e5e7eb;
    line-height: 1.65;
    margin-top: 0;
    margin-bottom: 14px;
}

.legal-preview ul {
    color: #e5e7eb;
    padding-left: 1.5rem;
    margin-top: 5px;
    margin-bottom: 15px;
}

.legal-preview li {
    color: #e5e7eb;
    line-height: 1.6;
    margin-bottom: 6px;
}

.legal-preview blockquote {
    border-left: 3px solid #60a5fa;
    padding-left: 14px;
    margin-left: 0;
    color: #cbd5e1;
    font-style: italic;
}

.preview-title {
    color: #94a3b8;
    font-size: 0.78rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    margin-bottom: 20px;
}

.preview-spacer {
    height: 5px;
}


/* -----------------------------
   Footer
------------------------------ */

.footer-text {
    text-align: center;
    color: #64748b;
    font-size: 0.85rem;
}

</style>
""",
    unsafe_allow_html=True,
)


# =========================================================
# SESSION STATE
# =========================================================

if "document_text" not in st.session_state:
    st.session_state.document_text = ""

if "edited_text" not in st.session_state:
    st.session_state.edited_text = ""

if "document_type" not in st.session_state:
    st.session_state.document_type = ""

if "company_name" not in st.session_state:
    st.session_state.company_name = settings.company_name


# =========================================================
# HEADER
# =========================================================

st.markdown(
    """
<div class="legal-header">
    <h1>⚖️ LegalEase</h1>
    <p>AI-Powered Legal Document Generator</p>
</div>
""",
    unsafe_allow_html=True,
)


# =========================================================
# INFORMATION MESSAGE
# =========================================================

st.info(
    "LegalEase provides AI-assisted drafting support. "
    "Generated documents should be reviewed by a qualified "
    "legal professional before use."
)


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.header("Document Details")


document_type = st.sidebar.text_input(
    "Document Type",
    value="Employment Contract",
    placeholder=(
        "Examples: NDA, Lease Agreement, "
        "Employment Contract"
    ),
)


parties = st.sidebar.text_area(
    "Parties Involved",
    value=(
        "Jane Doe (Employee), "
        "TechNova Inc. (Employer)"
    ),
    height=120,
    placeholder=(
        "Example: Jane Doe (Employee), "
        "ABC Corp (Employer)"
    ),
)


terms = st.sidebar.text_area(
    "Terms & Conditions",
    value=(
        "Role: Software Engineer; "
        "Compensation: INR 1,200,000 per year; "
        "Confidentiality must be maintained; "
        "Either party may terminate with 30 days notice"
    ),
    height=210,
    help=(
        "Separate individual terms using semicolons (;)."
    ),
)


dates = st.sidebar.text_input(
    "Effective Date",
    value="September 27, 2026",
)


company_name = st.sidebar.text_input(
    "Company / Brand Name",
    value=settings.company_name,
)


st.sidebar.markdown("---")


generate_clicked = st.sidebar.button(
    "Generate Document",
    type="primary",
    use_container_width=True,
)


# =========================================================
# GENERATE DOCUMENT
# =========================================================

if generate_clicked:

    # -----------------------------------------
    # Validation
    # -----------------------------------------

    if not document_type.strip():

        st.sidebar.error(
            "Please enter the document type."
        )

    elif not parties.strip():

        st.sidebar.error(
            "Please enter the parties involved."
        )

    elif not terms.strip():

        st.sidebar.error(
            "Please enter the terms and conditions."
        )

    elif not dates.strip():

        st.sidebar.error(
            "Please enter the effective date."
        )

    else:

        payload = {
            "document_type": document_type.strip(),
            "parties": parties.strip(),
            "terms": terms.strip(),
            "dates": dates.strip(),
            "company_name": (
                company_name.strip()
                or settings.company_name
            ),
        }

        try:

            with st.spinner(
                "Generating your legal document..."
            ):

                response = requests.post(
                    f"{settings.backend_url.rstrip('/')}/generate",
                    json=payload,
                    timeout=120,
                )

            response.raise_for_status()

            result = response.json()

            generated_text = (
                result.get("content", "")
            )

            if not generated_text.strip():

                raise ValueError(
                    "The backend returned an empty document."
                )

            # Save generated document.
            st.session_state.document_text = (
                generated_text
            )

            # Copy generated document into editor.
            st.session_state.edited_text = (
                generated_text
            )

            st.session_state.document_type = (
                result.get(
                    "document_type",
                    document_type,
                )
            )

            st.session_state.company_name = (
                company_name.strip()
                or settings.company_name
            )

            st.success(
                "Document generated successfully."
            )

            # Tell user when mock mode is active.
            if result.get("mock", False):

                st.warning(
                    "Mock AI mode is currently active. "
                    "The document was generated locally for testing."
                )

        except requests.exceptions.ConnectionError:

            st.error(
                "Cannot connect to the FastAPI backend."
            )

            st.info(
                "Start FastAPI in another terminal with:"
            )

            st.code(
                "uvicorn backend.main:app --reload",
                language="bash",
            )

        except requests.exceptions.Timeout:

            st.error(
                "The backend took too long to respond."
            )

        except requests.exceptions.HTTPError:

            try:

                detail = response.json().get(
                    "detail",
                    "Unknown backend error.",
                )

            except Exception:

                detail = response.text

            st.error(
                f"Backend error: {detail}"
            )

        except Exception as exc:

            st.error(
                f"Unexpected error: {exc}"
            )


# =========================================================
# GENERATED DOCUMENT SECTION
# =========================================================

if st.session_state.document_text:

    st.markdown(
        "### Generated Document"
    )

    # -----------------------------------------------------
    # FORMATTED PREVIEW
    # -----------------------------------------------------

    preview_html = format_html_preview(
        st.session_state.edited_text,
        st.session_state.document_type
        or document_type
        or "Legal Document",
    )

    # Render HTML instead of showing HTML source.
    st.html(preview_html)


    # -----------------------------------------------------
    # EDIT DOCUMENT
    # -----------------------------------------------------

    st.markdown("---")

    st.subheader(
        "Edit Document"
    )

    st.caption(
        "Modify the generated document below. "
        "Your edited version will be used for downloads."
    )

    st.text_area(
        "Document text",
        key="edited_text",
        height=550,
        label_visibility="collapsed",
    )


    # -----------------------------------------------------
    # DOWNLOADS
    # -----------------------------------------------------

    st.markdown("---")

    st.subheader(
        "Download Document"
    )

    current_text = (
        st.session_state.edited_text
    )

    current_type = (
        st.session_state.document_type
        or document_type
        or "Legal Document"
    )

    current_company = (
        st.session_state.company_name
        or company_name
        or settings.company_name
    )


    # -----------------------------------------
    # Safe filename
    # -----------------------------------------

    safe_name = "".join(
        char
        for char in current_type.lower()
        .replace(" ", "_")
        if char.isalnum()
        or char in "_-"
    )

    if not safe_name:

        safe_name = "legal_document"


    # -----------------------------------------
    # TXT
    # -----------------------------------------

    txt_data = format_txt(
        current_text
    )


    # -----------------------------------------
    # DOCX
    # -----------------------------------------

    docx_data = format_docx(
        current_text,
        current_type,
        terms=terms,
        logo_path=str(logo_path),
        company_name=current_company,
    )


    # -----------------------------------------
    # PDF
    # -----------------------------------------

    pdf_data = format_pdf(
        current_text,
        current_type,
        terms=terms,
        logo_path=str(logo_path),
        company_name=current_company,
    )


    # -----------------------------------------
    # Download buttons
    # -----------------------------------------

    col1, col2, col3 = st.columns(3)


    with col1:

        st.download_button(
            label="Download TXT",
            data=txt_data,
            file_name=f"{safe_name}.txt",
            mime="text/plain",
            use_container_width=True,
        )


    with col2:

        st.download_button(
            label="Download DOCX",
            data=docx_data,
            file_name=f"{safe_name}.docx",
            mime=(
                "application/"
                "vnd.openxmlformats-officedocument."
                "wordprocessingml.document"
            ),
            use_container_width=True,
        )


    with col3:

        st.download_button(
            label="Download PDF",
            data=pdf_data,
            file_name=f"{safe_name}.pdf",
            mime="application/pdf",
            use_container_width=True,
        )


    st.caption(
        "Review names, dates, terms, jurisdiction-specific "
        "requirements, and signatures before using the document."
    )


# =========================================================
# INITIAL SCREEN
# =========================================================

else:

    st.markdown(
        """
## Create your first legal document

Use the fields in the **Document Details** panel.

### 1. Document Type

Examples:

- Employment Contract
- Non-Disclosure Agreement
- Lease Agreement
- Freelance Work Contract

### 2. Parties Involved

Example:

`Alice Smith (Disclosing Party), TechNova Inc. (Receiving Party)`

### 3. Terms & Conditions

Separate multiple terms using semicolons.

Example:

`Confidentiality; Payment within 30 days; 15 days notice`

### 4. Effective Date

Enter the date on which the document should take effect.

Then click:

**Generate Document**
"""
    )


# =========================================================
# FOOTER
# =========================================================

st.markdown("---")

st.markdown(
    """
<div class="footer-text">
    LegalEase • Streamlit + FastAPI + Gemini
</div>
""",
    unsafe_allow_html=True,
)