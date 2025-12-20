from __future__ import annotations
import pytesseract
from PIL import Image
import pdfplumber


def ocr_pdf(pdf_path: str, dpi: int = 250) -> str:
    """
    Convert PDF pages to images and run OCR using Tesseract.
    Returns combined text.
    """
    texts: list[str] = []

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            img = page.to_image(resolution=dpi).original  # PIL Image
            if not isinstance(img, Image.Image):
                img = Image.fromarray(img)
            text = pytesseract.image_to_string(img)
            if text.strip():
                texts.append(text)

    return "\n".join(texts).strip()
