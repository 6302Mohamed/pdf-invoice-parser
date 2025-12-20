from __future__ import annotations
import re
from typing import Dict, Optional

from invoice_parser.config_loader import AppConfig


def _first_match(text: str, patterns: list[str]) -> Optional[str]:
    """
    Try regex patterns in order and return the first captured value.
    If a regex has multiple capture groups, return the LAST group.
    """
    for pat in patterns:
        m = re.search(pat, text, flags=re.IGNORECASE)
        if not m:
            continue

        if m.lastindex:
            return m.group(m.lastindex).strip()

    return None


def extract_fields(text: str, cfg: AppConfig) -> Dict[str, Optional[str]]:
    """
    Extract invoice fields using patterns defined in config.yml
    """
    results: Dict[str, Optional[str]] = {}

    for field_name, rule in cfg.fields.items():
        results[field_name] = _first_match(text, rule.patterns)

    return results
