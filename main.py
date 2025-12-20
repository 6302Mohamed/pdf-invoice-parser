import os
import pdfplumber

from invoice_parser.extract_fields import extract_invoice_fields
from invoice_parser.normalize import normalize_date, normalize_amount
from invoice_parser.export import export_to_csv, export_to_excel



def get_pdf_text(pdf_path: str) -> str:
    all_text = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                all_text.append(text)
    return "\n".join(all_text).strip()


def main():
    base_dir = os.path.dirname(__file__)
    samples_dir = os.path.join(base_dir, "samples")
    output_dir = os.path.join(base_dir, "outputs")
    os.makedirs(output_dir, exist_ok=True)

    if not os.path.isdir(samples_dir):
        print("❌ samples/ folder not found. Create it and add PDFs.")
        return

    pdf_files = sorted(
        os.path.join(samples_dir, f)
        for f in os.listdir(samples_dir)
        if f.lower().endswith(".pdf")
    )

    if not pdf_files:
        print("❌ No PDF files found in samples/")
        return

    rows = []
    failures = 0

    for pdf_path in pdf_files:
        try:
            text = get_pdf_text(pdf_path)
            fields = extract_invoice_fields(text)

            row = {
                "source_file": os.path.basename(pdf_path),
                "invoice_number": fields["invoice_number"],
                "invoice_date": normalize_date(fields["invoice_date"]),
                "total_amount": normalize_amount(fields["total_amount"]),
            }
            rows.append(row)

        except Exception as e:
            failures += 1
            print(f"❌ Failed: {os.path.basename(pdf_path)} | {e}")

    output_csv = os.path.join(output_dir, "invoices.csv")
    export_to_csv(rows, output_csv)
    output_xlsx = os.path.join(output_dir, "invoices.xlsx")
    export_to_excel(rows, output_xlsx)


    print(f"\n✅ Exported {len(rows)} invoices")
    print(f"📄 CSV  → {output_csv}")
    print(f"📊 XLSX → {output_xlsx}")



if __name__ == "__main__":
    main()
