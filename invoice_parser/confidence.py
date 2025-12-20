from __future__ import annotations
from typing import Optional


def confidence_for_value(value: Optional[object], used_ocr: bool) -> str:
    """
    Simple, client-friendly confidence scoring:
    - Low: value missing
    - High: value present and extracted from text-based PDF
    - Medium: value present but came from OCR
    """
    if value is None or str(value).strip() == "":
        return "Low"
    return "Medium" if used_ocr else "High"
