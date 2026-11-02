"""CSV read/write helpers for the base snapshot (B) and diagnostic output files."""
import csv


def write_csv_file(path, rows):
    """Write dict rows to CSV using the first row's keys as headers. No-op if `rows` is empty."""
    if not rows:
        return
    with open(path, "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=list(rows[0]), extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)
    print(f"  CSV written: {path} ({len(rows)} rows)")


def load_csv(path):
    """Load a CSV file, returning (fieldnames, rows) as a list of dicts."""
    with open(path, newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        return reader.fieldnames or [], list(reader)
