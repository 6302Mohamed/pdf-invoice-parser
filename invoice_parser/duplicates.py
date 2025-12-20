from __future__ import annotations
from typing import Set, Optional


class DuplicateTracker:
    """
    Tracks duplicate invoice numbers.
    """
    def __init__(self) -> None:
        self.seen: Set[str] = set()

    def is_duplicate(self, invoice_number: Optional[str]) -> bool:
        if not invoice_number:
            return False

        if invoice_number in self.seen:
            return True

        self.seen.add(invoice_number)
        return False
