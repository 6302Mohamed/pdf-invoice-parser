from __future__ import annotations
import pdfplumber


def extract_text_fast(pdf_path: str) -> str:
    parts: list[str] = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            t = page.extract_text() or ""
            if t.strip():
                parts.append(t)
    return "\n".join(parts).strip()


def looks_scanned(text: str, min_chars: int = 50) -> bool:
    return len(text.strip()) < min_chars
