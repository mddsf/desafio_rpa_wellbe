from src.services.ocr_service import TextExtractor
import re

MONTH_MAP = {
    "JAN": "01", "FEB": "02", "MAR": "03", "APR": "04",
    "MAY": "05", "JUN": "06", "JUL": "07", "AUG": "08",
    "SEP": "09", "OCT": "10", "NOV": "11", "DEC": "12"
}

def format_date(month: str, day: str, year: str) -> str | None:
    try:
        return f"{year}-{MONTH_MAP[month]}-{day.zfill(2)}"
    except:
        return None

def extract_text_from_invoice(image_path: str) -> str:
    text_extractor = TextExtractor()
    text = text_extractor.extract(image_path)

    while '\n\n' in text:
        text = text.replace('\n\n', '\n')

    return text.upper()

def extract_data_from_invoice(image_path: str) -> dict:
    """Lê uma imagem de invoice com OCR e retorna os dados extraídos (número, cliente, data, valores e itens)."""
    text = extract_text_from_invoice(image_path)
    data = {}

    match = re.search(r'#:?\s*(\d+)', text)
    data["invoice_number"] = match.group(1) if match else None
    
    match = re.search(r'BALANCE DUE\s*:\s*\$?([\d,]+.\d{2})', text)
    data["balance_due"] = match.group(1) if match else None

    match = re.search(r'DATE\s*:\s*(\w{3})\s+(\d{1,2}),\s+(\d{4})', text)
    data["month"] = match.group(1) if match else None
    data["day"] = match.group(2) if match else None
    data["year"] = match.group(3) if match else None
    data["date"] = format_date(data["month"], data["day"], data["year"])

    match = re.search(r'TOTAL\s*:\s*\$?([\d,]+.\d{2})', text)
    data["total"] = match.group(1) if match else None

    match = re.search(r'SUBTOTAL\s*:?\s*\$?([\d,]+.\d{2})', text)
    data["subtotal"] = match.group(1) if match else None

    match = re.search(r'TAX\s*(\([\d.,]+\%?\))?\s*:?\s*\$?([\d,]+.\d{2})', text)
    data["tax_amount"] = match.group(2) if match else None

    text_ln = text.splitlines()
    items = []
    items_found = False
    for idx, line in enumerate(text_ln):
        if items_found:
            line = re.sub(r'\$\s+', '$', line)
            tmp = " ".join(line.split())
            tmp = tmp.split(" ")
            items.append({
                "item": " ".join(tmp[0:-3]),
                "quantity": tmp[-3],
                "rate": tmp[-2],
                "amount": tmp[-1]
            })
        elif line.startswith("BILL TO:"):
            data["customer_name"] = text_ln[idx + 1].strip()

        elif all(word in line for word in ["ITEM", "QUANTITY", "RATE", "AMOUNT"]):
            items_found = True
            continue

        if items_found and 'SUBTOTAL' in text_ln[idx + 1]:
            break
    data["items"] = items

    return data


