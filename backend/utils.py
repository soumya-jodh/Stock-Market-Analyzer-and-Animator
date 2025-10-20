# backend/utils.py
import csv
from io import StringIO
from typing import List, Dict

def parse_csv_prices(text: str) -> List[Dict]:
    """
    Accepts CSV text with headers (date,price) OR no header.
    Returns list of {"date": str, "price": float}
    """
    if not text:
        raise ValueError("Empty CSV")
    f = StringIO(text)
    reader = csv.reader(f)
    rows = [r for r in reader if r and any(cell.strip() for cell in r)]
    if not rows:
        raise ValueError("No CSV rows found")
    # detect header if non-numeric second column in first row
    first = rows[0]
    has_header = False
    if len(first) >= 2:
        try:
            float(first[1])
        except Exception:
            has_header = True

    data_rows = rows[1:] if has_header else rows
    series = []
    for r in data_rows:
        if len(r) < 2:
            continue
        date = r[0].strip()
        try:
            price = float(r[1].strip())
        except Exception:
            raise ValueError(f"Invalid price value: {r[1]}")
        series.append({"date": date, "price": price})
    if len(series) < 2:
        raise ValueError("CSV must contain at least two data rows")
    return series
