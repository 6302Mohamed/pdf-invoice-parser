from __future__ import annotations

import os
import argparse

from invoice_parser.config_loader import load_config
from invoice_parser.extract_fields import extract_fields
from invoice_parser.normalize import normalize_date, normalize_amount
from invoice_parser.export import export_to_csv, export_to_excel
from invoice_parser.logger_setup import setup_logger
from invoice_parser.text_detect import extract_text_fast, looks_scanned
from invoice_parser.ocr import ocr_pdf
from invoice_parser.confidence import confidence_for_value
from invoice_parser.duplicates import DuplicateTracker


def _abs_path(base_dir: str, p: str) -> str:
    return p if os.path.isabs(p) else os.path.join(base_dir, p)


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="PDF Invoice Parser (Templates + OCR + confidence + duplicates)"
    )
    parser.add_argument("--input", default="samples", help="Folder containing PDF files")
    parser.add_argument("--out", default="outputs", help="Output folder (CSV/XLSX/log)")

    # New recommended arg name:
    parser.add_argument("--template", default=None, help="Path to template YAML (recommended)")

    # Backward compatible:
    parser.add_argument("--config", default=None, help="(Deprecated) Path to YAML config")

    return parser


def main() -> None:
    base_dir = os.path.dirname(__file__)
    args = build_arg_parser().parse_args()

    samples_dir = _abs_path(base_dir, args.input)
    output_dir = _abs_path(base_dir, args.out)

    # choose template path (template preferred)
    if args.template:
        template_path = _abs_path(base_dir, args.template)
    elif args.config:
        template_path = _abs_path(base_dir, args.config)
    else:
        template_path = os.path.join(base_dir, "templates", "northwind.yml")

    os.makedirs(output_dir, exist_ok=True)

    logger = setup_logger(output_dir)
    logger.info("Starting invoice parser run (template profiles enabled)")
    logger.info(f"Template: {template_path}")
    logger.info(f"Input folder: {samples_dir}")
    logger.info(f"Output folder: {output_dir}")

    if not os.path.isfile(template_path):
        logger.error(f"Template not found: {template_path}")
        return

    if not os.path.isdir(samples_dir):
        logger.error(f"Input folder not found: {samples_dir}")
        return

    pdf_files = sorted(
        os.path.join(samples_dir, f)
        for f in os.listdir(samples_dir)
        if f.lower().endswith(".pdf")
    )

    if not pdf_files:
        logger.error(f"No PDF files found in: {samples_dir}")
        return

    # Load template using existing loader (it expects same schema as before)
    cfg = load_config(template_path)

    rows = []
    failures = 0
    ocr_used_count = 0
    duplicate_count = 0

    duplicate_tracker = DuplicateTracker()

    for pdf_path in pdf_files:
        pdf_name = os.path.basename(pdf_path)

        try:
            logger.info(f"Processing {pdf_name}")

            used_ocr = False

            text = extract_text_fast(pdf_path)

            if looks_scanned(text, cfg.min_chars_text_pdf):
                logger.info(f"OCR triggered for {pdf_name}")
                text = ocr_pdf(pdf_path, dpi=cfg.ocr_dpi)
                used_ocr = True
                ocr_used_count += 1
            else:
                logger.info(f"Text-based PDF detected for {pdf_name}")

            fields = extract_fields(text, cfg)

            invoice_number = fields.get("invoice_number")
            invoice_date = normalize_date(fields.get("invoice_date"))
            total_amount = normalize_amount(fields.get("total_amount"))

            is_duplicate = duplicate_tracker.is_duplicate(invoice_number)
            if is_duplicate:
                duplicate_count += 1
                logger.warning(f"Duplicate detected: {pdf_name} (invoice_number={invoice_number})")

            invoice_number_conf = confidence_for_value(invoice_number, used_ocr)
            invoice_date_conf = confidence_for_value(invoice_date, used_ocr)
            total_amount_conf = confidence_for_value(total_amount, used_ocr)

            row = {
                "source_file": pdf_name,
                "used_ocr": used_ocr,
                "invoice_number": invoice_number,
                "invoice_number_conf": invoice_number_conf,
                "invoice_date": invoice_date,
                "invoice_date_conf": invoice_date_conf,
                "total_amount": total_amount,
                "total_amount_conf": total_amount_conf,
                "is_duplicate": is_duplicate,
            }
            rows.append(row)

            logger.info(f"Success: {pdf_name}")

        except Exception as e:
            failures += 1
            logger.error(f"Failed: {pdf_name} | {e}")

    output_csv = os.path.join(output_dir, "invoices.csv")
    output_xlsx = os.path.join(output_dir, "invoices.xlsx")

    export_to_csv(rows, output_csv)
    export_to_excel(rows, output_xlsx)

    logger.info("Run finished")
    logger.info(f"Exported documents: {len(rows)}")
    logger.info(f"Failures: {failures}")
    logger.info(f"OCR used on {ocr_used_count} files")
    logger.info(f"Duplicates detected: {duplicate_count}")
    logger.info(f"CSV  -> {output_csv}")
    logger.info(f"XLSX -> {output_xlsx}")


if __name__ == "__main__":
    main()
