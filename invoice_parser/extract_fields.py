import re
from typing import Dict, Optional


def extract_invoice_fields(text: str) -> Dict[str, Optional[str]]:
    """
    Extract core invoice fields from invoice text using regex.
    Expected labels in your dataset:
      - Order ID: 10248
      - Order Date: 2016-07-04
      - TotalPrice 440.0
    """
    fields: Dict[str, Optional[str]] = {
        "invoice_number": None,
        "invoice_date": None,
        "total_amount": None,
    }

    m = re.search(r"Order ID:\s*(\d+)", text)
    if m:
        fields["invoice_number"] = m.group(1)

    m = re.search(r"Order Date:\s*([0-9]{4}-[0-9]{2}-[0-9]{2})", text)
    if m:
        fields["invoice_date"] = m.group(1)

    # allow: TotalPrice 440.0 OR TotalPrice: 440.0
    m = re.search(r"TotalPrice\s*:?\s*([0-9]+(?:\.[0-9]+)?)", text)
    if m:
        fields["total_amount"] = m.group(1)

    return fields
