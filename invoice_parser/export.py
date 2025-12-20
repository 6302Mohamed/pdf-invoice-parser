import csv
from typing import List, Dict, Any
import pandas as pd


def export_to_csv(rows: List[Dict[str, Any]], output_path: str) -> None:
    if not rows:
        raise ValueError("No rows to export")

    fieldnames = list(rows[0].keys())
    with open(output_path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def export_to_excel(rows: List[Dict[str, Any]], output_path: str) -> None:
    if not rows:
        raise ValueError("No rows to export")

    df = pd.DataFrame(rows)
    df.to_excel(output_path, index=False)
