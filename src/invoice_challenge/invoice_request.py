import requests
import zipfile
import pandas as pd
from pathlib import Path
from src.invoice_challenge.invoice_extract import extract_data_from_invoice
from src.config import TEMP_DIR, OUTPUT_DIR
from datetime import datetime as dt

class InvoiceChallengeRequest:

    def __init__(self):
        self.session = requests.Session()
        self.invoices = []
    
    def get_invoices(self):
        url = "https://rpachallengeocr.azurewebsites.net/seed"
        res = self.session.post(url, {"sendHash": "false"})
        if res.status_code != 200:
            print(f"Falha ao buscar invoices: {res.text}")
            return []
        data = res.json()
        self.invoices = data["data"]
        return True

    def search_invoice(self, invoice_number):
        for invoice in self.invoices:
            if f'/{invoice_number}.' in invoice["invoice"]:
                return invoice["invoice"]
    
    def download_invoice(self, invoice_number):
        url_download = f"https://rpachallengeocr.azurewebsites.net/invoices/{invoice_number}.jpg"
        file_name = f"invoice_{invoice_number}.jpg"
        response = requests.get(url_download)
        image_path = f"{TEMP_DIR}/{file_name}"
        with open(image_path, "wb") as f:
            f.write(response.content)
        return image_path
    
    def zip_invoices(self, invoice_files):
        tmpid = dt.now().strftime("%Y%m%d%H%M%S")
        zip_path = f"{OUTPUT_DIR}/invoices_{tmpid}.zip"
        with zipfile.ZipFile(zip_path, "w") as zipf:
            for file in invoice_files:
                zipf.write(file, arcname=Path(file).name)
        return zip_path
    
    def export_to_excel(self, invoices_img_path: list):
        output = f"{TEMP_DIR}/data_invoices.xlsx"
        invoices_data = []
        try:
            for img_path in invoices_img_path:
                data = extract_data_from_invoice(img_path)
                invoices_data.append(data)
        except Exception as e:
            print("Tessaract não disponível no sistema")
            print(str(e))
            return

        try:
            rows = []
            for invoice in invoices_data:

                for item in invoice.get("items", []):
                    rows.append({
                        "invoice_number": invoice["invoice_number"],
                        "customer_name":  invoice["customer_name"],
                        "date":           invoice["date"],
                        "balance_due":    invoice["balance_due"],
                        "total":          invoice["total"],
                        "subtotal":       invoice["subtotal"],
                        "tax_amount":     invoice["tax_amount"],
                        "item":           item["item"],
                        "quantity":       item["quantity"],
                        "rate":           item["rate"],
                        "amount":         item["amount"],
                    })

            df = pd.DataFrame(rows)
            df.to_excel(output, index=False, engine="openpyxl")
        except:
            print("Falha na exportação dos dados")
            return

        return output

    def check_invoice_list(self, invoice_list: list):
        for invoice in invoice_list:
            if self.search_invoice(invoice) is None:
                raise Exception(f"Invoice {invoice} não encontrada.")