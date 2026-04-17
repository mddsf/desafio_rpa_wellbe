from run_invoice_by_request import main_invoice
from run_movie_by_request import main_movies
from run_selenium import main_selenium
from src.config import logger
import subprocess
import sys

def main(dashboard_process=None):
    logger.info("===================== Desafio-RPA Wellbe =====================")
    logger.info("1. Execução com selenium seguindo os passos solicitados de forma básica.")
    logger.info("2. Execução por requisição com Streamlit apresentando dados no final")
    logger.info("0. Sair")
    op = input("Opção: ")
    if op not in ["0", "1", "2"]:
        logger.info("Opção inválida!")
    if op == "0":
        logger.info("Finalizando...")
        if dashboard_process is not None:
            dashboard_process.terminate()
        sys.exit(0)
    elif op == "1":
        main_selenium()
    else:
        main_movies("avengers")
        main_invoice("2,4")
        if dashboard_process is None or dashboard_process.poll() is not None:
            dashboard_process = subprocess.Popen(["streamlit", "run", "run_dashboard.py"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    main(dashboard_process)

if __name__ == '__main__':
    main()
    logger.info("Finalizando...")
