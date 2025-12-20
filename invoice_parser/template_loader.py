from __future__ import annotations
import yaml
from pathlib import Path


def load_template(template_path: str) -> dict:
    path = Path(template_path)
    if not path.exists():
        raise FileNotFoundError(f"Template not found: {template_path}")

    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)
