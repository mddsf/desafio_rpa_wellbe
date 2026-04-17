from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import zipfile
from pathlib import Path
from datetime import datetime as dt

from src.config import TEMP_DIR, OUTPUT_DIR, logger

MOVIE_SEARCH_MENU = '//a[.="Movie Search"]'
MOVIE_IN_SEARCH = '//input[@name="searchStr"]'
MOVIE_BT_SUBMIT = '//button[.="Find" or .="FIND"]'
MOVIE_SEARCH_RESULT = ''
MOVIE_CARD_ITEM = '//div[@class="cardItem"]'
MOVIE_CARD_ITEM_TITLE = '//div[@class="cardItem"]//div[@class="card-content"]/*[contains(@class, "card-title")]'
MOVIE_CARD_ITEM_OVERVIEW = '//div[@class="cardItem"]//div[@class="card-reveal"]/p'

INVOICE_EXTRACTION_MENU = '//a[.="Invoice Extraction"]'
INVOICE_HEADER = '//table[@id="tableSandbox"]/thead/tr/th'
INVOICE_LIST = '//table[@id="tableSandbox"]/tbody/tr'
INVOICE_LIST_NEXT = '//a[@id="tableSandbox_next" and not(contains(@class, "disabled"))]'

class RpaChallengeSelenium:

    def __init__(self):
        logger.info("Iniciando navegador")
        chrome_options = Options()
        chrome_options.add_argument("--disable-extensions")
        self.driver = webdriver.Chrome(options=chrome_options)

    def get_element(self, xpath: str, by = By.XPATH, timeout = 10):
        element = WebDriverWait(self.driver, timeout
                                ).until(EC.presence_of_element_located((by, xpath)))
        return element

    def get_elements(self, xpath: str, by = By.XPATH, timeout = 10):
        elements = WebDriverWait(self.driver, timeout
                                ).until(EC.presence_of_all_elements_located((by, xpath)))
        return elements

    def write(self, xpath: str, value: str, by = By.XPATH, timeout = 10):
        element = self.get_element(xpath, by, timeout)
        element.clear()
        element.send_keys(value)
    
    def get_movie_results(self):
        try:
            cards = self.get_elements(MOVIE_CARD_ITEM)
        except:
            logger.info("Nenhum resultado encontrado para a busca.")
            return []
        
        results = []
        for card in cards:
            title = card.find_element(By.XPATH, './/div[@class="card-content"]/*[contains(@class, "card-title")]').text
            overview = card.find_element(By.XPATH, './/div[@class="card-reveal"]/p').get_attribute("innerText")
            results.append({"title": title, "description": overview})
        logger.info(f"Busca realizada retornou {len(results)} filme(s)")
        return results

    def movie_search(self, text):
        logger.info(f"Realizando busca por: {text}")
        for _ in range(3):
            try:
                self.driver.get("https://rpachallenge.com")
                self.get_element(MOVIE_SEARCH_MENU).click()
                self.write(MOVIE_IN_SEARCH, text)
                self.get_element(MOVIE_BT_SUBMIT).click()
                results = self.get_movie_results()
                return results
            except Exception as e:
                logger.error(f"Erro durante a busca: {e}")
                return []


    def invoice_extraction(self, invoice_list: list):
        logger.info("Navegando para Invoices")
        try:
            self.get_element(INVOICE_EXTRACTION_MENU, timeout=1).click()
        except:
            self.driver.get("https://rpachallenge.com")
            self.get_element(INVOICE_EXTRACTION_MENU).click()

        invoices = []
        logger.info("Buscando invoices na lista paginada")
        try:
            while invoice_list:
                items = self.get_elements(INVOICE_LIST)
                for item in items:
                    href = item.find_element(By.XPATH, "./td/a[contains(@href, 'invoices/')]").get_attribute("href")
                    invoice_number = None
                    
                    for invoice_item in invoice_list:
                        if f'invoices/{invoice_item}.' in href:
                            logger.info(f"Invoice {invoice_item} encontrada")
                            invoice_number = invoice_item
                            break
        
                    if invoice_number is not None:
                        logger.info(f"Baixando invoice {invoice_number}")
                        invoice_list.remove(invoice_number)
                        file_name = "invoice_" +href.split("/")[-1]
                        response = requests.get(href)
                        image_path = f"{TEMP_DIR}/{file_name}"
                        with open(image_path, "wb") as f:
                            f.write(response.content)
                        
                        invoices.append(image_path)
                        logger.info(f"Download da invoice {invoice_number} realizado com sucesso")
                    if not invoice_list:
                        return invoices
                try:
                    self.get_element(INVOICE_LIST_NEXT).click()
                except Exception as e:
                    logger.erro(f"Falha ao buscar invoice(s)\n{str(e)}")
                    raise Exception(f"Invoice {invoice_number} não encontrada.")
                
        except Exception as e:
            logger.erro(f"Erro durante a extração de invoice: {e}")

    
    def zip_invoices(self, invoice_files):
        logger.info("Gerando arquivo zip com as invoices")
        try:
            tmpid = dt.now().strftime("%Y%m%d%H%M%S")
            zip_path = f"{OUTPUT_DIR}/invoices_selenium_{tmpid}.zip"
            with zipfile.ZipFile(zip_path, "w") as zipf:
                for file in invoice_files:
                    zipf.write(file, arcname=Path(file).name)
            logger.info(f"Zip gerado com sucesso!\n{zip_path}")
            return zip_path
        except Exception as e:
            logger.error(f"Falha ao gerar zip\n{str(e)}")

    
    def close(self):
        logger.info("Finalizando navegador...")
        self.driver.quit()
