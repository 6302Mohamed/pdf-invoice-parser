from datetime import datetime
from typing import Optional


def normalize_date(date_str: Optional[str]) -> Optional[str]:
    if not date_str:
        return None

    try:
        return datetime.strptime(date_str.strip(), "%Y-%m-%d").strftime("%Y-%m-%d")
    except ValueError:
        return date_str.strip()


def normalize_amount(amount_str: Optional[str]) -> Optional[float]:
    if amount_str is None:
        return None

    try:
        return round(float(amount_str), 2)
    except ValueError:
        return None
