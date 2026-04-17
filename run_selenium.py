from src.movie_challenge.selenium_challege import RpaChallengeSelenium
from src.services.db_service import add_movies_selenium
from src.config import logger

def main_selenium():
    logger.info("Iniciando desafio com selenium")
    rc = RpaChallengeSelenium()
    movies = rc.movie_search("avengers")
    logger.info("Inserindo dados no banco")
    add_movies_selenium(movies)
    logger.info("Dados inseridos com sucesso!")

    logger.info("Passando para segunda etapa(invoices)")
    invoice_list = [2,4]
    invoices = rc.invoice_extraction(invoice_list)
    rc.zip_invoices(invoices)
    rc.close()
    logger.info("Desafio finalizado!")
    logger.info("Para visualizar os dados completos execute o script run_requests.py")


if __name__ == '__main__':
    main_selenium()