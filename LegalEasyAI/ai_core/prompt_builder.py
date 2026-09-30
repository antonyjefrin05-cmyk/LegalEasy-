from datetime import date


SYSTEM_INSTRUCTION = """
You are the drafting engine for LegalEase,
an AI-assisted legal document drafting tool.

Your task is to draft clear, structured legal documents
from user-supplied facts.

Rules:

- Treat user-provided facts as authoritative for the draft.
- Do not invent missing facts.
- Never fabricate statutes, regulations, court cases,
  legal citations, legal authorities, or legal claims.
- Do not claim that a document is legally valid,
  compliant, or enforceable unless the user supplied
  the relevant legal basis.
- Preserve every material user-supplied term.
- Use [INSERT ...] placeholders for missing material details.
- Use neutral, professional legal language.
- Return only the document body.
- Use simple Markdown headings.
- Do not use Markdown code fences.
- Include signatures when appropriate.
""".strip()


def build_prompt(
    *,
    document_type: str,
    parties: str,
    terms: str,
    dates: str,
    company_name: str | None = None,
) -> str:

    return f"""
Draft a professional {document_type}.

DOCUMENT TYPE
{document_type}

PARTIES INVOLVED
{parties}

TERMS AND CONDITIONS
{terms}

EFFECTIVE DATE / DATE DETAILS
{dates}

BRAND / COMPANY NAME
{company_name or "LegalEase"}

DRAFTING DATE
{date.today().isoformat()}

Use a professional legal-document structure.

Suggested sections:

# {document_type.upper()}

## 1. Parties

## 2. Effective Date

## 3. Purpose / Background

## 4. Terms and Conditions

## 5. Responsibilities

## 6. Confidentiality / Data / Intellectual Property

## 7. Term and Termination

## 8. General Provisions

## 9. Signatures

Instructions:

1. Preserve all user-provided terms.
2. Include the parties and dates.
3. Make the clauses logically coherent.
4. Omit sections that genuinely do not apply.
5. Use [INSERT ...] for missing material details.
6. Never invent addresses, payment amounts,
   laws, statutes, courts, jurisdictions, or dates.
7. Do not add fake legal citations.
8. Do not state that the final result is legal advice.
""".strip()