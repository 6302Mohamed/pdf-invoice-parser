from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List, Any
import yaml


@dataclass
class FieldRule:
    required: bool
    patterns: List[str]


@dataclass
class AppConfig:
    min_chars_text_pdf: int
    ocr_dpi: int
    fields: Dict[str, FieldRule]


def load_config(path: str = "config.yml") -> AppConfig:
    with open(path, "r", encoding="utf-8") as f:
        raw: Dict[str, Any] = yaml.safe_load(f)

    defaults = raw.get("defaults", {})
    fields_raw = raw.get("fields", {})

    fields: Dict[str, FieldRule] = {}
    for name, spec in fields_raw.items():
        fields[name] = FieldRule(
            required=bool(spec.get("required", False)),
            patterns=list(spec.get("patterns", [])),
        )

    return AppConfig(
        min_chars_text_pdf=int(defaults.get("min_chars_text_pdf", 50)),
        ocr_dpi=int(defaults.get("ocr_dpi", 250)),
        fields=fields,
    )
